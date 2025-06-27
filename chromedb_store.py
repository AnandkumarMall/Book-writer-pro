import chromadb
from chromadb.config import Settings

client = chromadb.Client(Settings(persist_directory="chromadb_data", anonymized_telemetry=False))
collection = client.get_or_create_collection("book_chapters")


def clean(value):
    return str(value).strip().strip('"') if value else "The Gates of Morning "


def save_to_chromadb(book_name, chapter_number, chapter_title,
                     final_story, ai_review, human_review,
                     source_url, version):
    clean_book_name = clean(book_name)
    clean_chapter_number = clean(chapter_number)
    collection.add(
        documents=[final_story],
        metadatas=[{
            "book_name": book_name,
            "chapter_number": chapter_number,
            "chapter_title": chapter_title,
            "version": version,
            "ai_review": ai_review,
            "human_review": human_review,
            "source_url": source_url
        }],
        ids=[f"{book_name}_{chapter_number}_v{version}".replace(" ", "_")]
    )
    print("✅ Chapter saved in ChromaDB.")
