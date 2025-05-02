#!/bin/bash

echo "[+] Setting up Sentra directory structure..."

# Create directories
mkdir -p sentra/core/engine
mkdir -p sentra/plugins
mkdir -p sentra/config
mkdir -p tests

# Core files
touch sentra/cli.py
touch sentra/__main__.py
touch sentra/core/scan.py
touch sentra/core/analyze.py
touch sentra/core/report.py
touch sentra/core/__init__.py
touch sentra/core/engine/__init__.py
touch sentra/core/engine/scanner_engine.py
touch sentra/core/engine/nmap_engine.py

# Config
touch sentra/config/settings.py

# Plugins
touch sentra/plugins/__init__.py

# Tests
touch tests/test_scan.py
touch tests/test_analyze.py
touch tests/test_report.py

# Root-level Python package files
touch setup.py
touch requirements.txt

# .gitignore (append if missing)
if ! grep -q "__pycache__/" .gitignore 2>/dev/null; then
  cat <<EOF >> .gitignore
__pycache__/
*.pyc
.env
*.log
EOF
fi

echo "[+] Structure created. Here's what we have now:"
tree sentra/
