from __future__ import annotations

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QMessageBox

from moriyama.imglist import ImageList


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Moriyama")
        self._image_list = ImageList()
        self.setCentralWidget(self._image_list)

        # Create the Menu Bar
        #         self.menuBar().setNativeMenuBar(False)
        self.about_action = QAction("About Moriyama", self)
        self.about_action.setMenuRole(QAction.MenuRole.AboutRole)  # Explicitly move to App Menu
        self.about_action.triggered.connect(self.about)

        self.exit_action = QAction("Quit Moriyama", self)
        self.exit_action.setMenuRole(QAction.MenuRole.QuitRole)  # Explicitly move to App Menu
        self.exit_action.triggered.connect(self.close)

        self.file_menu = self.menuBar().addMenu("&File")
        self.help_menu = self.menuBar().addMenu("&Help")

        # Add an Exit action
        patata_action = QAction("Patata", self)
        patata_action.triggered.connect(self.patata)
        self.file_menu.addAction(patata_action)

        # Add a Help action
        about_action = QAction("About PySide6", self)
        about_action.triggered.connect(self.about)
        self.help_menu.addAction(about_action)

    def about(self) -> None:
        QMessageBox.about(
            self,
            "About Moriyama",
            "Moriyama v1.0\n\nBuilt with PySide6 and Python 3.x. "
            "A simple Qt-based interface example.",
        )

    def patata(self) -> None:
        QMessageBox.about(self, "Patata", "🥔")
