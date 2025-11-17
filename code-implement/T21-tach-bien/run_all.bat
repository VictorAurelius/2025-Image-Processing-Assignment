@echo off
REM Run All Edge Detection Assignments
REM This script executes all 10 edge detection assignments sequentially

setlocal enabledelayedexpansion

REM Get script directory
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

REM Print header
echo =================================================================
echo Edge Detection Assignment - Running All Tests
echo =================================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    exit /b 1
)

REM Check if sample images exist, if not generate them
if not exist "input\sample-images" (
    echo Sample images not found. Generating them...
    python input\generate_samples.py
    echo.
)

REM Counter for success/failure
set /a total=10
set /a success=0
set /a failed=0

REM Assignment definitions (folder:script:image)
set "assignments[0]=bai-1-edge-detectors:compare.py:building.jpg"
set "assignments[1]=bai-2-document-scanning:scan.py:doc.jpg"
set "assignments[2]=bai-3-lane-detection:detect.py:road.jpg"
set "assignments[3]=bai-4-defect-detection:detect.py:surface.jpg"
set "assignments[4]=bai-5-coin-counting:count.py:coins.jpg"
set "assignments[5]=bai-6-product-cropping:crop.py:product.jpg"
set "assignments[6]=bai-7-crack-detection:detect.py:surface_crack.jpg"
set "assignments[7]=bai-8-leaf-measurement:measure.py:leaf.jpg"
set "assignments[8]=bai-9-object-measurement:measure.py:measure.jpg"
set "assignments[9]=bai-10-deskewing:deskew.py:receipt.jpg"

REM Run each assignment
for /l %%i in (0,1,9) do (
    set /a num=%%i+1

    REM Parse assignment info
    for /f "tokens=1,2,3 delims=:" %%a in ("!assignments[%%i]!") do (
        set "folder=%%a"
        set "script=%%b"
        set "image=%%c"
    )

    echo -----------------------------------------------------------------
    echo [!num!/%total%] Running: !folder!
    echo -----------------------------------------------------------------

    REM Check if folder exists
    if not exist "!folder!" (
        echo Error: Folder !folder! not found
        set /a failed+=1
        echo.
        goto :continue
    )

    REM Check if script exists
    if not exist "!folder!\!script!" (
        echo Error: Script !script! not found in !folder!
        set /a failed+=1
        echo.
        goto :continue
    )

    REM Check if input image exists
    set "input_path=input\sample-images\!image!"
    if not exist "!input_path!" (
        echo Error: Input image !image! not found
        set /a failed+=1
        echo.
        goto :continue
    )

    REM Run the script
    python "!folder!\!script!" "!input_path!"
    if errorlevel 1 (
        echo X Failed
        set /a failed+=1
    ) else (
        echo √ Success
        set /a success+=1
    )

    echo.

    :continue
)

REM Print summary
echo =================================================================
echo Summary
echo =================================================================
echo Total:   %total%
echo Success: %success%
echo Failed:  %failed%
echo =================================================================

REM Exit with error if any test failed
if %failed% gtr 0 (
    exit /b 1
)

echo.
echo All assignments completed successfully!
echo Check the 'output' directory for results.
