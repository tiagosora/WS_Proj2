#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Define the Docker Compose file path
COMPOSE_FILE="docker-compose.yml"

echo "Removing Services"
docker-compose -f $COMPOSE_FILE down

# Build and start the Docker Compose services
echo "Building and starting Docker Compose services..."
docker-compose -f $COMPOSE_FILE up --build -d

# Wait for services to become healthy
echo "Waiting for services to become healthy..."
docker-compose -f $COMPOSE_FILE ps

# Function to check the health status of a service
check_service_health() {
  service_name=$1
  max_attempts=20
  attempt=1

  while [ $attempt -le $max_attempts ]; do
    health_status=$(docker inspect --format='{{.State.Health.Status}}' "${service_name}")
    if [ "$health_status" == "healthy" ]; then
      echo "${service_name} is healthy."
      return 0
    fi
    echo "Waiting for ${service_name} to become healthy (attempt: $attempt)..."
    attempt=$((attempt + 1))
    sleep 10
  done

  echo "Service ${service_name} did not become healthy within the expected time."
  return 1
}

# Check the health of the graphdb service
check_service_health "ws_proj2-graphdb-1"

# Ensure that the GraphDB initialization is completed successfully
docker-compose -f $COMPOSE_FILE logs graphdb-init | grep -q "Data added to the repository" && echo "GraphDB initialization completed successfully."

# Check the health of the web service
check_service_health "ws_proj2-web-1"

echo "All services are up and running."

# Open the URLs in the default web browser
if command -v xdg-open > /dev/null; then
  xdg-open http://localhost:7200
  xdg-open http://localhost:8000
elif command -v open > /dev/null; then
  open http://localhost:7200
  open http://localhost:8000
else
  echo "Please open the following URLs in your browser in order to use the app and see the database interface:"
  echo "http://localhost:7200"
  echo "http://localhost:8000"
fi