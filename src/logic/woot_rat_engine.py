import ctypes
import os
from utils.paths import get_sdk_path
from pynput.mouse import Controller
import time

#
# The last three keycodes in mapping will always be F17-F20
#
KEYCODES = {
    "Arrow Keys":   [0x52, 0x51, 0x50, 0x4F, 0x6C, 0x6D, 0x6E, 0x6F],
    "WASD Keys":    [0x1A, 0x04, 0x16, 0x07, 0x6C, 0x6D, 0x6E, 0x6F],
    "F13-F16 Keys": [0x68, 0x69, 0x6A, 0x6B, 0x6C, 0x6D, 0x6E, 0x6F] 
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

    def run(self, sensitivity_m=15.0, sensitivity_s=0.5, deadzone=0.1, curve_factor=2.0, key_mapping="F13-F16 Keys", y_sensitivity_adjustment=0.0, stop_event=None):
        """
        Main loop for processing analog input and controlling mouse movement and scrolling.

        Args:
            sensitivity_m (float): Sensitivity for mouse movement.
            sensitivity_s (float): Sensitivity for scrolling.
            deadzone (float): Deadzone threshold for analog input.
            curve_factor (float): Curve factor for non-linear scaling of input.
            key_mapping (str): Key mapping to use for input (e.g., "F13-F16 Keys").
            y_sensitivity_adjustment (float): Adjustment factor for Y-axis sensitivity.
            stop_event (threading.Event): Event to signal the thread to stop.

        Raises:
            ValueError: If stop_event is not provided.
        """
        if stop_event is None:
            raise ValueError("A threading.Event object must be provided for stop_event.")

        keys = KEYCODES.get(key_mapping, KEYCODES["F13-F16 Keys"])
        (up, left, down, right, scrl_up, scrl_down, scrl_right, scrl_left) = keys 

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




