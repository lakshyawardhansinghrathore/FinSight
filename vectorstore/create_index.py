import os
import chromadb
from dotenv import load_dotenv

load_dotenv()

def create_index(
    collection_name: str = "documents",
    persist_directory: str = "./chroma_data"
) -> None:
    """
    Initialize ChromaDB collection.
    ChromaDB creates collections automatically when adding documents,
    but this ensures the directory and collection exist.
    """
    client = chromadb.PersistentClient(path=persist_directory)
    client.get_or_create_collection(name=collection_name)
    print(f"ChromaDB collection '{collection_name}' initialized at {persist_directory}")

if __name__ == "__main__":
    create_index()