#!/usr/bin/env python3
"""
Test script to verify .env configuration is loaded correctly
"""
import os
import sys
from dotenv import load_dotenv

# Add the backend directory to the Python path
sys.path.append('/Users/dianwang-mac/ai-workspace/no-hands-app/backend')

# Load environment variables from project root, overriding system environment variables
load_dotenv(dotenv_path='/Users/dianwang-mac/ai-workspace/no-hands-app/.env', override=True)

print("=== .env Configuration Test ===")
print(f"OPENAI_API_KEY: {'***' + os.getenv('OPENAI_API_KEY', 'NOT_FOUND')[-4:] if os.getenv('OPENAI_API_KEY') else 'NOT_FOUND'}")
print(f"OPENAI_API_BASE: {os.getenv('OPENAI_API_BASE', 'NOT_FOUND')}")
print(f"OPENAI_MODEL_NAME: {os.getenv('OPENAI_MODEL_NAME', 'NOT_FOUND')}")
print(f"EMBEDDINGS_PROVIDER: {os.getenv('EMBEDDINGS_PROVIDER', 'NOT_FOUND')}")
print(f"OLLAMA_BASE_URL: {os.getenv('OLLAMA_BASE_URL', 'NOT_FOUND')}")
print(f"OLLAMA_EMBEDDINGS_MODEL_NAME: {os.getenv('OLLAMA_EMBEDDINGS_MODEL_NAME', 'NOT_FOUND')}")

# Test importing and initializing the agent graph
try:
    from app.services.agent_graph import agent_graph, run_agent
    print("\n=== Agent Graph Test ===")
    print("✅ Agent graph imported successfully")

    # Test a simple query
    test_response = run_agent("Hello, this is a test. Please respond briefly.")
    print(f"✅ Agent response: {test_response[:100]}...")

except Exception as e:
    print(f"❌ Error testing agent graph: {e}")
    import traceback
    traceback.print_exc()