#!/bin/bash
path="$(dirname "$(realpath "$0")")"

# Define the path to the virtual environment and the Python script
VENV_PATH="$path/frontend/frontend_venv"  # Replace with the actual path to your virtual environment
SCRIPT_PATH="$path/frontend/translate_gui.py"
LOG_FILE="$path/translate_gui_launch.log"

# Redirect stdout and stderr to the log file
exec > >(tee -a "$LOG_FILE") 2>&1

# Log the start of the script
echo "[$(date)] Starting translate_gui_launch.sh"

# Check if the virtual environment exists
if [[ ! -d "$VENV_PATH" ]]; then
    echo "[$(date)] Error: Virtual environment not found at $VENV_PATH"
    exit 1
fi

# Activate the virtual environment
source "$VENV_PATH/bin/activate"

# Check if activation was successful
if [[ $? -ne 0 ]]; then
    echo "[$(date)] Error: Failed to activate the virtual environment."
    exit 1
fi

# Log the activation of the virtual environment
echo "[$(date)] Virtual environment activated."

# Run the Python script
python3 "$SCRIPT_PATH"

# Check if the script ran successfully
if [[ $? -ne 0 ]]; then
    echo "[$(date)] Error: Failed to run the Python script."
    deactivate
    exit 1
fi

# Log the successful execution of the script
echo "[$(date)] Python script executed successfully."

# Deactivate the virtual environment after the script finishes
deactivate

# Log the deactivation of the virtual environment
echo "[$(date)] Virtual environment deactivated."