FROM public.ecr.aws/docker/library/python:3.11-slim
RUN pip install fastapi uvicorn boto3
WORKDIR /app
COPY app.py .
ENV PORT=8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
