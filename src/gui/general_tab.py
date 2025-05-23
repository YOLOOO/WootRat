from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QCheckBox
from PyQt5.QtCore import Qt

#TODO: Fix names for deadzone to the updated ones.

class GeneralTab(QWidget):
    def __init__(self, settings, value_labels):
        super().__init__()
        layout = QVBoxLayout()

        # Mouse Sensitivity
        mouse_sensitivity_label = QLabel(value_labels[0])
        self.mouse_sensitivity_slider = QSlider(Qt.Horizontal)
        self.mouse_sensitivity_slider.setRange(1, 80)
        self.mouse_sensitivity_slider.setValue(int(settings[value_labels[0]]))
        self.mouse_sensitivity_value_label = QLabel(str(self.mouse_sensitivity_slider.value()))
        self.mouse_sensitivity_slider.valueChanged.connect(
            lambda v: self.mouse_sensitivity_value_label.setText(str(v))
        )
        mouse_sensitivity_layout = QHBoxLayout()
        mouse_sensitivity_layout.addWidget(self.mouse_sensitivity_slider)
        mouse_sensitivity_layout.addWidget(self.mouse_sensitivity_value_label)
        layout.addWidget(mouse_sensitivity_label)
        layout.addLayout(mouse_sensitivity_layout)

        # Y Sensitivity
        y_sensitivity_label = QLabel(value_labels[2])
        self.y_sensitivity_slider = QSlider(Qt.Horizontal)
        self.y_sensitivity_slider.setRange(0, 80)
        self.y_sensitivity_slider.setValue(int(settings[value_labels[2]] *  80))
        self.y_sensitivity_value_label = QLabel(f"{self.y_sensitivity_slider.value() / 80:.2f}")
        self.y_sensitivity_slider.valueChanged.connect(
            lambda v: self.y_sensitivity_value_label.setText(f"{v/80:.2f}")
        )
        y_sensitivity_layout = QHBoxLayout()
        y_sensitivity_layout.addWidget(self.y_sensitivity_slider)
        y_sensitivity_layout.addWidget(self.y_sensitivity_value_label)
        layout.addWidget(y_sensitivity_label)
        layout.addLayout(y_sensitivity_layout)

        # Scroll Sensitivity
        scroll_sensitivity_label = QLabel(value_labels[1])
        self.scroll_sensitivity_slider = QSlider(Qt.Horizontal)
        self.scroll_sensitivity_slider.setRange(1, 20)
        self.scroll_sensitivity_slider.setValue(int(settings[value_labels[1]] * 10))
        self.scroll_sensitivity_value_label = QLabel(f"{self.scroll_sensitivity_slider.value() / 10:.1f}")
        self.scroll_sensitivity_slider.valueChanged.connect(
            lambda v: self.scroll_sensitivity_value_label.setText(f"{v/10:.1f}")
        )
        scroll_sensitivity_layout = QHBoxLayout()
        scroll_sensitivity_layout.addWidget(self.scroll_sensitivity_slider)
        scroll_sensitivity_layout.addWidget(self.scroll_sensitivity_value_label)
        layout.addWidget(scroll_sensitivity_label)
        layout.addLayout(scroll_sensitivity_layout)

        # Curve Factor as Slider
        curve_factor_label = QLabel(value_labels[3])
        self.curve_factor_slider = QSlider(Qt.Horizontal)
        self.curve_factor_slider.setRange(10, 100)
        curve_factor_value = int(float(settings[value_labels[3]]) * 10)
        self.curve_factor_slider.setValue(curve_factor_value)
        self.curve_factor_value_label = QLabel(f"{curve_factor_value / 10:.1f}")
        self.curve_factor_slider.valueChanged.connect(
            lambda v: self.curve_factor_value_label.setText(f"{v/10:.1f}")
        )
        curve_factor_layout = QHBoxLayout()
        curve_factor_layout.addWidget(self.curve_factor_slider)
        curve_factor_layout.addWidget(self.curve_factor_value_label)
        layout.addWidget(curve_factor_label)
        layout.addLayout(curve_factor_layout)

        # Deadzone
        deadzone_label = QLabel(value_labels[4])
        self.deadzone_slider = QSlider(Qt.Horizontal)
        self.deadzone_slider.setRange(0, 50)
        deadzone_value = settings.get(value_labels[4], 0.08)
        self.deadzone_slider.setValue(int(deadzone_value * 100))
        self.deadzone_value_label = QLabel(f"{deadzone_value:.2f}")
        self.deadzone_slider.valueChanged.connect(
            lambda v: self.deadzone_value_label.setText(f"{v/100:.2f}")
        )
        deadzone_layout = QHBoxLayout()
        deadzone_layout.addWidget(self.deadzone_slider)
        deadzone_layout.addWidget(self.deadzone_value_label)
        layout.addWidget(deadzone_label)
        layout.addLayout(deadzone_layout)

        # Outer Deadzone
        outer_deadzone_label = QLabel(value_labels[5])
        self.outer_deadzone_slider = QSlider(Qt.Horizontal)
        self.outer_deadzone_slider.setRange(80, 100)
        outer_deadzone_value = settings.get(value_labels[5], 1.0)
        self.outer_deadzone_slider.setValue(int(outer_deadzone_value * 100))
        self.outer_deadzone_value_label = QLabel(f"{outer_deadzone_value:.2f}")
        self.outer_deadzone_slider.valueChanged.connect(
            lambda v: self.outer_deadzone_value_label.setText(f"{v/100:.2f}")
        )
        outer_deadzone_layout = QHBoxLayout()
        outer_deadzone_layout.addWidget(self.outer_deadzone_slider)
        outer_deadzone_layout.addWidget(self.outer_deadzone_value_label)
        layout.addWidget(outer_deadzone_label)
        layout.addLayout(outer_deadzone_layout)

        # Auto-Start Checkbox
        self.auto_start_checkbox = QCheckBox('Enable on system startup')
        self.auto_start_checkbox.setChecked(settings.get(value_labels[7], False))
        layout.addWidget(self.auto_start_checkbox)

        self.setLayout(layout)