# Moriyama

A cross-platform desktop application built with PySide6.

## Requirements

- Python ≥ 3.11
- [uv](https://docs.astral.sh/uv/) (dependency management)

## Setup

```bash
# Install dependencies (creates .venv automatically)
uv sync

# Run the application
uv run moriyama

# Or via Python module
uv run python -m moriyama
```

## Development

```bash
# Run tests
uv run pytest

# Lint / format
uv run ruff check src tests
uv run ruff format src tests
```

## Bundling (cross-platform)

Bundling is handled by [Briefcase](https://briefcase.readthedocs.io/).

```bash
# First time — scaffold platform-specific project
uv run briefcase create

# Build distributable artifact
uv run briefcase build

# Run the packaged app locally
uv run briefcase run

# Build + package in one step (creates .app / AppImage / .msi)
uv run briefcase package
```

### Platform outputs

| Platform | Artifact        |
|----------|-----------------|
| macOS    | `.app` bundle (inside `.dmg` when packaged) |
| Linux    | AppImage        |
| Windows  | MSI installer   |

## Project layout

```
moriyama/
├── pyproject.toml       # build system, deps, tool config
├── README.md
├── resources/
│   └── icon.*           # app icons (add .icns / .png / .ico)
├── src/
│   └── moriyama/
│       ├── __init__.py
│       └── __main__.py  # entry point
└── tests/
    └── test_main_window.py
```
