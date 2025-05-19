import threading
from utils.settings import load_settings
from logic.woot_rat_engine import WootRatEngine

woot_rat_thread = None
stop_event = threading.Event()


def start_woot_rat_thread():
    """
    Start the WootRat thread with the necessary settings.
    """
    global woot_rat_thread, stop_event

    if stop_event is None:
        raise ValueError("stop_event must be initialized before starting the thread.")

    settings = load_settings()
    engine = WootRatEngine()

    # Assemble the key mapping from individual key configurations
    key_mapping = {
        "Up": settings["key_mouse_up"],
        "Down": settings["key_mouse_down"],
        "Left": settings["key_mouse_left"],
        "Right": settings["key_mouse_right"],
        "Scroll Up": settings["key_scroll_up"],
        "Scroll Down": settings["key_scroll_down"],
        "Scroll Right": settings["key_scroll_right"],
        "Scroll Left": settings["key_scroll_left"]
    }

    args = (
        settings["mouse_sensitivity"],
        settings["scroll_sensitivity"],
        settings["deadzone"],
        settings["curve_factor"],
        key_mapping,
        settings["y_sensitivity_adjustment"],
        stop_event
    )
    woot_rat_thread = threading.Thread(target=engine.run, args=args, daemon=True)
    woot_rat_thread.start()
    print("WootRat thread started.")
    return woot_rat_thread


def cleanup_threads():
    """
    Signal the thread to stop and wait for it to finish.
    """
    global woot_rat_thread, stop_event

    stop_event.set()
    if woot_rat_thread and woot_rat_thread.is_alive():
        try:
            woot_rat_thread.join(timeout=5)
            print("WootRat thread stopped successfully.")
        except Exception as e:
            print(f"Failed to join WootRat thread: {e}")


def restart_woot_rat_thread(key_mapping=None):
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
    settings = load_settings()
    engine = WootRatEngine()

    # Ensure key_mapping is not None
    if key_mapping is None:
        print("Error: Key mapping is None. Using default key mapping.")
        key_mapping = {
            "Up": "Arrow Up",
            "Down": "Arrow Down",
            "Left": "Arrow Left",
            "Right": "Arrow Right",
            "Scroll Up": "Page Up",
            "Scroll Down": "Page Down",
            "Scroll Right": "End",
            "Scroll Left": "Home"
        }

    args = (
        settings["mouse_sensitivity"],
        settings["scroll_sensitivity"],
        settings["deadzone"],
        settings["curve_factor"],
        key_mapping,
        settings["y_sensitivity_adjustment"],
        stop_event
    )
    woot_rat_thread = threading.Thread(target=engine.run, args=args, daemon=True)
    woot_rat_thread.start()
    print("New WootRat thread started with key mapping:", key_mapping)
