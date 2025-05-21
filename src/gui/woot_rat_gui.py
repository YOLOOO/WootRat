import os
import sys
import numpy as np
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout,
    QPushButton, QWidget, QMessageBox, QTabWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from utils.settings import (
    load_settings, save_settings, DIRECTION_LABELS, KEYCODES, VALUE_LABELS
)
from logic.woot_rat_engine import WootRatEngine
from utils.paths import get_resource_path
from utils.startup_platform import add_to_startup, remove_from_startup
from utils.thread_manager import restart_woot_rat_thread
from gui.general_tab import GeneralTab
from gui.keymap_tab import KeyMappingTab
from gui.diagnostic_tab import DiagnosticsTab
from gui.support_tab import SupportTab
from gui.info_tab import InfoTab

ALL_KEYS = list(KEYCODES.keys())

class SettingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Try to set dark title bar on Windows 10/11
        if sys.platform == "win32":
            try:
                import ctypes
                hwnd = int(self.winId())
                DWMWA_USE_IMMERSIVE_DARK_MODE = 20
                value = ctypes.c_int(1)
                ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, ctypes.byref(value), ctypes.sizeof(value)
                )
            except Exception as e:
                print("Could not set dark mode for title bar:", e)
        self.settings = load_settings()
        self.engine = WootRatEngine()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Woot Rat Settings")
        self.setGeometry(100, 100, 450, 600)

        icon_path = get_resource_path("resources/woot_rat.png")
        self.setWindowIcon(QIcon(icon_path))

        main_layout = QVBoxLayout()
        tab_widget = QTabWidget()
        self.general_tab = GeneralTab(self.settings, VALUE_LABELS)
        self.keymap_tab = KeyMappingTab(self.settings, DIRECTION_LABELS, ALL_KEYS, KEYCODES)
        self.diagnostics_tab = DiagnosticsTab(self.settings)
        self.support_tab = SupportTab(get_resource_path)
        self.info_tab = InfoTab()

        tab_widget.addTab(self.general_tab, "General")
        tab_widget.addTab(self.keymap_tab, "Key Mapping")
        tab_widget.addTab(self.diagnostics_tab, "Diagnostics")
        tab_widget.addTab(self.info_tab, "Info")
        tab_widget.addTab(self.support_tab, "Support")

        # Add tabs to main layout
        main_layout.addWidget(tab_widget)

        # Buttons (save, etc.)
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save Settings")
        self.save_button.clicked.connect(self.save_settings)
        button_layout.addWidget(self.save_button)
        main_layout.addLayout(button_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # --- Tab change logic ---
        def on_tab_changed(index):
            tab_name = tab_widget.tabText(index)
            if tab_name == 'Support':
                self.save_button.hide()
            else:
                self.save_button.show()
        tab_widget.currentChanged.connect(on_tab_changed)
        on_tab_changed(tab_widget.currentIndex())

        # Connect sliders and dropdowns to plot_curve
        self.general_tab.deadzone_slider.valueChanged.connect(self.plot_curve)
        self.general_tab.outer_deadzone_slider.valueChanged.connect(self.plot_curve)
        self.general_tab.curve_factor_dropdown.currentTextChanged.connect(self.plot_curve)
        self.diagnostics_tab.curve_type_dropdown.currentTextChanged.connect(self.plot_curve)

        # Initial curve plot
        self.plot_curve()

    def save_settings(self):
        """
        Save the current settings and restart the WootRat thread.
        """
        try:
            self.settings[VALUE_LABELS[0]] = self.general_tab.mouse_sensitivity_slider.value()
            self.settings[VALUE_LABELS[1]] = self.general_tab.scroll_sensitivity_slider.value() / 10.0
            self.settings[VALUE_LABELS[2]] = self.general_tab.y_sensitivity_slider.value() / 100.0
            self.settings[VALUE_LABELS[3]] = float(self.general_tab.curve_factor_dropdown.currentText())
            self.settings[VALUE_LABELS[4]] = self.general_tab.deadzone_slider.value() / 100.0
            self.settings[VALUE_LABELS[5]] = self.general_tab.outer_deadzone_slider.value() / 100.0
            self.settings[VALUE_LABELS[6]] = self.diagnostics_tab.curve_type_dropdown.currentText()
            self.settings[VALUE_LABELS[7]] = self.general_tab.auto_start_checkbox.isChecked()
            for label, dropdown in self.keymap_tab.key_mapping_dropdowns.items():
                self.settings[label] = dropdown.currentText()
            save_settings(self.settings)
            restart_woot_rat_thread()
            QMessageBox.information(self, "Success", "Settings updated successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save settings: {e}")

    def toggle_auto_start(self, state):
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

    def plot_curve(self):
        deadzone = self.general_tab.deadzone_slider.value() / 100.0
        outer_deadzone = self.general_tab.outer_deadzone_slider.value() / 100.0
        curve_factor = float(self.general_tab.curve_factor_dropdown.currentText())
        curve_type = self.diagnostics_tab.curve_type_dropdown.currentText()
        x = np.linspace(0, 1, 200)
        y = [
            self.engine.process_input(
                val, deadzone, curve_factor, outer_deadzone, curve_type
            ) for val in x
        ]
        self.diagnostics_tab.curve_ax.clear()
        self.diagnostics_tab.curve_ax.plot(x, y, label="Processed Output")
        self.diagnostics_tab.curve_ax.axvline(deadzone, color='green', linestyle='--', label='Activation Point')
        self.diagnostics_tab.curve_ax.axvline(outer_deadzone, color='orange', linestyle='--', label='Maximum Actuation')
        self.diagnostics_tab.curve_ax.set_xlabel("Raw Input")
        self.diagnostics_tab.curve_ax.set_ylabel("Processed Output")
        self.diagnostics_tab.curve_ax.set_title("Wooting Response Curve")
        self.diagnostics_tab.curve_ax.set_xlim(0, 1)
        self.diagnostics_tab.curve_ax.set_ylim(0, 1)
        self.diagnostics_tab.curve_ax.legend()
        self.diagnostics_tab.curve_canvas.draw()

