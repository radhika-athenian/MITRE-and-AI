# MITRE-and-AI

This project provides a scaffolding for multiple services that work together via Docker Compose. The repository is organized into service directories under `services/` and shared libraries under `libs/`.

## Project Overview

- **services/** – Individual microservices such as `ingest` and `graph`.
- **libs/** – Shared libraries used across services.
- **docker-compose.yml** – Orchestrates services during development.
- **Makefile** – Convenience commands for building and running containers.

## Setup Instructions

1. Ensure you have Docker and Docker Compose installed.
2. Clone the repository and run `make build` to build the service images.
3. Start the stack with `make up`.
4. Stop services with `make down`.

## Development Workflow

- Modify or add code inside the appropriate service directory.
- Use the Makefile targets to build and run services locally.
- Continuous integration is handled via GitHub Actions in `.github/workflows/ci.yml`.

