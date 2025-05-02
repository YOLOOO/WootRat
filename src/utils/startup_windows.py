import os
import win32com.client

def get_shortcut_path(name="WootRat.lnk"):
    """
    Get the path to the Windows startup folder for the given shortcut name.

    Args:
        name (str): The name of the shortcut file.

    Returns:
        str: The full path to the shortcut file.
    """
    return os.path.join(
        os.environ["APPDATA"],
        "Microsoft\\Windows\\Start Menu\\Programs\\Startup",
        name,
    )

def add_to_startup(app_path: str, shortcut_name="WootRat.lnk"):
    """
    Add the application to the Windows startup folder.

    Args:
        app_path (str): The path to the application executable.
        shortcut_name (str): The name of the shortcut file.

    Raises:
        Exception: If the shortcut creation fails.
    """
    try:
        shortcut_path = get_shortcut_path(shortcut_name)
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = app_path
        shortcut.WorkingDirectory = os.path.dirname(app_path)
        shortcut.IconLocation = app_path
        shortcut.save()
        print(f"Shortcut created at: {shortcut_path}")
    except Exception as e:
        print(f"Failed to add to startup: {e}")
        raise

def remove_from_startup(shortcut_name="WootRat.lnk"):
    """
    Remove the application from the Windows startup folder.

    Args:
        shortcut_name (str): The name of the shortcut file.

    Raises:
        Exception: If the shortcut removal fails.
    """
    try:
        shortcut_path = get_shortcut_path(shortcut_name)
        if os.path.exists(shortcut_path):
            os.remove(shortcut_path)
            print(f"Shortcut removed from: {shortcut_path}")
        else:
            print(f"Shortcut does not exist: {shortcut_path}")
    except Exception as e:
        print(f"Failed to remove from startup: {e}")
        raise
