@echo off
set PYTHONIOENCODING=utf-8
cd /d "C:\Users\wanji\OneDrive\Desktop\HouseHunter"
echo [%DATE% %TIME%] Starting app >> run_app.log
venv\Scripts\python.exe app.py >> run_app.log 2>&1
echo [%DATE% %TIME%] Exited with %ERRORLEVEL% >> run_app.log
