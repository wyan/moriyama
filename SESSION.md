# Moriyama — Session State

_Last updated: 2026-03-03_

## Project overview

PySide6 cross-platform desktop app called **Moriyama**.

## Stack

- Python ≥ 3.11
- PySide6 ≥ 6.7
- uv — dependency management (`uv sync`, `uv run`)
- hatchling — PEP 517 build backend
- Briefcase ≥ 0.3 — cross-platform bundler (macOS `.app`/`.dmg`, Linux AppImage, Windows MSI)
- pytest + pytest-qt — testing (`qtbot` fixture)
- ruff — linting and formatting
- just — task runner (`brew install just`)

## Commands

```bash
uv sync                                      # install all deps, create .venv
uv run moriyama                              # run the app
uv run pytest                                # run tests
just compile-resources                       # recompile .qrc → resources_rc.py
uv run python scripts/compile_resources.py  # same, without just
just lint                                    # ruff check + format check
just fmt                                     # ruff autofix + reformat
uv run briefcase build                       # build native bundle
uv run briefcase package                     # produce .dmg / AppImage / MSI
```

## Files

| File | Description |
|---|---|
| `pyproject.toml` | Build system, deps, tool config. Uses hatchling backend, uv for deps, Briefcase for bundling. Dev deps in `[dependency-groups] dev` (PEP 735). |
| `src/moriyama/__init__.py` | Empty package marker. |
| `src/moriyama/__main__.py` | Entry point. `MainWindow` (hello world), `main()` with splash screen wired via `QTimer.singleShot(2000, on_ready)`. |
| `src/moriyama/splash.py` | `SplashScreen(QSplashScreen)` with `_make_placeholder_pixmap()`, `set_status()`, `finish_after()`. Accepts optional `QPixmap` override. |
| `src/moriyama/dropzone.py` | `DropZone(QWidget)` — drag-and-drop + click-to-browse, `files_added = Signal(list)`, `filter=` and `multiple=` kwargs. |
| `src/moriyama/resources_rc.py` | **Generated** by `pyside6-rcc`. Do not edit by hand. Compiled from `resources/resources.qrc`. |
| `resources/resources.qrc` | Qt resource file mapping `:/images/splash.png` → `resources/images/splash.png`. |
| `resources/images/splash.png` | Splash screen image (provided by user). |
| `resources/README.txt` | Instructions for icon files. |
| `scripts/compile_resources.py` | Auto-discovers all `*.qrc` files in `resources/` and compiles them. Cross-platform fallback for systems without `just`. |
| `Justfile` | Task runner recipes: `compile-resources`, `run`, `test`, `lint`, `fmt`, `build`, `package`. |
| `tests/test_main_window.py` | Smoke test for `MainWindow` title. |
| `tests/test_splash.py` | Tests for `SplashScreen`: pixmap size, default/custom pixmap, `set_status`. |
| `tests/test_dropzone.py` | Tests for `DropZone`: rendering, drag accept/reject, hover state, drop emission, dialog confirm/cancel, single-file mode. |
| `NOTES.md` | Session notes, all decisions, Qt resource system howto, `just` task reference. |
| `.gitignore` | Standard Python + Briefcase + macOS ignores. |
| `README.md` | Setup, dev workflow, bundling instructions, project layout. |

## Important line numbers

- `__main__.py:25` — splash pixmap: `SplashScreen(pixmap=QPixmap(":/images/splash.png"))`
- `__main__.py:29` — `on_ready()` closure: builds window, calls `splash.finish(window)`
- `__main__.py:33` — `QTimer.singleShot(2000, on_ready)` — 2 s aesthetic pause
- `__main__.py:34` — `app.exec()` — real event loop starts here
- `splash.py:1-90` — full `SplashScreen` implementation
- `dropzone.py:1-115` — full `DropZone` implementation

## Architecture decisions

**Splash screen**: Correct pattern for macOS — call `app.exec()` immediately and schedule work via `QTimer.singleShot`. Does `raise_()` + `activateWindow()` + `processEvents()` then `QTimer.singleShot(2000, on_ready)` before `app.exec()`.

**Known issue (splash)**: Splash does not appear until after the 2 s pause on macOS. Root cause: macOS compositor does not composite the window until the run loop hands back to the system. Long-term fix: do all heavy work in a `QThread` so `app.exec()` is truly the first thing called with no blocking before it.

**DropZone signal**: Emits `list[Path]` (not `list[str]`) — always resolved `pathlib.Path` objects.

**Qt resources**: `:/images/splash.png` URI works via compiled `resources_rc.py`. Must `import moriyama.resources_rc` before any `QPixmap(":/...")` call. Recompile with `just compile-resources` after changing images.

**Dev dependencies**: Use `[dependency-groups] dev` not `[tool.uv] dev-dependencies` (deprecated).

**src/ layout**: Prevents accidental uninstalled imports during testing.

**Generated files**: `resources_rc.py` produced by `just compile-resources` / `scripts/compile_resources.py` — never edited by hand.

**Future async pattern**: When real loading work replaces the aesthetic splash pause — `QThread` for CPU-bound work, `asyncio` + `qasync` for I/O-bound work, with `on_ready` as the signal completion callback.

## Completed work

- [x] Project scaffolding (pyproject.toml, src layout, Justfile, .gitignore, README)
- [x] Splash screen (`splash.py`, tests)
- [x] Qt resource system (`resources.qrc`, `resources_rc.py`, `scripts/compile_resources.py`)
- [x] DropZone widget (`dropzone.py`, tests)

## Next steps

1. Fix splash screen macOS compositor issue — restructure `main()` so `app.exec()` is called with zero blocking before it; handle 2 s pause entirely inside the event loop via `QTimer`.
2. Wire `DropZone` into `MainWindow` — replace `QLabel("Hello, World!")` with a `DropZone` instance and connect `files_added` to a handler.
3. Run `uv run pytest` to verify all tests pass after integration.
4. Decide on overall application architecture (what Moriyama actually does with the dropped files).
