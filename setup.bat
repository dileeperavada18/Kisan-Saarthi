@echo off
echo 🌾 Kisan Call Centre - Setup Script
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo ✅ Python found
python --version
echo.

REM Install dependencies
echo 📦 Installing Python dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed successfully
echo.

REM Setup .env file
if not exist .env (
    echo 📝 Creating .env file...
    copy .env.example .env
    echo ✅ .env file created
    echo.
    echo ⚠️  IMPORTANT: Please edit .env and add your API keys:
    echo    - GOOGLE_API_KEY (from https://makersuite.google.com/app/apikey^)
    echo    - ELEVENLABS_API_KEY (from https://elevenlabs.io/app/settings/api-keys^)
) else (
    echo ℹ️  .env file already exists, skipping...
)

echo.
echo ✅ Setup complete!
echo.
echo Next steps:
echo 1. Edit .env and add your API keys
echo 2. Run: python app.py
echo 3. Open index.html in your browser
echo.
pause
