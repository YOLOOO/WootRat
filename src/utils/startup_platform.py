import platform
from utils.startup_windows import add_to_startup as windows_add_to_startup, remove_from_startup as windows_remove_from_startup
from utils.startup_mac import add_to_startup as mac_add_to_startup, remove_from_startup as mac_remove_from_startup
from utils.startup_linux import add_to_startup as linux_add_to_startup, remove_from_startup as linux_remove_from_startup

PLATFORM = platform.system()

def add_to_startup(app_path, shortcut_name="WootRat"):
    """
    Add the application to the startup based on the platform.

    Args:
        app_path (str): The path to the application executable.
        shortcut_name (str): The name of the shortcut or startup entry.

    Raises:
        NotImplementedError: If the platform is unsupported.
    """
    if PLATFORM == "Windows":
        windows_add_to_startup(app_path, shortcut_name + ".lnk")
    elif PLATFORM == "Darwin":
        mac_add_to_startup(app_path, shortcut_name)
    elif PLATFORM == "Linux":
        linux_add_to_startup(app_path, shortcut_name)
    else:
        raise NotImplementedError(f"Unsupported OS: {PLATFORM}")

def remove_from_startup(shortcut_name="WootRat"):
    """
    Remove the application from the startup based on the platform.

    Args:
        shortcut_name (str): The name of the shortcut or startup entry.

    Raises:
        NotImplementedError: If the platform is unsupported.
    """
    if PLATFORM == "Windows":
        windows_remove_from_startup(shortcut_name + ".lnk")
    elif PLATFORM == "Darwin":
        mac_remove_from_startup(shortcut_name)
    elif PLATFORM == "Linux":
        linux_remove_from_startup(shortcut_name)
    else:
        raise NotImplementedError(f"Unsupported OS: {PLATFORM}")
