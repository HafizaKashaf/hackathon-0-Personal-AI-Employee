@echo off
REM Personal AI Employee - Complete System (Continuous Mode)
REM Both Watcher and Orchestrator run automatically every 30 seconds

echo ========================================
echo  Personal AI Employee - Continuous Mode
echo ========================================
echo.
echo Watcher: Checks Inbox/ every 30 seconds
echo Orchestrator: Checks Needs_Action/ every 30 seconds
echo.
echo Both processes will run continuously...
echo Press Ctrl+C in each window to stop
echo.

cd /d "%~dp0"

REM Start File System Watcher
echo [1/2] Starting File System Watcher...
start "AI Employee - Watcher" cmd /k "python filesystem_watcher.py"

timeout /t 2 /nobreak >nul

REM Start Orchestrator (Continuous Mode - 30 seconds)
echo [2/2] Starting Orchestrator (continuous, 30s interval)...
start "AI Employee - Orchestrator" cmd /k "python orchestrator.py qwen --continuous 30"

echo.
echo ========================================
echo  Both processes started!
echo ========================================
echo.
echo - Watcher: Monitors Inbox/ for new files
echo - Orchestrator: Processes Needs_Action/ every 30 seconds
echo.
echo To stop: Close both terminal windows
echo.
echo Drop files in AI_Employee_Vault\Inbox\ to begin!
echo.
pause
