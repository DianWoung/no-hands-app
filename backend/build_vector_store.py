import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import shutil

# --- Configuration ---
KNOWLEDGE_BASE_DIR = "backend/knowledge_base"
CHROMA_DB_DIR = "backend/chroma_db"

def build_vector_store():
    """
    Builds a ChromaDB vector store from documents in the knowledge base directory.
    """
    # Load environment variables (for OpenAI API key)
    load_dotenv(dotenv_path='backend/.env')
    openai_api_key = os.getenv("OPENAI_API_KEY")

    if not openai_api_key or openai_api_key == "YOUR_OPENAI_API_KEY_HERE":
        print("="*80)
        print("ERROR: OpenAI API key is not set.")
        print("Please set your OPENAI_API_KEY in the 'backend/.env' file.")
        print("="*80)
        return

    # --- 1. Load Documents ---
    print(f"Loading documents from '{KNOWLEDGE_BASE_DIR}'...")
    loader = DirectoryLoader(KNOWLEDGE_BASE_DIR, glob="**/*.[md|txt]")
    documents = loader.load()
    if not documents:
        print("No documents found. Aborting.")
        return
    print(f"Loaded {len(documents)} documents.")

    # --- 2. Split Documents into Chunks ---
    print("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(documents)
    print(f"Created {len(splits)} document chunks.")

    # --- 3. Create Embeddings and Vector Store ---
    print("Creating embeddings and building Chroma vector store...")

    # Clean up old database directory if it exists
    if os.path.exists(CHROMA_DB_DIR):
        print(f"Removing existing ChromaDB directory: '{CHROMA_DB_DIR}'")
        shutil.rmtree(CHROMA_DB_DIR)

    # Create the vector store with OpenAI embeddings
    embedding_function = OpenAIEmbeddings()
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