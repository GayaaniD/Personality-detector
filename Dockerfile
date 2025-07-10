# ─── Stage 1: Base Image ────────────────────────────────────────────────
FROM public.ecr.aws/docker/library/python:3.11-slim AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_NO_INTERACTION=1

# Set working directory
WORKDIR /app

# ─── Stage 2: Install dependencies ─────────────────────────────────────────────
FROM base AS dependencies

# Install Poetry
RUN pip install --upgrade pip poetry

# Copy only the dependency files
COPY pyproject.toml poetry.lock* /app/

# Install Python dependencies
RUN poetry config virtualenvs.create false \
 && poetry install --no-root --only main

# ─── Stage 3: Final build ──────────────────────────────────────────
FROM dependencies AS final

# only copy your streamlit_app folder into the container
COPY streamlit_app/ /app/

# Expose both FastAPI and Streamlit ports
EXPOSE 8000 8501

# Run FastAPI and Streamlit in parallel
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 & streamlit run streamlit_UI.py --server.port=8501 --server.address=0.0.0.0"]
