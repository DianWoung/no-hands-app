# Stage 1: Build the vector store
FROM python:3.12-slim as builder

WORKDIR /app

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and knowledge base
COPY backend/ ./backend/
COPY backend/.env.example ./backend/.env

# The build process needs the API key to generate embeddings
ARG OPENAI_API_KEY
RUN sed -i "s/YOUR_OPENAI_API_KEY_HERE/${OPENAI_API_KEY}/" backend/.env

# Build the vector store
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