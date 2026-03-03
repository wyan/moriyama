"""Entry point for the moriyama application."""

from __future__ import annotations

import sys

from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow

import moriyama.resources_rc  # noqa: F401
from moriyama.splash import SplashScreen


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Moriyama")
        self.setCentralWidget(QLabel("Hello, World!"))


def main() -> None:
    app = QApplication(sys.argv)

    splash = SplashScreen(pixmap=QPixmap(":/images/splash.png"))
    splash.show()
    splash.raise_()
    splash.activateWindow()

    app.processEvents()
    splash.set_status("Loading resources…")

    window = MainWindow()

    def on_ready() -> None:
        window.show()
        splash.finish(window)

    # --- heavy initialisation would go here ---
    # do_something_slow()
    QTimer.singleShot(2000, on_ready)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
