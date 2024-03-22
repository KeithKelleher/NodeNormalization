FROM python:3.9


RUN apt-get update && apt-get install -y git nano

COPY .. /app/NodeNormalization
WORKDIR /app/NodeNormalization

RUN cd /app/NodeNormalization
RUN pip install --no-cache-dir -r requirements.txt

# overwrite repo config with our config
COPY config.json /app/NodeNormalization
COPY redis_and_api_combined/redis_config.yaml /app/NodeNormalization

ENTRYPOINT ["uvicorn", "--host", "api-container", "--port", "2434", "--workers", "1", "node_normalizer.server:app"]