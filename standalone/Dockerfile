FROM python:3.9

RUN apt-get update && apt-get install -y git nano
RUN git clone https://github.com/TranslatorSRI/NodeNormalization /app/NodeNormalization

WORKDIR /app/NodeNormalization

RUN cd /app/NodeNormalization
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/NodeNormalization

# overwrite repo config with standalone config
COPY standalone/config.json /app/NodeNormalization
COPY standalone/redis_config.yaml /app/NodeNormalization

CMD uvicorn --host api-container --port 2434 --workers 1 node_normalizer.server:app
#CMD python load.py
