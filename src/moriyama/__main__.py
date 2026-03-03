"""Entry point for the moriyama application."""

from __future__ import annotations

import sys
import time

from PySide6.QtWidgets import QApplication, QLabel, QMainWindow

from moriyama.splash import SplashScreen


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Moriyama")
        self.setCentralWidget(QLabel("Hello, World!"))


def main() -> None:
    app = QApplication(sys.argv)

    splash = SplashScreen()
    splash.show()
    app.processEvents()  # ensure the splash is painted before heavy work starts

    # --- heavy initialisation would go here ---
    splash.set_status("Loading resources…")
    time.sleep(2)
    # do_something_slow()

    window = MainWindow()
    window.show()

    splash.finish(window)  # hides splash, reveals main window
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
