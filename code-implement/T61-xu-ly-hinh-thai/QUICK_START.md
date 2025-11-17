# HƯỚNG DẪN NHANH - T61 XỬ LÝ HÌNH THÁI

## Bắt đầu trong 3 bước

### Bước 1: Kiểm tra môi trường

```bash
python test_setup.py
```

### Bước 2: Cài đặt thư viện (nếu cần)

```bash
pip install -r requirements.txt
```

### Bước 3: Chạy bài tập

#### Chạy tất cả (khuyến nghị)

```bash
# Linux/Mac
./run_all.sh

# Windows
run_all.bat
```

#### Chạy từng bài

```bash
# Bài 1: Opening - Khử nhiễu
cd bai-1-opening
python denoise.py

# Bài 2: Closing - Lấp lỗ
cd bai-2-closing
python fill_holes.py

# Bài 3: Gradient - Trích biên
cd bai-3-gradient
python extract_edges.py

# Bài 4: Watershed - Đếm đồng xu
cd bai-4-watershed
python separate.py

# Bài 5: Character Segmentation
cd bai-5-character-segmentation
python segment.py

# Bài 6: Particle Measurement
cd bai-6-particle-measurement
python measure.py

# Bài 7: Pruning - Xóa pixel thừa
cd bai-7-pruning
python prune.py

# Bài 8: Foreground Extraction
cd bai-8-foreground-extraction
python extract.py

# Bài 9: Top-hat/Black-hat
cd bai-9-background-removal
python remove.py
```

## Tạo ảnh mẫu

Nếu muốn tạo tất cả ảnh mẫu trước:

```bash
cd input
python generate_samples.py
```

**Lưu ý**: Mỗi bài tập sẽ TỰ ĐỘNG tạo ảnh mẫu nếu thiếu input.

## Kết quả

Tất cả kết quả được lưu trong thư mục `output/`:

```
output/
├── bai-1-opening/
├── bai-2-closing/
├── bai-3-gradient/
├── bai-4-watershed/
├── bai-5-character-segmentation/
├── bai-6-particle-measurement/
├── bai-7-pruning/
├── bai-8-foreground-extraction/
└── bai-9-background-removal/
```

## Xử lý lỗi thường gặp

### Lỗi: `ModuleNotFoundError: No module named 'cv2'`

**Giải pháp**:
```bash
pip install opencv-python
```

### Lỗi: `matplotlib` không hiển thị

**Giải pháp**:
```bash
# Linux
sudo apt-get install python3-tk

# Mac
brew install python-tk
```

### Lỗi: Permission denied khi chạy .sh

**Giải pháp**:
```bash
chmod +x run_all.sh
```

## Tùy chỉnh

### Thay đổi ảnh input

Đặt ảnh của bạn vào thư mục tương ứng trong `input/`:

```
input/
├── docs/noisy_scan.png      # Bài 1
├── parts/gapped.png         # Bài 2
├── objects/sample.png       # Bài 3
├── coins/touching.jpg       # Bài 4
├── plates/plate.jpg         # Bài 5
├── surface/holes.png        # Bài 6
├── edges/jagged.png         # Bài 7
├── conveyor/items.png       # Bài 8
└── docs/uneven.jpg          # Bài 9
```

### Tắt hiển thị matplotlib

Thêm biến môi trường:

```bash
export MPLBACKEND=Agg  # Linux/Mac
set MPLBACKEND=Agg     # Windows
```

## Xem chi tiết

Đọc `README.md` để biết thêm chi tiết về:
- Mô tả từng bài tập
- Kỹ thuật sử dụng
- Ứng dụng thực tế
- Tham khảo

---

**Chúc bạn học tốt!**
