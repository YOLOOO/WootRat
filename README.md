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
1. Download the latest release of `WootRatGui.exe` from the [Releases](https://github.com/YOLOOO/WootRat/releases) page on GitHub.
2. Unzip folder.
3. Double-click the `.exe` file to launch the application.
4. Configure your settings in the GUI and start using WootRat.

The WootRatGui is a settings window. When it starts, WootRat becomes active.
This window must remain active during mouse emulation.
When you close the window the mouse emulation will be disabled and you will need to restart it to use it again.

The use-case is to simply start the application window and start mousing. Whenever you tweak values and press the 'Save Settings' button in the settings window, the values are stored in the settings file. 

The buttons F17 and F18 will for now always be your scroll buttons (up and down), regardless of the other configuration you choose.

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
python src/main.py
```
### Mac or Linux?
Yes, this probably works on these platforms. But if you are on these platforms you have to follow the guide below. Work is currently ongoing making sure it will work.

## Build Executable from Source
1. Install pyinstaller:
```bash
pip install pyinstaller
```
2. Navigate to repo src dir.
```bash
cd WootRat/src
```
3. Build command:
```bash
pyinstaller woot_rat.spec
```

When the build is done, you are free to rename the '/dist' folder to whatever makes sense and place it wherever you like. The application will run inside this folder only.

That's it! Have fun and make it your own.

### Folder Structure
src/
- ├── gui/
- │   └── woot_rat_gui.py
- ├── logic/
- │   └── woot_rat_engine.py
- ├── resources/
- │   ├── woot_rat.ico
- │   ├── woot_rat.png
- │   └── wooting_analog_sdk.dll
- ├── utils/
- │   ├── paths.py
- │   ├── settings.py
- │   ├── style.qss
- │   └── settings.json
- └── main.py
- └── woot_rat.spec

# Prerequisites
- A Wooting keyboard with at least WASD, arrow keys, or F13-F16 mapped using Wootility.
- For maximum mouse emulation, configure mouse button mapping in Wootility.
- Mapp F17 and F18 for the scroll functionality.
- Python 3.8 or higher (for programmers).

# Important Notes
This project is a proof of concept (POC) and is provided as-is. It is not actively maintained and is intended for use until Wooting adds native emulation support to Wootility and their firmware.

### Why Does Windows Show a Warning When Running WootRatGui.exe?
When you download and run WootRatGui.exe, you may see a warning from Windows Defender SmartScreen. This happens because the application is not signed with a code-signing certificate. 
Rest assured, WootRat is safe to use. You can bypass the warning by clicking **More Info** and then **Run Anyway**.
I am not working on obtaining a code-signing certificate to remove this warning it will be present for the time being.

## When using Wootility
Since Wootility also wants to read the analog values from your connected keyboard it is required that you close WootRat before using Wootility otherwise the keyboard will not be able to connect.
If this happens close WootRat and connect again to Wootility. 
