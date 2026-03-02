#!/bin/bash
# Setup script for AI Interview Coach

echo "Setting up AI Interview Coach..."

# Check if Python 3.12+ is available
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Please install Python 3.12 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
if [[ $(python3 -c "import sys; print(sys.version_info >= (3, 12))") != "True" ]]; then
    echo "Python version $PYTHON_VERSION is not 3.12+. Please upgrade to Python 3.12 or higher."
    exit 1
fi

# Check if virtual environment is available
if ! python3 -m venv --help &> /dev/null; then
    echo "Python venv module not available. Installing..."
    sudo apt-get update && sudo apt-get install python3-venv
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
else
    echo "Installing default dependencies..."
    pip install openai rich python-dotenv
fi

echo "Setup complete!"
echo "To run the AI Interview Coach, activate the virtual environment and run:"
echo "source .venv/bin/activate"
echo "python -m interview_coach"