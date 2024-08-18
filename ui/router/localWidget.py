import os

from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton

from ui.router.pagination import PaginationWidget
from ui.router.songItem import SongListScroller, Item
from ui.videoPlayer import VideoPlayer
from ui.utilities import AppSettings


class LocalBrowserWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setup_ui()
        self.player = VideoPlayer()
        self.songs = []

    def setup_ui(self):
        self._song_list = SongListScroller(self)
        self._pagination = PaginationWidget(self)

        self._main_layout = QVBoxLayout()
        self._main_layout.addWidget(self._pagination)
        self._main_layout.addWidget(self._song_list.scroller)

        self.setLayout(self._main_layout)

        # self._pagination.add_page_num(1)
        # self._pagination.add_page_num(2)
        # self._pagination.add_page_num(3)
        # self._pagination.add_page_num(4)
        # self._pagination.add_page_num(5)

        # self.addWidget()

    def set_songs(self, songs: list):
        self.songs = songs
        # TODO: clear self._pagination.page_num_layout to add new set of data
        self._pagination.clear_layout(self._pagination.page_num_layout)
        # TODO: clear self._song_list.main_layout to add new set of data
        self._pagination.clear_layout(self._song_list.main_layout)

        for song in self.songs[0:self._pagination.get_per_page_value()]:
            self.add_widget(song)

    def add_widget(self, song):
        item = Item()
        settings = AppSettings()
        item.set_cover_image(os.path.join(settings.app_path, "assets", "images", "logo.png"))

        item.set_song_name(song)
        item.set_artists("Someone, Other")
        item.set_movie_name("Movie Name")
        item.set_singers("Another, some Other")
        item._play_btn.clicked.connect(lambda: self.play_song(song))
        self._song_list.add_widget(item)

    def play_song(self, song_name):
        settings = AppSettings()
        if not self.player:
            print("Playing with new player")
            self.player = VideoPlayer()
        self.player.set_song(os.path.join(settings.songs_path, song_name))
        if not self.player.isVisible():
            self.player._controls.show()
            self.player.show()


if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication
    app = QApplication([])
    gui = LocalBrowserWidget()
    gui.show()
    app.exec()
