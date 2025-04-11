#!/bin/bash

# Redirect all errors to a log file
log_file="$(dirname "$0")/translate_gui.log"
exec 2>>"$log_file"

# Get the selected text from the clipboard
selected_text=$(xclip -o -selection primary)

# Check if text is selected
if [[ -z "$selected_text" ]]; then
    zenity --error --text="No text selected. Please select some text and try again."
    echo "$(date): No text selected." >> "$log_file"
    exit 1
fi

# Allow the user to choose an action
form_output=$(zenity --list --title="Hazmel Translator" \
    --text="Choose an action:\n\nText: <b> $selected_text </b>" \
    --column="Actions" \
    "Translate" "Pronounce" "AI" "Image" \
    --width=1000 --height=300)

# Check if the user canceled the form
if [[ -z "$form_output" ]]; then
    zenity --info --text="No action selected. Exiting."
    echo "$(date): No action selected by the user." >> "$log_file"
    exit 0
fi

# URL-encode the selected text
encoded_text=$(echo "$selected_text" | sed 's/ /%20/g') || { 
    zenity --error --text="Failed to URL-encode the text."
    echo "$(date): Failed to URL-encode the text." >> "$log_file"
    exit 1
}

# Run translate.sh with the appropriate flag based on the user's choice
case "$form_output" in
    "Translate")
        bash "$(dirname "$0")/translate.sh" --text="$encoded_text" || {
            echo "$(date): Error running translate.sh with Translate option." >> "$log_file"
        }
        ;;
    "Pronounce")
        bash "$(dirname "$0")/translate.sh" --pronounce --text="$encoded_text" || {
            echo "$(date): Error running translate.sh with Pronounce option." >> "$log_file"
        }
        ;;
    "AI")
        default_model="grok"
        
        template=$(zenity --list \
            --title="AI Query Options" \
            --text="Choose a template for the AI query (Model: $default_model):" \
            --radiolist \
            --column="Select" --column="Template" \
            FALSE "1 - Explain this" \
            FALSE "2 - What does this mean" \
            FALSE "3 - Translate this in Arabic" \
            TRUE  "4 - Just the selected text" \
            --width=500 --height=300)

        # Check if the user canceled the form
        if [[ -z "$ai_form_output" ]]; then
            zenity --info --text="No options selected. Exiting."
            echo "$(date): No options selected in AI form." >> "$log_file"
            exit 0
        fi

        # Parse the form output
        template_number=$(echo "$ai_form_output" | cut -d'|' -f1 | cut -d' ' -f1)
        model_choice=$(echo "$ai_form_output" | cut -d'|' -f2)

        # Run translate.sh with the selected template and model
        bash "$(dirname "$0")/translate.sh" --ai --template "$template_number" --model "$model_choice" --text="$encoded_text" || {
            echo "$(date): Error running translate.sh with AI option (template: $template_number, model: $model_choice)." >> "$log_file"
        }
        ;;
    "Image")
        bash "$(dirname "$0")/translate.sh" --image --text="$encoded_text" || {
            echo "$(date): Error running translate.sh with Image option." >> "$log_file"
        }
        ;;
    *)
        zenity --info --text="No valid action selected. Exiting."
        echo "$(date): Invalid action selected: $form_output." >> "$log_file"
        exit 0
        ;;
esac