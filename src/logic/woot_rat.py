import ctypes
import os
from utils.paths import get_sdk_path
from pynput.mouse import Controller
import time

# Load the Wooting Analog SDK from the current directory
sdk_path = get_sdk_path()
if not os.path.exists(sdk_path):
    print(sdk_path)
    raise FileNotFoundError(f"SDK not found at {sdk_path}")

wooting_sdk = ctypes.CDLL(sdk_path)

# Initialize the SDK
if wooting_sdk.wooting_analog_initialise() < 0:
    raise RuntimeError("Failed to initialize Wooting Analog SDK.")
else:
    print(f"Wooting Analog SDK initialized successfully.")

# Check if the SDK is initialized
if not wooting_sdk.wooting_analog_is_initialised():
    raise RuntimeError("Wooting Analog SDK is not initialized.")

# Define the return type for reading analog values
wooting_sdk.wooting_analog_read_analog.restype = ctypes.c_float
wooting_sdk.wooting_analog_read_analog.argtypes = [ctypes.c_ushort]

mouse = Controller()

# Keycodes for WASD
KEY_W, KEY_A, KEY_S, KEY_D = 0x1A, 0x04, 0x16, 0x07

# Keycodes for Arrow Keys
KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT = 0x52, 0x51, 0x50, 0x4F

# Keycodes for F13-F16
KEY_F13, KEY_F14, KEY_F15, KEY_F16 = 0x68, 0x69, 0x6A, 0x6B

# Scroll keys F17-F20
KEY_F17, KEY_F18, KEY_F19, KEY_F20 = 0x6C, 0x6D, 0x6E, 0x6F


def process_input(raw_value, deadzone, curve_factor):
    """
    Process raw analog input with deadzone and curve factor.
    """
    if raw_value < deadzone:
        return 0.0
    adj_value = (raw_value - deadzone) / (1.0 - deadzone)
    return pow(adj_value, curve_factor)


def run_woot_rat(sensitivity_m=15.0, sensitivity_s=0.5, deadzone=0.1, curve_factor=2.0, key_mapping="F13-F16 Keys", y_sensitivity_adjustment=0.0, stop_event=False):
    """
    Main function to handle mouse movement and scrolling based on Wooting keyboard input.
    """
    # Map key bindings based on key_mapping
    key_bindings = {
        "Arrow Keys": (KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_F17, KEY_F18, KEY_F19, KEY_F20),
        "WASD Keys": (KEY_W, KEY_S, KEY_A, KEY_D, KEY_F17, KEY_F18, KEY_F19, KEY_F20),
        "F13-F16 Keys": (KEY_F13, KEY_F15, KEY_F14, KEY_F16, KEY_F17, KEY_F18, KEY_F19, KEY_F20),
    }
    current_up, current_down, current_left, current_right, current_scroll_up, current_scroll_down, current_scroll_right, current_scroll_left = key_bindings.get(
        key_mapping, key_bindings["F13-F16 Keys"]
    )

    while not stop_event.is_set():
        dx = dy = scroll_y = scroll_x = 0.0

        # Read analog values for movement keys
        value_up = wooting_sdk.wooting_analog_read_analog(current_up)
        value_down = wooting_sdk.wooting_analog_read_analog(current_down)
        value_left = wooting_sdk.wooting_analog_read_analog(current_left)
        value_right = wooting_sdk.wooting_analog_read_analog(current_right)

        # Read analog values for scrolling keys
        value_scroll_up    = wooting_sdk.wooting_analog_read_analog(current_scroll_up)
        value_scroll_down  = wooting_sdk.wooting_analog_read_analog(current_scroll_down)
        value_scroll_right = wooting_sdk.wooting_analog_read_analog(current_scroll_right)
        value_scroll_left  = wooting_sdk.wooting_analog_read_analog(current_scroll_left)

        # Calculate movement
        dy -= process_input(value_up, deadzone, curve_factor) * sensitivity_m * (1 - y_sensitivity_adjustment)
        dy += process_input(value_down, deadzone, curve_factor) * sensitivity_m * (1 - y_sensitivity_adjustment)
        dx -= process_input(value_left, deadzone, curve_factor) * sensitivity_m
        dx += process_input(value_right, deadzone, curve_factor) * sensitivity_m

        # Calculate scrolling
        scroll_x += process_input(value_scroll_left, deadzone, curve_factor) * sensitivity_s
        scroll_x -= process_input(value_scroll_right, deadzone, curve_factor) * sensitivity_s
        scroll_y += process_input(value_scroll_up, deadzone, curve_factor) * sensitivity_s
        scroll_y -= process_input(value_scroll_down, deadzone, curve_factor) * sensitivity_s

        # Perform mouse actions
        if dx or dy:
            mouse.move(dx, dy)
        if scroll_x or scroll_y:
            mouse.scroll(scroll_x, scroll_y)

        # Avoid excessive CPU usage
        time.sleep(0.01)