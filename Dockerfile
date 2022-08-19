FROM python:3.7-alpine

ENV PYTHONPATH=/app/ablyproject

ENV PYTHONUNBUFFERED=1

RUN addgroup -S lazyer && adduser -h /app/config -S lazyer -G lazyer 

COPY --chown=lazyer:lazyer requirements.txt /app/requirements.txt

RUN apk update --no-cache \
 && apk add --no-cache postgresql-dev \
 && apk add --no-cache --virtual .build-deps \
    gcc \
    python3-dev \
    musl-dev \
    libffi-dev \
 && pip install --no-cache-dir --disable-pip-version-check -r /app/requirements.txt \
 && apk del .build-deps \
 && rm -rf /app/requirements.txt

COPY --chown=lazyer:lazyer . /app/ablyproject

WORKDIR /app/ablyproject/ablyproject/

EXPOSE 8000