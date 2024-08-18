from PySide6.QtWidgets import QDialog, QPushButton
from PySide6.QtMultimedia import QMediaPlayer


class PlayerControls(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Player Controls")
        self.resize(600, 200)

        self.setup_ui()

    def set_media_player(self, media_player: QMediaPlayer):
        self.media_player = media_player

    def setup_ui(self):
        self.play_btn = QPushButton(self)
        self.play_btn.setText("Play")
        self.play_btn.clicked.connect(self.play_media)

    def play_media(self):
        if self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()
