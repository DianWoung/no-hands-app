import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma

from .embeddings import get_embedding_function

# --- Configuration ---
CHROMA_DB_DIR = "backend/chroma_db"
load_dotenv(dotenv_path='backend/.env')

class KnowledgeService:
    def __init__(self):
        if not os.path.exists(CHROMA_DB_DIR):
             raise FileNotFoundError(
                f"ChromaDB directory not found at '{CHROMA_DB_DIR}'. "
                "Please run 'python -m backend.build_vector_store' first."
            )

        try:
            # Use the centralized function to get the embedding model
            self.embedding_function = get_embedding_function()
        except ValueError as e:
            # Re-raise the error to be caught by the FastAPI lifespan manager
            raise e

        self.vector_store = Chroma(
            persist_directory=CHROMA_DB_DIR,
            embedding_function=self.embedding_function
        )
        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})
        print("KnowledgeService initialized successfully with embeddings.")

    def answer_question(self, question: str) -> dict:
        """
        Answers a question by retrieving relevant documents from the vector store.
        """
        print(f"Received question: {question}")
        relevant_docs = self.retriever.invoke(question)

        if not relevant_docs:
            return {
                "answer": "I could not find an answer to that in my knowledge base.",
                "source": "N/A"
            }

        # For simplicity, we'll return the content of the most relevant document.
        # A more advanced implementation would synthesize an answer from all docs.
        most_relevant_doc = relevant_docs[0]
        answer = most_relevant_doc.page_content
        source_file = most_relevant_doc.metadata.get('source', 'Unknown')

        print(f"Found answer in source: {source_file}")

        return {
            "answer": answer,
            "source": source_file
        }

# The service will be initialized on application startup in main.py