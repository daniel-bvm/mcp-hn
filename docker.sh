#!/bin/bash

# Build the Docker image
echo "Building Docker image..."
docker build -t hackernews .

if [ $? -ne 0 ]; then
    echo "Docker build failed!"
    exit 1
fi

# Remove existing container if it exists
echo "Removing existing container..."
docker rm -f hackernews || true

# Check if .env file exists, create empty one if not
if [ ! -f .env ]; then
    echo "Creating empty .env file..."
    touch .env
fi

# Run the container
echo "Starting container..."
docker run --rm -it -p 4000:80 \
--env-file .env \
-v "$(pwd)/data:/storage" -v ./:/workspace \
--name hackernews \
hackernews