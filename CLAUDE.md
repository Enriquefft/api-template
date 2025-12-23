# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python FastAPI template for WhatsApp/Twilio integration with AI chat capabilities. Uses SQLModel for PostgreSQL persistence and OpenAI for chat completions.

## Development Environment

This project uses Nix Flakes with direnv for reproducible development:

```bash
direnv allow          # Auto-loads environment on cd
nix develop           # Alternative: manual nix shell
```

## Common Commands

```bash
# Run the application
uv run start

# Testing
uv run pytest                              # All tests
uv run pytest tests/sample_test.py::test_answer  # Single test

# Linting and formatting
uv run ruff format                         # Format code
uv run ruff check --fix                    # Lint with auto-fix
uv run pyright                             # Type check (strict mode)

# Dependencies
uv sync                                    # Install dependencies
uv lock                                    # Update lock file
```

## Architecture

- **main.py** - FastAPI app with `/health` and `/message` (Twilio webhook) endpoints
- **ai.py** - OpenAI client wrapper for chat completions (gpt-3.5-turbo)
- **models.py** - SQLModel models and database configuration (User model, schema auto-creation)
- **env.py** - Environment variable validation and configuration
- **wsp.py** - Twilio WhatsApp messaging client

Database uses PostgreSQL with schema name derived from `PROJECT_NAME` env var. Connection pooling configured with `pool_pre_ping=True` and 300s recycle.

## Git Hooks (Lefthook)

Pre-commit and pre-push hooks automatically run ruff, pyright, and pytest. Commit messages must follow conventional commits format (feat, fix, docs, refactor, etc.).

## Code Quality Settings

- **Ruff**: `select = ["ALL"]` with minimal ignores
- **Pyright**: `strict` mode, Python 3.14
- All code must pass type checking and linting before commit

## Coding Guidelines

- **Never use inline `# pyright: ignore` comments.** If a library has incomplete type stubs, configure the rule as a warning globally in `pyproject.toml` under `[tool.pyright]` instead of suppressing errors inline.
