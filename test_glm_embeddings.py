#!/usr/bin/env python3
"""
Test script for GLM embeddings functionality.
"""

import sys
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

sys.path.append('backend')

from backend.app.services.embeddings import GLMEmbeddings, get_embedding_function

def test_glm_embeddings():
    """Test GLM embedding functionality."""
    print("=== Testing GLM Embeddings ===")

    # Check if API key is available
    api_key = os.getenv("GLM_API_KEY")
    if not api_key:
        print("❌ GLM_API_KEY not found in environment variables.")
        print("Please set your GLM API key in the .env file.")
        return False

    try:
        # Initialize GLM embeddings
        print("Initializing GLM Embeddings...")
        glm = GLMEmbeddings(
            model="embedding-3",
            dimensions=1024,
            api_key=api_key
        )

        # Test single text embedding
        print("\n1. Testing single text embedding...")
        test_text = "推荐一些手机"
        embedding = glm.embed_query(test_text)
        print(f"✅ Successfully embedded text: '{test_text}'")
        print(f"   Embedding dimensions: {len(embedding)}")
        print(f"   First 5 values: {embedding[:5]}")

        # Test multiple text embeddings
        print("\n2. Testing multiple text embeddings...")
        test_texts = ["iPhone有什么功能？", "推荐一些手机", "苹果产品质量如何？"]
        embeddings = glm.embed_documents(test_texts)
        print(f"✅ Successfully embedded {len(test_texts)} texts")
        for i, text in enumerate(test_texts):
            print(f"   {i+1}. '{text}' -> dimensions: {len(embeddings[i])}")

        # Test with get_embedding_function
        print("\n3. Testing through get_embedding_function...")
        os.environ["EMBEDDINGS_PROVIDER"] = "glm"
        embedding_func = get_embedding_function()
        test_embedding = embedding_func.embed_query("测试文本")
        print(f"✅ Successfully embedded through get_embedding_function")
        print(f"   Embedding dimensions: {len(test_embedding)}")

        return True

    except Exception as e:
        print(f"❌ Error testing GLM embeddings: {e}")
        return False

def test_embedding_provider_selection():
    """Test provider selection functionality."""
    print("\n=== Testing Provider Selection ===")

    providers = ["openai", "ollama", "glm"]

    for provider in providers:
        try:
            os.environ["EMBEDDINGS_PROVIDER"] = provider
            embedding_func = get_embedding_function()
            print(f"✅ Successfully created {provider} embedding function")
        except Exception as e:
            print(f"❌ Failed to create {provider} embedding function: {e}")

if __name__ == "__main__":
    print("GLM Embeddings Test Script")
    print("=" * 50)

    # Test GLM embeddings (requires API key)
    success = test_glm_embeddings()

    # Test provider selection
    test_embedding_provider_selection()

    print("\n" + "=" * 50)
    if success:
        print("🎉 GLM embeddings test completed successfully!")
    else:
        print("⚠️  GLM embeddings test failed. Please check your API key configuration.")