import streamlit as st
import json
import os
from gemini_writer import spin_story
from ai_reviewer import story_review
from chromedb_store import save_to_chromadb

st.sidebar.title("📚 Navigation")
page = st.sidebar.radio("Choose Page", ["📝 Rewrite & Review", "📂 Retrieve Saved Chapters"])

if "chapter_data" not in st.session_state:
    st.session_state.chapter_data = None
if "rewritten_story" not in st.session_state:
    st.session_state.rewritten_story = ""
if "ai_review" not in st.session_state:
    st.session_state.ai_review = ""
if "version" not in st.session_state:
    st.session_state.version = 1
if page == "📝 Rewrite & Review":
    st.title("📚 Automated Book Publication Tool")


    @st.cache_data
    def list_chapter_files():
        return sorted([f for f in os.listdir("chapters") if f.endswith(".json")])


    chapter_files = list_chapter_files()

    selected_file = st.selectbox("📂 Select a Chapter File", chapter_files)


    def load_chapter(file_name):
        with open(os.path.join("chapters", file_name), "r", encoding="utf-8") as f:
            data = json.load(f)

        # Auto-fill missing metadata from filename
        if not data.get("book_name"):
            data["book_name"] = "Unknown Book"
        if not data.get("chapter_number"):
            data["chapter_number"] = file_name.split("_")[1] if "_" in file_name else "Unknown"
        return data


    if st.button("📥 Load Selected Chapter"):
        st.session_state.chapter_data = load_chapter(selected_file)
        st.session_state.rewritten_story = spin_story(
            st.session_state.chapter_data["text_content"],
            st.session_state.chapter_data["chapter_title"]
        )
        st.session_state.ai_review = story_review(
            st.session_state.rewritten_story,
            st.session_state.chapter_data["chapter_title"]
        )

    if st.session_state.chapter_data:
        st.subheader("📖 Original Chapter")
        st.text_area("Original Text", value=st.session_state.chapter_data["text_content"], height=400)

        st.subheader("📝 Rewritten Chapter")
        new_story = st.text_area("Rewritten Story", value=st.session_state.rewritten_story, height=400)

        st.subheader("🤖 AI Review")
        st.text_area("AI Review", value=st.session_state.ai_review, height=200, disabled=True)

        st.subheader("👤 Human Review")
        human_review = st.text_area("Your Review", value="", height=200)

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("🔁 Rewrite with Review"):
                review_combined = st.session_state.ai_review + "\n" + human_review if human_review else st.session_state.ai_review
                st.session_state.rewritten_story = spin_story(
                    st.session_state.chapter_data["text_content"],
                    st.session_state.chapter_data["chapter_title"],
                    review_combined
                )
                st.session_state.version += 1
                st.session_state.ai_review = story_review(
                    st.session_state.rewritten_story,
                    st.session_state.chapter_data["chapter_title"]
                )
                st.rerun()

        with col2:
            if st.button("💾 Save to ChromaDB"):
                chapter = st.session_state.chapter_data
                if chapter["book_name"] and chapter["chapter_number"]:
                    save_to_chromadb(
                        book_name=chapter["book_name"],
                        chapter_number=chapter["chapter_number"],
                        chapter_title=chapter["chapter_title"],
                        final_story=st.session_state.rewritten_story,
                        ai_review=st.session_state.ai_review,
                        human_review=human_review,
                        source_url=chapter["source_url"],
                        version=st.session_state.version
                    )
                else:
                    st.error("❌ Missing book name or chapter number. Please check the chapter JSON file.")


elif page == "📂 Retrieve Saved Chapters":
    from retrieval import render_retrieval_page

    render_retrieval_page()
