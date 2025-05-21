from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt5.QtCore import Qt

class InfoTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        info_text = (
            "<h2>WootRat - Analog Keyboard Mouse Control</h2>"
            "<p><b>WootRat</b> lets you use your Wooting analog keyboard to control your mouse and scrolling with analog precision. "
            "You can fine-tune how your key presses translate to mouse movement using activation points, maximum actuation, and response curves.</p>"
            "<h3>Usage</h3>"
            "<ul>"
            "<li>Assign keys for mouse movement and scrolling in the <b>Key Mapping</b> tab.</li>"
            "<li>Adjust sensitivity, activation point, and maximum actuation in the <b>General</b> tab.</li>"
            "<li>Adjust <b>Y Axis Sensitivity</b> to make vertical movement faster or slower compared to horizontal movement. "
            "A value above 1.0 increases vertical speed, below 1.0 decreases it. Useful for games or workflows where you want different X/Y response.</li>"
            "<li>Choose a curve type and factor to control how input ramps up as you press a key.</li>"
            "<li>Use the <b>Diagnostics</b> tab to visualize your curve and see how your settings affect input.</li>"
            "</ul>"
            "<h3>Activation Point & Maximum Actuation</h3>"
            "<p><b>Activation Point</b> sets how far you must press a key before it starts registering as mouse movement. "
            "A higher value means you need to press further before anything happens.</p>"
            "<p><b>Maximum Actuation</b> sets the point where the key is considered fully pressed. "
            "Any travel beyond this is ignored. This lets you avoid accidental max input if you bottom out the key hard.</p>"
            "<h3>Curve Types</h3>"
            "<ul>"
            "<li><b>Power:</b> Slower at first, faster as you press further. Good for fine control at low travel.</li>"
            "<li><b>Log:</b> Fast response at the start, then flattens out. Good for quick taps.</li>"
            "<li><b>S-Curve:</b> Gentle at the start and end, steep in the middle. Good for smooth transitions.</li>"
            "<li><b>Linear:</b> Direct 1:1 mapping. No curve applied.</li>"
            "</ul>"
            "<h3>Tips</h3>"
            "<ul>"
            "<li>Experiment with different curves and factors to find what feels best for you.</li>"
            "<li>The Diagnostics tab shows a live preview of your curve and settings.</li>"
            "<li>Raw input 0.0–1.0 corresponds to 0.0–4.0 mm of analog travel on most Wooting switches.</li>"
            "</ul>"
        )

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        info_widget = QWidget()
        info_layout = QVBoxLayout()
        info_label = QLabel(info_text)
        info_label.setWordWrap(True)
        info_label.setTextFormat(Qt.RichText)
        info_layout.addWidget(info_label)
        info_widget.setLayout(info_layout)
        scroll_area.setWidget(info_widget)

        layout.addWidget(scroll_area)
        self.setLayout(layout)

        self.setObjectName("InfoTab")
        scroll_area.setObjectName("InfoScrollArea")
        info_widget.setObjectName("InfoTabWidget")
        info_label.setObjectName("InfoLabel")