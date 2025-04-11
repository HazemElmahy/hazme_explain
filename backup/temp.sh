#!/bin/bash

# Get the selected text from the clipboard
selected_text=$(xclip -o -selection primary)

# Check if text is selected
if [[ -z "$selected_text" ]]; then
    zenity --error --text="No text selected. Please select some text and try again."
    exit 1
fi

# Allow the user to edit the selected text and choose an action
form_output=$(zenity --forms --title="Translate GUI" \
    --text="Select action to do:" \
    --add-entry="Text" \
    --add-list="Action" \
    --list-values="Translate|Pronounce|AI|Image" \
    --separator="|" \
    --icon-name="applications-accessories" \
    --width=400 --height=300)

# Check if the user canceled the form
if [[ -z "$form_output" ]]; then
    zenity --info --text="No action selected. Exiting."
    exit 0
fi

# Parse the form output
edited_text=$(echo "$form_output" | cut -d'|' -f1)
choice=$(echo "$form_output" | cut -d'|' -f2)

# URL-encode the edited text
encoded_text=$(echo "$edited_text" | sed 's/ /%20/g') || { zenity --error --text="Failed to URL-encode the text."; exit 1; }

# Run translate.sh with the appropriate flag based on the user's choice
case "$choice" in
    "Translate")
        bash "$(dirname "$0")/translate.sh" --text="$encoded_text"
        ;;
    "Pronounce")
        bash "$(dirname "$0")/translate.sh" --pronounce --text="$encoded_text"
        ;;
    "AI")
        bash "$(dirname "$0")/translate.sh" --ai --text="$encoded_text"
        ;;
    "Image")
        bash "$(dirname "$0")/translate.sh" --image --text="$encoded_text"
        ;;
    *)
        zenity --info --text="No valid action selected. Exiting."
        exit 0
        ;;
esac