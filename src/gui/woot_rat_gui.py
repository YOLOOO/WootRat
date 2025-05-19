import os
import sys
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QComboBox,
    QPushButton, QLineEdit, QWidget, QMessageBox, QCheckBox, QTabWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from utils.settings import (
    load_settings, save_settings, DIRECTION_LABELS, KEYCODES, VALUE_LABELS
)
from utils.paths import get_resource_path
from utils.startup_platform import add_to_startup, remove_from_startup
from utils.thread_manager import restart_woot_rat_thread

ALL_KEYS = list(KEYCODES.keys())

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
        tab_widget = QTabWidget()

        # --- General Tab ---
        general_tab = QWidget()
        general_layout = QVBoxLayout()

        mouse_sensitivity_label = QLabel(VALUE_LABELS[0])
        self.mouse_sensitivity_slider = QSlider(Qt.Horizontal)
        self.mouse_sensitivity_slider.setRange(1, 80)
        self.mouse_sensitivity_slider.setValue(int(self.settings[VALUE_LABELS[0]]))
        general_layout.addWidget(mouse_sensitivity_label)
        general_layout.addWidget(self.mouse_sensitivity_slider)

        y_sensitivity_label = QLabel(VALUE_LABELS[2])
        self.y_sensitivity_slider = QSlider(Qt.Horizontal)
        self.y_sensitivity_slider.setRange(0, 50)
        self.y_sensitivity_slider.setValue(int(self.settings[VALUE_LABELS[2]] * 100))
        general_layout.addWidget(y_sensitivity_label)
        general_layout.addWidget(self.y_sensitivity_slider)

        scroll_sensitivity_label = QLabel(VALUE_LABELS[1])
        self.scroll_sensitivity_slider = QSlider(Qt.Horizontal)
        self.scroll_sensitivity_slider.setRange(1, 20)
        self.scroll_sensitivity_slider.setValue(int(self.settings[VALUE_LABELS[1]] * 10))
        general_layout.addWidget(scroll_sensitivity_label)
        general_layout.addWidget(self.scroll_sensitivity_slider)

        curve_factor_label = QLabel(VALUE_LABELS[3])
        self.curve_factor_dropdown = QComboBox()
        self.curve_factor_dropdown.addItems([f"{x:.1f}" for x in [i * 0.5 for i in range(2, 21)]])
        self.curve_factor_dropdown.setCurrentText(str(self.settings[VALUE_LABELS[3]]))
        general_layout.addWidget(curve_factor_label)
        general_layout.addWidget(self.curve_factor_dropdown)

        deadzone_label = QLabel(VALUE_LABELS[4])
        self.deadzone_entry = QLineEdit(str(self.settings[VALUE_LABELS[4]]))
        general_layout.addWidget(deadzone_label)
        general_layout.addWidget(self.deadzone_entry)

        # Auto-Start Checkbox
        self.auto_start_checkbox = QCheckBox('Enable on system startup')
        self.auto_start_checkbox.setChecked(self.settings.get(VALUE_LABELS[5], False))
        self.auto_start_checkbox.stateChanged.connect(self.toggle_auto_start)
        general_layout.addWidget(self.auto_start_checkbox)

        general_tab.setLayout(general_layout)
        tab_widget.addTab(general_tab, "General")

        # --- Key Mapping Tab ---
        keymap_tab = QWidget()
        keymap_layout = QVBoxLayout()
        self.key_mapping_dropdowns = {}
        for label in DIRECTION_LABELS:
            dropdown_label = QLabel(label)
            dropdown = QComboBox()
            dropdown.addItems(ALL_KEYS)
            saved_key = self.settings.get(label)
            if saved_key is not None:
                if isinstance(saved_key, int):
                    key_name = next((k for k, v in KEYCODES.items() if v == saved_key), ALL_KEYS[0])
                else:
                    key_name = saved_key
            else:
                key_name = ALL_KEYS[0]
            dropdown.setCurrentText(key_name)
            self.key_mapping_dropdowns[label] = dropdown
            keymap_layout.addWidget(dropdown_label)
            keymap_layout.addWidget(dropdown)
        keymap_tab.setLayout(keymap_layout)
        tab_widget.addTab(keymap_tab, "Key Mapping")

        # Add tabs to main layout
        main_layout.addWidget(tab_widget)

        # Buttons (save, etc.)
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
            # Save the updated main settings using VALUE_LABELS
            self.settings[VALUE_LABELS[0]] = self.mouse_sensitivity_slider.value()
            self.settings[VALUE_LABELS[1]] = self.scroll_sensitivity_slider.value() / 10.0
            self.settings[VALUE_LABELS[2]] = self.y_sensitivity_slider.value() / 100.0
            self.settings[VALUE_LABELS[3]] = float(self.curve_factor_dropdown.currentText())
            self.settings[VALUE_LABELS[4]] = float(self.deadzone_entry.text())
            self.settings[VALUE_LABELS[5]] = self.auto_start_checkbox.isChecked()

            # Save the updated key mappings as key names
            for label, dropdown in self.key_mapping_dropdowns.items():
                self.settings[label] = dropdown.currentText()

            save_settings(self.settings)

            restart_woot_rat_thread()

            QMessageBox.information(self, "Success", "Settings updated successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save settings: {e}")


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
            self.settings[VALUE_LABELS[5]] = enable
            save_settings(self.settings)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update auto-start: {e}")

