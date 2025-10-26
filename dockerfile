# Dockerfile
FROM public.ecr.aws/docker/library/python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system deps (optional but helpful for ssl/cert robustness)
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates && rm -rf /var/lib/apt/lists/*

# Add requirements first for layer caching
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Add app code
COPY app.py .

ENV PORT=8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
