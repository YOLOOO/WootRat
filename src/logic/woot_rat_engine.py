import ctypes
import os
from pynput.mouse import Controller
from utils.settings import KEYCODES, DIRECTION_LABELS
from utils.paths import get_sdk_path
import time
import math

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

    def process_input(self, raw_value, deadzone, curve_factor, outer_deadzone=1.0, curve_type="power"):
        """
        Process analog input with inner/outer deadzone and selectable curve type.

        Args:
            raw_value (float): Analog input (0.0 to 1.0)
            deadzone (float): Inner deadzone (0.0 to <1.0)
            curve_factor (float): Curve steepness (>0)
            outer_deadzone (float): Outer deadzone (>deadzone to 1.0)
            curve_type (str): "power", "log", "s_curve", or "linear"

        Returns:
            float: Processed value (0.0 to 1.0)
        """
        if not (0.0 <= deadzone < outer_deadzone <= 1.0):
            raise ValueError("Deadzone values must satisfy 0.0 <= deadzone < outer_deadzone <= 1.0")
        if curve_factor <= 0.0:
            raise ValueError("Curve factor must be greater than 0.0.")

        if raw_value < deadzone:
            return 0.0
        if raw_value > outer_deadzone:
            return 1.0

        # Normalize between deadzone and outer_deadzone
        adj_value = (raw_value - deadzone) / (outer_deadzone - deadzone)
        adj_value = max(0.0, min(adj_value, 1.0))  # Clamp

        # Apply curve
        if curve_type == "power":
            return math.pow(adj_value, curve_factor)
        elif curve_type == "log":
            # log1p(x) = log(1 + x), safe for x=0
            return math.log1p(curve_factor * adj_value) / math.log1p(curve_factor)
        elif curve_type == "s_curve":
            # S-curve (sigmoid), curve_factor controls steepness
            return 1 / (1 + math.exp(-curve_factor * (adj_value - 0.5)))
        elif curve_type == "linear":
            return adj_value
        else:
            raise ValueError(f"Unknown curve_type: {curve_type}")

    def run(self, sensitivity_m=15.0, sensitivity_s=0.5, y_sensitivity_adjustment=0.0, curve_factor=2.0, deadzone=0.1, outer_deadzone=1.0, curve_type='power', key_mapping=None, stop_event=None):
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
        keys = {
            action: KEYCODES[key_name] if isinstance(key_name, str) else key_name
            for action, key_name in key_mapping.items()
        }

        # Use DIRECTION_LABELS to extract the correct keys
        try:
            up = keys[DIRECTION_LABELS[0]]
            down = keys[DIRECTION_LABELS[1]]
            left = keys[DIRECTION_LABELS[2]]
            right = keys[DIRECTION_LABELS[3]]
            scrl_up = keys[DIRECTION_LABELS[4]]
            scrl_down = keys[DIRECTION_LABELS[5]]
            scrl_left = keys[DIRECTION_LABELS[6]]
            scrl_right = keys[DIRECTION_LABELS[7]]
        except KeyError as e:
            raise KeyError(f"Missing direction in key mapping: {e}")

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
                dy -= self.process_input(val_up, deadzone, curve_factor, outer_deadzone, curve_type) * sensitivity_m * (1 - y_sensitivity_adjustment)
                dy += self.process_input(val_down, deadzone, curve_factor, outer_deadzone, curve_type) * sensitivity_m * (1 - y_sensitivity_adjustment)
                dx -= self.process_input(val_left, deadzone, curve_factor, outer_deadzone, curve_type) * sensitivity_m
                dx += self.process_input(val_right, deadzone, curve_factor, outer_deadzone, curve_type) * sensitivity_m

                # Process input for scrolling
                scr_x += self.process_input(val_scrl_left, deadzone, curve_factor, outer_deadzone, curve_type) * sensitivity_s
                scr_x -= self.process_input(val_scrl_right, deadzone, curve_factor, outer_deadzone, curve_type) * sensitivity_s
                scr_y += self.process_input(val_scrl_up, deadzone, curve_factor, outer_deadzone, curve_type) * sensitivity_s
                scr_y -= self.process_input(val_scrl_down, deadzone, curve_factor, outer_deadzone, curve_type) * sensitivity_s

                # Apply movement and scrolling
                if dx or dy:
                    mouse.move(dx, dy)
                if scr_x or scr_y:
                    mouse.scroll(scr_x, scr_y)

            except Exception as e:
                print(f"Error in WootRatEngine.run: {e}")

            time.sleep(0.01)




