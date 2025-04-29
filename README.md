# WootRat
Mouse emulation for Wooting keyboards.

WootRat is a Python-based application that allows users to control mouse movement using analog inputs from a Wooting keyboard. It includes a GUI for configuring settings and a precompiled executable for non-programmers.

Why? Because I just hate mice.... #Python

## Features
- Based on Wooting analog SDK.
- Smooth mouse movement using analog inputs.
- Configurable sensitivity (movement and scroll), deadzone, and curve factor.
- Dampened Y axis for better control.
- Multiple key mapping options (Arrow Keys, WASD, F13-F16).
- Easy-to-use GUI for settings.

## How to Use
### For Non-Programmers
1. Download the `WootRatGui.exe` file from the `dist/` folder.
2. Double-click the `.exe` file to launch the application.
3. Configure your settings in the GUI and start using WootRat.

The WootRatGui is a settings window. When it starts, WootRat becomes active.
This window must remain active during mouse emulation.
When you close the window the mouse emulation will be disabled and you will need to restart it to use it again.

The use-case is to simply start the application window and start mousing. Whenever you tweak values and press the 'Save Settings' button in the settings window, the values are stored in the settings file. However, WootRat needs to be restarted to access them, as it only reads these settings at startup. You will need to restart the application for the changes to take effect.

The buttons F17 and F18 will always be your scroll buttons (up and down), regardless of the other configuration you choose.

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
Yes, this probably works on these platforms. But if you are on these platforms you have to follow the guide below.

## Build Executable from Source
1. Install pyinstaller:
```bash
pip install pyinstaller
```
2. Navigate to repo src dir.
```bash
cd WootRat/src
```
3. Initial build command:
```bash
pyinstaller --onefile --noconsole --add-binary "wooting_analog_sdk.dll;." --add-data "WootRat.png;icon" --add-data "WootRat.ico;ico" --add-data "style.qss;." --add-data "settings.json;." --icon "WootRat.ico" WootRatGui.py
```

This will build the executable in the '/dist' directory now created in the '/src' directory. It will also create the '.spec' file which make rebuilding a breeze. When the build is done, you are free to rename the '/dist' folder to whatever makes sense and place it wherever you like. The application will run inside this folder only.

4. Rebuild from source using '.spec' file
```bash
pyinstaller WootRatGui.spec
```

That's it! Have fun and make it your own.

### Folder Structure
- `src/`: Contains the source code and Wooting SDK DLL file.
- `dist/`: Contains the precompiled executable for non-programmers.
- `settings.json`: Default settings file.
- `requirements.txt`: Python dependencies.
- `LICENSE`: MIT License.

# Prerequisites
- A Wooting keyboard with at least WASD, arrow keys, or F13-F16 mapped using Wootility.
- For maximum mouse emulation, configure mouse button mapping in Wootility.
- Mapp F17 and F18 for the scroll functionality.
- Python 3.8 or higher (for programmers).

# Important Notes
This project is a proof of concept (POC) and is provided as-is. It is not actively maintained and is intended for use until Wooting adds native emulation support to Wootility and their firmware.
