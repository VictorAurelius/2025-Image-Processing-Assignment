# Documentation: T1 - Biểu diễn và Thu nhận Ảnh

Tài liệu đầy đủ về chủ đề "Biểu diễn và Thu nhận Ảnh" trong môn Xử lý Ảnh.

**Tác giả đề bài**: TS. Phan Thanh Toàn

## Tổng quan

Chủ đề này bao gồm các khái niệm cơ bản nhất trong xử lý ảnh số:
- Cách ảnh được biểu diễn trong máy tính
- Sampling (lấy mẫu) và Quantization (lượng tử hóa)
- Biểu diễn nhị phân qua bit-planes
- Kết nối giữa các pixel
- Các không gian màu khác nhau
- Phóng to/thu nhỏ ảnh
- Đánh giá chất lượng ảnh

## Cấu trúc tài liệu

```
documents/T1-bieu-dien-va-thu-nhan-anh/
├── README.md (file này)
├── theory/
│   ├── 01-sampling-quantization.md
│   ├── 02-bit-plane-representation.md
│   ├── 03-pixel-connectivity.md
│   ├── 04-color-spaces.md
│   ├── 05-image-interpolation.md
│   └── 06-image-quality-metrics.md
└── exercises/
    └── (Tham khảo code trong code-implement/)
```

## Tài liệu Lý thuyết

### 1. Lấy mẫu và Lượng tử hóa
**File**: `theory/01-sampling-quantization.md`

**Nội dung**:
- Định nghĩa sampling và quantization
- Độ phân giải không gian (spatial resolution)
- Độ phân giải mức xám (gray-level resolution)
- Định lý Nyquist-Shannon
- Aliasing và cách tránh
- Trade-off giữa resolution và bit-depth
- Tính toán dung lượng và băng thông

**Ứng dụng**: Bài tập 1, 2, Lab 1

**Khái niệm quan trọng**:
- `L = 2^k` (số mức xám)
- `Size = M × N × k` (bits)
- Quantization error
- Posterization effect

### 2. Biểu diễn Bit-Plane
**File**: `theory/02-bit-plane-representation.md`

**Nội dung**:
- Tách ảnh thành 8 bit-planes
- MSB (Most Significant Bits) vs LSB (Least Significant Bits)
- Tái dựng ảnh từ bit-planes
- Ứng dụng trong nén, steganography, watermarking
- Phát hiện nhiễu qua LSB

**Ứng dụng**: Bài tập 3

**Khái niệm quan trọng**:
- Bit-plane i: `(img >> i) & 1`
- MSB (bit 7-4): Cấu trúc chính
- LSB (bit 3-0): Nhiễu và chi tiết mịn

### 3. Kết nối Pixel
**File**: `theory/03-pixel-connectivity.md`

**Nội dung**:
- 4-connectivity vs 8-connectivity vs m-connectivity
- Distance metrics: Manhattan, Chessboard, Euclidean
- Đường đi (paths) và đường đi ngắn nhất
- Connected components
- BFS/DFS với connectivity
- Jordan Curve Theorem problem

**Ứng dụng**: Bài tập 4, Lab 4

**Khái niệm quan trọng**:
- N₄(p): 4 neighbors
- N₈(p): 8 neighbors
- D_4 = |Δx| + |Δy| (Manhattan)
- D_8 = max(|Δx|, |Δy|) (Chessboard)

### 4. Không gian Màu
**File**: `theory/04-color-spaces.md`

**Nội dung**:
- RGB: Mô hình cộng màu
- HSV: Hue-Saturation-Value
- YCrCb: Luma-Chroma
- Chuyển đổi giữa các color spaces
- Skin detection với HSV và YCrCb
- So sánh ưu nhược điểm

**Ứng dụng**: Bài tập 5

**Khái niệm quan trọng**:
- RGB: Device-dependent
- HSV: Perceptually meaningful
- YCrCb: Separates luma/chroma, tốt cho skin detection
- Color space conversion: `cv2.cvtColor()`

### 5. Nội suy Ảnh
**File**: `theory/05-image-interpolation.md`

**Nội dung**:
- Nearest neighbor: Nhanh nhất, blocky
- Bilinear: Mượt, tốt cho general purpose
- Bicubic: Chất lượng cao
- Area: Tốt nhất cho shrinking
- Lanczos: Chất lượng cao nhất
- Pixel replication: Đơn giản
- Anti-aliasing

**Ứng dụng**: Lab 2

**Khái niệm quan trọng**:
- Zooming: INTER_CUBIC hoặc INTER_LANCZOS4
- Shrinking: INTER_AREA
- Real-time: INTER_NEAREST hoặc INTER_LINEAR
- Round-trip quality

