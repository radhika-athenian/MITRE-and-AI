# MITRE-and-AI

This project provides a scaffolding for multiple services that work together via Docker Compose. The repository is organized into service directories under `services/` and shared libraries under `libs/`.

## Project Overview

 - **services/** – Individual microservices such as `ingest`.
   Additional agents will be added over time.
- **libs/** – Shared libraries used across services.
- **docker-compose.yml** – Orchestrates services during development.
- **Makefile** – Convenience commands for building and running containers.
  It now includes targets for running unit tests and linting.

## Setup Instructions

1. Ensure you have Python 3.11, Docker, and Docker Compose installed.
2. Clone the repository.
3. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install -r services/ingest/requirements.txt  # service-specific
   pip install -r services/graph/requirements.txt   # service-specific
   pip install -r services/analysis/requirements.txt  # service-specific
   ```
4. The `graph` service listens to classified alerts via Redis and maintains
   a directed NetworkX graph. It runs alongside the `ingest` service using
   the provided Dockerfile in `services/graph`.
5. The `analysis` service computes the top attack paths from the graph and
   re-ranks them using a simple Random Forest model.
6. Build the service images with `make build`.
7. Start the stack with `make up` and stop it with `make down`.
8. Run tests with `make test` and lint with `make lint`.

## Branching Strategy

Development happens on short-lived feature branches created from the
`main` branch. The `main` branch always contains stable code and is
where pull requests should target when merging new features or fixes.

## Development Workflow

- Modify or add code inside the appropriate service directory.
- Use the Makefile targets to build and run services locally.
- Continuous integration is handled via GitHub Actions in `.github/workflows/ci.yml`.

### Ingest Service

The `ingest` service exposes a `POST /alerts` endpoint which classifies
incoming alerts using a simple LLM-based stub and publishes the result to the
internal message bus.


## License

This project is licensed under the [MIT License](LICENSE).

