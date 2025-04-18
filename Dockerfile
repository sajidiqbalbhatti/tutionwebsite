# Use official Python image
FROM python:3.12-slim as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy project files
COPY . .

# Run migrations and collectstatic before starting the app
RUN python manage.py makemigrations \
    && python manage.py migrate \
    && python manage.py collectstatic --noinput

# Expose port 8000 for the application
EXPOSE 8000

# Run Gunicorn server in production
CMD ["gunicorn", "tuition_porject.wsgi:application", "--bind", "0.0.0.0:8000"]
