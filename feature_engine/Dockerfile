FROM python:3.12-slim

WORKDIR /app

COPY feature_engine/requirements.txt /app/feature_engine/requirements.txt
RUN pip install --no-cache-dir -r /app/feature_engine/requirements.txt

COPY shared /app/shared
COPY feature_engine /app/feature_engine

ENV PYTHONPATH=/app/shared:/app

EXPOSE 8001

CMD ["uvicorn", "feature_engine.app.main:app", "--host", "0.0.0.0", "--port", "8001"]
