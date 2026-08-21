# Variables
COMPOSE = docker compose -f deploy/docker-compose.yml

.PHONY: help build up down re logs clean debug

# Default target
help:
	@echo "Available commands:"
	@echo "  make build   - Build the Docker image"
	@echo "  make up      - Run the ETL pipeline inside the container"
	@echo "  make re      - Rebuild the image and rerun the pipeline"
	@echo "  make logs    - Tail the container logs"
	@echo "  make down    - Stop and remove containers"
	@echo "  make debug   - Run the local CSV debug export script"
	@echo "  make clean   - Remove cache files and raw/debug data"

# Build image
build:
	$(COMPOSE) build

# Run pipeline
up:
	$(COMPOSE) up

# Full rebuild and run (42-style 're')
re:
	$(COMPOSE) up --build

# View logs
logs:
	$(COMPOSE) logs -f

# Stop containers
down:
	$(COMPOSE) down

# Run local debug exports
debug:
	python3 scripts/export_debug_csv.py

# Clean build caches and generated data
clean:
	$(COMPOSE) down -v
	docker run --rm -v $(PWD)/data:/data alpine rm -rf /data/raw/* /data/debug_exports/*
	rm -rf __pycache__ src/__pycache__
