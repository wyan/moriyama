from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QPixmap
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


class ImageList(QWidget):
    THUMBNAIL_SIZE = 80

    files_added = Signal(list)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._files: list[Path] = []

        self.setAcceptDrops(True)

        self._layout = QVBoxLayout(self)
        self._layout.setSpacing(4)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._scroll_area = QScrollArea()
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self._scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._scroll_area.setFixedHeight(self.THUMBNAIL_SIZE + 10)

        self._thumbnails_widget = QWidget()
        self._thumbnails_layout = QHBoxLayout(self._thumbnails_widget)
        self._thumbnails_layout.setSpacing(4)
        self._thumbnails_layout.setContentsMargins(0, 0, 0, 0)

        self._add_button = QPushButton("+")
        self._add_button.setFixedSize(self.THUMBNAIL_SIZE, self.THUMBNAIL_SIZE)
        self._add_button.clicked.connect(self._open_file_picker)
        self._thumbnails_layout.addWidget(self._add_button)

        self._thumbnails_layout.addStretch()

        self._scroll_area.setWidget(self._thumbnails_widget)
        self._layout.addWidget(self._scroll_area)

        self._file_label = QLabel("No files added")
        self._file_label.setStyleSheet("color: gray;")
        self._layout.addWidget(self._file_label)

    def files(self) -> list[Path]:
        return list(self._files)

    def _open_file_picker(self) -> None:
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilters(["Images (*.png *.jpg *.jpeg *.bmp *.gif)"])
        if dialog.exec() == QFileDialog.DialogCode.Accepted:
            self.add_files(dialog.selectedFiles())

    def add_files(self, file_paths: list[str]) -> None:
        new_files = [Path(p) for p in file_paths if Path(p).exists()]
        self._files.extend(new_files)
        self._update_label()
        for f in new_files:
            self._add_thumbnail(f)
        if new_files:
            self.files_added.emit(new_files)

    def _add_thumbnail(self, file_path: Path) -> None:
        thumbnail = QLabel()
        pixmap = QPixmap(str(file_path))
        scaled = pixmap.scaled(
            self.THUMBNAIL_SIZE,
            self.THUMBNAIL_SIZE,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )
        thumbnail.setPixmap(scaled)
        thumbnail.setToolTip(file_path.name)
        self._thumbnails_layout.insertWidget(self._thumbnails_layout.count() - 1, thumbnail)

    def _update_label(self) -> None:
        count = len(self._files)
        if count == 0:
            self._file_label.setText("No files added")
            self._file_label.setStyleSheet("color: gray;")
        else:
            self._file_label.setText(f"{count} file(s)")
            self._file_label.setStyleSheet("")

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent) -> None:
        paths = [url.toLocalFile() for url in event.mimeData().urls()]
        self.add_files(paths)
