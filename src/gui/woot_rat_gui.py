import os
import sys
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QComboBox,
    QPushButton, QLineEdit, QWidget, QMessageBox, QCheckBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from utils.settings import load_settings, save_settings
from utils.paths import get_resource_path
from utils.startup_platform import add_to_startup, remove_from_startup
from utils.thread_manager import restart_woot_rat_thread

ALL_KEYS = [
    # Alphanumeric keys
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
    "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",

    # Function keys
    "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10",
    "F11", "F12", "F13", "F14", "F15", "F16", "F17", "F18", "F19", "F20",

    # Arrow keys
    "Arrow Up", "Arrow Down", "Arrow Left", "Arrow Right",

    # Modifier keys
    "Shift", "Ctrl", "Alt", "Caps Lock", "Tab", "Esc",

    # Punctuation and symbols
    "`", "-", "=", "[", "]", "\\", ";", "'", ",", ".", "/",

    # Space and Enter
    "Space", "Enter", "Backspace", "Delete", "Insert",

    # Other special keys
    "Home", "End", "Page Up", "Page Down", "Print Screen", "Pause"
]

class SettingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = load_settings()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Woot Rat Settings")
        self.setGeometry(100, 100, 400, 600)

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

        # Key Mapping Dropdowns
        self.key_mapping_dropdowns = {}
        key_mapping_labels = [
            "Mouse Up", "Mouse Down", "Mouse Left", "Mouse Right",
            "Scroll Up", "Scroll Down", "Scroll Right", "Scroll Left"
        ]

        for label in key_mapping_labels:
            dropdown_label = QLabel(label)
            dropdown = QComboBox()
            dropdown.addItems(ALL_KEYS)
            dropdown.setCurrentText(self.settings.get(f"key_{label.lower().replace(' ', '_')}", "F13"))
            self.key_mapping_dropdowns[label] = dropdown
            main_layout.addWidget(dropdown_label)
            main_layout.addWidget(dropdown)

        # Auto-Start Checkbox
        self.auto_start_checkbox = QCheckBox("Enable Auto-Start")
        self.auto_start_checkbox.setChecked(self.settings.get("auto_start", False))
        self.auto_start_checkbox.stateChanged.connect(self.toggle_auto_start)
        main_layout.addWidget(self.auto_start_checkbox)

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

            # Save the updated key mappings
            for label, dropdown in self.key_mapping_dropdowns.items():
                self.settings[f"key_{label.lower().replace(' ', '_')}"] = dropdown.currentText()

            save_settings(self.settings)

            # Assemble and pass the new key mapping
            key_mapping = self.assemble_key_mapping()
            restart_woot_rat_thread(key_mapping)

            QMessageBox.information(self, "Success", "Settings updated successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save settings: {e}")

    def assemble_key_mapping(self):
        """
        Assemble a new key mapping based on the selected keys and pass it to the WootRatEngine.
        """
        try:
            key_mapping = {
                "Up": self.settings["key_mouse_up"],
                "Down": self.settings["key_mouse_down"],
                "Left": self.settings["key_mouse_left"],
                "Right": self.settings["key_mouse_right"],
                "Scroll Up": self.settings["key_scroll_up"],
                "Scroll Down": self.settings["key_scroll_down"],
                "Scroll Right": self.settings["key_scroll_right"],
                "Scroll Left": self.settings["key_scroll_left"]
            }
            print(f"New key mapping: {key_mapping}")
            return key_mapping
        except KeyError as e:
            QMessageBox.critical(self, "Error", f"Error assembling key mapping: {e}")
            # Return a default key mapping to avoid NoneType issues
            return { #Review if this is needed
                "Up": "Arrow Up",
                "Down": "Arrow Down",
                "Left": "Arrow Left",
                "Right": "Arrow Right",
                "Scroll Up": "Page Up",
                "Scroll Down": "Page Down",
                "Scroll Right": "End",
                "Scroll Left": "Home"
            }

    def toggle_auto_start(self, state):
        """
        Enable or disable auto-start based on the checkbox state.

        Args:
            state (int): The state of the checkbox (Qt.Checked or Qt.Unchecked).
        """
        enable = state == Qt.Checked
        app_path = os.path.abspath(sys.argv[0])
        try:
            if enable:
                add_to_startup(app_path, "WootRat")
                QMessageBox.information(self, "Auto-Start", "Auto-start enabled successfully!")
            else:
                remove_from_startup("WootRat")
                QMessageBox.information(self, "Auto-Start", "Auto-start disabled successfully!")
            self.settings["auto_start"] = enable
            save_settings(self.settings)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update auto-start: {e}")

