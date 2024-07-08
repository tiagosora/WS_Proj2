#!/bin/sh

# Wait for GraphDB to be ready
until curl -f -H 'Accept: text/html' http://graphdb:7200; do
  echo "Waiting for GraphDB to be ready..."
  sleep 5
done

# Check if the repository already exists
if ! curl -f -s -X GET -H "Accept: application/json" "http://graphdb:7200/rest/repositories" | grep -q ws_project; then
  echo "Creating repository ws_project..."
  curl -X POST \
    http://graphdb:7200/rest/repositories \
    -H 'Content-Type: multipart/form-data' \
    -F "config=@/repo-config.ttl"
    echo "Repository Created"

  echo "Loading data into repository ws_project..."
  curl -X POST \
    http://graphdb:7200/repositories/ws_project/statements \
    -H "Content-Type: application/rdf+xml" \
    --data-binary @/data.rdf

  curl -X POST \
    http://graphdb:7200/repositories/ws_project/statements \
    -H "Content-Type: application/rdf+xml" \
    --data-binary @/ontology.owl
  echo "Data loaded successfully"

else
  echo "Repository ws_project already exists."
fi
