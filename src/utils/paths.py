import os
import sys

def get_resource_path(relative_path):
    """
    Get the absolute path to a resource, works for development and PyInstaller.
    """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

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