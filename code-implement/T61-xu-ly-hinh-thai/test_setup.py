"""
Test script để kiểm tra môi trường
"""

import sys

print("="*80)
print("KIỂM TRA MÔI TRƯỜNG T61 - XỬ LÝ HÌNH THÁI")
print("="*80)

print(f"\nPython version: {sys.version}")

# Kiểm tra các thư viện
libraries = [
    ('cv2', 'opencv-python'),
    ('numpy', 'numpy'),
    ('matplotlib', 'matplotlib'),
    ('scipy', 'scipy'),
    ('skimage', 'scikit-image')
]

print("\nKiểm tra thư viện:")
print("-"*80)

all_ok = True
for module_name, package_name in libraries:
    try:
        if module_name == 'cv2':
            import cv2
            version = cv2.__version__
        elif module_name == 'numpy':
            import numpy
            version = numpy.__version__
        elif module_name == 'matplotlib':
            import matplotlib
            version = matplotlib.__version__
        elif module_name == 'scipy':
            import scipy
            version = scipy.__version__
        elif module_name == 'skimage':
            import skimage
            version = skimage.__version__

        print(f"✓ {package_name:20s} version {version:15s} - OK")
    except ImportError as e:
        print(f"✗ {package_name:20s} - CHƯA CÀI ĐẶT")
        all_ok = False

print("-"*80)

if all_ok:
    print("\n✓ TẤT CẢ THƯ VIỆN ĐÃ SẴN SÀNG!")
    print("\nBạn có thể chạy các bài tập:")
    print("  - Từng bài: cd bai-X-xxx && python script.py")
    print("  - Tất cả:   ./run_all.sh (Linux/Mac) hoặc run_all.bat (Windows)")
else:
    print("\n✗ VUI LÒNG CÀI ĐẶT THƯ VIỆN THIẾU:")
    print("  pip install -r requirements.txt")

print("="*80)
