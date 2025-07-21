#!/bin/bash

# MiniZipper Package Publishing Script

set -e

echo "🚀 Starting MiniZipper package publishing process..."

# Check if we're in the right directory
if [ ! -f "setup.py" ]; then
    echo "❌ Error: setup.py not found. Please run this script from the project root."
    exit 1
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info/

# Install build tools
echo "📦 Installing build tools..."
python -m pip install --upgrade build twine

# Build package
echo "🔨 Building package..."
python -m build

# Check package
echo "✅ Checking package..."
python -m twine check dist/*

# Ask user which repository to publish to
echo ""
echo "📋 Choose publishing destination:"
echo "1) TestPyPI (for testing)"
echo "2) PyPI (production)"
echo "3) Both"
read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo "🚀 Publishing to TestPyPI..."
        python -m twine upload --repository testpypi dist/*
        ;;
    2)
        echo "🚀 Publishing to PyPI..."
        python -m twine upload dist/*
        ;;
    3)
        echo "🚀 Publishing to TestPyPI first..."
        python -m twine upload --repository testpypi dist/*
        echo "🚀 Publishing to PyPI..."
        python -m twine upload dist/*
        ;;
    *)
        echo "❌ Invalid choice. Exiting."
        exit 1
        ;;
esac

echo "✅ Package published successfully!"
echo "📦 Package files:"
ls -la dist/
