@echo off
REM Setup and test script for n8n Railway deployment

echo ====================================
echo n8n Railway Deployment - Quick Setup
echo ====================================
echo.

echo Installing Python dependencies...
python -m pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install dependencies
    exit /b 1
)

echo.
echo ====================================
echo Running Ruff Linter...
echo ====================================
python -m ruff check src/ tests/
if %ERRORLEVEL% NEQ 0 (
    echo WARNING: Linting issues found
)

echo.
echo ====================================
echo Running Tests...
echo ====================================
python -m pytest tests/ -v --cov=src --cov-report=term-missing
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Tests failed
    exit /b 1
)

echo.
echo ====================================
echo Setup Complete!
echo ====================================
echo.
echo Next steps:
echo 1. Copy .env.example to .env and configure
echo 2. Push to GitHub
echo 3. Connect to Railway
echo 4. Add PostgreSQL service in Railway
echo 5. Set environment variables in Railway
echo.
