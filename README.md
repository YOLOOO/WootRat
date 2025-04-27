# WootRat
Mouse emulation for Wooting keyboards.

WootRat is a Python-based application that allows users to control mouse movement using analog inputs from a Wooting keyboard. It includes a GUI for configuring settings and a precompiled executable for non-programmers.

Why? Because I just hate mice.... #Python

## Features
- Based on Wooting analog SDK
- Smooth mouse movement using analog inputs.
- Configurable sensitivity, deadzone, and curve factor.
- Multiple key mapping options (Arrow Keys, WASD, F13-F16).
- Easy-to-use GUI for settings.

## How to Use
### For Non-Programmers
1. Download the `WootRatGui.exe` file from the `dist/` folder.
2. Double-click the `.exe` file to launch the application.
3. Configure your settings in the GUI and start using WootRat.

The WootRatGui is a minimal settings window. When it starts, WootRat becomes active.
This window must remain active during mouse emulation.
When you close the window the mouse emulation will be disabled and you will need to restart it to use it again. So the use case here is that you start the application and minimize it. Whenever you tweak values and press the 'Save and Restart' button, the values are stored in the settings file. However, WootRat needs to be restarted to access them, as it only reads the settings at startup. This auto-restart feature works on Windows. Its behavior on other platforms is uncertain.

### For Programmers
1. Clone the repository: 
```bash
git clone https://github.com/YOLOOO/WootRat.git
cd WootRat
```
2.  Install dependencies:
```bash
pip install -r requirements.txt
```
3.  Launch the GUI:
```bash
python src/WootRatGui.py
```
### Mac or Linux?
Yes, this probably works on these platforms. However, you need to use PyInstaller on your system to create the executables. Ensure you include the Wooting SDK DLL.

### Folder Structure
- `src/`: Contains the source code and Wooting SDK DLL file.
- `dist/`: Contains the precompiled executable for non-programmers.
- `settings.json`: Default settings file.
- `requirements.txt`: Python dependencies.
- `LICENSE`: MIT License.

# Prerequisites
- A Wooting keyboard with at least WASD, arrow keys, or F13-F16 mapped using Wootility.
- For maximum mouse emulation, configure mouse button mapping in Wootility.
- Python 3.8 or higher (for programmers).

# Important Notes
To make this work, you need to have at least WASD, arrow keys, or F13-F16 mapped on your Wooting keyboard. It is recommended to configure these mappings using Wootility. For maximum mouse emulation, also use Wootility to map mouse buttons.

# Finally
This project is a proof of concept (POC) and is provided as-is. It is not actively maintained and is intended for use until Wooting adds native emulation support to Wootility.
