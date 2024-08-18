from PySide6.QtWidgets import QWidget, QFormLayout, QLineEdit, QPushButton, QFileDialog
from PySide6.QtCore import Signal

from ui.customWidgets.widgetOverlay import WidgetOverlay
from ui.utilities import AppSettings


class PathSelector(WidgetOverlay):
    path_selected = Signal()
    def __init__(self, parent=None):
        super().__init__(parent)

    def get_widget(self) -> QWidget:
        widget = QWidget(self)

        layout = QFormLayout()
        widget.setLayout(layout)

        self._path_input = QLineEdit(self)
        self._path_input.setProperty("class", "inputField")
        self._path_input.setPlaceholderText("Select the path for the local directory")

        self._path_button = QPushButton(self)
        self._path_button.setText("Set Path")
        self._path_button.setObjectName("submit_btn")
        self._path_button.clicked.connect(self.open_path_dialog)

        layout.addRow(self._path_input)
        layout.addRow(self._path_button)

        return widget

    def open_path_dialog(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Song Directory")
        if directory:
            settings = AppSettings()
            settings.last_used_folder = directory
            settings.songs_path = directory
            self.hide()
            self.path_selected.emit()
