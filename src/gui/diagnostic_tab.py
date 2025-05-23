from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from utils.settings import CURVE_LABELS, VALUE_LABELS

class DiagnosticsTab(QWidget):
    def __init__(self, settings):
        super().__init__()
        layout = QVBoxLayout()

        curve_type_label = QLabel(VALUE_LABELS[6])
        self.curve_type_dropdown = QComboBox()
        self.curve_type_dropdown.addItems([CURVE_LABELS[0], CURVE_LABELS[1], CURVE_LABELS[2], CURVE_LABELS[3]])
        self.curve_type_dropdown.setCurrentText(settings.get(VALUE_LABELS[6], CURVE_LABELS[0]))
        layout.addWidget(curve_type_label)
        layout.addWidget(self.curve_type_dropdown)

        curve_label = QLabel("Curve Visualization")
        layout.addWidget(curve_label)

        curve_explanation = QLabel(
            "Note: Raw input 0.0–1.0 corresponds to 0.0–4.0 mm of analog travel\n"
            "on most Wooting Lekker switches. 0.0 = not pressed, 1.0 = fully pressed (4.0 mm)."
        )
        curve_explanation.setStyleSheet("color: #bbbbbb; font-size: 12px;")
        curve_explanation.setWordWrap(True)
        layout.addWidget(curve_explanation)

        self.curve_canvas = FigureCanvas(plt.Figure(figsize=(4, 2)))
        layout.addWidget(self.curve_canvas)
        self.curve_ax = self.curve_canvas.figure.subplots()

        self.setLayout(layout)