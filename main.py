import os
import subprocess
import json
import sys
import re

# Define the base backup directory for profiles
backup_dir = os.path.expanduser('~/.monitor_config_profiles')

def get_kscreen_doctor_json():
    """
    Fetches the JSON output from the kscreen-doctor command and returns it as a Python dictionary.

    Returns:
        dict: Parsed JSON output from kscreen-doctor.
    Raises:
        FileNotFoundError: If the kscreen-doctor command is not found.
        ValueError: If the output cannot be parsed as JSON.
        subprocess.SubprocessError: If an error occurs while running the command.
    """
    try:
        result = subprocess.run(
            ["kscreen-doctor", "--json"],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)

    except FileNotFoundError:
        raise FileNotFoundError("The 'kscreen-doctor' command is not installed or not in the PATH.")

    except json.JSONDecodeError:
        raise ValueError("Failed to parse JSON output from 'kscreen-doctor'.")

    except subprocess.SubprocessError as e:
        raise RuntimeError(f"An error occurred while running 'kscreen-doctor': {e}")

def parse_to_kscreen_commands(data):
    """
    Convert display configuration data into kscreen commands.

    Args:
        data (dict): Parsed JSON containing the display configuration data.

    Returns:
        list: A list of kscreen commands.
    """
    rotation_mapping = {
        1: "normal",
        2: "left",
        4: "inverted",
        8: "right"
    }

    commands = []
    for output in data.get("outputs", []):
        name = output.get("name")
        if output.get("enabled"):
            mode_id = output.get("currentModeId")
            pos_x = output["pos"].get("x", 0)
            pos_y = output["pos"].get("y", 0)
            scale = output.get("scale", 1.0)
            priority = output.get("priority", 0)  # Default priority to 0 if not provided

            mode = next((m for m in output.get("modes", []) if m["id"] == mode_id), None)
            if mode:
                resolution = f"{mode['size']['width']}x{mode['size']['height']}"
                refresh_rate = round(mode["refreshRate"])
                rotation = rotation_mapping.get(output.get("rotation"), "normal")

                command = (
                    f"kscreen-doctor output.{name}.enable "
                    f"output.{name}.mode.{resolution}@{refresh_rate} "
                    f"output.{name}.position.{pos_x},{pos_y} "
                    f"output.{name}.rotation.{rotation} "
                    f"output.{name}.scale.{scale} "
                    f"output.{name}.priority.{priority}"
                )
                commands.append(command)
        else:
            # Handle disabled outputs
            command = f"kscreen-doctor output.{name}.disable"
            commands.append(command)

    return commands


def save_profile(profile_name):
    """Save the current monitor configuration as a profile."""
    profile_path = os.path.join(backup_dir, f"{profile_name}.json")
    os.makedirs(backup_dir, exist_ok=True)

    try:
        kscreen_data = get_kscreen_doctor_json()
        with open(profile_path, 'w') as file:
            json.dump(kscreen_data, file, indent=4)
        print(f"Monitor configuration saved as profile: {profile_name}")
    except Exception as e:
        print(f"Error saving profile: {e}")

def load_profile(profile_name):
    """Load and apply a monitor configuration from a profile."""
    profile_path = os.path.join(backup_dir, f"{profile_name}.json")
    if not os.path.exists(profile_path):
        print(f"Profile '{profile_name}' not found.")
        return

    try:
        with open(profile_path, 'r') as file:
            kscreen_data = json.load(file)

        commands = parse_to_kscreen_commands(kscreen_data)
        for command in commands:
            subprocess.run(command, shell=True, check=True)
        print(f"Profile '{profile_name}' applied successfully.")

    except Exception as e:
        print(f"Error applying profile: {e}")

def list_profiles():
    """List all saved profiles."""
    if not os.path.exists(backup_dir):
        print("No profiles found.")
        return []

    profiles = os.listdir(backup_dir)
    if profiles:
        print("Available profiles:")
        for profile in profiles:
            print(f"- {profile.replace('.json', '')}")
    else:
        print("No profiles available.")
    return profiles

def print_usage():
    """Prints the usage information for the script."""
    print("Usage: monitormanager <command> [<profile_name>]")
    print("Commands:")
    print("  save <profile_name>  : Save current monitor configuration.")
    print("  load <profile_name>  : Load monitor configuration from a profile.")
    print("  list                 : List all saved profiles.")

def print_usage():
    """Prints the usage information for the script."""
    print("Usage: monitormanager <command> [<profile_name>]")
    print("Commands:")
    print("  save <profile_name>  | -s : Save current monitor configuration.")
    print("  load <profile_name>  | -l : Load monitor configuration from a profile.")
    print("  remove <profile_name> | -r : Remove a saved monitor configuration.")
    print("  list                  | -L : List all saved profiles.")

def main():
    """Main function to handle command-line arguments."""
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    command = sys.argv[1]
    profile_name = sys.argv[2] if len(sys.argv) > 2 else None

    # Mapping of commands and their abbreviations
    if command in ("save", "-s"):
        if not profile_name:
            print("Error: Missing profile name for 'save' command.")
            print("Usage: monitormanager save <profile_name>")
            sys.exit(1)
        save_profile(profile_name)

    elif command in ("load", "-l"):
        if not profile_name:
            print("Error: Missing profile name for 'load' command.")
            print("Usage: monitormanager load <profile_name>")
            sys.exit(1)
        load_profile(profile_name)

    elif command in ("remove", "-r"):
        if not profile_name:
            print("Error: Missing profile name for 'remove' command.")
            print("Usage: monitormanager remove <profile_name>")
            sys.exit(1)
        remove_profile(profile_name)

    elif command in ("list", "-L"):
        list_profiles()

    else:
        print(f"Error: Unknown command '{command}'.")
        print_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
