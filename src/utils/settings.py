import os
import sys
import json
# JSON file for settings
SETTINGS_FILE = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "WootRat_settings.json")

KEYCODES = {
    # Alphanumeric keys
    "A": 0x04, "B": 0x05, "C": 0x06, "D": 0x07, "E": 0x08, "F": 0x09, "G": 0x0A,
    "H": 0x0B, "I": 0x0C, "J": 0x0D, "K": 0x0E, "L": 0x0F, "M": 0x10, "N": 0x11,
    "O": 0x12, "P": 0x13, "Q": 0x14, "R": 0x15, "S": 0x16, "T": 0x17, "U": 0x18,
    "V": 0x19, "W": 0x1A, "X": 0x1B, "Y": 0x1C, "Z": 0x1D,
    "1": 0x1E, "2": 0x1F, "3": 0x20, "4": 0x21, "5": 0x22, "6": 0x23, "7": 0x24,
    "8": 0x25, "9": 0x26, "0": 0x27,

    # Function keys
    "F1": 0x3A, "F2": 0x3B, "F3": 0x3C, "F4": 0x3D, "F5": 0x3E, "F6": 0x3F,
    "F7": 0x40, "F8": 0x41, "F9": 0x42, "F10": 0x43, "F11": 0x44, "F12": 0x45,
    "F13": 0x68, "F14": 0x69, "F15": 0x6A, "F16": 0x6B, "F17": 0x6C, "F18": 0x6D,
    "F19": 0x6E, "F20": 0x6F,

    # Arrow keys
    "Arrow Up": 0x52, "Arrow Down": 0x51, "Arrow Left": 0x50, "Arrow Right": 0x4F,

    # Modifier keys
    "Shift": 0xE1, "Ctrl": 0xE0, "Alt": 0xE2, "Caps Lock": 0x39, "Tab": 0x2B, "Esc": 0x29,

    # Punctuation and symbols
    "`": 0x35, "-": 0x2D, "=": 0x2E, "[": 0x2F, "]": 0x30, "\\": 0x31,
    ";": 0x33, "'": 0x34, ",": 0x36, ".": 0x37, "/": 0x38,

    # Space and Enter
    "Space": 0x2C, "Enter": 0x28, "Backspace": 0x2A, "Delete": 0x4C, "Insert": 0x49,

    # Other special keys
    "Home": 0x4A, "End": 0x4D, "Page Up": 0x4B, "Page Down": 0x4E,
    "Print Screen": 0x46, "Pause": 0x48
}

DIRECTION_LABELS = [
    "Mouse Up",
    "Mouse Down",
    "Mouse Left",
    "Mouse Right",
    "Scroll Up",
    "Scroll Down",
    "Scroll Left",
    "Scroll Right"
]
VALUE_LABELS = [
    "Mouse Sensitivity",
    "Scroll Sensitivity",
    "Y Sensitivity Adjustment",
    "Curve Factor",
    "Deadzone",
    "Auto Start"
]

# Default settings
default_settings = {
    VALUE_LABELS[0]: 23,
    VALUE_LABELS[1]: 0.4,
    VALUE_LABELS[2]: 0.23,
    VALUE_LABELS[3]: 10.0,
    VALUE_LABELS[4]: 0.8,
    DIRECTION_LABELS[0]: KEYCODES['Arrow Up'],
    DIRECTION_LABELS[1]: KEYCODES["Arrow Down"],
    DIRECTION_LABELS[2]: KEYCODES["Arrow Left"],
    DIRECTION_LABELS[3]: KEYCODES["Arrow Right"],
    DIRECTION_LABELS[4]: KEYCODES["Page Up"],
    DIRECTION_LABELS[5]: KEYCODES["Page Down"],
    DIRECTION_LABELS[6]: KEYCODES["End"],
    DIRECTION_LABELS[7]: KEYCODES["Home"],
    VALUE_LABELS[5]: False
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