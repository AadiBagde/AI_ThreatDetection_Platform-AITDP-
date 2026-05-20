FROM python:3.12-slim

WORKDIR /app

COPY ml_engine/requirements.txt /app/ml_engine/requirements.txt
RUN pip install --no-cache-dir -r /app/ml_engine/requirements.txt

COPY shared /app/shared
COPY models /app/models
COPY ml_engine /app/ml_engine

ENV PYTHONPATH=/app/shared:/app

EXPOSE 8002

CMD ["uvicorn", "ml_engine.app.main:app", "--host", "0.0.0.0", "--port", "8002"]
