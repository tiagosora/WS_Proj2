FROM python:3.11-slim
LABEL authors="pjnp5"

# Set work directory
WORKDIR /django

# Install dependencies
COPY requirements.txt /django/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install Node.js and npm
RUN apt-get update && apt-get install -y curl gnupg \
    && curl -sL https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get install -y nodejs supervisor

# Copy project
COPY webproj /django/webproj

WORKDIR /django/webproj

# Install Tailwind dependencies
RUN npm install

# Set environment variable to skip SPARQL queries during build
ENV RUN_SPARQL_QUERIES=false

# Install Tailwind and migrate the database
RUN python manage.py tailwind install
RUN python manage.py migrate

# Reset environment variable for runtime
ENV RUN_SPARQL_QUERIES=true

# Add supervisor configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Run supervisord
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
