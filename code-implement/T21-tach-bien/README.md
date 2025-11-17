# Edge Detection Assignment (T21-tach-bien)

Bài tập xử lý ảnh về tách biên - 10 bài thực hành với các kỹ thuật phát hiện cạnh khác nhau.

## Cấu trúc thư mục

```
T21-tach-bien/
├── bai-1-edge-detectors/      # So sánh các thuật toán phát hiện cạnh
├── bai-2-document-scanning/   # Quét và cắt tài liệu
├── bai-3-lane-detection/      # Phát hiện làn đường
├── bai-4-defect-detection/    # Phát hiện khuyết tật bề mặt
├── bai-5-coin-counting/       # Đếm và phân loại xu
├── bai-6-product-cropping/    # Cắt sản phẩm khỏi nền
├── bai-7-crack-detection/     # Phát hiện vết nứt
├── bai-8-leaf-measurement/    # Đo đạc đặc điểm lá cây
├── bai-9-object-measurement/  # Đo kích thước đối tượng
├── bai-10-deskewing/          # Xoay ảnh bị nghiêng
├── input/                     # Thư mục ảnh đầu vào
│   ├── generate_samples.py    # Script tạo ảnh mẫu
│   ├── sample-images/         # Ảnh mẫu được tạo tự động
│   └── README.md
├── output/                    # Thư mục kết quả
├── requirements.txt           # Danh sách thư viện cần thiết
├── run_all.sh                # Script chạy tất cả (Linux/Mac)
├── run_all.bat               # Script chạy tất cả (Windows)
└── README.md                 # File này
```

## Cài đặt

### 1. Cài đặt Python

Đảm bảo Python 3.8+ đã được cài đặt:

```bash
python3 --version
```

### 2. Cài đặt thư viện

**Linux/Mac:**
```bash
pip3 install -r requirements.txt
```

**Windows:**
```cmd
pip install -r requirements.txt
```

### 3. Tạo ảnh mẫu

Chạy script để tạo 10 ảnh mẫu:

**Linux/Mac:**
```bash
python3 input/generate_samples.py
```

**Windows:**
```cmd
python input\generate_samples.py
```

Script sẽ tạo các file sau trong `input/sample-images/`:
- `building.jpg` - Ảnh tòa nhà (600x800)
- `doc.jpg` - Ảnh tài liệu nghiêng (800x600)
- `road.jpg` - Ảnh đường với làn (600x800)
- `surface.jpg` - Bề mặt có khuyết tật (600x800)
- `coins.jpg` - Ảnh các đồng xu (600x800)
- `product.jpg` - Sản phẩm trên nền trắng (600x800)
- `surface_crack.jpg` - Bề mặt có vết nứt (600x800)
- `leaf.jpg` - Ảnh lá cây (800x600)
- `measure.jpg` - Đối tượng cần đo (600x800)
- `receipt.jpg` - Hóa đơn nghiêng (800x600)

## Sử dụng

### Chạy từng bài riêng lẻ

**Bài 1: So sánh các thuật toán phát hiện cạnh**
```bash
python3 bai-1-edge-detectors/compare.py input/sample-images/building.jpg
```

**Bài 2: Quét tài liệu**
```bash
python3 bai-2-document-scanning/scan.py input/sample-images/doc.jpg
```

**Bài 3: Phát hiện làn đường**
```bash
python3 bai-3-lane-detection/detect.py input/sample-images/road.jpg
```

**Bài 4: Phát hiện khuyết tật**
```bash
python3 bai-4-defect-detection/detect.py input/sample-images/surface.jpg
```

**Bài 5: Đếm xu**
```bash
python3 bai-5-coin-counting/count.py input/sample-images/coins.jpg
```

**Bài 6: Cắt sản phẩm**
```bash
python3 bai-6-product-cropping/crop.py input/sample-images/product.jpg
```

**Bài 7: Phát hiện vết nứt**
```bash
python3 bai-7-crack-detection/detect.py input/sample-images/surface_crack.jpg
```

**Bài 8: Đo lá cây**
```bash
python3 bai-8-leaf-measurement/measure.py input/sample-images/leaf.jpg
```

**Bài 9: Đo đối tượng**
```bash
python3 bai-9-object-measurement/measure.py input/sample-images/measure.jpg
```

**Bài 10: Xoay ảnh**
```bash
python3 bai-10-deskewing/deskew.py input/sample-images/receipt.jpg
```

### Chạy tất cả các bài

**Linux/Mac:**
```bash
./run_all.sh
```
hoặc
```bash
bash run_all.sh
```

**Windows:**
```cmd
run_all.bat
```

Script sẽ:
- Tự động tạo ảnh mẫu nếu chưa có
- Chạy tuần tự 10 bài
- Hiển thị tiến độ và kết quả
- Báo cáo tổng hợp cuối cùng

## Kết quả

Kết quả được lưu trong thư mục `output/` với cấu trúc:

```
output/
├── bai-1/
│   ├── original.jpg
│   ├── canny.jpg
│   ├── sobel.jpg
│   └── ...
├── bai-2/
│   ├── original.jpg
│   ├── edges.jpg
│   ├── contours.jpg
│   └── scanned.jpg
└── ...
```

## Thư viện sử dụng

- **OpenCV** (cv2): Xử lý ảnh cơ bản
- **NumPy**: Tính toán mảng
- **scikit-image**: Các thuật toán xử lý ảnh nâng cao
- **SciPy**: Tính toán khoa học
- **Matplotlib**: Hiển thị và lưu kết quả

## Các kỹ thuật được sử dụng

### Bài 1: Edge Detectors
- Canny Edge Detection
- Sobel Operator
- Laplacian of Gaussian (LoG)
- Prewitt Operator
- Scharr Operator

### Bài 2: Document Scanning
- Canny Edge Detection
- Contour Detection
- Perspective Transform
- Adaptive Thresholding

### Bài 3: Lane Detection
- Canny Edge Detection
- Hough Line Transform
- Region of Interest Masking
- Lane Interpolation

### Bài 4: Defect Detection
- Gaussian Blur
- Canny Edge Detection
- Morphological Operations
- Contour Analysis

### Bài 5: Coin Counting
- Bilateral Filter
- Canny Edge Detection
- Hough Circle Transform
- Circle Classification

### Bài 6: Product Cropping
- Canny Edge Detection
- Contour Detection
- Bounding Box Calculation
- Background Removal

### Bài 7: Crack Detection
- Gaussian Blur
- Canny Edge Detection
- Morphological Operations
- Crack Highlighting

### Bài 8: Leaf Measurement
- Canny Edge Detection
- Contour Analysis
- Area & Perimeter Calculation
- Convex Hull Analysis

### Bài 9: Object Measurement
- Canny Edge Detection
- Contour Detection
- Size Calculation with Reference
- Multiple Object Processing

### Bài 10: Deskewing
- Canny Edge Detection
- Hough Line Transform
- Angle Calculation
- Rotation Correction

## Xử lý lỗi

### Lỗi: "No module named 'cv2'"
```bash
pip3 install opencv-python
```

### Lỗi: "Sample images not found"
```bash
python3 input/generate_samples.py
```

### Lỗi: "Permission denied: ./run_all.sh"
```bash
chmod +x run_all.sh
```

## Tác giả

Bài tập thực hành xử lý ảnh - T21 Tách biên

## License

Educational use only
