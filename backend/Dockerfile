# Stage 1: Build the vector store
FROM python:3.12-slim as builder

WORKDIR /app

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and knowledge base
COPY backend/ ./backend/

# The build process needs several environment variables.
# These are passed from docker-compose as build arguments.
ARG OPENAI_API_KEY
ARG OPENAI_API_BASE
ARG OPENAI_EMBEDDINGS_MODEL_NAME
ARG EMBEDDINGS_PROVIDER
ARG OLLAMA_BASE_URL
ARG OLLAMA_EMBEDDINGS_MODEL_NAME

# Set them as environment variables for the build script to use.
ENV OPENAI_API_KEY=${OPENAI_API_KEY}
ENV OPENAI_API_BASE=${OPENAI_API_BASE}
ENV OPENAI_EMBEDDINGS_MODEL_NAME=${OPENAI_EMBEDDINGS_MODEL_NAME}
ENV EMBEDDINGS_PROVIDER=${EMBEDDINGS_PROVIDER}
ENV OLLAMA_BASE_URL=${OLLAMA_BASE_URL}
ENV OLLAMA_EMBEDDINGS_MODEL_NAME=${OLLAMA_EMBEDDINGS_MODEL_NAME}

# Build the vector store. The script uses os.getenv() to get these values.
RUN python -m backend.build_vector_store

# Stage 2: Final application image
FROM python:3.12-slim

WORKDIR /app

# Copy only the necessary files from the builder stage
COPY --from=builder /app/backend/ ./backend/
COPY --from=builder /app/backend/ecommerce.db ./backend/
COPY --from=builder /app/backend/chroma_db/ ./backend/chroma_db/
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/

# Set the entrypoint
# The PYTHONPATH=. is crucial for uvicorn to find the 'backend' module
CMD ["sh", "-c", "PYTHONPATH=. uvicorn backend.main:app --host 0.0.0.0 --port 8000"]