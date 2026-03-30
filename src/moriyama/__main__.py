"""Entry point for the moriyama application."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from moriyama.mainwindow import MainWindow


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("Moriyama")
    app.setApplicationDisplayName("Moriyama")
    app.setOrganizationName("finitudlabs")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
