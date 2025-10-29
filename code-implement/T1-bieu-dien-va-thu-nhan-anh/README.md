# T1: Biểu diễn và Thu nhận Ảnh

Implementation code cho chủ đề "Biểu diễn và Thu nhận Ảnh" - Bài thực hành Xử lý Ảnh.

**Tác giả đề bài**: TS. Phan Thanh Toàn

## Tổng quan

Chủ đề này bao gồm 5 bài tập và 5 lab về các khái niệm cơ bản trong xử lý ảnh số:
- Lấy mẫu (Sampling) và Lượng tử hóa (Quantization)
- Biểu diễn bit-plane
- Kết nối pixel (4/8-connectivity)
- Không gian màu (Color spaces)
- Nội suy ảnh (Image interpolation)
- Đánh giá chất lượng ảnh (Image quality metrics)

## Cấu trúc thư mục

```
T1-bieu-dien-va-thu-nhan-anh/
├── bai-tap-1-camera-storage/      # Bài 1: Tính dung lượng camera
├── bai-tap-2-quantization/        # Bài 2: Lượng tử hóa
├── bai-tap-3-bitplane-slicing/    # Bài 3: Tách bit-plane
├── bai-tap-4-connectivity/        # Bài 4: Kết nối & pathfinding
├── bai-tap-5-color-space/         # Bài 5: Không gian màu
├── lab-1-quantization-eval/       # Lab 1: Đánh giá lượng tử hóa
├── lab-2-zooming-shrinking/       # Lab 2: Phóng/thu ảnh
├── lab-3-measure-circle/          # Lab 3: Đo đường tròn
├── lab-4-connected-components/    # Lab 4: Gán nhãn liên thông
├── lab-5-image-quality/           # Lab 5: Đánh giá chất lượng
├── input/                         # Ảnh đầu vào
│   ├── sample-images/            # Ảnh mẫu
│   ├── README.md                 # Hướng dẫn chuẩn bị ảnh
│   └── generate_samples.py       # Script tạo ảnh mẫu
├── output/                        # Kết quả output (tự tạo)
├── requirements.txt               # Dependencies
├── run_all.sh                     # Script chạy tất cả (Linux/Mac)
├── run_all.bat                    # Script chạy tất cả (Windows)
└── README.md                      # File này
```

## Cài đặt

### 1. Yêu cầu hệ thống
- Python >= 3.8
- pip hoặc conda

### 2. Cài đặt dependencies

**Cách 1: Sử dụng virtual environment (khuyến nghị)**
```bash
# Tạo virtual environment
python3 -m venv venv

# Kích hoạt (Linux/Mac)
source venv/bin/activate

# Kích hoạt (Windows)
venv\Scripts\activate

# Cài đặt packages
pip install -r requirements.txt
```

**Cách 2: Cài đặt trực tiếp**
```bash
pip install -r requirements.txt
```

### 3. Chuẩn bị ảnh đầu vào

**Cách 1: Tạo ảnh mẫu tự động (khuyến nghị cho testing)**
```bash
cd input
python generate_samples.py
```

**Cách 2: Tự chuẩn bị ảnh**
- Đọc hướng dẫn trong `input/README.md`
- Đặt ảnh vào `input/sample-images/`

**Cách 3: Để code tự tạo**
- Các script đã tích hợp tạo ảnh mẫu tự động nếu không tìm thấy

## Sử dụng

### Chạy tất cả bài tập

**Linux/Mac:**
```bash
./run_all.sh
```

**Windows:**
```bash
run_all.bat
```

### Chạy từng bài riêng lẻ

```bash
# Bài tập 1: Camera storage calculator
python bai-tap-1-camera-storage/calculator.py

# Bài tập 2: Quantization
python bai-tap-2-quantization/quantize_scan.py

# Bài tập 3: Bit-plane slicing
python bai-tap-3-bitplane-slicing/bitplane.py

# Bài tập 4: Connectivity & pathfinding
python bai-tap-4-connectivity/robot_path.py

# Bài tập 5: Color space & skin detection
python bai-tap-5-color-space/skin_detection.py

# Lab 1: Quantization evaluation
python lab-1-quantization-eval/evaluate.py

# Lab 2: Zooming & shrinking
python lab-2-zooming-shrinking/resize.py

# Lab 3: Circle measurement
python lab-3-measure-circle/measure.py

# Lab 4: Connected components
python lab-4-connected-components/labeling.py

# Lab 5: Image quality assessment
python lab-5-image-quality/assess.py
```

## Mô tả chi tiết các bài

