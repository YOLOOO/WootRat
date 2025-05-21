from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class SupportTab(QWidget):
    def __init__(self, get_resource_path):
        super().__init__()
        layout = QVBoxLayout()
        image_path = get_resource_path("resources/rat.png")
        support_pixmap = QPixmap(image_path)
        image_label = QLabel()
        image_label.setPixmap(support_pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_label)
        support_text = QLabel("Need help?\nContact me at:\nviktortornborg@hotmail.com")
        support_text.setAlignment(Qt.AlignCenter)
        support_text.setStyleSheet("color: #cccccc; font-size: 16px;")
        layout.addWidget(support_text)
        self.setLayout(layout)