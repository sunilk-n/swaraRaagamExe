from PySide6.QtWidgets import QMessageBox, QWidget, QLabel, QVBoxLayout


class ErrorDialog(QMessageBox):
    def __init__(self, parent: QWidget = None, *args, **kwargs) -> None:
        super().__init__(parent=parent, *args, **kwargs)

        self.setIcon(QMessageBox.Icon.Critical)

    def set_message(self, title: str, message: str):
        self.setWindowTitle(title)
        self.setText(message)
