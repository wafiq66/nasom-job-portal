FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_CACHE_DIR=/tmp/pip-cache

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --default-timeout=120 --retries=10 -r requirements.txt

COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run the app
CMD ["gunicorn", "nasom_job_portal.wsgi:application", "--bind", "0.0.0.0:8000"]
