# AGENTS.md

## Project Overview

- **Project name**: Moriyama
- **Type**: Cross-platform PySide6 desktop application (Python ≥ 3.11)
- **Package manager**: uv
- **Build backend**: hatchling
- **Bundler**: Briefcase

## Setup

```bash
uv sync
```

## Running the Application

```bash
uv run moriyama
# or
uv run python -m moriyama
```

## Common Commands

All commands available via `just` (run `just` to list them):

| Command | Description |
|---------|-------------|
| `just run` | Run the application |
| `just test` | Run pytest |
| `just lint` | Run ruff check + format check |
| `just fmt` | Run ruff autofix + reformat |
| `just compile-resources` | Compile Qt resource files (.qrc → _rc.py) |
| `just build` | Run briefcase build |
| `just package` | Run briefcase package |

Without `just`, use:
```bash
uv run pytest
uv run ruff check src tests
uv run ruff format src tests
uv run python scripts/compile_resources.py
uv run briefcase build
uv run briefcase package
```

## Testing

```bash
uv run pytest
```

## Linting/Formatting

```bash
uv run ruff check src tests
uv run ruff format src tests
```

## Building

```bash
uv run briefcase create  # First time: scaffold platform-specific project
uv run briefcase build   # Build distributable
uv run briefcase run    # Run packaged app locally
uv run briefcase package # Build + package (.dmg / AppImage / MSI)
```

## Qt Resources

Place images in `resources/images/` and update `resources/resources.qrc`, then run:
```bash
just compile-resources
```
Import with `import moriyama.resources_rc  # noqa: F401` and use `QPixmap(":/images/filename.png")`.