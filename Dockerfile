FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_CACHE_DIR=/tmp/pip-cache

WORKDIR /app

# Dependency layer (optimized for caching)
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --default-timeout=120 --retries=10 -r requirements.txt

# Application code layer
COPY . . 
# REMOVE: COPY .env.docker /app/.env  <-- Not needed due to docker-compose env_file

# Optional: Since docker-compose overrides it, you can simplify the CMD or leave it.
CMD ["gunicorn", "nasom_job_portal.wsgi:application", "--bind", "0.0.0.0:8000"]