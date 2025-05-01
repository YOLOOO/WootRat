import os
import sys
import json
# JSON file for settings
SETTINGS_FILE = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "WootRat_settings.json")

# Default settings
default_settings = {
    "mouse_sensitivity": 23,
    "y_sensitivity_adjustment": 0.23,
    "scroll_sensitivity": 0.4,
    "deadzone": 0.08,
    "curve_factor": 10.0,
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