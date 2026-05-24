# syntax=docker/dockerfile:1

# ARG before any FROM is global — available to all FROM lines
ARG PYTHON_VERSION=3.12.3

# ── Stage 1: build React frontend ────────────────────────────
FROM node:20-alpine AS frontend-builder
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm ci && npm install --no-save @rollup/rollup-linux-x64-musl
COPY frontend/ ./
RUN npm run build

# ── Stage 2: Python / Flask backend ──────────────────────────
FROM python:${PYTHON_VERSION}-alpine AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

RUN apk update && apk add --no-cache \
    gcc \
    g++ \
    gfortran \
    libc-dev \
    libffi-dev \
    musl-dev \
    build-base \
    python3-dev \
    py3-pip \
    openblas-dev

WORKDIR /app

COPY backend/requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser . .

# Copy the built React app from stage 1
COPY --from=frontend-builder --chown=appuser:appuser /frontend/dist ./frontend/dist

ENV HOME=/tmp

USER appuser

EXPOSE 5000

CMD ["gunicorn", "--chdir", "backend", "interface:app", "-b", "0.0.0.0:5000", "--workers", "2", "--worker-tmp-dir", "/tmp"]
