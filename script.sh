#!/bin/bash

echo "[+] Setting up Sentra directory structure..."

# Define directories
DIRS=("sentra/core/engine" "sentra/plugins" "sentra/config" "tests")

# Create directories
for dir in "${DIRS[@]}"; do
    mkdir -p "$dir" || { echo "Failed to create directory $dir"; exit 1; }
done

# Define files
FILES=(
    "sentra/cli.py"
    "sentra/__main__.py"
    "sentra/core/scan.py"
    "sentra/core/analyze.py"
    "sentra/core/report.py"
    "sentra/core/__init__.py"
    "sentra/core/engine/__init__.py"
    "sentra/core/engine/scanner_engine.py"
    "sentra/core/engine/nmap_engine.py"
    "sentra/config/settings.py"
    "sentra/plugins/__init__.py"
    "tests/test_scan.py"
    "tests/test_analyze.py"
    "tests/test_report.py"
    "setup.py"
    "requirements.txt"
)

# Create files if they don't exist
for file in "${FILES[@]}"; do
    [ ! -f "$file" ] && touch "$file"
done

# .gitignore (append if missing)
GITIGNORE_ENTRIES=("__pycache__/" "*.pyc" ".env" "*.log")
for entry in "${GITIGNORE_ENTRIES[@]}"; do
    grep -qxF "$entry" .gitignore || echo "$entry" >> .gitignore
done

# Check for tree command
if command -v tree &>/dev/null; then
    echo "[+] Structure created. Here's what we have now:"
    tree sentra/
else
    echo "[+] Structure created. Install 'tree' to view the directory structure."
fi
