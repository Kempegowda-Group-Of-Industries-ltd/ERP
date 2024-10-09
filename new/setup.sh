#!/bin/bash

# Print a message
echo "Setting up the project environment..."

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating a virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists. Skipping creation."
fi

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip to the latest version
echo "Upgrading pip..."
pip install --upgrade pip

# Install required packages
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Print success message
echo "Setup complete! Your environment is ready."

# Deactivate the virtual environment
deactivate

# Reminder to the user
echo "To activate the virtual environment in the future, run:"
echo "source venv/bin/activate"
