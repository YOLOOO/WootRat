from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QComboBox,
    QPushButton, QLineEdit, QWidget, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from utils.settings import load_settings, save_settings
from utils.paths import get_resource_path


class SettingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = load_settings()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Woot Rat Settings")
        self.setGeometry(100, 100, 400, 300)

        icon_path = get_resource_path("resources/woot_rat.png")
        self.setWindowIcon(QIcon(icon_path))

        main_layout = QVBoxLayout()

        mouse_sensitivity_label = QLabel("Mouse Sensitivity")
        self.mouse_sensitivity_slider = QSlider(Qt.Horizontal)
        self.mouse_sensitivity_slider.setRange(1, 80)
        self.mouse_sensitivity_slider.setValue(int(self.settings["mouse_sensitivity"]))
        main_layout.addWidget(mouse_sensitivity_label)
        main_layout.addWidget(self.mouse_sensitivity_slider)

        y_sensitivity_label = QLabel("Y-Axis Dampening (%)")
        self.y_sensitivity_slider = QSlider(Qt.Horizontal)
        self.y_sensitivity_slider.setRange(0, 50)
        self.y_sensitivity_slider.setValue(int(self.settings["y_sensitivity_adjustment"] * 100))
        main_layout.addWidget(y_sensitivity_label)
        main_layout.addWidget(self.y_sensitivity_slider)

        scroll_sensitivity_label = QLabel("Scroll Sensitivity")
        self.scroll_sensitivity_slider = QSlider(Qt.Horizontal)
        self.scroll_sensitivity_slider.setRange(1, 20)
        self.scroll_sensitivity_slider.setValue(int(self.settings["scroll_sensitivity"] * 10))
        main_layout.addWidget(scroll_sensitivity_label)
        main_layout.addWidget(self.scroll_sensitivity_slider)

        deadzone_label = QLabel("Deadzone")
        self.deadzone_entry = QLineEdit(str(self.settings["deadzone"]))
        main_layout.addWidget(deadzone_label)
        main_layout.addWidget(self.deadzone_entry)

        curve_factor_label = QLabel("Curve Factor")
        self.curve_factor_dropdown = QComboBox()
        self.curve_factor_dropdown.addItems([f"{x:.1f}" for x in [i * 0.5 for i in range(2, 21)]])
        self.curve_factor_dropdown.setCurrentText(str(self.settings["curve_factor"]))
        main_layout.addWidget(curve_factor_label)
        main_layout.addWidget(self.curve_factor_dropdown)

        key_mapping_label = QLabel("Key Mapping")
        self.key_mapping_dropdown = QComboBox()
        self.key_mapping_dropdown.addItems(["Arrow Keys", "WASD Keys", "F13-F16 Keys"])
        self.key_mapping_dropdown.setCurrentText(self.settings["key_mapping"])
        main_layout.addWidget(key_mapping_label)
        main_layout.addWidget(self.key_mapping_dropdown)

        button_layout = QHBoxLayout()
        save_button = QPushButton("Save Settings")
        save_button.clicked.connect(self.save_settings)
        button_layout.addWidget(save_button)

        main_layout.addLayout(button_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def save_settings(self):
        """
        Save the current settings and restart the WootRat thread.
        """
        try:
            # Save the updated settings
            self.settings["mouse_sensitivity"] = self.mouse_sensitivity_slider.value()
            self.settings["y_sensitivity_adjustment"] = self.y_sensitivity_slider.value() / 100.0
            self.settings["scroll_sensitivity"] = self.scroll_sensitivity_slider.value() / 10.0
            self.settings["deadzone"] = float(self.deadzone_entry.text())
            self.settings["curve_factor"] = float(self.curve_factor_dropdown.currentText())
            self.settings["key_mapping"] = self.key_mapping_dropdown.currentText()
            save_settings(self.settings)

            # Restart the WootRat thread
            from main import restart_woot_rat_thread  # Import the function
            restart_woot_rat_thread()

            QMessageBox.information(self, "Success", "Settings updated successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save settings: {e}")