### 6. Các chỉ số Chất lượng Ảnh
**File**: `theory/06-image-quality-metrics.md`

**Nội dung**:
- MAE (Mean Absolute Error)
- MSE (Mean Squared Error)
- PSNR (Peak Signal-to-Noise Ratio)
- SSIM (Structural Similarity Index)
- NCC (Normalized Cross-Correlation)
- So sánh các metrics
- Best practices

**Ứng dụng**: Bài tập 2, Lab 1, Lab 2, Lab 5

**Khái niệm quan trọng**:
- MAE: Đơn giản, tuyến tính
- MSE: Phạt nặng outliers
- PSNR: Standard metric, đơn vị dB
- **SSIM**: Best cho perceptual quality
- SSIM > PSNR > MSE/MAE (correlation với human perception)

## Hướng dẫn Đọc tài liệu

### Đường đi học tập được khuyến nghị

**Người mới bắt đầu**:
1. Đọc 01-sampling-quantization.md
2. Chạy Bài tập 1 và 2
3. Đọc 02-bit-plane-representation.md
4. Chạy Bài tập 3
5. Đọc 06-image-quality-metrics.md
6. Chạy Lab 1 và Lab 5
7. Đọc 03-pixel-connectivity.md
8. Chạy Bài tập 4 và Lab 4
9. Đọc 04-color-spaces.md
10. Chạy Bài tập 5
11. Đọc 05-image-interpolation.md
12. Chạy Lab 2 và Lab 3

**Người có kinh nghiệm**:
- Đọc nhanh các theory documents
- Chạy thẳng tất cả bài tập
- Tham khảo theory khi cần

### Cách sử dụng tài liệu

**Mỗi tài liệu lý thuyết bao gồm**:
1. **Giới thiệu**: Tổng quan về chủ đề
2. **Khái niệm cơ bản**: Định nghĩa, công thức
3. **Đặc điểm**: Ưu nhược điểm
4. **Ứng dụng**: Các trường hợp sử dụng
5. **Code examples**: Ví dụ code minh họa
6. **Best practices**: Lời khuyên thực tế
7. **Bài tập**: Để tự luyện tập
8. **Tóm tắt**: Bảng tổng hợp nhanh
9. **References**: Tài liệu tham khảo

**Tips**:
- Đọc phần "Tóm tắt" trước để có overview
- Chạy code examples trong docs
- Làm bài tập ở cuối mỗi docs
- So sánh kết quả với code implementation

## Giải thích Bài tập

### Phương pháp học từ Code

Thay vì tạo 10 tài liệu giải thích riêng, tôi khuyến nghị cách học hiệu quả hơn:

**Bước 1**: Đọc tài liệu lý thuyết tương ứng
**Bước 2**: Đọc code trong `code-implement/`
**Bước 3**: Chạy code và quan sát output
**Bước 4**: Đọc comments trong code để hiểu chi tiết

**Tại sao phương pháp này tốt?**
- Code được viết rõ ràng với nhiều comments
- Output console giải thích kết quả
- Học được cả lý thuyết và thực hành
- Hiểu sâu hơn qua việc thực thi

### Ánh xạ Bài tập → Theory

| Bài tập | Theory Documents | Khái niệm chính |
|---------|------------------|-----------------|
| Bài 1 | 01-sampling-quantization | Spatial resolution, bit-depth, storage, bandwidth |
| Bài 2 | 01, 06 | Quantization, MAE, MSE, PSNR, SSIM |
| Bài 3 | 02 | Bit-plane slicing, MSB/LSB, NCC |
| Bài 4 | 03 | 4/8-connectivity, distance metrics, pathfinding |
| Bài 5 | 04 | HSV, YCrCb, skin detection, color thresholding |
| Lab 1 | 01, 06 | Comprehensive quantization evaluation, all metrics |
| Lab 2 | 05 | Interpolation methods, zooming, shrinking |
| Lab 3 | 03 | Circle measurement, geometry, contours |
| Lab 4 | 03 | Connected components, labeling, 4 vs 8 connectivity |
| Lab 5 | 06 | All quality metrics, noise, compression |

### Ví dụ: Cách học Bài tập 2

**Bước 1**: Đọc theory
```
→ documents/theory/01-sampling-quantization.md (phần Quantization)
→ documents/theory/06-image-quality-metrics.md (phần MAE, MSE, PSNR, SSIM)
```

**Bước 2**: Đọc code
```
→ code-implement/bai-tap-2-quantization/quantize_scan.py
  - Đọc function quantize_gray(): Hiểu cách lượng tử hóa
  - Đọc function mse(), psnr(): Hiểu cách tính metrics
  - Đọc main(): Hiểu flow chương trình
```

