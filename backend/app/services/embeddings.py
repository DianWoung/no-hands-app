import os
import json
import requests
from typing import List
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import OllamaEmbeddings

# Load environment variables from project root
load_dotenv(dotenv_path='../.env', override=True)


class GLMEmbeddings:
    """
    GLM (智谱AI) Embedding class for generating embeddings using GLM API.
    """

    def __init__(self, model: str = "embedding-3", dimensions: int = 1024,
                 api_key: str = None, base_url: str = None):
        """
        Initialize GLM Embeddings.

        Args:
            model: GLM model name (embedding-3 or embedding-2)
            dimensions: Embedding dimensions (embedding-3: 256/512/1024/2048, embedding-2: 1024)
            api_key: GLM API key
            base_url: GLM API base URL
        """
        self.model = model
        self.dimensions = dimensions
        self.api_key = api_key or os.getenv("GLM_API_KEY") or os.getenv("ZHIPU_API_KEY")
        self.base_url = base_url or os.getenv("GLM_BASE_URL", "https://open.bigmodel.cn/api/paas/v4/embeddings")

        if not self.api_key:
            raise ValueError("GLM_API_KEY or ZHIPU_API_KEY is required for GLM embeddings")

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents."""
        return self._embed(texts)

    def embed_query(self, text: str) -> List[float]:
        """Embed a single query text."""
        embeddings = self._embed([text])
        return embeddings[0] if embeddings else []

    def _embed(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for the given texts."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.model,
            "input": texts,
            "dimensions": self.dimensions
        }

        try:
            response = requests.post(self.base_url, headers=headers, json=data)
            response.raise_for_status()

            result = response.json()

            if "data" not in result:
                raise ValueError(f"GLM API response missing 'data' field: {result}")

            # Sort by index and extract embeddings
            embeddings = []
            for item in sorted(result["data"], key=lambda x: x["index"]):
                embeddings.append(item["embedding"])

            return embeddings

        except requests.RequestException as e:
            raise ValueError(f"GLM API request failed: {e}")
        except (KeyError, ValueError) as e:
            raise ValueError(f"GLM API response parsing failed: {e}")

def get_embedding_function():
    """
    Dynamically creates and returns an embedding function based on the provider
    specified in the environment variables.

    Returns:
        An instance of an embedding class (e.g., OpenAIEmbeddings, OllamaEmbeddings, GLMEmbeddings).

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
    elif provider == "glm":
        print("Using GLM for embeddings.")
        return GLMEmbeddings(
            model=os.getenv("GLM_EMBEDDINGS_MODEL_NAME", "embedding-3"),
            dimensions=int(os.getenv("GLM_EMBEDDINGS_DIMENSIONS", "1024")),
            api_key=os.getenv("GLM_API_KEY"),
            base_url=os.getenv("GLM_BASE_URL", "https://open.bigmodel.cn/api/paas/v4/embeddings"),
        )
    else:
        raise ValueError(
            f"Unsupported embeddings provider: '{provider}'. "
            "Please choose 'openai', 'ollama', or 'glm'."
        )