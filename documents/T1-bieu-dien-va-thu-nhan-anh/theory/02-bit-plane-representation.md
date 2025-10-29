# Lý thuyết: Biểu diễn Bit-Plane (Bit-plane Representation)

## 1. Giới thiệu

Mỗi pixel trong ảnh xám k-bit có thể được phân tách thành k bit-planes (mặt phẳng bit), mỗi plane chứa 1 bit thông tin từ tất cả các pixel.

## 2. Khái niệm cơ bản

### 2.1. Biểu diễn nhị phân
Pixel 8-bit có giá trị [0, 255] được biểu diễn bằng 8 bit:

```
Pixel value = b₇×2⁷ + b₆×2⁶ + b₅×2⁵ + b₄×2⁴ + b₃×2³ + b₂×2² + b₁×2¹ + b₀×2⁰
```

**Ví dụ**:
- 150₁₀ = 10010110₂
- bit 7 (MSB): 1, bit 0 (LSB): 0

### 2.2. Bit-plane
- **Bit-plane i**: Ảnh nhị phân chứa bit thứ i từ tất cả pixel
- **MSB (Most Significant Bit)**: Bit 7 - quan trọng nhất
- **LSB (Least Significant Bit)**: Bit 0 - ít quan trọng nhất

## 3. Tách Bit-planes

### 3.1. Thuật toán
```python
def extract_bitplane(img, bit_position):
    """Tách bit-plane thứ bit_position"""
    return (img >> bit_position) & 1
```

**Giải thích**:
- `img >> bit_position`: Dịch phải bit_position vị trí
- `& 1`: Lấy bit cuối cùng (AND với 00000001)

### 3.2. Ví dụ
Pixel value = 150 = 10010110₂

```
Bit 7: (150 >> 7) & 1 = 1
Bit 6: (150 >> 6) & 1 = 0
Bit 5: (150 >> 5) & 1 = 0
Bit 4: (150 >> 4) & 1 = 1
Bit 3: (150 >> 3) & 1 = 0
Bit 2: (150 >> 2) & 1 = 1
Bit 1: (150 >> 1) & 1 = 1
Bit 0: (150 >> 0) & 1 = 0
```

## 4. Đặc điểm các Bit-planes

### 4.1. MSB (Bit 7-4)
**Đặc điểm**:
- Chứa thông tin cấu trúc chính
- Thay đổi chậm giữa các pixel liền kề
- Chứa các biên và hình dạng chính
- Ít nhiễu

**Giá trị đóng góp**:
- Bit 7: 128 (50% giá trị)
- Bit 6: 64 (25%)
- Bit 5: 32 (12.5%)
- Bit 4: 16 (6.25%)

### 4.2. LSB (Bit 3-0)
**Đặc điểm**:
- Chứa chi tiết mịn và nhiễu
- Thay đổi nhanh giữa các pixel
- Có vẻ ngẫu nhiên (noise-like)
- Ít ảnh hưởng đến nhận thức

**Giá trị đóng góp**:
- Bit 3: 8 (3.125%)
- Bit 2: 4 (1.56%)
- Bit 1: 2 (0.78%)
- Bit 0: 1 (0.39%)

## 5. Tái dựng ảnh từ Bit-planes

### 5.1. Tái dựng đầy đủ
```python
reconstructed = sum(bitplane[i] << i for i in range(8))
```

### 5.2. Tái dựng từ MSB (bit 4-7)
```python
reconstructed = sum(bitplane[i] << i for i in range(4, 8))
```

**Hiệu quả**:
- Chỉ dùng 50% thông tin
- Giữ được ~93.75% giá trị (128+64+32+16 = 240/255)
- Mất chi tiết mịn nhưng cấu trúc chính còn nguyên

## 6. Ứng dụng

### 6.1. Nén ảnh
- Loại bỏ LSB để giảm dung lượng
- Chỉ lưu MSB (4-6 bit thay vì 8 bit)
- Loss minimal nhưng tiết kiệm 25-50% dung lượng

### 6.2. Phát hiện nhiễu
- Nhiễu tập trung ở LSB
- Quan sát bit-plane 0-3 để nhận diện loại nhiễu
- Salt & pepper noise rất rõ ở LSB

### 6.3. Steganography (Giấu tin)
- Giấu thông tin bí mật trong LSB
- Thay đổi LSB ít ảnh hưởng đến ảnh gốc
- Mắt người khó phát hiện

