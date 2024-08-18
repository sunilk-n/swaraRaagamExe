from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy, QComboBox


class PaginationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setup_ui()
        self.total_files = 0

    def setup_ui(self):
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.setLayout(self.main_layout)

        pages_layout = QHBoxLayout()

        self._prev_btn = QPushButton(self)
        self._prev_btn.setObjectName("previousBtn")
        self._prev_btn.setMaximumSize(25, 25)
        self._prev_btn.setText("<")

        self.page_num_layout = QHBoxLayout()

        self._next_btn = QPushButton(self)
        self._next_btn.setObjectName("nextBtn")
        self._next_btn.setMaximumSize(25, 25)
        self._next_btn.setText(">")

        pages_layout.addWidget(self._prev_btn)
        pages_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        pages_layout.addLayout(self.page_num_layout)
        pages_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        pages_layout.addWidget(self._next_btn)

        per_page_layout = QHBoxLayout()

        self._per_page_lb = QLabel(self)
        self._per_page_lb.setObjectName("perPageLabel")
        self._per_page_lb.setText("Per Page: ")

        self._per_page_combo = QComboBox(self)
        self._per_page_combo.setObjectName("perPageCombo")
        self._per_page_combo.addItem("10")
        self._per_page_combo.addItem("25")
        self._per_page_combo.addItem("50")
        self._per_page_combo.addItem("100")
        self._per_page_combo.setCurrentIndex(3)

        per_page_layout.addWidget(self._per_page_lb)
        per_page_layout.addWidget(self._per_page_combo)

        self.main_layout.addLayout(pages_layout)
        pages_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.main_layout.addLayout(per_page_layout)

    def add_page_num(self, page: int):
        page_num = QPushButton(self)
        page_num.setObjectName(f"page{page}Btn")
        page_num.setText(str(page))
        page_num.setMaximumSize(25, 25)
        self.page_num_layout.addWidget(page_num)

    def get_per_page_value(self):
        return int(self._per_page_combo.currentText())

    def generate_pages(self, total, max_pages=5):
        total_pages = 0

        self.clear_layout(self.page_num_layout)

    def clear_layout(self, layout):
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            if item.widget():
                widget = item.widget()
                widget.setParent(None)
                widget.deleteLater()
            elif item.layout():
                inner_layout = item.layout()
                self.clear_layout(inner_layout)


if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication
    app = QApplication([])
    gui = PaginationWidget()
    gui.show()
    app.exec()
