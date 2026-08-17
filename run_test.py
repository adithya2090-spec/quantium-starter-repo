#!/bin/bash

# 1. Activate the project virtual environment
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
else
    echo "Error: Virtual environment not found at .venv/"
    exit 1
fi

# 2. Execute the test suite using pytest
pytest test_app.py

# Capture the exit code of pytest
EXIT_CODE=$?

# 3. Return exit code 0 if all tests passed, or 1 if something went wrong
if [ $EXIT_CODE -eq 0 ]; then
    echo "All tests passed successfully!"
    exit 0
else
    echo "Tests failed with exit code $EXIT_CODE."
    exit 1
fi