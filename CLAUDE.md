# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build and Run Commands
- Run application: `docker-compose up --build`
- Stop application: `docker-compose down`
- Stop and remove volumes: `docker-compose down -v`
- Development environment: `mise install` (requires mise)
- Install dependencies: `uv pip install -r requirements.txt`
- Lint code: `ruff check .`
- Format code: `ruff format .`

## Code Style Guidelines
- Python version: 3.13+
- Formatting: Follow PEP 8 style guide
- Imports: Standard library first, then third-party packages
- Type annotations: Use for function parameters and return values
- Variable naming: snake_case for variables and functions
- Error handling: Use try/except blocks with specific exceptions
- Logging: Use Python's built-in logging module with consistent formatting
- Environment variables: Used for configuration
- Database operations: Use parameterized queries to prevent SQL injection

## Git Workflow
- Use Conventional Commits format for all commit messages
- Prefixes: feat, fix, docs, style, refactor, perf, test, build, ci, chore, work
- Format: `<type>: <description>` (e.g., `feat: add new sensor support`)

## Project Structure
- Main application code in `shelly-to-postgres/main.py`
- Containerized with Docker and PostgreSQL
- Using mise for tool management and uv for Python package management