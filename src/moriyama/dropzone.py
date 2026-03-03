"""Drop zone widget — accepts files via drag-and-drop or click-to-browse."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QMimeData, Qt, Signal
from PySide6.QtGui import QColor, QDragEnterEvent, QDragLeaveEvent, QDropEvent, QPainter, QPaintEvent, QMouseEvent
from PySide6.QtWidgets import QFileDialog, QSizePolicy, QWidget


class DropZone(QWidget):
    """A widget that accepts files by drag-and-drop or by clicking to open a file dialog.

    Signals
    -------
    files_added(list[Path])
        Emitted whenever the user adds files, either by dropping or by selecting
        via the file dialog.  Only paths that pass the current filter are reported.

    Usage::

        zone = DropZone(filter="Images (*.png *.jpg *.tiff)")
        zone.files_added.connect(on_files)

        def on_files(paths: list[Path]) -> None:
            for p in paths:
                print(p)
    """

    files_added = Signal(list)

    # ------------------------------------------------------------------ style
    _COLOR_IDLE = QColor("#2a2a3d")
    _COLOR_IDLE_BORDER = QColor("#555577")
    _COLOR_HOVER = QColor("#32324a")
    _COLOR_HOVER_BORDER = QColor("#8888cc")
    _BORDER_RADIUS = 12
    _BORDER_WIDTH = 2

    def __init__(
        self,
        parent: QWidget | None = None,
        *,
        filter: str = "All files (*)",
        multiple: bool = True,
    ) -> None:
        """
        Parameters
        ----------
        filter:
            File dialog filter string, e.g. ``"Images (*.png *.jpg)"``.
        multiple:
            Whether the user may select more than one file at a time.
        """
        super().__init__(parent)
        self._filter = filter
        self._multiple = multiple
        self._hovering = False

        self.setAcceptDrops(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumSize(300, 160)

    # ----------------------------------------------------------------- paint

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        bg = self._COLOR_HOVER if self._hovering else self._COLOR_IDLE
        border = self._COLOR_HOVER_BORDER if self._hovering else self._COLOR_IDLE_BORDER

        pen = painter.pen()
        pen.setColor(border)
        pen.setWidth(self._BORDER_WIDTH)
        pen.setStyle(Qt.PenStyle.DashLine)
        painter.setPen(pen)
        painter.setBrush(bg)
        painter.drawRoundedRect(
            self.rect().adjusted(
                self._BORDER_WIDTH, self._BORDER_WIDTH,
                -self._BORDER_WIDTH, -self._BORDER_WIDTH,
            ),
            self._BORDER_RADIUS,
            self._BORDER_RADIUS,
        )

        painter.setPen(QColor("#ccccdd") if self._hovering else QColor("#888899"))
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "Drop files here\nor click to browse")

    # -------------------------------------------------------------- drag/drop

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self._set_hovering(True)
        else:
            event.ignore()

    def dragLeaveEvent(self, event: QDragLeaveEvent) -> None:
        self._set_hovering(False)

    def dropEvent(self, event: QDropEvent) -> None:
        self._set_hovering(False)
        paths = self._urls_to_paths(event.mimeData())
        if paths:
            self.files_added.emit(paths)
        event.acceptProposedAction()

    # ------------------------------------------------------------------ click

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self._open_dialog()

    # ---------------------------------------------------------------- private

    def _set_hovering(self, state: bool) -> None:
        if self._hovering != state:
            self._hovering = state
            self.update()

    def _open_dialog(self) -> None:
        if self._multiple:
            paths, _ = QFileDialog.getOpenFileNames(self, "Select files", "", self._filter)
        else:
            path, _ = QFileDialog.getOpenFileName(self, "Select file", "", self._filter)
            paths = [path] if path else []

        resolved = [Path(p) for p in paths if p]
        if resolved:
            self.files_added.emit(resolved)

    @staticmethod
    def _urls_to_paths(mime: QMimeData) -> list[Path]:
        return [Path(url.toLocalFile()) for url in mime.urls() if url.isLocalFile()]
