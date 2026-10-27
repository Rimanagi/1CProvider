FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Proxy values are supplied only during `docker build`; do not hard-code them here.
ARG HTTP_PROXY
ARG HTTPS_PROXY
ARG NO_PROXY
ARG http_proxy
ARG https_proxy
ARG no_proxy

COPY requirements.txt ./
RUN python -m pip install --no-cache-dir --require-hashes -r requirements.txt

COPY src ./src

RUN addgroup --system app && adduser --system --ingroup app app
USER app

EXPOSE 52010

CMD ["python", "-m", "src.main"]
