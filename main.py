import os
import sys
from dotenv import load_dotenv

load_dotenv()
if getattr(sys, 'frozen', False):
    APP_PATH = os.path.join(sys._MEIPASS, "swaraRaagam")
else:
    APP_PATH = os.path.dirname(os.path.abspath(__file__))

sys.path.append(APP_PATH)
os.environ['APP_PATH'] = APP_PATH

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from ui.mainWindow import MainWindow
from ui.utilities import AppSettings


if __name__ == '__main__':
    app = QApplication(sys.argv)
    settings = AppSettings()
    settings.app_path = APP_PATH
    app.setWindowIcon(QIcon(os.path.join(APP_PATH, "assets", "images", "logo.png")))

    window = MainWindow()
    window.show()

    app.exec()
