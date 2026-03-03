# Session Notes — Moriyama Project

## Context

Starting a new PySide6 desktop application called **Moriyama**.
Goals: runs on macOS, Linux, and (optionally) Windows.
Current state: project skeleton only, no real application code yet.

---

## Decisions made

### Dependency management — `uv`
- Chosen over Poetry and Hatch for its speed and native pyproject.toml support.
- `uv sync` reads `pyproject.toml` and writes `uv.lock`, creates `.venv`.
- Dev dependencies (briefcase, pytest, ruff) live under `[tool.uv] dev-dependencies`.

### Build backend — `hatchling`
- Lightweight PEP 517/660 compliant backend.
- `[tool.hatch.build.targets.wheel] packages = ["src/moriyama"]` tells it
  where the source lives.
- No compiled extensions, so any pure-Python backend would work; hatchling
  is the natural companion to the Hatch ecosystem and plays well with uv.

### Project layout — `src/` layout
- Source lives in `src/moriyama/` rather than at the repo root.
- Prevents accidental imports of the un-installed package during testing.
- Entry point: `src/moriyama/__main__.py` — exposes `main()` and supports
  `python -m moriyama`.
- Console script `moriyama` and GUI script `moriyama-gui` both point to
  `moriyama.__main__:main`.

### Bundling — `Briefcase`
- Chosen over PyInstaller and Nuitka because it is purpose-built for GUI
  applications and handles the full lifecycle (create / build / run / package).
- Produces platform-native artifacts without hand-edited spec files:
  - macOS → `.app` bundle (optionally wrapped in `.dmg`)
  - Linux → AppImage (via `manylinux_2_28`)
  - Windows → MSI installer
- Config lives entirely in `pyproject.toml` under `[tool.briefcase]`.
- `universal_build = true` set for macOS to produce arm64+x86_64 fat binary.
- Icons: place `resources/icon.icns` (macOS), `resources/icon.png` (Linux),
  `resources/icon.ico` (Windows) — Briefcase appends the right extension
  automatically.

### Linting / formatting — `ruff`
- Replaces flake8 + isort + pyupgrade in a single fast tool.
- `select = ["E", "F", "W", "I", "UP"]` covers errors, warnings, imports,
  and pyupgrade modernisations.
- `line-length = 100`, `target-version = "py311"`.

### Testing — `pytest` + `pytest-qt`
- `pytest-qt` provides the `qtbot` fixture which manages widget lifecycle
  and event-loop plumbing.
- Smoke test in `tests/test_main_window.py` verifies the window title.

---

## Qt resource system (images, icons, etc.)

Qt uses a virtual filesystem addressed with `:/prefix/file` URIs.
To add an image (e.g. the splash screen):

1. **Place the file** at `resources/images/splash.png` (or any subfolder under `resources/`).

2. **Create / update** `resources/resources.qrc`:
   ```xml
   <!DOCTYPE RCC>
   <RCC version="1.0">
       <qresource prefix="/images">
           <file alias="splash.png">images/splash.png</file>
       </qresource>
   </RCC>
   ```

3. **Compile** (re-run whenever images change):
   ```bash
   just compile-resources
   # or, without just:
   uv run python scripts/compile_resources.py
   ```
   `scripts/compile_resources.py` discovers all `*.qrc` files in `resources/`
   automatically — no manual updates needed when adding new `.qrc` files.

4. **Import** the compiled module once at startup (the import registers all resources):
   ```python
   import moriyama.resources_rc  # noqa: F401
   ```

5. **Use** the URI anywhere in the app:
   ```python
   QPixmap(":/images/splash.png")
   ```

> `resources_rc.py` is a generated file — add it to `.gitignore` or commit it,
> but never edit it by hand.

### Task runner — `just`

`uv` has no built-in task runner. We use `just` (`brew install just`).
All common tasks are in `Justfile` at the repo root:

```
just                    # list all recipes
just compile-resources  # recompile .qrc → *_rc.py
just run                # uv run moriyama
just test               # uv run pytest
just lint               # ruff check + format check
just fmt                # ruff autofix + reformat
just build              # briefcase build
just package            # briefcase package (.dmg / AppImage / MSI)
```

On Windows without `just`, every recipe maps directly to its `uv run …` equivalent.

---

## What has NOT been done yet

- No real application logic — only a `QMainWindow` with a `QLabel("Hello, World!")`.
- No icons added yet.
- `uv sync` / `uv.lock` not run (uv was not available in the session environment);
  the user must run `uv sync` locally on first checkout.
- No CI/CD configuration (GitHub Actions, etc.).
- No application-level architecture decisions (MVC, signals/slots patterns, etc.).

---

## Next logical steps (when resuming)

1. `uv sync` to materialise the lockfile and `.venv`.
2. `uv run moriyama` to verify the hello-world window opens.
3. `uv run pytest` to verify the smoke test passes.
4. Add app icons to `resources/`.
5. Decide on application architecture before writing real code:
   - How to structure windows / views (single-window vs multi-window).
   - Whether to use Qt Designer (`.ui` files) or code-only layouts.
   - Resource management (Qt resource system `pyrcc6` vs plain file paths).
6. Set up CI (GitHub Actions matrix: ubuntu-latest, macos-latest, windows-latest).
