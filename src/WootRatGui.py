import os
import sys
import json
import tkinter as tk
from tkinter import ttk
import threading
from PIL import Image
from pystray import Icon, Menu, MenuItem
from WootRat import run_woot_rat

# JSON file for settings
SETTINGS_FILE = "settings.json"

# Default settings
default_settings = {
    "mouse_sensitivity": 15.0,
    "scroll_sensitivity": 0.5,
    "deadzone": 0.1,
    "curve_factor": 2.0,
    "mouse_active": True,
    "key_mapping": "F13-F16 Keys"
}

def load_settings():
    """
    Load settings from the JSON file. If the file does not exist, 
    create it with default settings.

    Returns:
        dict: The settings loaded from the JSON file.
    """
    try:
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        save_settings(default_settings)
        return default_settings

def save_settings(settings):
    """
    Save the given settings to the JSON file.

    Args:
        settings (dict): The settings to save.
    """
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

def open_settings_window():
    """
    Open the settings window using Tkinter. Allows the user to adjust
    mouse sensitivity, scroll sensitivity, deadzone, curve factor, 
    and key mapping. Changes can be saved and the application restarted.
    """
    settings = load_settings()

    def save_and_restart():
        """
        Save the settings and restart the application.
        """
        settings["mouse_sensitivity"] = sensitivity_slider.get()
        settings["scroll_sensitivity"] = scroll_sensitivity_slider.get()
        settings["deadzone"] = float(deadzone_entry.get())
        settings["curve_factor"] = float(curve_factor_var.get())
        settings["mouse_active"] = bool(toggle_var.get())
        settings["key_mapping"] = key_mapping_var.get()
        save_settings(settings)

        # Restart the application
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def on_close():
        """
        Close the settings window without restarting the application.
        """
        root.destroy()

    root = tk.Tk()
    root.title("Woot Rat Settings")

    # Bind the close button to the on_close function
    root.protocol("WM_DELETE_WINDOW", on_close)

    # Mouse sensitivity slider
    tk.Label(root, text="Mouse Sensitivity").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    sensitivity_slider = ttk.Scale(root, from_=1.0, to=100.0, orient="horizontal")
    sensitivity_slider.set(settings["mouse_sensitivity"])
    sensitivity_slider.grid(row=0, column=1, padx=10, pady=5)

    # Scroll sensitivity slider
    tk.Label(root, text="Scroll Sensitivity").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    scroll_sensitivity_slider = ttk.Scale(root, from_=0.1, to=10.0, orient="horizontal")
    scroll_sensitivity_slider.set(settings["scroll_sensitivity"])
    scroll_sensitivity_slider.grid(row=1, column=1, padx=10, pady=5)

    # Deadzone entry
    tk.Label(root, text="Deadzone").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    deadzone_entry = ttk.Entry(root)
    deadzone_entry.insert(0, str(settings["deadzone"]))
    deadzone_entry.grid(row=2, column=1, padx=10, pady=5)

    # Curve factor dropdown
    tk.Label(root, text="Curve Factor").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    curve_factor_var = tk.StringVar(value=str(settings["curve_factor"]))
    curve_factor_dropdown = ttk.Combobox(
        root,
        textvariable=curve_factor_var,
        values=["1.0", "1.5", "2.0", "2.5", "3.0"],
        state="readonly",
    )
    curve_factor_dropdown.grid(row=3, column=1, padx=10, pady=5)

    # Key mapping dropdown
    tk.Label(root, text="Key Mapping").grid(row=4, column=0, padx=10, pady=5, sticky="w")
    key_mapping_var = tk.StringVar(value=settings.get("key_mapping", "Arrow Keys"))
    key_mapping_dropdown = ttk.Combobox(
        root,
        textvariable=key_mapping_var,
        values=["Arrow Keys", "WASD Keys", "F13-F16 Keys"],
        state="readonly",
    )
    key_mapping_dropdown.grid(row=4, column=1, padx=10, pady=5)

    # Mouse active toggle
    tk.Label(root, text="Enable").grid(row=5, column=0, padx=10, pady=5, sticky="w")
    toggle_var = tk.IntVar(value=int(settings["mouse_active"]))
    toggle_button = ttk.Checkbutton(root, variable=toggle_var, text="On/Off")
    toggle_button.grid(row=5, column=1, padx=10, pady=5)

    # Save and Restart button
    save_button = ttk.Button(root, text="Save and Restart", command=save_and_restart)
    save_button.grid(row=6, column=0, columnspan=2, pady=10)

    root.mainloop()

def create_tray_icon():
    """
    Create a system tray icon with options to open the settings window
    or exit the application.
    """
    def on_open_settings(icon, item):
        """
        Open the settings window from the tray menu.
        """
        open_settings_window()

    def on_exit(icon, item):
        """
        Exit the application from the tray menu.
        """
        icon.stop()
        sys.exit()

    # Load the icon image from the icon folder
    icon_path = os.path.join(os.path.dirname(__file__), "icon", "WootRat.png")
    icon_image = Image.open(icon_path).convert("RGBA")

    # Add a white background under the transparent icon
    white_background = Image.new("RGBA", icon_image.size, (255, 255, 255, 255))
    icon_image = Image.alpha_composite(white_background, icon_image)  

    # Create the tray menu
    menu = Menu(
        MenuItem("Open Settings", on_open_settings),
        MenuItem("Exit", on_exit)
    )

    # Create and run the tray icon
    tray_icon = Icon("WootRat", icon_image, "WootRat", menu)
    tray_icon.run()

def start_woot_rat_thread():
    """
    Start the WootRat functionality in a separate thread to handle
    mouse movement and scrolling based on Wooting keyboard input.
    """
    settings      = load_settings()
    sensitivity_m = settings["mouse_sensitivity"]
    sensitivity_s = settings["scroll_sensitivity"]
    deadzone      = settings["deadzone"]
    curve_factor  = settings["curve_factor"]
    is_active     = settings["mouse_active"]
    key_map       = settings["key_mapping"]

    woot_rat_thread = threading.Thread(
        target=run_woot_rat,
        args=(sensitivity_m, sensitivity_s, deadzone, curve_factor, is_active, key_map),
        daemon=True,
    )
    woot_rat_thread.start()

if __name__ == "__main__":
    """
    Entry point of the application. Starts the WootRat thread and
    creates the system tray icon.
    """
    start_woot_rat_thread()
    create_tray_icon()