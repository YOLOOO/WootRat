import ctypes
import os
from pynput.mouse import Controller
import time

# Load the Wooting Analog SDK from the current directory
sdk_path = os.path.join(os.path.dirname(__file__), "wooting_analog_sdk.dll")
if not os.path.exists(sdk_path):
    raise FileNotFoundError(f"SDK not found at {sdk_path}")

wooting_sdk = ctypes.CDLL(sdk_path)

# Define the return type and argument types for the initialization function
wooting_sdk.wooting_analog_initialise.restype = ctypes.c_int

# Initialize the SDK
result = wooting_sdk.wooting_analog_initialise()

# Check the result of initialization
if result < 0:
    raise RuntimeError(f"Failed to initialize Wooting Analog SDK. Error code: {result}")
else:
    print(f"Wooting Analog SDK initialized successfully. Devices found: {result}")

# Check if the SDK is initialized
wooting_sdk.wooting_analog_is_initialised.restype = ctypes.c_bool
is_initialized = wooting_sdk.wooting_analog_is_initialised()
print(f"SDK is initialized: {is_initialized}")

# Define the return type for reading analog values
wooting_sdk.wooting_analog_read_analog.restype = ctypes.c_float
wooting_sdk.wooting_analog_read_analog.argtypes = [ctypes.c_ushort]

mouse = Controller()

# Keycodes for WASD
KEY_W = 0x1A
KEY_A = 0x04
KEY_S = 0x16
KEY_D = 0x07

# Keycodes for Arrow Keys
KEY_UP    = 0x52    
KEY_LEFT  = 0x50  
KEY_DOWN  = 0x51  
KEY_RIGHT = 0x4F 

# Keycodes for F13-F16
KEY_F13 = 0x68
KEY_F14 = 0x69
KEY_F15 = 0x6A
KEY_F16 = 0x6B

# Additional F keys
KEY_F17 = 0x6C
KEY_F18 = 0x6D

def process_input(raw_value=None, deadzone=None, curve_factor=None):

    if raw_value < deadzone:
        return 0.0
    
    adj_value = (raw_value - deadzone) / (1.0 - deadzone)
    curved = pow(adj_value, curve_factor)

    return curved

def run_woot_rat(sensitivity_m=None, sensitivity_s=None, deadzone=None, curve_factor=None, mouse_active=True, key_mapping=None):

    match key_mapping:
        case "Arrow Keys":
            current_up = KEY_UP
            current_down = KEY_DOWN
            current_left = KEY_LEFT
            current_right = KEY_RIGHT
            current_scroll_up = KEY_F17
            current_scroll_down = KEY_F18
        case "WASD Keys":
            current_up = KEY_W
            current_down = KEY_S
            current_left = KEY_A
            current_right = KEY_D
            current_scroll_up = KEY_F17
            current_scroll_down = KEY_F18
        case "F13-F16 Keys":
            current_up = KEY_F13
            current_down = KEY_F15
            current_left = KEY_F14
            current_right = KEY_F16
            current_scroll_up = KEY_F17
            current_scroll_down = KEY_F18
        case _:
            current_up = KEY_F13
            current_down = KEY_F15
            current_left = KEY_F14
            current_right = KEY_F16
            current_scroll_up = KEY_F17
            current_scroll_down = KEY_F18

    while mouse_active:
        dx = 0.0
        dy = 0.0
        scroll = 0.0  # Initialize scroll to 0.0

        # Read analog values for each key
        value_up = wooting_sdk.wooting_analog_read_analog(current_up)
        value_left = wooting_sdk.wooting_analog_read_analog(current_left)
        value_down = wooting_sdk.wooting_analog_read_analog(current_down)
        value_right = wooting_sdk.wooting_analog_read_analog(current_right)

        # Read analog values for scrolling keys (if defined)
        if current_scroll_up and current_scroll_down:
            value_scroll_up = wooting_sdk.wooting_analog_read_analog(current_scroll_up)
            value_scroll_down = wooting_sdk.wooting_analog_read_analog(current_scroll_down)
        else:
            value_scroll_up = 0.0
            value_scroll_down = 0.0

        # Apply deadzone and calculate movement
        if value_up > deadzone:
            dy -= process_input(value_up, deadzone, curve_factor) * sensitivity_m
        if value_down > deadzone:
            dy += process_input(value_down, deadzone, curve_factor) * sensitivity_m
        if value_left > deadzone:
            dx -= process_input(value_left, deadzone, curve_factor) * sensitivity_m
        if value_right > deadzone:
            dx += process_input(value_right, deadzone, curve_factor) * sensitivity_m

        # Apply deadzone and calculate scrolling
        if value_scroll_up > deadzone:
            scroll += process_input(value_scroll_up, deadzone, curve_factor) * sensitivity_s
        if value_scroll_down > deadzone:
            scroll -= process_input(value_scroll_down, deadzone, curve_factor) * sensitivity_s

        # Move the mouse
        if dx or dy:
            mouse.move(dx, dy)

        # Scroll the mouse
        if scroll:
            mouse.scroll(0, scroll)

        # Avoid excessive CPU usage
        time.sleep(0.01)