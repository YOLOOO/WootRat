import os

def get_launch_agent_path(name):
    """
    Get the path to the LaunchAgents .plist file for the given application name.

    Args:
        name (str): The name of the application.

    Returns:
        str: The full path to the .plist file.
    """
    return os.path.expanduser(f"~/Library/LaunchAgents/{name}.plist")

def add_to_startup(app_path, name):
    """
    Add the application to the macOS LaunchAgents folder.

    Args:
        app_path (str): The path to the application executable.
        name (str): The name of the application.

    Raises:
        Exception: If the .plist file cannot be created.
    """
    try:
        plist_path = get_launch_agent_path(name)
        plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>Label</key>
    <string>{name}</string>
    <key>ProgramArguments</key>
    <array>
      <string>{app_path}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
  </dict>
</plist>
"""
        os.makedirs(os.path.dirname(plist_path), exist_ok=True)
        with open(plist_path, "w") as f:
            f.write(plist_content)
        os.chmod(plist_path, 0o644)  # Ensure the file has the correct permissions
        print(f"LaunchAgent entry created at: {plist_path}")
    except Exception as e:
        print(f"Failed to add to startup: {e}")
        raise

def remove_from_startup(name):
    """
    Remove the application from the macOS LaunchAgents folder.

    Args:
        name (str): The name of the application.

    Raises:
        Exception: If the .plist file cannot be removed.
    """
    try:
        plist_path = get_launch_agent_path(name)
        if os.path.exists(plist_path):
            os.remove(plist_path)
            print(f"LaunchAgent entry removed from: {plist_path}")
        else:
            print(f"LaunchAgent entry does not exist: {plist_path}")
    except Exception as e:
        print(f"Failed to remove from startup: {e}")
        raise
