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
   ```
4. Build the service images with `make build`.
5. Start the stack with `make up` and stop it with `make down`.
6. Run tests with `make test` and lint with `make lint`.

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

### Graph Service

The `graph` service maintains an in-memory directed graph using NetworkX. It
provides a `/graph/update` endpoint to add edges and a `/graph` endpoint to
retrieve the graph in node-link JSON format.

### Analysis Service

The `analysis` service exposes a `/analysis/path` endpoint that returns up to
`k` shortest paths between two nodes using Dijkstra-based search. For testing
purposes it also provides `/analysis/edge` to add edges to its internal graph.


## License

This project is licensed under the [MIT License](LICENSE).

