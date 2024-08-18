from PySide6.QtWidgets import (
    QVBoxLayout, QLabel, QWidget, QFrame, QApplication
)
from PySide6.QtCore import QEvent, Signal
from PySide6.QtGui import QPainter, QColor


class WidgetOverlay(QWidget):
    finished = Signal()
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)

        self._title_lb = None
        self._widget_layout = None
        self.setVisible(False)
        self.setup_ui()

    def show_widget(self, title: str, widget: QWidget) -> None:
        self.setVisible(True)
        self._title_lb.setText(title)
        self.update_widget(widget)
        self.raise_()

    def update_widget(self, widget: QWidget) -> None:
        self._widget_layout.addWidget(widget)
        self._update_widget()
        QApplication.processEvents()

    def setup_ui(self) -> None:
        self._main_frame = QFrame(self)
        self._main_frame.setObjectName("main_frame")

        vlayout = QVBoxLayout(self._main_frame)

        self._title_lb = QLabel()
        self._title_lb.setObjectName("title_lb")
        vlayout.addWidget(self._title_lb)

        separator_lb = QLabel()
        separator_lb.setObjectName("separator_lb")
        separator_lb.setMaximumHeight(2)
        vlayout.addWidget(separator_lb)

        self._widget_layout = QVBoxLayout()
        vlayout.addLayout(self._widget_layout)

        self.parent().installEventFilter(self)

        # TODO: Change colours according to Hogarth colour branding.
        self.setStyleSheet(
            """
            QFrame#main_frame {
                background-color: #686868;
                border: 2px solid #5baac9;
                border-radius: 5px;
                padding: 20px;
            }

            QLabel#title_lb {
                font: bold 18px;
                color: #FFF;
            }

            QLabel#separator_lb {
                background-color: #5baac9;
            }
            
            .inputField {
                border: 2px solid #5baac9;
                border-radius: 5px;
                padding: 10px;
            }
            
            QPushButton#submit_btn {
                background-color: #5baac9;
                color: #FFF;
                font-weight: bold;
                border: 2px solid #5baac9;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton#submit_btn:hover {
                background-color: #3d8cab;
                border: 2px solid #3d8cab;
            }
            QPushButton#submit_btn:pressed {
                background-color: #0d5c7b;
                border: 2px solid #0d5c7b;
            }
            """
        )

    def eventFilter(  # pylint: disable=invalid-name
            self,
            widget_object: QWidget,  # pylint: disable=unused-argument
            event: QEvent,
    ) -> bool:
        """Catches Resize events from parent widget to rezise accordingly.

        Args:
            widget_object (QWidget): Parent UI object.
            event (QEvent): Contains event parameters.

        Return:
            bool: Indicates whether or not the event has been dealt with.
        """
        if event.type() == QEvent.Resize and self.isVisible() is True:
            self._update_widget()
            return True
        return False

    def _update_widget(self) -> None:
        """Rezies the widget and repositions it in the centrer of its parent."""
        parent_size = self.parent().size()
        self.resize(parent_size)
        self._main_frame.adjustSize()

        self._main_frame.setMinimumWidth(int(parent_size.width() / 2))

        widget_size = self._main_frame.size()

        self._main_frame.move(
            (parent_size.width() - widget_size.width()) / 2,
            (parent_size.height() - widget_size.height()) / 2,
        )

    def paintEvent(  # pylint: disable=invalid-name
            self, event: QEvent  # pylint: disable=unused-argument
    ) -> None:
        """Repaints the widget.

        Args:
            event (QPaintEvent): Contains event parameters for paint events.
        """
        parent_size = self.parent().size()
        overlay = QPainter(self)
        overlay.fillRect(
            0, 0, parent_size.width(), parent_size.height(), QColor(0, 0, 0, 100)
        )
