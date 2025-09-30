import os
import shutil
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

from .embeddings import get_embedding_function

# --- Configuration ---
KNOWLEDGE_BASE_DIR = "backend/knowledge_base"
CHROMA_DB_DIR = "backend/chroma_db"

def build_vector_store():
    """
    Builds a ChromaDB vector store from documents in the knowledge base directory,
    using the embedding provider specified in the environment variables.
    """
    # Load environment variables from .env file in the backend directory
    load_dotenv(dotenv_path='backend/.env')

    # --- 1. Get Embedding Function ---
    try:
        embedding_function = get_embedding_function()
    except ValueError as e:
        print(f"ERROR: Could not initialize embeddings. {e}")
        return

    # --- 2. Load Documents ---
    print(f"Loading documents from '{KNOWLEDGE_BASE_DIR}'...")
    loader = DirectoryLoader(KNOWLEDGE_BASE_DIR, glob="**/*.[md|txt]")
    documents = loader.load()
    if not documents:
        print("No documents found. Aborting.")
        return
    print(f"Loaded {len(documents)} documents.")

    # --- 3. Split Documents into Chunks ---
    print("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(documents)
    print(f"Created {len(splits)} document chunks.")

    # --- 4. Create Embeddings and Vector Store ---
    print("Creating embeddings and building Chroma vector store...")

    # Clean up old database directory if it exists
    if os.path.exists(CHROMA_DB_DIR):
        print(f"Removing existing ChromaDB directory: '{CHROMA_DB_DIR}'")
        shutil.rmtree(CHROMA_DB_DIR)

    # Create the vector store using the selected embedding function
    vector_store = Chroma.from_documents(
        documents=splits,
        embedding=embedding_function,
        persist_directory=CHROMA_DB_DIR
    )

    print("="*80)
    print("Vector store built successfully!")
    print(f"ChromaDB is persisted in: '{CHROMA_DB_DIR}'")
    print("="*80)


if __name__ == "__main__":
    build_vector_store()