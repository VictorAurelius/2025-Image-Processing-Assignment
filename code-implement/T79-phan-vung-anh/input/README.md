# Thư mục Input - Ảnh và Video Mẫu

Thư mục này chứa các ảnh và video đầu vào cho 10 bài tập về Phân vùng ảnh (T79-99).

## Danh sách files cần thiết:

### Bài 1: Global Thresholding
- `conveyor.jpg` - Ảnh băng chuyền với sản phẩm

### Bài 2: Otsu
- `parts.jpg` - Ảnh linh kiện điện tử trên nền phẳng

### Bài 3: Adaptive Thresholding
- `receipt.jpg` - Ảnh hóa đơn với độ sáng không đều

### Bài 4: Bayes-ML
- `steel_rust.jpg` - Ảnh bề mặt kim loại có rỉ sét

### Bài 5: Edge + Hough
- `lanes.jpg` - Ảnh vạch kẻ đường/lằn cắt

### Bài 6: Region Growing
- `ultrasound.png` - Ảnh siêu âm/CT với tổn thương

### Bài 7: Split-Merge
- `landscape.jpg` - Ảnh phong cảnh (trời/biển/đất)

### Bài 8: K-means
- `satellite.jpg` - Ảnh vệ tinh (vườn cây/sông/nhà)

### Bài 9: Motion Segmentation
- `gate.mp4` - Video camera cổng (người/xe di chuyển)

### Bài 10: Watershed
- `coins.png` - Ảnh đồng xu/hạt bi dính nhau

## Tự động tạo ảnh mẫu

Nếu không có file ảnh/video, mỗi bài tập sẽ **TỰ ĐỘNG TẠO** ảnh mẫu khi chạy.

Bạn cũng có thể chạy script để tạo tất cả ảnh mẫu:

```bash
python generate_samples.py
```

## Thay thế ảnh của bạn

Bạn có thể thay thế bằng ảnh thực tế của mình, đặt đúng tên file như trên.

**Lưu ý:**
- Định dạng ảnh: JPG, PNG
- Kích thước: Không quá lớn (khuyến nghị < 2MB)
- Video: MP4, AVI (khuyến nghị < 10MB)
