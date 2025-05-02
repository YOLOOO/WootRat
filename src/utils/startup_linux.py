import os

def get_autostart_path(name):
    """
    Get the path to the autostart .desktop file for the given application name.

    Args:
        name (str): The name of the application.

    Returns:
        str: The full path to the .desktop file.
    """
    return os.path.expanduser(f"~/.config/autostart/{name}.desktop")

def add_to_startup(app_path, name):
    """
    Add the application to the Linux autostart folder.

    Args:
        app_path (str): The path to the application executable.
        name (str): The name of the application.

    Raises:
        Exception: If the .desktop file cannot be created.
    """
    try:
        desktop_path = get_autostart_path(name)
        content = f"""[Desktop Entry]
Type=Application
Exec={app_path}
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name={name}
"""
        os.makedirs(os.path.dirname(desktop_path), exist_ok=True)
        with open(desktop_path, "w") as f:
            f.write(content)
        os.chmod(desktop_path, 0o755)  # Ensure the file is executable
        print(f"Autostart entry created at: {desktop_path}")
    except Exception as e:
        print(f"Failed to add to startup: {e}")
        raise

def remove_from_startup(name):
    """
    Remove the application from the Linux autostart folder.

    Args:
        name (str): The name of the application.

    Raises:
        Exception: If the .desktop file cannot be removed.
    """
    try:
        desktop_path = get_autostart_path(name)
        if os.path.exists(desktop_path):
            os.remove(desktop_path)
            print(f"Autostart entry removed from: {desktop_path}")
        else:
            print(f"Autostart entry does not exist: {desktop_path}")
    except Exception as e:
        print(f"Failed to remove from startup: {e}")
        raise
