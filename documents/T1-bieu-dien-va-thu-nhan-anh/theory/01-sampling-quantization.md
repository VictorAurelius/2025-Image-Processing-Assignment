# Lý thuyết: Lấy Mẫu và Lượng Tử Hóa (Sampling & Quantization)

## 1. Giới thiệu

Ảnh số (digital image) được tạo ra từ ảnh tương tự (analog image) thông qua hai quá trình:
1. **Lấy mẫu (Sampling)**: Rời rạc hóa tọa độ không gian
2. **Lượng tử hóa (Quantization)**: Rời rạc hóa giá trị mức xám

## 2. Lấy Mẫu (Sampling)

### 2.1. Định nghĩa
Lấy mẫu là quá trình chia ảnh liên tục thành một lưới các pixel rời rạc.

**Ảnh liên tục**: f(x, y) với x, y ∈ ℝ
**Ảnh rời rạc**: f[i, j] với i, j ∈ ℤ

### 2.2. Độ phân giải không gian (Spatial Resolution)
- Số lượng pixel trong ảnh: M × N
  - M: số hàng (height)
  - N: số cột (width)
- Mật độ pixel: DPI (Dots Per Inch) hoặc PPI (Pixels Per Inch)

**Ví dụ**:
- 720p: 1280 × 720 pixels
- 1080p (Full HD): 1920 × 1080 pixels
- 4K (UHD): 3840 × 2160 pixels

### 2.3. Định lý Nyquist-Shannon
Để tránh hiện tượng aliasing khi lấy mẫu:

```
f_sampling >= 2 × f_max
```

Trong đó:
- f_sampling: Tần số lấy mẫu
- f_max: Tần số cao nhất trong tín hiệu gốc

**Ý nghĩa**: Cần lấy mẫu ít nhất 2 lần tần số cao nhất để tái tạo lại tín hiệu.

### 2.4. Aliasing
**Hiện tượng**: Khi lấy mẫu không đủ dày, chi tiết cao tần bị méo thành chi tiết thấp tần.

**Ví dụ**:
- Bánh xe quay trong phim có vẻ quay ngược
- Đường kẻ chéo bị răng cưa (jagged edges)

**Giải pháp**:
- Tăng tần số lấy mẫu
- Dùng anti-aliasing filter trước khi lấy mẫu

## 3. Lượng Tử Hóa (Quantization)

### 3.1. Định nghĩa
Lượng tử hóa là quá trình chuyển giá trị liên tục của mức xám thành các giá trị rời rạc.

**Ảnh liên tục**: I(x, y) ∈ [0, ∞)
**Ảnh lượng tử hóa**: I_q(x, y) ∈ {0, 1, 2, ..., L-1}

### 3.2. Độ phân giải mức xám (Gray-level Resolution)
Số lượng mức xám có thể biểu diễn:

```
L = 2^k
```

Trong đó:
- L: Số mức xám
- k: Số bit dùng để biểu diễn (bit-depth)

**Ví dụ**:
- k = 1 bit: L = 2 (nhị phân: 0, 1)
- k = 4 bit: L = 16 (0-15)
- k = 8 bit: L = 256 (0-255) - Tiêu chuẩn
- k = 10 bit: L = 1024 (0-1023)
- k = 12 bit: L = 4096 (0-4095)
- k = 16 bit: L = 65536 (0-65535)

### 3.3. Lượng tử hóa đều (Uniform Quantization)
Chia khoảng giá trị thành L khoảng bằng nhau:

```
Δ = (I_max - I_min) / L
```

**Thuật toán**:
```python
# Normalize to [0, 1]
normalized = (img - img.min()) / (img.max() - img.min())

# Quantize
quantized_index = round(normalized * (L - 1))

# Reconstruct
reconstructed = quantized_index / (L - 1) * (img.max() - img.min()) + img.min()
```

### 3.4. Sai số lượng tử hóa (Quantization Error)
```
e(i, j) = I_q(i, j) - I(i, j)
```

**Đặc điểm**:
- Sai số tối đa: ±Δ/2
- Giảm k → tăng Δ → tăng sai số
- Xuất hiện hiệu ứng "false contour" (đường viền giả)

### 3.5. Hiệu ứng Posterization
Khi k quá nhỏ, ảnh có vẻ như poster với các vùng màu phẳng rõ ràng.

**Nguyên nhân**: Không đủ mức xám để biểu diễn gradient mượt

