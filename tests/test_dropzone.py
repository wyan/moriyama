"""Tests for the DropZone widget."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest
from PySide6.QtCore import QMimeData, QUrl, Qt
from PySide6.QtGui import QDropEvent, QDragEnterEvent
from PySide6.QtWidgets import QWidget

from moriyama.dropzone import DropZone


@pytest.fixture()
def zone(qtbot):
    widget = DropZone()
    qtbot.addWidget(widget)
    return widget


def _make_mime_urls(paths: list[Path]) -> QMimeData:
    mime = QMimeData()
    mime.setUrls([QUrl.fromLocalFile(str(p)) for p in paths])
    return mime


# ------------------------------------------------------------------ rendering

def test_widget_renders(zone: DropZone) -> None:
    zone.show()
    assert zone.isVisible()


def test_minimum_size(zone: DropZone) -> None:
    assert zone.minimumWidth() >= 300
    assert zone.minimumHeight() >= 160


# ----------------------------------------------------------------- drag/drop

def test_drag_enter_accepts_file_urls(zone: DropZone, qtbot, tmp_path) -> None:
    f = tmp_path / "test.txt"
    f.write_text("hi")
    mime = _make_mime_urls([f])

    received: list[list[Path]] = []
    zone.files_added.connect(received.append)

    # simulate drop
    zone.show()
    qtbot.mouseMove(zone)

    # manually call dropEvent with valid mime data
    pos = zone.rect().center()
    drop = QDropEvent(
        zone.mapToGlobal(pos).toPointF(),
        Qt.DropAction.CopyAction,
        mime,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )
    zone.dropEvent(drop)

    assert len(received) == 1
    assert received[0] == [f]


def test_drag_enter_ignores_non_files(zone: DropZone) -> None:
    mime = QMimeData()
    mime.setText("just text")

    enter = QDragEnterEvent(
        zone.rect().center().toPointF(),
        Qt.DropAction.CopyAction,
        mime,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )
    zone.dragEnterEvent(enter)
    assert not enter.isAccepted()


def test_drag_hovering_state(zone: DropZone, tmp_path) -> None:
    f = tmp_path / "a.txt"
    f.write_text("x")
    mime = _make_mime_urls([f])

    enter = QDragEnterEvent(
        zone.rect().center().toPointF(),
        Qt.DropAction.CopyAction,
        mime,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )
    zone.dragEnterEvent(enter)
    assert zone._hovering is True

    zone.dragLeaveEvent(None)  # type: ignore[arg-type]
    assert zone._hovering is False


# ---------------------------------------------------------------- file dialog

def test_click_emits_files(zone: DropZone, qtbot, tmp_path) -> None:
    f = tmp_path / "pick.png"
    f.write_text("")

    received: list[list[Path]] = []
    zone.files_added.connect(received.append)

    with patch("moriyama.dropzone.QFileDialog.getOpenFileNames", return_value=([str(f)], "")):
        zone._open_dialog()

    assert received == [[f]]


def test_dialog_cancel_emits_nothing(zone: DropZone) -> None:
    received: list = []
    zone.files_added.connect(received.append)

    with patch("moriyama.dropzone.QFileDialog.getOpenFileNames", return_value=([], "")):
        zone._open_dialog()

    assert received == []


def test_single_mode(qtbot, tmp_path) -> None:
    zone = DropZone(multiple=False)
    qtbot.addWidget(zone)

    f = tmp_path / "one.txt"
    f.write_text("")

    received: list[list[Path]] = []
    zone.files_added.connect(received.append)

    with patch("moriyama.dropzone.QFileDialog.getOpenFileName", return_value=(str(f), "")):
        zone._open_dialog()

    assert received == [[f]]
