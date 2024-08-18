from PySide6.QtWidgets import QWidget, QGridLayout
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QPropertyAnimation

from ui.customWidgets import playerControls, messageOverlay


class VideoPlayer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Swara Raagam Player")
        self.resize(800, 600)

        self.pending_song_path = None

        self.setup_ui()

    def setup_ui(self):

        self.loader_window = messageOverlay.MessageOverlay(self)
        self.loader_window.show_message("Song Name", "Song details \n will be displayed here")

        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        self.media_player.mediaStatusChanged.connect(self.change_source)
        # self.media_player.playbackStateChanged.connect(self.change_playing)
        self.video_widget = QVideoWidget()

        self._layout = QGridLayout()
        self._layout.addWidget(self.video_widget, 0, 0, 2, 2)
        self.setLayout(self._layout)

        self.media_player.setVideoOutput(self.video_widget)

        self._controls = playerControls.PlayerControls(self)
        self._controls.set_media_player(self.media_player)

        self.fade_animation = QPropertyAnimation(self.video_widget, b"opacity")
        self.fade_animation.setDuration(500)
        # self.fade_animation.finished.connect(self.handle_fade_out_finished)
        # self._controls.show()

    def change_source(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia and hasattr(self, "pending_song_path"):
            print(self.pending_song_path)
            self.media_player.setSource(self.pending_song_path)
            del self.pending_song_path
            self.media_player.play()

    def change_playing(self, status):
        print(self.pending_song_path)

    def set_song(self, song_path):
        if self.media_player.playbackState() in [QMediaPlayer.PlaybackState.PlayingState, QMediaPlayer.PlaybackState.PausedState]:
            self.pending_song_path = song_path.replace("\\", "/")
            self.media_player.setPosition(self.media_player.duration())
            # self.media_player.stop()
        else:
            self.media_player.setSource(song_path.replace("\\", "/"))
            self.media_player.play()

    def fade_out(self):
        if self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.fade_animation.setStartValue(1.0)
            self.fade_animation.setEndValue(0.0)
            self.fade_animation.start()
        else:
            self.video_widget.setWindowOpacity(0.0)
            self.handle_fade_out_finished()

    def fade_in(self):
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.start()

    def handle_fade_out_finished(self):
        if self.fade_animation.direction() == QPropertyAnimation.Direction.Forward:
            self.media_player.play()
            self.fade_in()
