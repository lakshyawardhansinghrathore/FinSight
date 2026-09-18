import uuid
import os
from types import SimpleNamespace
from langchain_community.vectorstores import Chroma

class ChromaDBVectorStore:
    """Local ChromaDB vector store."""

    def __init__(
        self,
        collection_name: str = "documents",
        persist_directory: str = "./chroma_data"
    ) -> None:
        self.collection_name = collection_name
        self.persist_directory = persist_directory

    def upload_chunks(
        self,
        chunks,
        embeddings,
        company: str,
        year: str,
        source_file: str
    ) -> None:
        """
        Upload chunks to ChromaDB.
        """
        # Add metadata to chunks
        for chunk in chunks:
            chunk.metadata = {
                "company": company,
                "year": year,
                "source_file": source_file,
            }

        # Initialize Chroma vector store with chunks and embeddings
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            collection_name=self.collection_name,
            persist_directory=self.persist_directory
        )
        
        print(f"Uploaded {len(chunks)} chunks to ChromaDB collection '{self.collection_name}'.")

class Retriever:
    """Simple wrapper around ChromaDB for retrieving relevant chunks.
    Mirrors the Retriever used in the RAG extractor.
    """
    def __init__(self, embeddings, collection_name: str = "documents", persist_directory: str = "./chroma_data"):
        self.vectorstore = Chroma(
            collection_name=collection_name,
            embedding_function=embeddings,
            persist_directory=persist_directory
        )

    def invoke(
        self,
        query: str,
        company: str | None = None,
        year: int | None = None,
        top_k: int = 20
    ) -> list:
        """Retrieve relevant chunks from ChromaDB.
        Returns a list of SimpleNamespace objects with `page_content`.
        """
        filter_dict = {}
        if company and year:
            filter_dict = {"$and": [{"company": company}, {"year": str(year)}]}
        elif company:
            filter_dict = {"company": company}
        elif year:
            filter_dict = {"year": str(year)}

        search_kwargs = {"k": top_k}
        if filter_dict:
            search_kwargs["filter"] = filter_dict

        results = self.vectorstore.similarity_search(
            query,
            **search_kwargs
        )
        
        documents = []
        for result in results:
            documents.append(SimpleNamespace(page_content=result.page_content))
            
        return documents
