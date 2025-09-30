# Stage 1: Build the vector store and dependencies
FROM python:3.12-slim as builder

# Set the working directory inside the container
WORKDIR /app

# Copy requirements and install dependencies
# The context from docker-compose is the repo root, so we specify the path to backend/
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend directory into the working directory /app
COPY backend/ .

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

# Set PYTHONPATH. Since our code is now in /app, we add it to the python path.
ENV PYTHONPATH "${PYTHONPATH}:/app"

# Build the vector store. The script expects to be run from the 'backend' root.
# The module path is app.scripts.build_vector_store
RUN python -m app.scripts.build_vector_store

# Stage 2: Final application image
FROM python:3.12-slim

WORKDIR /app

# Set the python path to include the app directory
ENV PYTHONPATH "${PYTHONPATH}:/app"

# Copy only the necessary files from the builder stage
# Copy installed packages
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
# Copy application code, which now includes the generated vector store and db
COPY --from=builder /app/ .

# Set the entrypoint
# The working directory is /app, which contains the refactored backend code.
# The main application object is in app/main.py.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]