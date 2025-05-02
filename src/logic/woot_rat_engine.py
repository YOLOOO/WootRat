import ctypes
import os
from utils.paths import get_sdk_path
from pynput.mouse import Controller
import time

KEYCODES = {
    # Alphanumeric keys
    "A": 0x04, "B": 0x05, "C": 0x06, "D": 0x07, "E": 0x08, "F": 0x09, "G": 0x0A,
    "H": 0x0B, "I": 0x0C, "J": 0x0D, "K": 0x0E, "L": 0x0F, "M": 0x10, "N": 0x11,
    "O": 0x12, "P": 0x13, "Q": 0x14, "R": 0x15, "S": 0x16, "T": 0x17, "U": 0x18,
    "V": 0x19, "W": 0x1A, "X": 0x1B, "Y": 0x1C, "Z": 0x1D,
    "1": 0x1E, "2": 0x1F, "3": 0x20, "4": 0x21, "5": 0x22, "6": 0x23, "7": 0x24,
    "8": 0x25, "9": 0x26, "0": 0x27,

    # Function keys
    "F1": 0x3A, "F2": 0x3B, "F3": 0x3C, "F4": 0x3D, "F5": 0x3E, "F6": 0x3F,
    "F7": 0x40, "F8": 0x41, "F9": 0x42, "F10": 0x43, "F11": 0x44, "F12": 0x45,
    "F13": 0x68, "F14": 0x69, "F15": 0x6A, "F16": 0x6B, "F17": 0x6C, "F18": 0x6D,
    "F19": 0x6E, "F20": 0x6F,

    # Arrow keys
    "Arrow Up": 0x52, "Arrow Down": 0x51, "Arrow Left": 0x50, "Arrow Right": 0x4F,

    # Modifier keys
    "Shift": 0xE1, "Ctrl": 0xE0, "Alt": 0xE2, "Caps Lock": 0x39, "Tab": 0x2B, "Esc": 0x29,

    # Punctuation and symbols
    "`": 0x35, "-": 0x2D, "=": 0x2E, "[": 0x2F, "]": 0x30, "\\": 0x31,
    ";": 0x33, "'": 0x34, ",": 0x36, ".": 0x37, "/": 0x38,

    # Space and Enter
    "Space": 0x2C, "Enter": 0x28, "Backspace": 0x2A, "Delete": 0x4C, "Insert": 0x49,

    # Other special keys
    "Home": 0x4A, "End": 0x4D, "Page Up": 0x4B, "Page Down": 0x4E,
    "Print Screen": 0x46, "Pause": 0x48
}

mouse = Controller()

