@echo off
setlocal

REM Check if the Python script exists in the current directory
set script_name=visualize_dataset_captions_v2.py

if exist %script_name% (
    echo Running %script_name%...
    python %script_name%
) else (
    echo %script_name% not found in the current directory.
)

endlocal
pause
