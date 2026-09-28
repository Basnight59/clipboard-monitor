"""
ProfAI Simple Installer Generator
==================================
Creates a working ProfAI installation with one click.

Usage: python simple_installer.py
"""

import os
from pathlib import Path

print("\n" + "="*60)
print("  ProfAI Simple Installer")
print("="*60 + "\n")

# Create directory
output = Path("profai-windows-installer")
output.mkdir(exist_ok=True)
print(f"✓ Created folder: {output}")

# Create install.bat
install_bat = output / "install.bat"
with open(install_bat, 'w') as f:
    f.write("""@echo off
echo ========================================
echo ProfAI Installation
echo ========================================
echo.

echo [1/7] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    pause
    exit /b 1
)
echo OK
echo.

echo [2/7] Creating directories...
if not exist "profai-backend" mkdir profai-backend
cd profai-backend
mkdir app 2>nul
mkdir app\\core 2>nul
mkdir app\\api 2>nul
mkdir app\\models 2>nul
mkdir app\\services 2>nul
echo OK
echo.

echo [3/7] Creating virtual environment...
python -m venv venv
call venv\\Scripts\\activate.bat
echo OK
echo.

echo [4/7] Upgrading pip...
python -m pip install --upgrade pip
echo OK
echo.

echo [5/7] Creating requirements.txt...
(
echo fastapi==0.109.0
echo uvicorn[standard]==0.27.0
echo python-multipart==0.0.6
echo psycopg2-binary==2.9.9
echo sqlalchemy==2.0.25
echo asyncpg==0.29.0
echo python-dotenv==1.0.0
echo pydantic==2.5.3
echo pydantic-settings==2.1.0
echo anthropic==0.18.1
echo openai==1.12.0
) > requirements.txt
echo OK
echo.

echo [6/7] Installing packages...
pip install -r requirements.txt
echo OK
echo.

echo [7/7] Creating files...
(
echo APP_NAME=ProfAI
echo DEBUG=True
echo ANTHROPIC_API_KEY=your-key-here
echo OPENAI_API_KEY=your-key-here
) > .env

(
echo from fastapi import FastAPI
echo app = FastAPI^(^)
echo @app.get^("/"^)
echo def root^(^):
echo     return {"status": "ok"}
) > app\\main.py

echo. > app\\__init__.py
echo. > app\\core\\__init__.py

(
echo @echo off
echo call venv\\Scripts\\activate.bat
echo uvicorn app.main:app --reload
) > run.bat

echo OK
echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo To start: run.bat
echo.
pause
""")

print(f"✓ Created: install.bat")

# Create run instructions
readme = output / "HOW_TO_RUN.txt"
with open(readme, 'w') as f:
    f.write("""ProfAI - How to Run
===================

STEP 1: Run the installer
   Double-click: install.bat
   Wait for it to finish

STEP 2: Start the server
   Go to: profai-backend folder
   Double-click: run.bat

STEP 3: Open browser
   Go to: http://localhost:8000

That's it!
""")

print(f"✓ Created: HOW_TO_RUN.txt")

print("\n" + "="*60)
print("  DONE!")
print("="*60)
print(f"\nFolder: {output.absolute()}")
print("\nNext:")
print("  1. Go to folder above")
print("  2. Double-click: install.bat")
print("\n" + "="*60 + "\n")