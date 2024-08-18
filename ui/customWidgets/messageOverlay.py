from PySide6.QtWidgets import (
    QVBoxLayout, QLabel, QWidget, QFrame, QApplication, QPushButton
)
from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QPainter, QColor


class MessageOverlay(QWidget):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)

        self.setVisible(False)
        self.setup_ui()

    def show_message(self, title: str, message: str, dismiss: bool = False, error: bool = False) -> None:
        self.setVisible(True)
        self._title_lb.setText(title)
        if dismiss:
            self._dismiss_btn.show()
            self.setVisible(True)
        if error:
            self.setStyleSheet(
                """
                QFrame#main_frame {
                    background-color: #686868;
                    border: 2px solid #ff015b;
                    border-radius: 5px;
                    padding: 20px;
                }
                
                QLabel#title_lb {
                    font: bold 18px;
                    color: white;
                }
    
                QLabel#separator_lb {
                    background: #5baac9;
                }
    
                QLabel#message_lb {
                    font: 14px;
                    color: white;
                }
                
                QPushButton#dismiss_btn {
                    min-width: 100px;
                    background-color: #ff015b;
                    color: #FFF;
                }
                QPushButton#dismiss_btn:hover {
                    background-color: #df013b;
                    color: #FFF;
                }
                QPushButton#dismiss_btn:pressed {
                    background-color: #b9011b;
                    color: #FFF;
                }
                """
            )
        self.update_message(message)

    def hide_message(self) -> None:
        self.setVisible(False)

    def update_message(self, message: str) -> None:
        self._message_lb.setText(message)
        self._update_widget()
        QApplication.processEvents()

    def setup_ui(self) -> None:
        self._main_frame = QFrame(self)
        self._main_frame.setObjectName("main_frame")

        vlayout = QVBoxLayout(self._main_frame)

        self._dismiss_btn = QPushButton(self)
        self._dismiss_btn.setText("Close")
        self._dismiss_btn.setObjectName("dismiss_btn")
        self._dismiss_btn.clicked.connect(self.hide_message)
        self._dismiss_btn.setVisible(False)

        self._title_lb = QLabel()
        self._title_lb.setObjectName("title_lb")
        vlayout.addWidget(self._title_lb)

        separator_lb = QLabel()
        separator_lb.setObjectName("separator_lb")
        separator_lb.setMaximumHeight(2)
        vlayout.addWidget(separator_lb)

        self._message_lb = QLabel()
        self._message_lb.setWordWrap(True)
        self._message_lb.setObjectName("message_lb")
        vlayout.addWidget(self._message_lb)

        vlayout.addWidget(self._dismiss_btn)

        self.parent().installEventFilter(self)

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
                color: white;
            }

            QLabel#separator_lb {
                background: #5baac9;
            }

            QLabel#message_lb {
                font: 14px;
                color: white;
            }
            
            QPushButton#dismiss_btn {
                min-width: 100px;
                background-color: #5baac9;
                color: #FFF;
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
