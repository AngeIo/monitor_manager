# Monitor Configuration Manager

Monitor Configuration Manager is a Python script designed to help users save, load, and list monitor configurations on Linux systems. It interacts with the `kscreen-doctor` command-line tool to retrieve and apply display configurations. This script is particularly useful for users who frequently switch between different monitor setups and want to easily save and reapply configurations.

## Features

- **Save** the current monitor configuration to a profile.
- **Load** a saved monitor configuration and apply it.
- **List** all available profiles.
- **Remove** a saved profile.
- Handles display rotation, resolution, scale, position, and priority settings.

## Installation

Download the project
```bash
git clone https://github.com/AngeIo/monitor_manager.git
cd monitor_manager
```
Then choose between:

Using traditionnal `venv`
```bash
mkdir -p $HOME/.venvs
python3 -m venv $HOME/.venvs/monitormanager
source $HOME/.venvs/monitormanager/bin/activate
pip install setuptools
python setup.py install
```

Or

(Recommended) Using `pipx`
```bash
pipx install .
```

## Usage

### Command-Line Interface

The script can be run from the terminal with the following syntax:

```bash
monitormanager <command> [<profile_name>]
```

### Commands

- **Save a Profile**

    Save the current monitor configuration to a profile.

    ```bash
    monitormanager save <profile_name> | -s <profile_name>
    ```

- **Load a Profile**

    Load and apply a saved monitor configuration.

    ```bash
    monitormanager load <profile_name> | -l <profile_name>
    ```

- **List Profiles**

    List all saved profiles.

    ```bash
    monitormanager list | -L
    ```

- **Remove a Profile**

    Remove a saved profile from disk.

    ```bash
    monitormanager remove <profile_name> | -r <profile_name>
    ```

### Example Commands

- Save a new profile called `work`:

    ```bash
    monitormanager save work
    ```

- Load and apply the `work` profile:

    ```bash
    monitormanager load work
    ```

- List all available profiles:

    ```bash
    monitormanager list
    ```

- Remove the `work` profile:

    ```bash
    monitormanager remove work
    ```

## Script Details

### Functions

- **`get_kscreen_doctor_json()`**: Runs `kscreen-doctor` and parses the JSON output.
- **`parse_to_kscreen_commands(data)`**: Converts parsed JSON data to `kscreen-doctor` commands.
- **`save_profile(profile_name)`**: Saves the current configuration to a profile.
- **`load_profile(profile_name)`**: Loads and applies a saved configuration.
- **`list_profiles()`**: Lists all saved profiles in the backup directory.
- **`print_usage()`**: Displays usage instructions for the script.

## Configuration Backup Directory

Profiles are stored in `~/.monitor_config_profiles`. The script creates this directory automatically if it does not already exist.

## Error Handling

- The script will raise errors if `kscreen-doctor` is not installed or accessible.
- JSON parsing errors are handled with a `ValueError`.
- Other command or subprocess errors will raise a `RuntimeError`.

## License

This project is licensed under the GPLv2 License. See the [LICENSE](LICENSE) file for details.

## Contributions

Feel free to contribute by opening issues or pull requests. All contributions are welcome!

## Acknowledgments

This script relies on the `kscreen-doctor` tool provided by KDE for managing display settings.
