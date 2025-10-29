@echo off
REM Run all exercises for T1: Biểu diễn và Thu nhận Ảnh (Windows)

echo ==========================================
echo T1: BIỂU DIỄN VÀ THU NHẬN ẢNH
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

REM Get script directory
cd /d "%~dp0"
echo Working directory: %CD%
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Virtual environment not found. Creating...
    python -m venv venv
    call venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    echo Virtual environment created and dependencies installed.
    echo.
) else (
    call venv\Scripts\activate.bat
    echo Virtual environment activated.
    echo.
)

echo Starting all exercises...
echo.

REM Run all exercises
call :run_script "bai-tap-1-camera-storage\calculator.py" "Bai tap 1"
call :run_script "bai-tap-2-quantization\quantize_scan.py" "Bai tap 2"
call :run_script "bai-tap-3-bitplane-slicing\bitplane.py" "Bai tap 3"
call :run_script "bai-tap-4-connectivity\robot_path.py" "Bai tap 4"
call :run_script "bai-tap-5-color-space\skin_detection.py" "Bai tap 5"

call :run_script "lab-1-quantization-eval\evaluate.py" "Lab 1"
call :run_script "lab-2-zooming-shrinking\resize.py" "Lab 2"
call :run_script "lab-3-measure-circle\measure.py" "Lab 3"
call :run_script "lab-4-connected-components\labeling.py" "Lab 4"
call :run_script "lab-5-image-quality\assess.py" "Lab 5"

echo ==========================================
echo ALL EXERCISES COMPLETED!
echo ==========================================
echo.
echo Output files are saved in the 'output' folder.
echo.
pause
exit /b 0

:run_script
echo ==========================================
echo Running: %~2
echo ==========================================
python %~1
echo.
echo Completed: %~2
echo.
goto :eof
