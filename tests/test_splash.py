"""Tests for the splash screen."""

from __future__ import annotations

import pytest

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from moriyama.splash import SplashScreen, _make_placeholder_pixmap


def test_placeholder_pixmap_size() -> None:
    pixmap = _make_placeholder_pixmap(600, 340)
    assert pixmap.width() == 600
    assert pixmap.height() == 340


def test_splash_created_with_default_pixmap(qapp) -> None:
    splash = SplashScreen()
    assert not splash.pixmap().isNull()
    splash.close()


def test_splash_created_with_custom_pixmap(qapp) -> None:
    custom = QPixmap(200, 100)
    custom.fill(Qt.GlobalColor.red)
    splash = SplashScreen(pixmap=custom)
    assert splash.pixmap().width() == 200
    splash.close()


def test_set_status_does_not_raise(qapp) -> None:
    splash = SplashScreen()
    splash.set_status("Initialising…")
    splash.close()
