# MITRE-and-AI

This project provides a scaffolding for multiple services that work together via Docker Compose. The repository is organized into service directories under `services/` and shared libraries under `libs/`.

## Project Overview

 - **services/** – Individual microservices such as `ingest`.
   A `graph` directory is included only as a placeholder.
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
4. The `graph` service is only a placeholder. Add your own Dockerfile in
   `services/graph` or comment out the service in `docker-compose.yml`.
5. Build the service images with `make build`.
6. Start the stack with `make up` and stop it with `make down`.
7. Run tests with `make test` and lint with `make lint`.

## Branching Strategy

Development happens on short-lived feature branches created from the
`main` branch. The `main` branch always contains stable code and is
where pull requests should target when merging new features or fixes.

## Development Workflow

- Modify or add code inside the appropriate service directory.
- Use the Makefile targets to build and run services locally.
- Continuous integration is handled via GitHub Actions in `.github/workflows/ci.yml`.


## License

This project is licensed under the [MIT License](LICENSE).

