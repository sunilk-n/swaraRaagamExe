import os

from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QPixmap

from ui.customWidgets.messageOverlay import MessageOverlay


class SongWidget(QWidget):
    def __init__(self, parent: QWidget=None) -> None:
        super().__init__(parent)

        self.loader_window = MessageOverlay(self)

        self.setup_ui()

    def set_song_info(self, song_name: str, movie_name: str, movie_year: int) -> None:
        self._song_name.setText(song_name)
        self._movie_name.setText(f"{movie_name} ({movie_year})")

    def set_icon(self, icon_path: str) -> None:
        self._icon.setPixmap(QPixmap(icon_path))

    def setup_ui(self):
        self._icon = QLabel(self)
        self._icon.setObjectName("icon")

        self._song_name = QLabel(self)
        self._song_name.setObjectName("song_name")

        self._movie_name = QLabel(self)
        self._movie_name.setObjectName("movie_name")

        self._name_layout = QVBoxLayout(self)
        self._name_layout.addWidget(self._song_name)
        self._name_layout.addWidget(self._movie_name)

        self._main_layout = QHBoxLayout(self)
        self._main_layout.addWidget(self._icon)
        self._main_layout.addLayout(self._name_layout)

        self.setLayout(self._main_layout)

        self.setStyleSheet(
            """
            QLabel#icon {
                width: 40px;
                height: 40px;
            }

            QLabel#song_name {
                font-size: 18px;
                font-weight: bold;
            }

            QLabel#movie_name {
                font-size: 12px;
            }
            """
        )
