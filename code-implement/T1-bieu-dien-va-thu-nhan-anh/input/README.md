# Input Images Guide

Hướng dẫn chuẩn bị ảnh đầu vào cho các bài tập T1: Biểu diễn và Thu nhận Ảnh.

## Danh sách ảnh cần thiết

### 1. `scan_de_thi.png` (Bài tập 2)
- **Mô tả**: Ảnh scan đề thi hoặc tài liệu văn bản
- **Yêu cầu**:
  - Ảnh xám (grayscale)
  - Độ phân giải khuyến nghị: 600-1200 DPI
  - Kích thước: Khoảng 800x600 pixels trở lên
  - Nội dung: Văn bản rõ ràng, có chữ
- **Cách chuẩn bị**:
  - Scan tài liệu thật với máy scanner
  - Hoặc chụp ảnh tài liệu và convert sang grayscale
  - Hoặc chạy `generate_samples.py` để tạo tự động

### 2. `bill.png` (Bài tập 3)
- **Mô tả**: Hóa đơn/phiếu thu có nhiễu muối tiêu
- **Yêu cầu**:
  - Ảnh xám (grayscale)
  - Có nhiễu muối tiêu (salt & pepper noise)
  - Kích thước: 600x800 pixels trở lên
  - Nội dung: Văn bản hóa đơn, số tiền, items
- **Cách chuẩn bị**:
  - Scan hóa đơn thật (chất lượng thấp)
  - Thêm nhiễu muối tiêu bằng code
  - Hoặc chạy `generate_samples.py`

### 3. `portrait.jpg` (Bài tập 5)
- **Mô tả**: Ảnh chân dung có vùng da rõ ràng
- **Yêu cầu**:
  - Ảnh màu RGB
  - Có vùng da mặt/tay rõ ràng
  - Ánh sáng đều, không quá tối/sáng
  - Kích thước: 480x640 pixels trở lên
- **Cách chuẩn bị**:
  - Chụp ảnh chân dung
  - Tải ảnh portrait từ dataset công khai
  - Hoặc chạy `generate_samples.py` (tạo ảnh synthetic)

### 4. `doc.png` (Lab 1)
- **Mô tả**: Ảnh tài liệu cho đánh giá lượng tử hóa
- **Yêu cầu**:
  - Ảnh xám với nhiều mức xám khác nhau
  - Có gradient/texture
  - Kích thước: 600x800 pixels trở lên
- **Cách chuẩn bị**:
  - Tương tự `scan_de_thi.png`
  - Hoặc chạy `generate_samples.py`

### 5. `campus.jpg` (Lab 2)
- **Mô tả**: Ảnh cảnh trường học/campus
- **Yêu cầu**:
  - Ảnh xám hoặc màu
  - Có nhiều chi tiết (tòa nhà, cây, đường)
  - Kích thước: 480x640 pixels trở lên
- **Cách chuẩn bị**:
  - Chụp ảnh campus
  - Tải ảnh từ dataset
  - Hoặc chạy `generate_samples.py`

### 6. `pcb.png` (Lab 4)
- **Mô tả**: Ảnh mạch in hoặc đường kẻ chéo
- **Yêu cầu**:
  - Ảnh xám
  - Có các đường kẻ, đối tượng rời rạc
  - Phù hợp để test connected components
- **Cách chuẩn bị**:
  - Chụp ảnh mạch in
  - Vẽ đường kẻ trên ảnh
  - Hoặc chạy `generate_samples.py`

### 7. `scene.jpg` (Lab 5)
- **Mô tả**: Ảnh cảnh tự nhiên phức tạp
- **Yêu cầu**:
  - Ảnh xám hoặc màu
  - Có nhiều chi tiết, texture
  - Kích thước: 480x640 pixels trở lên
- **Cách chuẩn bị**:
  - Chụp ảnh cảnh tự nhiên
  - Tải từ dataset
  - Hoặc chạy `generate_samples.py`

## Tự động tạo ảnh mẫu

### Cách 1: Chạy script generate_samples.py
```bash
cd input
python generate_samples.py
```

Script sẽ tự động tạo tất cả ảnh mẫu cần thiết vào folder `sample-images/`.

### Cách 2: Tự động tạo khi chạy code
Các file code đã được thiết kế để tự động tạo ảnh mẫu nếu không tìm thấy file input. Chỉ cần chạy code trực tiếp:

```bash
python bai-tap-2-quantization/quantize_scan.py
```

Nếu không tìm thấy `scan_de_thi.png`, code sẽ tự động tạo.

## Tải ảnh từ dataset công khai

### Nguồn miễn phí:
1. **Unsplash** (https://unsplash.com/): Ảnh chất lượng cao, free license
2. **Pexels** (https://pexels.com/): Ảnh và video miễn phí
3. **Pixabay** (https://pixabay.com/): Ảnh miễn phí
4. **USC-SIPI Image Database** (http://sipi.usc.edu/database/): Dataset ảnh xử lý ảnh
5. **Kaggle Datasets**: Nhiều dataset ảnh cho computer vision

### Dataset chuyên dụng:
- **Document Images**: MNIST, IAM Handwriting, DocVQA
- **Faces/Portraits**: LFW, CelebA, WIDER FACE
- **Natural Scenes**: COCO, ImageNet, Places365
- **PCB/Electronics**: PCB Defects, Electronics Datasets

## Lưu ý quan trọng

1. **Kích thước**: Không cần quá lớn, 480p-1080p là đủ
2. **Format**:
   - Grayscale: PNG (không mất dữ liệu)
   - Color: JPG hoặc PNG
3. **Chất lượng**: Ảnh rõ nét, không bị blur quá mức
4. **Bản quyền**: Chỉ dùng ảnh có license phù hợp (CC0, Public Domain) hoặc ảnh tự chụp
5. **Đặt tên**: Đúng tên như trong danh sách trên
6. **Vị trí**: Đặt trong `input/sample-images/`

## Cấu trúc thư mục

```
input/
├── README.md (file này)
├── generate_samples.py (script tạo ảnh mẫu)
├── sample-images/
│   ├── scan_de_thi.png
│   ├── bill.png
│   ├── portrait.jpg
│   ├── doc.png
│   ├── campus.jpg
│   ├── pcb.png
│   └── scene.jpg
└── test-images/
    └── (ảnh test khác nếu cần)
```

## Kiểm tra ảnh đã sẵn sàng

Chạy script kiểm tra:
```bash
python check_inputs.py
```

Hoặc kiểm tra thủ công xem các file đã tồn tại trong `sample-images/` chưa.

## Hỗ trợ

Nếu gặp vấn đề với ảnh đầu vào, hãy:
1. Kiểm tra format và kích thước ảnh
2. Chạy `generate_samples.py` để tạo ảnh mẫu
3. Đọc error message từ code để biết ảnh nào thiếu
4. Tham khảo code của từng bài tập để hiểu yêu cầu cụ thể
