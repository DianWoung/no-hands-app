import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import OllamaEmbeddings

def get_embedding_function():
    """
    Dynamically creates and returns an embedding function based on the provider
    specified in the environment variables.

    Returns:
        An instance of an embedding class (e.g., OpenAIEmbeddings, OllamaEmbeddings).

    Raises:
        ValueError: If the specified provider is not supported.
    """
    provider = os.getenv("EMBEDDINGS_PROVIDER", "openai").lower()

    if provider == "openai":
        print("Using OpenAI for embeddings.")
        return OpenAIEmbeddings(
            model=os.getenv("OPENAI_EMBEDDINGS_MODEL_NAME", "text-embedding-3-small"),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            openai_api_base=os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1"),
        )
    elif provider == "ollama":
        print("Using Ollama for embeddings.")
        return OllamaEmbeddings(
            model=os.getenv("OLLAMA_EMBEDDINGS_MODEL_NAME", "nomic-embed-text"),
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        )
    else:
        raise ValueError(
            f"Unsupported embeddings provider: '{provider}'. "
            "Please choose 'openai' or 'ollama'."
        )