FROM python:3.9

RUN apt-get update && apt-get install -y git nano

WORKDIR /app/NodeNormalization
RUN cd /app/NodeNormalization
COPY . /app/NodeNormalization

RUN pip install --no-cache-dir -r requirements.txt

COPY standalone/config.json /app/NodeNormalization
COPY standalone/redis_config.yaml /app/NodeNormalization

CMD uvicorn --host api-container --port 2434 --workers 1 node_normalizer.server:app
#CMD python load.py
