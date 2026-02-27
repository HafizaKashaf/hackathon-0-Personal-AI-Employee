@echo off
REM Personal AI Employee - Bronze Tier Startup Script
REM This script starts both the File Watcher and Orchestrator

echo ========================================
echo  Personal AI Employee - Bronze Tier
echo ========================================
echo.

cd /d "%~dp0AI_Employee_Vault\scripts"

echo Starting File System Watcher...
start "AI Employee Watcher" cmd /k "python filesystem_watcher.py .."

timeout /t 2 /nobreak >nul

echo Starting Orchestrator in continuous mode...
start "AI Employee Orchestrator" cmd /k "python orchestrator.py .. --continuous 60"

echo.
echo Both processes started!
echo - Watcher: Monitors Inbox folder every 30 seconds
echo - Orchestrator: Processes Needs_Action every 60 seconds
echo.
echo To stop: Close the terminal windows or press Ctrl+C in each
echo.
echo Drop files into AI_Employee_Vault\Inbox\ to begin!
echo.
pause
