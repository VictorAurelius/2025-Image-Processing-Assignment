@echo off
REM Script chay tat ca 10 bai tap T79 - Phan vung anh

echo ============================================================
echo CHAY TAT CA BAI TAP T79 - PHAN VUNG ANH
echo ============================================================
echo.

REM Kiem tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Loi: Khong tim thay Python
    pause
    exit /b 1
)

REM Cai dat dependencies
echo Kiem tra dependencies...
pip install -q -r requirements.txt
echo Dependencies da san sang
echo.

REM Chay tung bai
echo ------------------------------------------------------------
echo BAI 1: Global Thresholding
echo ------------------------------------------------------------
cd bai-1-global-thresholding
python threshold.py
cd ..
echo.

echo ------------------------------------------------------------
echo BAI 2: Otsu
echo ------------------------------------------------------------
cd bai-2-otsu
python threshold.py
cd ..
echo.

echo ------------------------------------------------------------
echo BAI 3: Adaptive Thresholding
echo ------------------------------------------------------------
cd bai-3-adaptive-thresholding
python threshold.py
cd ..
echo.

echo ------------------------------------------------------------
echo BAI 4: Bayes-ML
echo ------------------------------------------------------------
cd bai-4-bayes-ml
python threshold.py
cd ..
echo.

echo ------------------------------------------------------------
echo BAI 5: Edge + Hough
echo ------------------------------------------------------------
cd bai-5-edge-hough
python detect.py
cd ..
echo.

echo ------------------------------------------------------------
echo BAI 6: Region Growing
echo ------------------------------------------------------------
cd bai-6-region-growing
python grow.py
cd ..
echo.

echo ------------------------------------------------------------
echo BAI 7: Split-Merge
echo ------------------------------------------------------------
cd bai-7-split-merge
python segment.py
cd ..
echo.

echo ------------------------------------------------------------
echo BAI 8: K-means
echo ------------------------------------------------------------
cd bai-8-kmeans
python cluster.py
cd ..
echo.

echo ------------------------------------------------------------
echo BAI 9: Motion Segmentation
echo ------------------------------------------------------------
cd bai-9-motion-segmentation
python segment.py
cd ..
echo.

echo ------------------------------------------------------------
echo BAI 10: Watershed
echo ------------------------------------------------------------
cd bai-10-watershed
python segment.py
cd ..
echo.

echo ============================================================
echo HOAN THANH TAT CA!
echo ============================================================
pause
