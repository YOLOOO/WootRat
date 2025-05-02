import sys
import threading
from PyQt5.QtWidgets import QApplication
from utils.settings import load_settings
from utils.paths import get_qss_path
from gui.woot_rat_gui import SettingsWindow
from logic.woot_rat_engine import WootRatEngine

woot_rat_thread = None
stop_event = threading.Event()


def start_woot_rat_thread():
    """
    Start the WootRat thread with the necessary settings.
    """
    if stop_event is None:
        raise ValueError("stop_event must be initialized before starting the thread.")
    
    settings = load_settings()
    engine = WootRatEngine()
    args = (
        settings["mouse_sensitivity"],
        settings["scroll_sensitivity"], 
        settings["deadzone"],
        settings["curve_factor"],
        settings["key_mapping"],
        settings["y_sensitivity_adjustment"],
        stop_event
    )
    global woot_rat_thread
    woot_rat_thread = threading.Thread(target=engine.run, args=args, daemon=True)
    woot_rat_thread.start()
    return woot_rat_thread


def cleanup_threads():
    """
    Signal the thread to stop and wait for it to finish.
    """
    global woot_rat_thread
    stop_event.set()
    if woot_rat_thread and woot_rat_thread.is_alive():
        try:
            woot_rat_thread.join(timeout=5)
        except Exception as e:
            print(f"Failed to join WootRat thread: {e}")


def restart_woot_rat_thread():
    """
    Gracefully stop the current thread and start a new one with updated settings.
    """
    global woot_rat_thread, stop_event

    # Stop the current thread
    if stop_event:
        stop_event.set()
    if woot_rat_thread and woot_rat_thread.is_alive():
        try:
            woot_rat_thread.join(timeout=5)
            print("Previous WootRat thread stopped successfully.")
        except Exception as e:
            print(f"Failed to stop WootRat thread: {e}")

    # Reset the stop_event for the new thread
    stop_event = threading.Event()

    # Start a new thread with updated settings
    start_woot_rat_thread()

if __name__ == "__main__":
    try:
        start_woot_rat_thread()
        app = QApplication(sys.argv)

        qss_path = get_qss_path()
        with open(qss_path, "r") as f:
            app.setStyleSheet(f.read())

        window = SettingsWindow()
        window.show()
        sys.exit(app.exec_())
    finally:
        cleanup_threads()