### Bài tập 1: Tính dung lượng & băng thông camera
- **Mục tiêu**: Tính toán dung lượng lưu trữ và băng thông cho hệ thống giám sát
- **Kỹ năng**: Hiểu về spatial resolution, bit-depth, frame rate
- **Output**: So sánh các kịch bản 1080p, 720p, 4K

### Bài tập 2: Lượng tử hóa
- **Mục tiêu**: Mô phỏng giảm bit-depth từ 8-bit xuống 6, 4, 2 bit
- **Kỹ năng**: Quantization, đánh giá chất lượng (MAE, MSE, PSNR, SSIM)
- **Output**: Ảnh lượng tử hóa + metrics

### Bài tập 3: Bit-plane slicing
- **Mục tiêu**: Tách và phân tích 8 mặt phẳng bit
- **Kỹ năng**: Biểu diễn nhị phân, phát hiện nhiễu
- **Output**: 8 bit-planes + ảnh tái dựng từ MSB

### Bài tập 4: Kết nối pixel
- **Mục tiêu**: So sánh 4-connectivity vs 8-connectivity trong pathfinding
- **Kỹ năng**: Distance metrics, BFS, kết nối pixel
- **Output**: Đường đi ngắn nhất với 2 loại connectivity

### Bài tập 5: Không gian màu
- **Mục tiêu**: Phát hiện vùng da bằng HSV và YCrCb
- **Kỹ năng**: Color space conversion, thresholding
- **Output**: Mask vùng da từ 2 color spaces

### Lab 1: Đánh giá lượng tử hóa động
- **Mục tiêu**: Thực nghiệm đầy đủ với nhiều mức bit
- **Kỹ năng**: Tính toán 5 metrics (MAE, MSE, PSNR, SSIM, NCC)
- **Output**: Bảng so sánh + khuyến nghị

### Lab 2: Zooming & Shrinking
- **Mục tiêu**: So sánh các phương pháp nội suy
- **Kỹ năng**: Nearest, bilinear, cubic, pixel replication
- **Output**: Ảnh zoom/shrink + đánh giá round-trip quality

### Lab 3: Đo đường tròn
- **Mục tiêu**: Tính tâm, bán kính, góc, cung từ 3 điểm
- **Kỹ năng**: Giải hệ phương trình, geometry, quy đổi đơn vị
- **Output**: Measurements + visualization

### Lab 4: Gán nhãn liên thông
- **Mục tiêu**: So sánh 4-connectivity vs 8-connectivity trong labeling
- **Kỹ năng**: Connected components, contour analysis
- **Output**: Labeled images + statistics

### Lab 5: Đánh giá chất lượng ảnh
- **Mục tiêu**: Thực nghiệm với nhiễu Gaussian, salt & pepper, JPEG, bit-depth
- **Kỹ năng**: Noise models, compression, quality metrics
- **Output**: Bảng so sánh các metrics + phân tích

## Kết quả Output

Tất cả kết quả được lưu trong thư mục `output/`:
- Ảnh xử lý (PNG, JPG)
- Visualizations
- Console output với metrics

## Troubleshooting

### Lỗi: "No module named 'cv2'"
```bash
pip install opencv-python
```

### Lỗi: "No such file or directory: 'scan_de_thi.png'"
```bash
cd input
python generate_samples.py
```

### Lỗi: Permission denied khi chạy run_all.sh
```bash
chmod +x run_all.sh
```

### Ảnh output bị lỗi hoặc trống
- Kiểm tra ảnh input có đúng format không
- Xem error message trong console
- Thử tạo lại ảnh mẫu với `generate_samples.py`

## Tài liệu tham khảo

Xem thêm documentation chi tiết tại:
```
documents/T1-bieu-dien-va-thu-nhan-anh/
├── theory/          # Lý thuyết nền tảng
├── exercises/       # Giải thích từng bài
└── README.md        # Tổng quan
```

## Dependencies

- **opencv-python** (>=4.8.0): Xử lý ảnh cơ bản
- **numpy** (>=1.24.0): Tính toán ma trận
- **scikit-image** (>=0.21.0): SSIM và các metrics nâng cao
- **matplotlib** (>=3.7.0): Visualization (optional)

## License

Code mẫu cho mục đích học tập. Đề bài và yêu cầu bài tập thuộc bản quyền của TS. Phan Thanh Toàn.

## Liên hệ

Nếu có vấn đề hoặc câu hỏi, vui lòng tạo issue hoặc liên hệ giảng viên.

---

**Lưu ý**: Code trong repository này được viết y nguyên theo đề bài, với mục đích học tập và thực hành xử lý ảnh cơ bản.