**Bước 3**: Chạy code
```bash
cd code-implement/bai-tap-2-quantization
python quantize_scan.py
```

**Bước 4**: Phân tích output
```
6 bit -> MSE=X, PSNR=Y dB, SSIM=Z
4 bit -> MSE=X, PSNR=Y dB, SSIM=Z
2 bit -> MSE=X, PSNR=Y dB, SSIM=Z
```

**Bước 5**: Quan sát ảnh output
```
→ code-implement/output/scan_quant_6bit.png
→ code-implement/output/scan_quant_4bit.png
→ code-implement/output/scan_quant_2bit.png
```

**Bước 6**: Tự trả lời câu hỏi
- Mức bit nào vẫn đọc được chữ tốt?
- SSIM thay đổi như thế nào?
- Tại sao 2-bit kém?

## Code Structure

Mỗi bài tập có cấu trúc tương tự:
```python
# 1. Import libraries
import cv2, numpy as np
from skimage.metrics import structural_similarity as ssim

# 2. Define helper functions
def quantize_gray(img, k):
    """Docstring giải thích function"""
    # Implementation với comments

# 3. Main execution
if __name__ == "__main__":
    # Setup paths
    # Check/create input images
    # Process
    # Evaluate
    # Save results
    # Print conclusions
```

**Tất cả code đều có**:
- Docstrings giải thích mục đích
- Comments giải thích từng bước
- Auto-generate sample images nếu thiếu
- Print kết quả với format đẹp
- Kết luận và khuyến nghị

## Tài liệu Tham khảo Thêm

### Sách
1. **Gonzalez & Woods** - "Digital Image Processing" (4th Edition)
   - Chapter 2: Digital Image Fundamentals
   - Chapter 6: Color Image Processing

2. **Burger & Burge** - "Digital Image Processing: An Algorithmic Introduction"
   - Excellent for understanding algorithms

3. **Pratt** - "Digital Image Processing" (4th Edition)
   - Advanced topics

### Online Resources
1. **OpenCV Documentation**: https://docs.opencv.org/
2. **Scikit-image Documentation**: https://scikit-image.org/
3. **Image Processing Course (Stanford CS231n)**
4. **Wikipedia**: Excellent for definitions và formulas

### Papers
1. Wang et al. (2004) - "Image Quality Assessment: From Error Visibility to Structural Similarity"
2. Keys (1981) - "Cubic convolution interpolation for digital image processing"
3. Rosenfeld & Pfaltz (1966) - "Sequential Operations in Digital Picture Processing"

## FAQ

### Q: Tài liệu này có đủ để hiểu bài tập không?
**A**: Có, kết hợp với code. Đọc theory → đọc code → chạy code → quan sát kết quả.

### Q: Tôi nên bắt đầu từ đâu?
**A**: Bắt đầu từ 01-sampling-quantization.md, sau đó làm theo thứ tự bài tập.

### Q: Code khó hiểu, làm sao?
**A**:
1. Đọc theory trước
2. Đọc docstring và comments trong code
3. Chạy code và debug từng bước
4. Tham khảo OpenCV docs

### Q: Tôi muốn tìm hiểu sâu hơn?
**A**: Đọc references ở cuối mỗi theory document, đặc biệt Gonzalez & Woods.

### Q: Metrics nào quan trọng nhất?
**A**: **SSIM** - correlation tốt nhất với human perception. Nhưng vẫn nên biết tất cả.

### Q: Color space nào dùng để detect skin?
**A**: **YCrCb** tốt nhất, hoặc kết hợp với HSV.

### Q: Interpolation method nào cho zooming?
**A**: **INTER_CUBIC** cho quality, **INTER_LINEAR** cho speed.

### Q: 4-connectivity hay 8-connectivity?
**A**: Tùy ứng dụng. 8-conn cho general purpose, 4-conn cho strict grid.

## Kết luận

Tài liệu này cung cấp:
- ✅ 6 tài liệu lý thuyết đầy đủ và chi tiết
- ✅ Công thức toán học và code examples
- ✅ Best practices và ứng dụng thực tế
- ✅ So sánh ưu nhược điểm các phương pháp
- ✅ Hướng dẫn cách học hiệu quả

**Phương pháp học được khuyến nghị**:
```
Theory → Code → Execution → Analysis → Understanding
```

**Chúc bạn học tốt!**

---

**Liên hệ**: Nếu có thắc mắc, vui lòng tạo issue hoặc liên hệ giảng viên.

**License**: Tài liệu học tập, code mẫu thuộc bản quyền TS. Phan Thanh Toàn.