class WootRatEngine:
    """
    WootRatEngine handles the interaction with the Wooting Analog SDK and processes
    analog input to control mouse movement and scrolling.
    """

    def __init__(self):
        """
        Initialize the WootRatEngine by loading and initializing the Wooting Analog SDK.
        """
        self.sdk_path = get_sdk_path()
        self.sdk = self.load_sdk()
        self.init_sdk()

    def load_sdk(self):
        """
        Load the Wooting Analog SDK from the specified path.

        Returns:
            ctypes.CDLL: The loaded SDK library.

        Raises:
            FileNotFoundError: If the SDK file is not found at the specified path.
        """
        if not os.path.exists(self.sdk_path):
            raise FileNotFoundError(f"SDK not found at {self.sdk_path}")
        return ctypes.CDLL(self.sdk_path)

    def init_sdk(self):
        """
        Initialize the Wooting Analog SDK and configure its function signatures.

        Raises:
            RuntimeError: If the SDK fails to initialize.
        """
        if self.sdk.wooting_analog_initialise() < 0:
            raise RuntimeError("Failed to initialize Wooting Analog SDK.")
        self.sdk.wooting_analog_read_analog.restype = ctypes.c_float
        self.sdk.wooting_analog_read_analog.argtypes = [ctypes.c_ushort]

    def process_input(self, raw_value, deadzone, curve_factor):
        """
        Process raw analog input by applying a deadzone and curve factor.

        Args:
            raw_value (float): The raw analog input value (0.0 to 1.0).
            deadzone (float): The deadzone threshold (0.0 to 1.0).
            curve_factor (float): The curve factor to apply for non-linear scaling.

        Returns:
            float: The processed input value after applying the deadzone and curve factor.

        Raises:
            ValueError: If the deadzone is not between 0.0 and 1.0 (exclusive) or if the curve factor is <= 0.
        """
        if deadzone < 0.0 or deadzone >= 1.0:
            raise ValueError("Deadzone must be between 0.0 and 1.0 (exclusive).")
        if curve_factor <= 0.0:
            raise ValueError("Curve factor must be greater than 0.0.")

        if raw_value < deadzone:
            return 0.0
        adj_value = (raw_value - deadzone) / (1.0 - deadzone)
        return pow(adj_value, curve_factor)

    def run(self, sensitivity_m=15.0, sensitivity_s=0.5, deadzone=0.1, curve_factor=2.0, key_mapping=None, y_sensitivity_adjustment=0.0, stop_event=None):
        """
        Main loop for processing analog input and controlling mouse movement and scrolling.

        Args:
            sensitivity_m (float): Sensitivity for mouse movement.
            sensitivity_s (float): Sensitivity for scrolling.
            deadzone (float): Deadzone threshold for analog input.
            curve_factor (float): Curve factor for non-linear scaling of input.
            key_mapping (dict): Dictionary mapping actions (e.g., "Up", "Down") to key names.
            y_sensitivity_adjustment (float): Adjustment factor for Y-axis sensitivity.
            stop_event (threading.Event): Event to signal the thread to stop.

        Raises:
            ValueError: If stop_event is not provided.
        """
        if stop_event is None:
            raise ValueError("A threading.Event object must be provided for stop_event.")

        # Map key names to keycodes
        keys = {action: KEYCODES[key_name] for action, key_name in key_mapping.items()}
        up = keys["Up"]
        down = keys["Down"]
        left = keys["Left"]
        right = keys["Right"]
        scrl_up = keys["Scroll Up"]
        scrl_down = keys["Scroll Down"]
        scrl_right = keys["Scroll Right"]
        scrl_left = keys["Scroll Left"]

        while not stop_event.is_set():
            try:
                dx = dy = scr_x = scr_y = 0.0

                # Read analog values for movement
                val_up = self.sdk.wooting_analog_read_analog(up)
                val_down = self.sdk.wooting_analog_read_analog(down)
                val_left = self.sdk.wooting_analog_read_analog(left)
                val_right = self.sdk.wooting_analog_read_analog(right)

                # Read analog values for scrolling
                val_scrl_up = self.sdk.wooting_analog_read_analog(scrl_up)
                val_scrl_down = self.sdk.wooting_analog_read_analog(scrl_down)
                val_scrl_right = self.sdk.wooting_analog_read_analog(scrl_right)
                val_scrl_left = self.sdk.wooting_analog_read_analog(scrl_left)

                # Process input for movement
                dy -= self.process_input(val_up, deadzone, curve_factor) * sensitivity_m * (1 - y_sensitivity_adjustment)
                dy += self.process_input(val_down, deadzone, curve_factor) * sensitivity_m * (1 - y_sensitivity_adjustment)
                dx -= self.process_input(val_left, deadzone, curve_factor) * sensitivity_m
                dx += self.process_input(val_right, deadzone, curve_factor) * sensitivity_m

                # Process input for scrolling
                scr_x += self.process_input(val_scrl_left, deadzone, curve_factor) * sensitivity_s
                scr_x -= self.process_input(val_scrl_right, deadzone, curve_factor) * sensitivity_s
                scr_y += self.process_input(val_scrl_up, deadzone, curve_factor) * sensitivity_s
                scr_y -= self.process_input(val_scrl_down, deadzone, curve_factor) * sensitivity_s

                # Apply movement and scrolling
                if dx or dy:
                    mouse.move(dx, dy)
                if scr_x or scr_y:
                    mouse.scroll(scr_x, scr_y)

            except Exception as e:
                print(f"Error in WootRatEngine.run: {e}")

            time.sleep(0.01)