**Ví dụ**:
```python
# Giấu 1 bit message vào LSB của pixel
pixel_original = 150  # 10010110
message_bit = 1
pixel_stego = (pixel_original & 0xFE) | message_bit  # 10010111 = 151
# Chênh lệch: ±1, không nhận biết được
```

### 6.4. Watermarking
- Nhúng watermark vào bit-plane trung bình (bit 3-5)
- Trade-off giữa robust và invisible
- Khó bị loại bỏ nhưng vẫn khó nhận thấy

### 6.5. Phân tích ảnh
- Phát hiện tampering (chỉnh sửa ảnh)
- Phân tích histogram của từng bit-plane
- LSB thường có phân phối đều nếu ảnh tự nhiên

## 7. Bit-plane Slicing trong thực tế

### 7.1. Image Enhancement
```python
# Loại bỏ nhiễu bằng cách reset LSB
img_denoised = img & 0xF0  # Chỉ giữ 4 bit cao
```

### 7.2. Thresholding dựa trên bit
```python
# Ngưỡng tại bit 7
threshold = img & 0x80  # Chỉ lấy bit 7
binary = threshold > 0
```

## 8. So sánh với các phương pháp khác

| Phương pháp | Mục đích | Ưu điểm | Nhược điểm |
|-------------|----------|---------|------------|
| Bit-plane slicing | Phân tích/nén | Dễ hiểu, nhanh | Không tối ưu nén |
| Quantization | Giảm bit-depth | Điều chỉnh được | Mất toàn bộ LSB |
| DCT (JPEG) | Nén | Hiệu quả cao | Phức tạp |
| Wavelet | Nén/phân tích | Đa scale | Phức tạp |

## 9. Công thức quan trọng

### 9.1. Trích xuất bit
```
bit_i = (pixel >> i) & 1
```

### 9.2. Tái dựng
```
pixel = Σ(bit_i × 2^i) for i = 0 to k-1
```

### 9.3. Đóng góp của bit i
```
Contribution = 2^i / (2^k - 1) × 100%
```

## 10. Thí nghiệm minh họa

### Thí nghiệm 1: Tách bit-planes
```
Input: Ảnh 8-bit
Output: 8 ảnh nhị phân (bit-planes 0-7)
Quan sát:
- Bit 7: Rõ nét, cấu trúc chính
- Bit 6-5: Chi tiết quan trọng
- Bit 4-3: Chi tiết mịn
- Bit 2-0: Nhiễu, ngẫu nhiên
```

### Thí nghiệm 2: Tái dựng từ MSB
```
Bit 7 only: 50% thông tin, nhận diện được cấu trúc
Bit 7-6: 75%, khá rõ
Bit 7-5: 87.5%, tốt
Bit 7-4: 93.75%, rất tốt
```

### Thí nghiệm 3: Ảnh hưởng LSB
```
Thay đổi bit 0: Khó nhận biết (±1/255)
Thay đổi bit 1: Khó nhận biết (±2/255)
Thay đổi bit 2: Bắt đầu nhận biết (±4/255)
Thay đổi bit 3: Rõ ràng (±8/255)
```

## 11. Bài tập

### Bài 1
Pixel = 200. Tách thành 8 bit-planes. Bit nào có giá trị 1?

**Giải**:
```
200 = 11001000₂
Bit có giá trị 1: bit 7, 6, 3
```

### Bài 2
Nếu chỉ giữ bit 7-5, mất bao nhiêu % thông tin?

**Giải**:
```
Giữ: 128 + 64 + 32 = 224 (87.8% của 255)
Mất: 255 - 224 = 31 (12.2%)
```

## 12. Tóm tắt

| Bit Planes | Nội dung | Ứng dụng |
|------------|----------|----------|
| Bit 7-6 (MSB) | Cấu trúc chính | Nén, phân tích |
| Bit 5-4 | Chi tiết quan trọng | Cân bằng chất lượng/dung lượng |
| Bit 3-2 | Chi tiết mịn | Watermarking |
| Bit 1-0 (LSB) | Nhiễu, chi tiết cực mịn | Steganography, phát hiện nhiễu |

**Key Point**: MSB chứa cấu trúc, LSB chứa nhiễu và chi tiết mịn.

---

**References**:
- Gonzalez & Woods - Digital Image Processing (Chapter 2.6)
- Information Hiding Techniques: A Tutorial Review
