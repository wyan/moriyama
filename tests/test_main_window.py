"""Smoke test — verifies the application window can be constructed."""

from __future__ import annotations

import pytest

from moriyama.__main__ import MainWindow


@pytest.fixture()
def main_window(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    return window


def test_window_title(main_window: MainWindow) -> None:
    assert main_window.windowTitle() == "Moriyama"
