import sys
import threading
from PyQt5.QtWidgets import QApplication
from utils.settings import load_settings
from utils.paths import get_qss_path
from gui.woot_rat_gui import SettingsWindow
from logic.woot_rat import run_woot_rat

woot_rat_thread = None
stop_event = threading.Event()

def start_woot_rat_thread():
    """
    Start the WootRat thread with the necessary settings.
    """
    settings = load_settings()
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
    woot_rat_thread = threading.Thread(target=run_woot_rat, args=args, daemon=True)
    woot_rat_thread.start()

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
