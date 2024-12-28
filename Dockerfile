# Use the official Python image from the Docker Hub
FROM python:3.13.0-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PEGASUS_MEDIA_URL=$PEGASUS_MEDIA_URL
ENV PEGASUS_MEDIA_ROOT=$PEGASUS_MEDIA_ROOT
#ENV PEGASUS_DATABASE_URL=$PEGASUS_DATABASE_URL

# Set the working directory
WORKDIR /app/

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    gettext-base \
    libgconf-2-4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libgdk-pixbuf2.0-0 \
    libgtk-3-0 \
    libgbm-dev \
    libnss3-dev \
    libxss-dev \
    unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project
COPY src /app/

ENV PYTHONPATH=/app/__pypackages__/3.13/lib/:/app/ \
    PATH=/app/:__pypackages__/3.13/bin/:$PATH \
#    CHDIR=/src/ \
    DJANGO_SETTINGS_MODULE=albdif.config.settings

#RUN python manage.py migrate \
#    && python manage.py showmigrations

#CMD ["python", "manage.py", "showmigrations"]

# Expose the port on which Django will run
EXPOSE 8000

# Run the application
CMD ["django-admin", "runserver", "0.0.0.0:8000"]
