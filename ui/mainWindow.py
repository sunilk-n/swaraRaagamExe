import os
from typing import List
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QDialog, QPushButton, QLineEdit
from PySide6.QtCore import QThread, Signal, QSize

# from models.songs import SongCollection, Song
from ui.utilities import AppSettings
from ui.customWidgets import messageOverlay, widgetOverlay, errorDialog
from ui.router.localWidget import LocalBrowserWidget
from ui.router.songItem import Item
from ui.router.pathSelector import PathSelector
from ui.videoPlayer import VideoPlayer
from controller.utilities import is_connected


# class SongLoader(QThread):
#     songInfo = Signal(list)
#     error = Signal(str)
#     loaded = Signal()
#
#     def __init__(self):
#         super().__init__()
#
#     def run(self) -> None:
#         if not is_connected():
#             self.error.emit("No internet connection")
#         else:
#             try:
#                 _song = SongCollection()
#                 _song.get_all_songs()
#
#                 self.songInfo.emit(_song.songs)
#                 self.loaded.emit()
#             except Exception as e:
#                 self.error.emit(str(e))


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Swara Raagam")

        self.message_overlay = messageOverlay.MessageOverlay(self)
        self.settings = AppSettings()
        self.resize(QSize(self.settings.window_size[0], self.settings.window_size[1]))

        self.btn = LocalBrowserWidget(self)
        self.setCentralWidget(self.btn)
        self.widget_overlay = PathSelector(self)
        self.widget_overlay.path_selected.connect(self.update_songs)

        if not self.settings.songs_path or not os.path.exists(self.settings.songs_path):
            self.widget_overlay.show_widget("Select Path", self.widget_overlay.get_widget())
        else:
            self.update_songs()

    def update_songs(self):
        print("Updating songs")
        self.settings.load()
        self.btn.set_songs(
            [song for song in os.listdir(self.settings.songs_path) if song.endswith(".mp4")]
        )

    def open_player(self):
        self.player = VideoPlayer()
        self.player.show()
