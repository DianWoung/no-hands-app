# AI E-commerce Shopping Assistant

This project is a fully functional prototype of an AI-powered shopping assistant for an e-commerce platform. It features a conversational web interface where users can ask about products, check stock, and get order status updates in natural language.

The assistant is built with a modern, robust tech stack:
- **Backend**: FastAPI (Python) with a WebSocket endpoint for real-time chat.
- **AI Brain**: LangChain and LangGraph for creating a stateful, tool-using AI agent.
- **Database**: SQLAlchemy ORM for interacting with a SQLite database (easily switchable to MySQL/PostgreSQL).
- **Knowledge Base**: ChromaDB as a vector store for Retrieval-Augmented Generation (RAG).
- **Frontend**: React with TailwindCSS for a clean, modern user interface.

---

## How to Run This Project

Follow these steps to get the AI assistant running on your local machine.

### Prerequisites

- Python 3.10+
- Node.js and npm
- An OpenAI API Key

### Step 1: Configure Your API Key

1.  Navigate to the `backend/` directory.
2.  You will find a file named `.env`. Open it.
3.  Replace the placeholder text `"YOUR_OPENAI_API_KEY_HERE"` with your actual OpenAI API key.

### Step 2: Set Up and Run the Backend

1.  **Install Dependencies**:
    Open your terminal, navigate to the project's root directory, and run:
    ```bash
    pip install -r backend/requirements.txt
    ```

2.  **Build the Knowledge Base**:
    This step "teaches" the AI about the products by reading the documents in `backend/knowledge_base/` and storing them in the vector database.
    ```bash
    python -m backend.build_vector_store
    ```
    *Note: This command requires a valid OpenAI API key to be set, as it generates embeddings.*

3.  **Run the Backend Server**:
    Now, start the FastAPI server. The `PYTHONPATH=.` part is important to ensure Python can find the `backend` module.
    ```bash
    PYTHONPATH=. uvicorn backend.main:app --host 0.0.0.0 --port 8000
    ```
    Your backend is now running at `http://localhost:8000`.

### Step 3: Set Up and Run the Frontend

1.  **Install Dependencies**:
    Open a **new terminal window**, navigate to the `frontend/` directory, and run:
    ```bash
    npm install
    ```

2.  **Run the Frontend Server**:
    Once the installation is complete, start the React development server:
    ```bash
    npm start
    ```
    This will automatically open a new tab in your web browser.

### Step 4: Chat with Your AI!

Your browser should now be open to `http://localhost:3000`, displaying the chat interface. The status on the page should say "Connected".

You can now start asking questions! Try these:

- `How much is the iPhone 15 Pro?`
- `What is the battery life of the Sony WH-1000XM5 Headphones?` (This will use the knowledge base)
- `Is the Organic Cotton T-Shirt in stock?` (This will use the database tool)
- `What is the status of order #12345?` (This will use the database tool)
- `Compare the iPhone 15 Pro and the MacBook Pro` (This will test the agent's reasoning)