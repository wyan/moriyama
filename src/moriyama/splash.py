"""Splash screen shown while the application is initialising."""

from __future__ import annotations

from typing import Callable

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QFont, QPainter, QPixmap
from PySide6.QtWidgets import QSplashScreen


def _make_placeholder_pixmap(width: int = 600, height: int = 340) -> QPixmap:
    """Return a simple painted pixmap used as the default splash image.

    Replace this function (or pass a pre-loaded QPixmap to SplashScreen) once
    a real asset is available.  The placeholder draws a solid background and
    centred application name so the splash is not invisible during development.
    """
    pixmap = QPixmap(width, height)
    pixmap.fill(QColor("#1e1e2e"))

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    # App name
    font = QFont()
    font.setPointSize(36)
    font.setBold(True)
    painter.setFont(font)
    painter.setPen(QColor("#cdd6f4"))
    painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "Moriyama")

    # Subtitle / version — easy to swap for real text later
    font.setPointSize(13)
    font.setBold(False)
    painter.setFont(font)
    painter.setPen(QColor("#6c7086"))
    subtitle_rect = pixmap.rect().adjusted(0, height // 2 + 20, 0, 0)
    painter.drawText(subtitle_rect, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop, "Loading…")

    painter.end()
    return pixmap


class SplashScreen(QSplashScreen):
    """Transient splash screen displayed during application startup.

    Usage (aesthetic / no real work)::

        splash = SplashScreen()
        splash.show()
        # ... build MainWindow ...
        splash.finish(main_window)

    Usage (with real async/heavy work)::

        splash = SplashScreen()
        splash.show()
        splash.set_status("Connecting to database…")
        do_heavy_work()
        splash.set_status("Ready.")
        splash.finish(main_window)

    Pass a pre-loaded ``QPixmap`` to override the built-in placeholder::

        splash = SplashScreen(pixmap=QPixmap(":/images/splash.png"))
    """

    def __init__(self, pixmap: QPixmap | None = None) -> None:
        resolved = pixmap if pixmap is not None else _make_placeholder_pixmap()
        super().__init__(resolved, Qt.WindowType.WindowStaysOnTopHint)
        self.setEnabled(False)  # clicks pass through

    def set_status(self, message: str) -> None:
        """Update the status message painted at the bottom of the splash."""
        self.showMessage(
            message,
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom,
            QColor("#cdd6f4"),
        )

    # ------------------------------------------------------------------
    # Convenience: schedule finish after a fixed delay (aesthetic mode)
    # ------------------------------------------------------------------

    def finish_after(self, window: object, delay_ms: int = 1500) -> None:
        """Close the splash and reveal *window* after *delay_ms* milliseconds.

        Useful when there is no real work to wait for.  Once actual loading
        work exists, call ``finish(window)`` directly instead.
        """
        QTimer.singleShot(delay_ms, lambda: self.finish(window))  # type: ignore[arg-type]
