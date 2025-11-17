@echo off
REM ================================================================================
REM Script chay tat ca bai tap T61 - Xu ly hinh thai (Windows)
REM ================================================================================

chcp 65001 > nul
echo ================================================================================
echo CHẠY TẤT CẢ BÀI TẬP T61 - XỬ LÝ HÌNH THÁI
echo ================================================================================

REM Kiem tra Python
python --version > nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python chua duoc cai dat!
    pause
    exit /b 1
)

echo [OK] Python:
python --version

REM Cai dat requirements
echo.
echo Kiem tra dependencies...
if not exist "venv" (
    echo [WARNING] Virtual environment chua ton tai. Tao moi...
    python -m venv venv
)

call venv\Scripts\activate.bat

echo Cai dat requirements...
pip install -q -r requirements.txt

echo.
echo ================================================================================
echo BẮT ĐẦU CHẠY CÁC BÀI TẬP
echo ================================================================================

set success_count=0
set fail_count=0
set total=9

REM Bai 1
echo.
echo --------------------------------------------------------------------------------
echo [Bai 1/9] Lam sach van ban quet - Opening
echo --------------------------------------------------------------------------------
cd bai-1-opening
python denoise.py
if errorlevel 1 (
    echo [X] Bai 1: That bai
    set /a fail_count+=1
) else (
    echo [OK] Bai 1: Thanh cong
    set /a success_count+=1
)
cd ..

REM Bai 2
echo.
echo --------------------------------------------------------------------------------
echo [Bai 2/9] Lap lo va noi net - Closing
echo --------------------------------------------------------------------------------
cd bai-2-closing
python fill_holes.py
if errorlevel 1 (
    echo [X] Bai 2: That bai
    set /a fail_count+=1
) else (
    echo [OK] Bai 2: Thanh cong
    set /a success_count+=1
)
cd ..

REM Bai 3
echo.
echo --------------------------------------------------------------------------------
echo [Bai 3/9] Trich bien - Morphological Gradient
echo --------------------------------------------------------------------------------
cd bai-3-gradient
python extract_edges.py
if errorlevel 1 (
    echo [X] Bai 3: That bai
    set /a fail_count+=1
) else (
    echo [OK] Bai 3: Thanh cong
    set /a success_count+=1
)
cd ..

REM Bai 4
echo.
echo --------------------------------------------------------------------------------
echo [Bai 4/9] Dem dong xu - Watershed
echo --------------------------------------------------------------------------------
cd bai-4-watershed
python separate.py
if errorlevel 1 (
    echo [X] Bai 4: That bai
    set /a fail_count+=1
) else (
    echo [OK] Bai 4: Thanh cong
    set /a success_count+=1
)
cd ..

REM Bai 5
echo.
echo --------------------------------------------------------------------------------
echo [Bai 5/9] Phan doan ky tu
echo --------------------------------------------------------------------------------
cd bai-5-character-segmentation
python segment.py
if errorlevel 1 (
    echo [X] Bai 5: That bai
    set /a fail_count+=1
) else (
    echo [OK] Bai 5: Thanh cong
    set /a success_count+=1
)
cd ..

REM Bai 6
echo.
echo --------------------------------------------------------------------------------
echo [Bai 6/9] Do duong kinh hat
echo --------------------------------------------------------------------------------
cd bai-6-particle-measurement
python measure.py
if errorlevel 1 (
    echo [X] Bai 6: That bai
    set /a fail_count+=1
) else (
    echo [OK] Bai 6: Thanh cong
    set /a success_count+=1
)
cd ..

REM Bai 7
echo.
echo --------------------------------------------------------------------------------
echo [Bai 7/9] Xoa pixel thua - Pruning
echo --------------------------------------------------------------------------------
cd bai-7-pruning
python prune.py
if errorlevel 1 (
    echo [X] Bai 7: That bai
    set /a fail_count+=1
) else (
    echo [OK] Bai 7: Thanh cong
    set /a success_count+=1
)
cd ..

REM Bai 8
echo.
echo --------------------------------------------------------------------------------
echo [Bai 8/9] Tach tien canh
echo --------------------------------------------------------------------------------
cd bai-8-foreground-extraction
python extract.py
if errorlevel 1 (
    echo [X] Bai 8: That bai
    set /a fail_count+=1
) else (
    echo [OK] Bai 8: Thanh cong
    set /a success_count+=1
)
cd ..

REM Bai 9
echo.
echo --------------------------------------------------------------------------------
echo [Bai 9/9] Khu nen khong dong deu - Top-hat/Black-hat
echo --------------------------------------------------------------------------------
cd bai-9-background-removal
python remove.py
if errorlevel 1 (
    echo [X] Bai 9: That bai
    set /a fail_count+=1
) else (
    echo [OK] Bai 9: Thanh cong
    set /a success_count+=1
)
cd ..

REM Tong ket
echo.
echo ================================================================================
echo KẾT QUẢ TỔNG HỢP
echo ================================================================================
echo Tong so bai tap: %total%
echo Thanh cong: %success_count%
echo That bai: %fail_count%

if %fail_count% EQU 0 (
    echo.
    echo [OK] TAT CA BAI TAP DA CHAY THANH CONG!
    echo ================================================================================
) else (
    echo.
    echo [!] CO %fail_count% BAI TAP THAT BAI. VUI LONG KIEM TRA LAI!
    echo ================================================================================
)

pause
