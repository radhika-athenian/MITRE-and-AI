# Contributing

Thank you for your interest in improving this project!

## Branching Strategy

- **main**: Stable branch. All production-ready code lives here.
- **feature branches**: Start new work from `main` using short-lived branches. Merge back via pull request.

## Development Workflow

1. Create a feature branch off `main`.
2. Make your changes and commit them with descriptive messages.
3. Verify quality by running:
   ```
   make lint
   make test
   ```
4. Push your branch and open a pull request targeting `main`.
5. A project maintainer will review your PR before merging.
