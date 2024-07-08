#!/bin/bash

REPO_DIR=$(basename "$(pwd)")
REPO_DIR=$(echo "$REPO_DIR" | tr '[:upper:]' '[:lower:]')

set -e

COMPOSE_FILE="docker-compose.yml"

echo "Removing Services"
docker-compose -f $COMPOSE_FILE down

echo "Building and starting Docker Compose services..."
docker-compose -f $COMPOSE_FILE up --build -d

echo "Waiting for services to become healthy..."
docker-compose -f $COMPOSE_FILE ps

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

check_service_health "$REPO_DIR-graphdb-1"

docker-compose -f $COMPOSE_FILE logs graphdb-init | grep -q "Data added to the repository" && echo "GraphDB initialization completed successfully."

check_service_health "$REPO_DIR-web-1"

echo "All services are up and running."

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