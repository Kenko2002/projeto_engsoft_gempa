FROM python:3.10-slim-bullseye AS python

# Environment variables
ENV DJANGO_SETTINGS_MODULE=vepemamoduloum.settings.local
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV DEBUG=true

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    python3-dev \
    musl-dev \
    #libpq-dev \
    python3-dev \
    libpq-dev \
    libffi-dev \
    && pip install -r requirements.txt

# Copy application code
COPY . .

# Set secret keys
ARG DJANGO_SECRET_KEY
ENV DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY

ARG SECRET_KEY
ENV SECRET_KEY=${SECRET_KEY}

# Remove PostgreSQL-related environment variable
# ENV DB_ENGINE_PRODUCTION=django.db.backends.postgresql

# Collect static files
RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--reload", "--timeout=8000", "--workers=2", "vepemamoduloum.wsgi:application"]
