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

There are two ways to run this project: using Docker (recommended for ease of use) or running the services manually.

### Option 1: Using Docker (Recommended)

This is the easiest way to get the entire application running with a single command.

**Prerequisites:**
- Docker and Docker Compose installed.
- An OpenAI API Key.

**Instructions:**

1.  **Configure Environment**:
    - In the project's root directory, you'll find a file named `.env.example`.
    - Create a copy of this file and name it `.env`.
    - Open the new `.env` file and fill in your values.
      - **`OPENAI_API_KEY`** is always required.
      - To use a local model for embeddings (like Llama), set **`EMBEDDINGS_PROVIDER="ollama"`**.
      - You can also customize the API base URL, chat model, and embedding model names.

2.  **Build and Run**:
    - Open your terminal in the project's root directory.
    - Run the following command:
      ```bash
      docker-compose up --build
      ```
    - This command will build all images (including the vector store) and start all services (backend, frontend, and ollama). It may take a few minutes the first time.

3.  **(If using Ollama) Pull a Local Model**:
    - While `docker-compose` is running in another terminal, you need to pull the embedding model for Ollama to use.
    - Run the following command:
      ```bash
      docker exec -it ollama ollama pull nomic-embed-text
      ```
    - You only need to do this once.

4.  **Chat with Your AI!**
    - Once the services are running, open your web browser and navigate to:
      [http://localhost:3000](http://localhost:3000)
    - The chat interface should be ready to use.

---

### Option 2: Running Manually

Follow these steps to run the frontend and backend services separately.

**Prerequisites:**
- Python 3.10+
- Node.js and npm
- An OpenAI API Key

**Step 1: Configure Environment**

1.  Navigate to the `backend/` directory.
2.  You will find a file named `backend/.env.example`. Create a copy named `.env` in the same directory.
3.  Open the new `.env` file and fill in your values. At a minimum, you must provide your `OPENAI_API_KEY`. You can also customize the API base URL and model names here.

**Step 2: Set Up and Run the Backend**

1.  **Install Dependencies**:
    From the project's root directory, run:
    ```bash
    pip install -r backend/requirements.txt
    ```

2.  **Build the Knowledge Base**:
    This step "teaches" the AI about the products. *This requires a valid OpenAI API key.*
    ```bash
    python -m backend.build_vector_store
    ```

3.  **Run the Backend Server**:
    The `PYTHONPATH=.` part is important.
    ```bash
    PYTHONPATH=. uvicorn backend.main:app --host 0.0.0.0 --port 8000
    ```
    Your backend is now running at `http://localhost:8000`.

**Step 3: Set Up and Run the Frontend**

1.  **Install Dependencies**:
    In a **new terminal window**, navigate to the `frontend/` directory and run:
    ```bash
    npm install
    ```

2.  **Run the Frontend Server**:
    ```bash
    npm start
    ```

**Step 4: Chat with Your AI!**

Your browser should open to `http://localhost:3000`. The status on the page should say "Connected".

You can now start asking questions! Try these:

- `How much is the iPhone 15 Pro?`
- `What is the battery life of the Sony WH-1000XM5 Headphones?` (This will use the knowledge base)
- `Is the Organic Cotton T-Shirt in stock?` (This will use the database tool)
- `What is the status of order #12345?` (This will use the database tool)
- `Compare the iPhone 15 Pro and the MacBook Pro` (This will test the agent's reasoning)