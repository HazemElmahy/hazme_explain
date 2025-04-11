#!/bin/bash


# Define the path to the script being tested
script_path="$(dirname "$0")/translate.sh"

# Mock clipboard content
mock_clipboard="Hello, world!"

# Mock xclip to simulate clipboard content
mock_xclip() {
    echo "$mock_clipboard"
}

# Replace xclip with the mock function
alias xclip=mock_xclip

# Test cases
echo "Running tests for translate.sh..."

# Test 1: Pronounce
echo "Test 1: Pronounce"
output=$(bash "$script_path" --pronounce)
if [[ "$output" == *"https://www.google.com/search?q=pronounce+Hello%2C%20world%21"* ]]; then
    echo "Test 1 passed!"
else
    echo "Test 1 failed!"
fi

# Test 2: AI with default template
echo "Test 2: AI with default template"
output=$(bash "$script_path" --ai)
if [[ "$output" == *"https://chat.openai.com/?q=Hello%2C%20world%21"* ]]; then
    echo "Test 2 passed!"
else
    echo "Test 2 failed!"
fi

# Test 3: AI with template 1
echo "Test 3: AI with template 1"
output=$(bash "$script_path" --ai --template 1)
if [[ "$output" == *"https://chat.openai.com/?q=explain%20this%20%22Hello%2C%20world%21%22"* ]]; then
    echo "Test 3 passed!"
else
    echo "Test 3 failed!"
fi

# Test 4: AI with template 2
echo "Test 4: AI with template 2"
output=$(bash "$script_path" --ai --template 2)
if [[ "$output" == *"https://chat.openai.com/?q=what%20does%20this%20mean%20%22Hello%2C%20world%21%22"* ]]; then
    echo "Test 4 passed!"
else
    echo "Test 4 failed!"
fi

# Test 5: AI with template 3
echo "Test 5: AI with template 3"
output=$(bash "$script_path" --ai --template 3)
if [[ "$output" == *"https://chat.openai.com/?q=translate%20this%20in%20arabic%20%22Hello%2C%20world%21%22"* ]]; then
    echo "Test 5 passed!"
else
    echo "Test 5 failed!"
fi

# Test 6: AI with invalid template
echo "Test 6: AI with invalid template"
output=$(bash "$script_path" --ai --template 99)
if [[ "$output" == *"https://chat.openai.com/?q=%22Hello%2C%20world%21%22"* ]]; then
    echo "Test 6 passed!"
else
    echo "Test 6 failed!"
fi

# Test 7: AI with model gemini
echo "Test 7: AI with model gemini"
output=$(bash "$script_path" --ai --template 1 --model gemini)
if [[ "$output" == *"https://gemini.google.com/?q=explain%20this%20%22Hello%2C%20world%21%22"* ]]; then
    echo "Test 7 passed!"
else
    echo "Test 7 failed!"
fi

# Test 8: AI with model grok
echo "Test 8: AI with model grok"
output=$(bash "$script_path" --ai --template 1 --model grok)
if [[ "$output" == *"https://grok.meta.com/?q=explain%20this%20%22Hello%2C%20world%21%22"* ]]; then
    echo "Test 8 passed!"
else
    echo "Test 8 failed!"
fi

# Test 9: Image search
echo "Test 9: Image search"
output=$(bash "$script_path" --image)
if [[ "$output" == *"https://www.google.com/search?tbm=isch&q=Hello%2C%20world%21"* ]]; then
    echo "Test 9 passed!"
else
    echo "Test 9 failed!"
fi

echo "All tests completed!"