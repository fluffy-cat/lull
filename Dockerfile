FROM python:3.8.6-alpine3.12

WORKDIR /app

# Build requirements
COPY requirements.txt .
RUN apk add --update --no-cache --virtual .build-deps build-base python3-dev || true && \
  pip install --no-cache-dir -r requirements.txt && \
  apk del .build-deps && \
  apk add --no-cache tzdata

COPY lull lull
COPY bin/run.sh default_config.yml ./
RUN chmod +x run.sh

VOLUME /config
ENV PYTHONUNBUFFERED=1
CMD /app/run.sh
