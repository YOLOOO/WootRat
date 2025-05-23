import sys
import os

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', relative_path)

def get_qss_path():
    """
    Get the path to the QSS stylesheet.
    """
    return os.path.join(os.path.dirname(__file__), "style.qss")

def get_sdk_path():
    """
    Get the path to the SDK directory.
    """
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "wooting_analog_sdk.dll")

def get_runtime_settings():
    """
    Get the path to runtime settings.
    """
    return os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "WootRat_settings.json")