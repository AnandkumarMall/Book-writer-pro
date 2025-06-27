import streamlit as st
import chromadb
from chromadb.config import Settings
import io
from fpdf import FPDF
import unicodedata


def sanitize_text(text):
    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")


client = chromadb.Client(Settings(persist_directory="chromadb_data", anonymized_telemetry=False))
collection = client.get_or_create_collection("book_chapters")



@st.cache_data
def get_all_metadata():
    results = collection.get(include=["metadatas"])
    return results['metadatas']


@st.cache_data
def get_filtered_versions(book_name, chapter_number):
    filters = {}
    if book_name:
        filters["book_name"] = book_name
    if chapter_number:
        filters["chapter_number"] = chapter_number

    if "book_name" in filters and "chapter_number" in filters:
        where_clause = {
            "$and": [
                {"book_name": filters["book_name"]},
                {"chapter_number": filters["chapter_number"]}
            ]
        }
    else:
        where_clause = filters

    return collection.get(where=where_clause, include=["documents", "metadatas"])


def query_versions_by_semantic(query, book_name, chapter_number):
    return collection.query(
        query_texts=[query],
        n_results=10,
        where={
            "$and": [
                {"book_name": book_name},
                {"chapter_number": chapter_number}
            ]
        },
        include=["documents", "metadatas", "distances"]
    )


def rank_chapters(chapters, objective="clarity"):
    def score(metadata):
        review = metadata.get("ai_review", "").lower()
        s = 0
        if objective == "clarity":
            s += review.count("clear")
            s -= review.count("confusing")
        elif objective == "emotional":
            s += review.count("emotional")
            s -= review.count("flat")
        return s

    return sorted(chapters, key=lambda x: score(x["metadata"]), reverse=True)


def render_retrieval_page():
    st.title("📖 Retrieve and Explore Saved Chapters")

    query_input = st.text_input("🔎 Optional Semantic Search Query")

    all_meta = get_all_metadata()
    book_options = sorted(set(meta["book_name"] for meta in all_meta if meta.get("book_name")))

    if not book_options:
        st.warning("No valid book data found.")
        return

    book_name = st.selectbox("📚 Select Book Name", book_options)

    chapter_options = sorted(set(
        meta["chapter_number"] for meta in all_meta if meta.get("book_name") == book_name
    ))

    if not chapter_options:
        st.warning("No chapters for selected book.")
        return

    chapter_number = st.selectbox("📄 Select Chapter Number", chapter_options)
    objective = st.radio("📊 RL-style Ranking Focus", ["clarity", "emotional"], horizontal=True)

    if st.button("🔍 Retrieve Best Versions"):
        with st.spinner("Searching and ranking chapter versions..."):
            try:
                if query_input.strip():
                    result = query_versions_by_semantic(query_input, book_name, chapter_number)
                    documents = result["documents"][0]
                    metadatas = result["metadatas"][0]
                else:
                    result = get_filtered_versions(book_name, chapter_number)
                    documents = result["documents"]
                    metadatas = result["metadatas"]

                combined = [{"document": doc, "metadata": meta} for doc, meta in zip(documents, metadatas)]
                ranked = rank_chapters(combined, objective)

                # Store chapters in session
                st.session_state.chapter_results = ranked
                st.session_state.pdf_buffers = [None] * len(ranked)

            except Exception as e:
                st.error(f"🚫 Retrieval failed: {e}")
                return

    if "chapter_results" in st.session_state:
        for i, chapter in enumerate(st.session_state.chapter_results):
            chapter_text = chapter["document"]
            version = chapter["metadata"].get("version", i + 1)

            st.subheader(f"📝 Version {version}")
            st.text_area("📚 Chapter Text", value=chapter_text, height=400, key=f"doc_{i}")

            if st.button(f"📄 Export Version {version} to PDF", key=f"export_btn_{i}"):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_auto_page_break(auto=True, margin=15)

                pdf.set_font("Arial", style="B", size=14)
                pdf.cell(0, 10, f"Book: {book_name}", ln=True)
                pdf.cell(0, 10, f"Chapter: {chapter_number} - Version {version}", ln=True)
                pdf.ln()

                pdf.set_font("Arial", size=12)
                for line in chapter_text.split('\n'):
                    clean_line = sanitize_text(line)
                    pdf.multi_cell(0, 10, clean_line)

                pdf_output = pdf.output(dest='S').encode('latin-1')
                st.session_state.pdf_buffers[i] = io.BytesIO(pdf_output)

            if st.session_state.pdf_buffers[i]:
                st.download_button(
                    label="⬇️ Download PDF",
                    data=st.session_state.pdf_buffers[i],
                    file_name=f"{book_name}_Chapter_{chapter_number}_v{version}.pdf",
                    mime="application/pdf",
                    key=f"download_btn_{i}"
                )
