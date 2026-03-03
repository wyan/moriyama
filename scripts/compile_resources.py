"""Compile Qt resource files (.qrc) into Python modules.

Run with:
    uv run python scripts/compile_resources.py

This is the cross-platform fallback for systems without `just`.
The Justfile `compile-resources` recipe calls this script directly.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
RESOURCES_DIR = ROOT / "resources"
OUT_DIR = ROOT / "src" / "moriyama"


def compile_qrc(qrc: Path) -> None:
    out = OUT_DIR / (qrc.stem + "_rc.py")
    print(f"  {qrc.relative_to(ROOT)}  →  {out.relative_to(ROOT)}")
    subprocess.run(
        ["pyside6-rcc", str(qrc), "-o", str(out)],
        check=True,
    )


def main() -> None:
    qrc_files = sorted(RESOURCES_DIR.glob("*.qrc"))
    if not qrc_files:
        print("No .qrc files found in resources/ — nothing to do.")
        return
    print(f"Compiling {len(qrc_files)} .qrc file(s)…")
    for qrc in qrc_files:
        compile_qrc(qrc)
    print("Done.")


if __name__ == "__main__":
    main()
