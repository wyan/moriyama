# Moriyama — Justfile
# Install just: https://just.systems/  (brew install just)
#
# Usage:
#   just                  # list all recipes
#   just compile-resources
#   just test
#   just lint
#   just run

set dotenv-load := false

# List available recipes
default:
    @just --list

# Compile all .qrc files in resources/ into src/moriyama/*_rc.py
compile-resources:
    uv run python scripts/compile_resources.py

# Run the application
run:
    uv run moriyama

# Run the test suite
test:
    uv run pytest

# Lint and format check
lint:
    uv run ruff check src tests
    uv run ruff format --check src tests

# Auto-fix lint issues and reformat
fmt:
    uv run ruff check --fix src tests
    uv run ruff format src tests

# Build a distributable bundle via Briefcase
build:
    uv run briefcase build

# Package (produces .dmg / AppImage / MSI)
package:
    uv run briefcase package
