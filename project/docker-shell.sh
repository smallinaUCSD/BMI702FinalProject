#!/bin/bash

set -e

export IMAGE_NAME="frontend_702"

# Build the image based on the Dockerfile
docker build -t $IMAGE_NAME -f Dockerfile.dev .

# Run the container
docker run --rm --name $IMAGE_NAME -ti -v "$(pwd)/:/app/" -p 5173:5173 $IMAGE_NAME