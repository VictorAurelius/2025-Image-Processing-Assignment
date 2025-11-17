# Quick Start Guide - T21 Tách Biên

## Cài đặt nhanh

### Bước 1: Cài đặt thư viện
```bash
pip3 install -r requirements.txt
```

### Bước 2: Tạo ảnh mẫu
```bash
python3 input/generate_samples.py
```

### Bước 3: Chạy thử một bài
```bash
python3 bai-1-edge-detectors/compare.py input/sample-images/building.jpg
```

## Chạy tất cả các bài

### Linux/Mac:
```bash
chmod +x run_all.sh
./run_all.sh
```

### Windows:
```cmd
run_all.bat
```

## Cấu trúc đơn giản

```
T21-tach-bien/
├── input/                      # Ảnh đầu vào
│   ├── generate_samples.py     # Tạo 10 ảnh mẫu
│   └── sample-images/          # Thư mục chứa ảnh
│
├── bai-1-edge-detectors/       # 10 bài tập
├── bai-2-document-scanning/
├── ...
├── bai-10-deskewing/
│
├── output/                     # Kết quả
│
├── requirements.txt            # Thư viện cần thiết
├── run_all.sh                 # Chạy tất cả (Linux/Mac)
└── run_all.bat                # Chạy tất cả (Windows)
```

## 10 Bài tập

| Bài | Tên | Script | Ảnh mẫu |
|-----|-----|--------|---------|
| 1 | Edge Detectors | `compare.py` | `building.jpg` |
| 2 | Document Scanning | `scan.py` | `doc.jpg` |
| 3 | Lane Detection | `detect.py` | `road.jpg` |
| 4 | Defect Detection | `detect.py` | `surface.jpg` |
| 5 | Coin Counting | `count.py` | `coins.jpg` |
| 6 | Product Cropping | `crop.py` | `product.jpg` |
| 7 | Crack Detection | `detect.py` | `surface_crack.jpg` |
| 8 | Leaf Measurement | `measure.py` | `leaf.jpg` |
| 9 | Object Measurement | `measure.py` | `measure.jpg` |
| 10 | Deskewing | `deskew.py` | `receipt.jpg` |

## Ví dụ chạy từng bài

```bash
# Bài 1: So sánh các thuật toán
python3 bai-1-edge-detectors/compare.py input/sample-images/building.jpg

# Bài 2: Quét tài liệu
python3 bai-2-document-scanning/scan.py input/sample-images/doc.jpg

# Bài 5: Đếm xu
python3 bai-5-coin-counting/count.py input/sample-images/coins.jpg

# Bài 10: Xoay ảnh
python3 bai-10-deskewing/deskew.py input/sample-images/receipt.jpg
```

## Xem kết quả

Kết quả được lưu trong thư mục `output/`:
```bash
ls -la output/
```

Hoặc mở trực tiếp các file ảnh trong `output/bai-X/`

## Xử lý lỗi thường gặp

### 1. Không có module 'cv2'
```bash
pip3 install opencv-python
```

### 2. Không tìm thấy ảnh mẫu
```bash
python3 input/generate_samples.py
```

### 3. Permission denied (Linux/Mac)
```bash
chmod +x run_all.sh
chmod +x input/generate_samples.py
```

### 4. Script không chạy (Windows)
- Đảm bảo Python đã được thêm vào PATH
- Chạy Command Prompt với quyền Administrator

## Tùy chỉnh

### Sử dụng ảnh của bạn
```bash
python3 bai-X-name/script.py /path/to/your/image.jpg
```

### Thay đổi tham số
Mở file `.py` và điều chỉnh các tham số trong code.

## Thư viện sử dụng

- **OpenCV**: Xử lý ảnh
- **NumPy**: Tính toán
- **scikit-image**: Thuật toán nâng cao
- **SciPy**: Tính toán khoa học
- **Matplotlib**: Hiển thị kết quả
