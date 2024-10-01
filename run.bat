@echo off
REM Run the Flask application from the current directory
start python app.py

REM Wait for a few seconds to ensure the app starts before opening the browser
timeout /t 1 /nobreak >nul

REM Open the app in the default web browser
start http://127.0.0.1:5000

pause