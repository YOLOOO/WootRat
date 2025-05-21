import threading
from utils.settings import (
    load_settings, DIRECTION_LABELS, KEYCODES,
    default_settings, VALUE_LABELS
    )
from logic.woot_rat_engine import WootRatEngine

woot_rat_thread = None
stop_event = threading.Event()


def assemble_key_mapping_from_settings(settings):
    """
    Assemble a key mapping dictionary for the engine: label -> keycode
    """
    try:
        return {
            label: KEYCODES[settings[label]] if isinstance(settings[label], str) else settings[label]
            for label in DIRECTION_LABELS
        }
    except KeyError as e:
        print(f"Error assembling key mapping: {e}")
        # Fallback to defaults
        return {
            label: KEYCODES[default_settings[label]] if isinstance(default_settings[label], str) else default_settings[label]
            for label in DIRECTION_LABELS
        }


def start_woot_rat_thread():
    """
    Start the WootRat thread with the necessary settings.
    """
    global woot_rat_thread, stop_event

    if stop_event is None:
        raise ValueError("stop_event must be initialized before starting the thread.")

    settings = load_settings()
    engine = WootRatEngine()

    key_mapping = assemble_key_mapping_from_settings(settings)

    args = (
        settings[VALUE_LABELS[0]],
        settings[VALUE_LABELS[1]],
        settings[VALUE_LABELS[2]],
        settings[VALUE_LABELS[3]],
        settings[VALUE_LABELS[4]],
        settings[VALUE_LABELS[5]],
        settings[VALUE_LABELS[6]],
        key_mapping,
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

    settings = load_settings()
    engine = WootRatEngine()

    # If no key_mapping is passed, assemble from settings
    if key_mapping is None:
        key_mapping = assemble_key_mapping_from_settings(settings)

    args = (
        settings[VALUE_LABELS[0]],
        settings[VALUE_LABELS[1]],
        settings[VALUE_LABELS[2]],
        settings[VALUE_LABELS[3]],
        settings[VALUE_LABELS[4]],
        settings[VALUE_LABELS[5]],
        settings[VALUE_LABELS[6]],
        key_mapping,
        stop_event
    )
    woot_rat_thread = threading.Thread(target=engine.run, args=args, daemon=True)
    woot_rat_thread.start()
    print("New WootRat thread started with key mapping:", key_mapping)
