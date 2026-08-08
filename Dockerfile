FROM python:3.11-slim
WORKDIR /app
RUN pip install mcp httpx uvicorn starlette
COPY server.py .
CMD ["python", "server.py"]
