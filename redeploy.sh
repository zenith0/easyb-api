#!/bin/bash

# Stop and remove existing containers
docker-compose down

# Build and start new containers
docker-compose up --build -d