import os
import sys
import json
import threading
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QComboBox,
    QPushButton, QLineEdit, QWidget, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from WootRat import run_woot_rat

# JSON file for settings
SETTINGS_FILE = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "WootRat_settings.json")

woot_rat_thread = None

# Default settings
default_settings = {
    "mouse_sensitivity": 25,
    "y_sensitivity_adjustment": 0.5,
    "scroll_sensitivity": 0.3,
    "deadzone": 0.1,
    "curve_factor": 2.0,
    "key_mapping": "F13-F16 Keys"
}


def load_settings():
    """
    Load settings from the JSON file. If the file does not exist, 
    create it with default settings. Ensure all default keys are present.

    Returns:
        dict: The settings loaded from the JSON file.
    """
    try:
        with open(SETTINGS_FILE, "r") as f:
            settings = json.load(f)
    except FileNotFoundError:
        # If the file does not exist, create it with default settings
        settings = default_settings.copy()

    # Ensure all default keys are present
    for key, value in default_settings.items():
        if key not in settings:
            settings[key] = value

    # Save updated settings if any defaults were added
    save_settings(settings)
    return settings


def save_settings(settings):
    """
    Save the given settings to the JSON file.

    Args:
        settings (dict): The settings to save.
    """
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=4)
        print(f"Settings saved to {SETTINGS_FILE}")
    except Exception as e:
        print(f"Failed to save settings: {e}")


def get_resource_path(filename):
    """
    Get the absolute path to a resource file, whether running as a script or as a PyInstaller executable.
    """
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:  # Running as a script
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, filename)


class SettingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = load_settings()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Woot Rat Settings")
        self.setGeometry(100, 100, 400, 300)

        # Set the window icon
        icon_path = get_resource_path(os.path.join("icon", "WootRat.png"))
        self.setWindowIcon(QIcon(icon_path))

        # Main layout
        main_layout = QVBoxLayout()

        # Mouse sensitivity slider
        mouse_sensitivity_label = QLabel("Mouse Sensitivity")
        self.mouse_sensitivity_slider = QSlider(Qt.Horizontal)
        self.mouse_sensitivity_slider.setMinimum(1)
        self.mouse_sensitivity_slider.setMaximum(80)
        self.mouse_sensitivity_slider.setValue(int(self.settings["mouse_sensitivity"]))  
        main_layout.addWidget(mouse_sensitivity_label)
        main_layout.addWidget(self.mouse_sensitivity_slider)

        # Y-axis sensitivity adjustment slider
        y_sensitivity_label = QLabel("Y-Axis Dampening (%)")
        self.y_sensitivity_slider = QSlider(Qt.Horizontal)
        self.y_sensitivity_slider.setMinimum(0)
        self.y_sensitivity_slider.setMaximum(50)
        self.y_sensitivity_slider.setValue(int(self.settings["mouse_sensitivity"]))  
        main_layout.addWidget(y_sensitivity_label)
        main_layout.addWidget(self.y_sensitivity_slider)

        # Scroll sensitivity slider
        scroll_sensitivity_label = QLabel("Scroll Sensitivity")
        self.scroll_sensitivity_slider = QSlider(Qt.Horizontal)
        self.scroll_sensitivity_slider.setMinimum(1)
        self.scroll_sensitivity_slider.setMaximum(20)
        self.scroll_sensitivity_slider.setValue(int(self.settings["scroll_sensitivity"] * 10))  
        main_layout.addWidget(scroll_sensitivity_label)
        main_layout.addWidget(self.scroll_sensitivity_slider)

        # Deadzone entry
        deadzone_label = QLabel("Deadzone")
        self.deadzone_entry = QLineEdit(str(self.settings["deadzone"]))
        main_layout.addWidget(deadzone_label)
        main_layout.addWidget(self.deadzone_entry)

        # Curve factor dropdown
        curve_factor_label = QLabel("Curve Factor")
        self.curve_factor_dropdown = QComboBox()
        self.curve_factor_dropdown.addItems(["1.0", "1.5", "2.0", "2.5", "3.0"])
        self.curve_factor_dropdown.setCurrentText(str(self.settings["curve_factor"]))
        main_layout.addWidget(curve_factor_label)
        main_layout.addWidget(self.curve_factor_dropdown)

        # Key mapping dropdown
        key_mapping_label = QLabel("Key Mapping")
        self.key_mapping_dropdown = QComboBox()
        self.key_mapping_dropdown.addItems(["Arrow Keys", "WASD Keys", "F13-F16 Keys"])
        self.key_mapping_dropdown.setCurrentText(self.settings["key_mapping"])
        main_layout.addWidget(key_mapping_label)
        main_layout.addWidget(self.key_mapping_dropdown)

        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save Settings")
        save_button.clicked.connect(self.save_settings)
        button_layout.addWidget(save_button)

        main_layout.addLayout(button_layout)

        # Set central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def save_settings(self):
        """
        Save the settings to the JSON file.
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

            QMessageBox.information(self, "Success", "Settings saved successfully! Please restart application for them to take effect.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save settings: {e}")


def start_woot_rat_thread():
    """
    Start the WootRat functionality in a separate thread to handle
    mouse movement and scrolling based on Wooting keyboard input.
    """
    settings       = load_settings()
    sensitivity_m  = settings["mouse_sensitivity"]
    sensitivity_mY = settings["y_sensitivity_adjustment"]
    sensitivity_s  = settings["scroll_sensitivity"]
    deadzone       = settings["deadzone"]
    curve_factor   = settings["curve_factor"]
    key_map        = settings["key_mapping"]

    woot_rat_thread = threading.Thread(
        target=run_woot_rat,
        args=(sensitivity_m, sensitivity_s, deadzone, curve_factor, key_map, sensitivity_mY),
        daemon=True,
    )
    woot_rat_thread.start()


def cleanup_threads():
    """
    Ensure all threads are properly stopped or joined before exiting.
    """
    global woot_rat_thread
    if woot_rat_thread and woot_rat_thread.is_alive():
        try:
            woot_rat_thread.join(timeout=5)
        except Exception as e:
            print(f"Failed to join WootRat thread: {e}")


if __name__ == "__main__":
    """
    Entry point of the application. Starts the WootRat thread and
    opens the settings window.
    """
    try:
        start_woot_rat_thread()
        app = QApplication(sys.argv)

        # Load and apply the QSS stylesheet
        qss_path = os.path.join(os.path.dirname(__file__), "style.qss")
        with open(qss_path, "r") as f:
            app.setStyleSheet(f.read())

        settings_window = SettingsWindow()
        settings_window.show()
        sys.exit(app.exec_())
    finally:
        cleanup_threads()
