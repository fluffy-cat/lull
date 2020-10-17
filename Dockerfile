FROM python:3.6.9-alpine3.10

WORKDIR /app

# Build requirements
COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && \
  apk add --update --no-cache --virtual .build-deps build-base python3-dev || true && \
  pipenv install --system --deploy --ignore-pipfile && \
  apk del .build-deps build-base python3-dev && \
  pip uninstall pipenv -y && \
  apk add --no-cache tzdata openssh-client

COPY lull lull
COPY bin/run.sh default_config.yml ./
RUN chmod +x run.sh

VOLUME /config
ENV PYTHONUNBUFFERED=1
CMD /app/run.sh
