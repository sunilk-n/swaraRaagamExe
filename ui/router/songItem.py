import os

from PySide6.QtWidgets import QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QWidget, QScrollArea, QSizePolicy
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QImage

from ui.utilities import AppSettings


class Item(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(75)

        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QGridLayout()
        self.main_layout.setObjectName("songItemLayout")

        self._icon = QLabel(self)
        self._icon.setObjectName("songCover")
        self._icon.resize(50, 50)
        self._icon.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        # self._icon.setScaledContents(True)

        self._song_name = QLabel(self)
        self._song_name.setObjectName("songName")
        self._song_name.setStyleSheet("font-weight: 600; font-size: 15px;")
        # self._song_name.setWordWrap(True)
        self._song_name.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

        info_layout = QHBoxLayout()

        self._movie_name = QLabel(self)
        self._movie_name.setObjectName("movieName")

        self._play_btn = QPushButton(self)
        self._play_btn.setObjectName("playBtn")
        settings = AppSettings()
        icon = QImage(os.path.join(settings.app_path, "assets", "images", "play.png"))
        self._play_btn.setIcon(QPixmap(icon))
        self._play_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

        self._artists = QLabel(self)
        self._artists.setObjectName("artists")

        self._singers = QLabel(self)
        self._singers.setObjectName("singers")

        info_layout.addWidget(self._movie_name)
        info_layout.addWidget(self._artists)
        info_layout.addWidget(self._singers)

        self.main_layout.addWidget(self._icon, 0, 0, 2, 1, Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self._song_name, 0, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)
        self.main_layout.addWidget(self._play_btn, 0, 2, 2, 1)
        self.main_layout.addLayout(info_layout, 1, 1, 1, 1)

        self.main_layout.setColumnStretch(0, 1)
        self.main_layout.setColumnStretch(1, 10)
        self.main_layout.setColumnStretch(2, 1)

        self.setLayout(self.main_layout)

    def set_cover_image(self, img_path):
        img = QImage(img_path)
        pixmap = QPixmap(img.scaledToWidth(50))

        self._icon.setPixmap(pixmap)

    def set_song_name(self, song_name):
        self._song_name.setText(song_name)

    def set_movie_name(self, movie_name):
        self._movie_name.setText(movie_name)

    def set_singers(self, singers):
        self._singers.setText(singers)

    def set_artists(self, artists):
        self._artists.setText(artists)


class SongListScroller(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.main_layout)

        self.scroller = QScrollArea()
        self.scroller.setWidgetResizable(True)
        self.scroller.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroller.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroller.setWidget(self)

    def add_widget(self, widget:QWidget):
        self.main_layout.addWidget(widget)
