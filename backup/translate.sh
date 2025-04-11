#!/bin/bash

# Redirect all errors to the log file
log_file="$(dirname "$0")/translate.log"
exec 2>>"$log_file"

# Get the selected text from the clipboard
selected_text=$(xclip -o -selection primary)

# Notify the user of the selected text
notify-send "$selected_text"

# URL-encode the text
encoded_text=$(echo "$selected_text" | sed 's/ /%20/g') || { echo "$(date): Failed to URL-encode the text"; exit 1; }

# Determine the URL based on the argument
if [[ "$1" == "--pronounce" || "$1" == "-p" ]]; then
    url="https://www.google.com/search?q=pronounce+${encoded_text}"

elif [[ "$1" == "--ai" ]]; then
    # Default template
    question="$selected_text"

    # Check for the template flag
    if [[ "$2" == "--template" || "$2" == "-t" ]]; then
        case "$3" in
            1)
                question="explain this \"$selected_text\""
                ;;
            2)
                question="what does this mean \"$selected_text\""
                ;;
            3)
                question="translate this in arabic \"$selected_text\""
                ;;
            *)
                question="\"$selected_text\"" # Default to just the selected text
                ;;
        esac
    fi

    # Default model is chatgpt
    model="chatgpt"
    if [[ "$4" == "--model" || "$4" == "-m" ]]; then
        case "$5" in
            gemini)
                model="gemini"
                ;;
            grok)
                model="grok"
                ;;
            chatgpt)
                model="chatgpt"
                ;;
            *)
                echo "$(date): Invalid model choice. Defaulting to chatgpt." >> "$log_file"
                model="chatgpt"
                ;;
        esac
    fi

    # URL-encode the question
    encoded_question=$(echo "$question" | sed 's/ /%20/g')

    # Determine the URL based on the model
    case "$model" in
        gemini)
            url="https://gemini.google.com/?q=${encoded_question}"
            ;;
        grok)
            url="https://grok.meta.com/?q=${encoded_question}"
            ;;
        chatgpt)
            url="https://chat.openai.com/?q=${encoded_question}"
            ;;
    esac

elif [[ "$1" == "--image" || "$1" == "-i" ]]; then
    url="https://www.google.com/search?tbm=isch&q=${encoded_text}"

else
    url="https://translate.google.com/details?sl=en&tl=ar&text=${encoded_text}&op=translate"
    echo "URL: $url" >> "$log_file"
fi

# Open the determined URL in Firefox
firefox "$url" -P "main"