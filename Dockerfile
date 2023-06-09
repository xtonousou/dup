# syntax=docker/dockerfile:1

FROM python:alpine3.18

LABEL org.opencontainers.image.authors="root@xtonousou.com"

USER 0

WORKDIR /app

COPY ./dup.py ./requirements.txt /app
COPY ./notifications /app/notifications
COPY ./providers /app/providers

RUN python -m pip install pip -U --no-cache-dir && \
    python -m pip install -r ./requirements.txt --no-cache-dir

ENTRYPOINT ["python", "-BO", "dup.py", "--"]
