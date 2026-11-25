@echo off
REM Windows variant of scripts/supervisor.sh (requires the claude CLI on PATH). Stop: create state\STOP
cd /d %~dp0\..
:loop
findstr /C:"\"status\": \"FINISHED\"" state\agent_state.json >nul && goto :eof
if exist state\STOP goto :eof
echo %date% %time% starting agent >> logs\supervisor.log
claude -p "Read HANDOFF.md and MASTER_PROMPT.md, verify state with python scripts/status.py, then continue from NEXT ACTION. Do not restart finished work. Do not ask me questions." --dangerously-skip-permissions >> logs\supervisor.log 2>&1
timeout /t 900 /nobreak >nul
goto loop
