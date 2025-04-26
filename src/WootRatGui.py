import os
import sys
import json
import tkinter as tk
from tkinter import ttk
import threading
from WootRat import run_woot_rat

# JSON file for settings
SETTINGS_FILE = "settings.json"

# Default settings
default_settings = {
    "sensitivity": 12.0,
    "deadzone": 0.1,
    "curve_factor": 1.5,
    "mouse_active": True,
    "key_mapping": "F13-F16 Keys"
}

# Load settings from JSON file
def load_settings():
    try:
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        # If the file doesn't exist, create it with default settings
        save_settings(default_settings)
        return default_settings

# Save settings to JSON file
def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

# Tkinter GUI for settings
def open_settings_window():
    settings = load_settings()

    def save_and_close():
        # Save updated settings
        settings["sensitivity"] = sensitivity_slider.get()
        settings["deadzone"] = float(deadzone_entry.get())
        settings["curve_factor"] = float(curve_factor_var.get())  # Get selected curve factor
        settings["mouse_active"] = bool(toggle_var.get())
        settings["key_mapping"] = key_mapping_var.get()  # Save selected key mapping
        save_settings(settings)

        # Restart the app
        python = sys.executable
        os.execl(python, python, *sys.argv)

    root = tk.Tk()
    root.title("Woot Rat Settings")

    # Sensitivity slider
    tk.Label(root, text="Sensitivity").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    sensitivity_slider = ttk.Scale(root, from_=1.0, to=100.0, orient="horizontal")
    sensitivity_slider.set(settings["sensitivity"])
    sensitivity_slider.grid(row=0, column=1, padx=10, pady=5)

    # Deadzone entry
    tk.Label(root, text="Deadzone").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    deadzone_entry = ttk.Entry(root)
    deadzone_entry.insert(0, str(settings["deadzone"]))
    deadzone_entry.grid(row=1, column=1, padx=10, pady=5)

    # Curve factor dropdown
    tk.Label(root, text="Curve Factor").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    curve_factor_var = tk.StringVar(value=str(settings["curve_factor"]))  # Default value
    curve_factor_dropdown = ttk.Combobox(
        root,
        textvariable=curve_factor_var,
        values=["1.0", "1.5", "2.0", "2.5", "3.0"],  
        state="readonly",
    )
    curve_factor_dropdown.grid(row=2, column=1, padx=10, pady=5)

    # Key mapping dropdown
    tk.Label(root, text="Key Mapping").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    key_mapping_var = tk.StringVar(value=settings.get("key_mapping", "Arrow Keys"))  # Default to "Arrow Keys"
    key_mapping_dropdown = ttk.Combobox(
        root,
        textvariable=key_mapping_var,
        values=["Arrow Keys", "WASD Keys", "F13-F16 Keys"],  
        state="readonly",
    )
    key_mapping_dropdown.grid(row=3, column=1, padx=10, pady=5)

    # Mouse active toggle
    tk.Label(root, text="Enable").grid(row=4, column=0, padx=10, pady=5, sticky="w")
    toggle_var = tk.IntVar(value=int(settings["mouse_active"]))
    toggle_button = ttk.Checkbutton(root, variable=toggle_var, text="On/Off")
    toggle_button.grid(row=4, column=1, padx=10, pady=5)

    # Save button
    save_button = ttk.Button(root, text="Save and Restart", command=save_and_close)
    save_button.grid(row=5, column=0, columnspan=2, pady=10)

    root.mainloop()

def start_woot_rat_thread():
    # Load settings from the JSON file
    settings     = load_settings()
    sensitivity  = settings["sensitivity"]
    deadzone     = settings["deadzone"]
    curve_factor = settings["curve_factor"]
    is_active    = settings["mouse_active"]
    key_map      = settings["key_mapping"]  

    woot_rat_thread = threading.Thread(target=run_woot_rat, args=(sensitivity, deadzone, curve_factor, is_active, key_map), daemon=True)
    woot_rat_thread.start()

if __name__ == "__main__":
    start_woot_rat_thread()
    open_settings_window()