## 4. Trade-off giữa Sampling và Quantization

### 4.1. Kích thước file
```
Size = M × N × k (bits)
     = M × N × k / 8 (bytes)
```

**Ví dụ**: Ảnh 1920×1080, 8-bit:
```
Size = 1920 × 1080 × 8 / 8 = 2,073,600 bytes ≈ 2 MB
```

### 4.2. So sánh

| Yếu tố | Ảnh hưởng | Trade-off |
|--------|-----------|-----------|
| M × N ↑ | Tăng chi tiết không gian | Tăng dung lượng theo O(MN) |
| k ↑ | Tăng chi tiết mức xám | Tăng dung lượng tuyến tính |
| M × N ↓ | Mất chi tiết, blur, blocky | Giảm dung lượng |
| k ↓ | False contour, posterization | Giảm dung lượng |

### 4.3. Quy tắc thumb
- **Spatial**: Tăng resolution quan trọng hơn nếu cần chi tiết hình học
- **Quantization**: Tăng bit-depth quan trọng hơn nếu cần gradient mượt
- **Cân bằng**: 8-bit thường đủ cho mắt người; resolution tùy ứng dụng

## 5. Ứng dụng thực tế

### 5.1. Photography
- **JPEG**: 8-bit per channel (24-bit RGB)
- **RAW**: 12-14 bit per channel
- **Lý do**: RAW cần dynamic range cao cho post-processing

### 5.2. Medical Imaging
- **X-ray**: 10-16 bit
- **CT/MRI**: 12-16 bit
- **Lý do**: Cần chi tiết mức xám cao để phân biệt mô

### 5.3. Video Streaming
- **SD**: 480p, 8-bit
- **HD**: 720p/1080p, 8-bit
- **4K HDR**: 3840×2160, 10-bit
- **Lý do**: Trade-off giữa chất lượng và băng thông

### 5.4. Surveillance
- **Resolution**: 720p-4K tùy yêu cầu
- **Bit-depth**: 8-bit thường đủ
- **FPS**: 15-30 fps
- **Lý do**: Cân bằng giữa chi tiết, storage, băng thông

## 6. Công thức quan trọng

### 6.1. Kích thước ảnh
```
Total pixels = M × N
Total bits = M × N × k
Total bytes = M × N × k / 8
```

### 6.2. Số mức xám
```
L = 2^k
k = log₂(L)
```

### 6.3. Bandwidth (video)
```
Bandwidth (bps) = M × N × k × fps
Bandwidth (Mbps) = M × N × k × fps / (1024 × 1024)
```

### 6.4. Storage (video)
```
Storage (bytes) = M × N × k × fps × duration / 8
```

## 7. Bài tập áp dụng

### Bài 1
Ảnh 1920×1080, 8-bit, cần lưu 30 ngày, 25 fps.
Tính dung lượng cần thiết?

**Giải**:
```
Storage = 1920 × 1080 × 8 × 25 × (30 × 24 × 3600) / 8
        = 1920 × 1080 × 25 × 2,592,000 bytes
        ≈ 126 TB (không nén)
```

→ **Kết luận**: Cần nén (H.264/H.265) để giảm ~95%

### Bài 2
Giảm từ 8-bit xuống 4-bit, mất bao nhiêu % mức xám?

**Giải**:
```
8-bit: L = 256 mức
4-bit: L = 16 mức
Mất: (256 - 16) / 256 = 93.75%
```

## 8. Tóm tắt

| Khái niệm | Định nghĩa | Công thức | Ảnh hưởng |
|-----------|-----------|-----------|-----------|
| Sampling | Rời rạc hóa không gian | M × N | Chi tiết hình học |
| Quantization | Rời rạc hóa mức xám | L = 2^k | Gradient, màu sắc |
| Spatial Resolution | Số pixel | M × N | Càng cao càng chi tiết |
| Gray-level Resolution | Số mức xám | 2^k | Càng cao càng mượt |
| File Size | Dung lượng | M×N×k bits | Tăng theo M, N, k |

## 9. References

1. Gonzalez & Woods - "Digital Image Processing" (Chapter 2)
2. Burger & Burge - "Digital Image Processing: An Algorithmic Introduction"
3. OpenCV Documentation
4. IEEE Standards for Image Coding

---

**Lưu ý**: Tài liệu này phục vụ mục đích học tập cho môn Xử lý Ảnh.
