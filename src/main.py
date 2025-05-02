import sys
import threading
from PyQt5.QtWidgets import QApplication
from utils.paths import get_qss_path
from gui.woot_rat_gui import SettingsWindow
from utils.thread_manager import start_woot_rat_thread, cleanup_threads

woot_rat_thread = None
stop_event = threading.Event()

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
