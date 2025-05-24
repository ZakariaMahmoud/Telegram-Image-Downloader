#!/bin/bash

echo "Telegram Image Downloader"
echo "========================="

if [ ! -f ".env" ]; then
    echo "Error: .env file not found"
    echo "Please run: python setup.py"
    exit 1
fi

if [ "$1" = "download" ]; then
    echo "Starting image download..."
    python telegram_downloader.py
elif [ "$1" = "setup" ]; then
    echo "Running setup..."
    python setup.py
else
    echo "Usage:"
    echo "  ./run.sh setup    - Setup the project"
    echo "  ./run.sh download - Download images from Telegram"
    echo ""
    echo "Example:"
    echo "  ./run.sh download"
fi
