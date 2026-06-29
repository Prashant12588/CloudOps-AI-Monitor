#!/bin/bash

CONTAINER_NAME="cloudops-app"

if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "$(date): $CONTAINER_NAME is down. Restarting..."
    docker start $CONTAINER_NAME
else
    echo "$(date): $CONTAINER_NAME is running."
fi
