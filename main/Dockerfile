FROM python:3.10-slim-bullseye AS python

# Environment variables
ENV DJANGO_SETTINGS_MODULE=vepemamoduloum.settings.local
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
# Ensure you set DEBUG to false in production!
ENV DEBUG=false

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    python3-dev \
    musl-dev \
    python3-dev \
    libffi-dev \
    && pip install -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
    
# Copy application code
COPY . .

# Set secret keys
ARG DJANGO_SECRET_KEY
ENV DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY

ARG SECRET_KEY
ENV SECRET_KEY=${SECRET_KEY}

# Collect static files
RUN python manage.py collectstatic --noinput

# Apply migrations
RUN python manage.py makemigrations
RUN python manage.py migrate

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--reload", "--timeout=8000", "--workers=2", "vepemamoduloum.wsgi:application"]
