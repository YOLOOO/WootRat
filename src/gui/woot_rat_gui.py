import os
import sys
import numpy as np
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QComboBox,
    QPushButton, QWidget, QMessageBox, QCheckBox, QTabWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from utils.settings import (
    load_settings, save_settings, DIRECTION_LABELS, KEYCODES, VALUE_LABELS
)
from logic.woot_rat_engine import WootRatEngine
from utils.paths import get_resource_path
from utils.startup_platform import add_to_startup, remove_from_startup
from utils.thread_manager import restart_woot_rat_thread

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

        # Deadzone
        deadzone_label = QLabel(VALUE_LABELS[4])
        self.deadzone_slider = QSlider(Qt.Horizontal)
        self.deadzone_slider.setRange(0, 50)  # 0.00 to 0.50
        deadzone_value = self.settings.get(VALUE_LABELS[4], 0.08)
        self.deadzone_slider.setValue(int(deadzone_value * 100))
        self.deadzone_slider.valueChanged.connect(
            lambda v: self.deadzone_value_label.setText(f"{v/100:.2f}")
        )
        deadzone_layout = QHBoxLayout()
        self.deadzone_value_label = QLabel(f"{deadzone_value:.2f}")
        deadzone_layout.addWidget(self.deadzone_slider)
        deadzone_layout.addWidget(self.deadzone_value_label)
        general_layout.addWidget(deadzone_label)
        general_layout.addLayout(deadzone_layout)

        # Outer Deadzone
        outer_deadzone_label = QLabel(VALUE_LABELS[5])
        self.outer_deadzone_slider = QSlider(Qt.Horizontal)
        self.outer_deadzone_slider.setRange(80, 100)
        outer_deadzone_value = self.settings.get(VALUE_LABELS[5], 1.0)
        self.outer_deadzone_slider.setValue(int(outer_deadzone_value * 100))
        self.outer_deadzone_slider.valueChanged.connect(
            lambda v: self.outer_deadzone_value_label.setText(f"{v/100:.2f}")
        )
        outer_deadzone_layout = QHBoxLayout()
        self.outer_deadzone_value_label = QLabel(f"{outer_deadzone_value:.2f}")
        outer_deadzone_layout.addWidget(self.outer_deadzone_slider)
        outer_deadzone_layout.addWidget(self.outer_deadzone_value_label)
        general_layout.addWidget(outer_deadzone_label)
        general_layout.addLayout(outer_deadzone_layout)

        # Auto-Start Checkbox
        self.auto_start_checkbox = QCheckBox('Enable on system startup')
        self.auto_start_checkbox.setChecked(self.settings.get(VALUE_LABELS[7], False))
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

        # --- Diagnostics Tab ---
        diagnostics_tab = QWidget()
        diagnostics_layout = QVBoxLayout()

        # Curve type dropdown (now only in Diagnostics tab)
        curve_type_label = QLabel(VALUE_LABELS[6])
        self.curve_type_dropdown = QComboBox()
        self.curve_type_dropdown.addItems(["power", "log", "s_curve", "linear"])
        self.curve_type_dropdown.setCurrentText(self.settings.get("Curve Type", "power"))
        diagnostics_layout.addWidget(curve_type_label)
        diagnostics_layout.addWidget(self.curve_type_dropdown)

        # Curve visualization
        curve_label = QLabel("Curve Visualization")
        diagnostics_layout.addWidget(curve_label)

        curve_explanation = QLabel(
            "Note: Raw input 0.0–1.0 corresponds to 0.0–4.0 mm of analog travel\n"
            "on most Wooting switches. 0.0 = not pressed, 1.0 = fully pressed (4.0 mm)."
        )
        curve_explanation.setStyleSheet("color: #bbbbbb; font-size: 12px;")
        curve_explanation.setWordWrap(True)
        diagnostics_layout.addWidget(curve_explanation)

        self.curve_canvas = FigureCanvas(plt.Figure(figsize=(4, 2)))
        diagnostics_layout.addWidget(self.curve_canvas)
        self.curve_ax = self.curve_canvas.figure.subplots()

        diagnostics_tab.setLayout(diagnostics_layout)
        tab_widget.addTab(diagnostics_tab, "Diagnostics")

        # --- Support Tab ---
        support_tab = QWidget()
        support_layout = QVBoxLayout()
        image_path = get_resource_path("resources/rat.png")
        support_pixmap = QPixmap(image_path)
        image_label = QLabel()
        image_label.setPixmap(support_pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        image_label.setAlignment(Qt.AlignCenter)
        support_layout.addWidget(image_label)
        support_text = QLabel("Need help?\nContact me at:\nviktortornborg@hotmail.com")
        support_text.setAlignment(Qt.AlignCenter)
        support_text.setStyleSheet("color: #cccccc; font-size: 16px;")
        support_layout.addWidget(support_text)
        support_tab.setLayout(support_layout)
        tab_widget.addTab(support_tab, "Support")

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
        self.deadzone_slider.valueChanged.connect(self.plot_curve)
        self.outer_deadzone_slider.valueChanged.connect(self.plot_curve)
        self.curve_factor_dropdown.currentTextChanged.connect(self.plot_curve)
        self.curve_type_dropdown.currentTextChanged.connect(self.plot_curve)

        # Initial curve plot
        self.plot_curve()

    def save_settings(self):
        """
        Save the current settings and restart the WootRat thread.
        """
        try:
            self.settings[VALUE_LABELS[0]] = self.mouse_sensitivity_slider.value()
            self.settings[VALUE_LABELS[1]] = self.scroll_sensitivity_slider.value() / 10.0
            self.settings[VALUE_LABELS[2]] = self.y_sensitivity_slider.value() / 100.0
            self.settings[VALUE_LABELS[3]] = float(self.curve_factor_dropdown.currentText())
            self.settings[VALUE_LABELS[4]] = self.deadzone_slider.value() / 100.0
            self.settings[VALUE_LABELS[5]] = self.outer_deadzone_slider.value() / 100.0
            self.settings[VALUE_LABELS[6]] = self.curve_type_dropdown.currentText()
            self.settings[VALUE_LABELS[7]] = self.auto_start_checkbox.isChecked()
            for label, dropdown in self.key_mapping_dropdowns.items():
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
        deadzone = self.deadzone_slider.value() / 100.0
        outer_deadzone = self.outer_deadzone_slider.value() / 100.0
        curve_factor = float(self.curve_factor_dropdown.currentText())
        curve_type = self.curve_type_dropdown.currentText()
        x = np.linspace(0, 1, 200)
        y = [
            self.engine.process_input(
                val, deadzone, curve_factor, outer_deadzone, curve_type
            ) for val in x
        ]
        self.curve_ax.clear()
        self.curve_ax.plot(x, y, label="Processed Output")
        self.curve_ax.axvline(deadzone, color='red', linestyle='--', label='Deadzone')
        self.curve_ax.axvline(outer_deadzone, color='orange', linestyle='--', label='Outer Deadzone')
        self.curve_ax.set_xlabel("Raw Input")
        self.curve_ax.set_ylabel("Processed Output")
        self.curve_ax.set_title("Analog Response Curve")
        self.curve_ax.set_xlim(0, 1)
        self.curve_ax.set_ylim(0, 1)
        self.curve_ax.legend()
        self.curve_canvas.draw()

