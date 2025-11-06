# REQ-2 Solutions: Giải Câu Hỏi Trắc Nghiệm Xử Lý Ảnh

## Tổng Quan

Đây là tài liệu giải chi tiết cho **32 câu hỏi trắc nghiệm** từ đề thi "CAU HOI TRAC NGHIEM XU LY ANH-1-1-25(N03).pdf"

## Cấu Trúc

```
req-2-solutions/
├── theory/                    # Tài liệu lý thuyết
│   ├── laplacian-operators.md
│   ├── fourier-transforms.md
│   ├── morphological-operations.md
│   ├── histogram-equalization.md
│   ├── image-transformations.md
│   └── interpolation-methods.md
├── answers/                   # Đáp án và giải thích
│   └── all_answers.md
└── README.md                  # File này
```

## Nội Dung

### 📚 Theory Documents (6 files)

#### 1. Laplacian Operators
**File:** `theory/laplacian-operators.md`

**Nội dung:**
- Định nghĩa toán tử Laplacian
- Các kernel variants (3×3, 8-neighbor)
- Padding modes (zero, edge, reflect, wrap)
- Ví dụ tính toán chi tiết
- Ứng dụng: Edge detection, Sharpening
- So sánh với Gradient
- Laplacian of Gaussian (LoG)

**Áp dụng cho:** Câu 1-3, Câu 8

---

#### 2. Fourier Transforms
**File:** `theory/fourier-transforms.md`

**Nội dung:**
- DFT và FFT
- Phân bố năng lượng trong frequency domain
- Tần số thấp vs tần số cao
- Low-pass filters: Ideal, Butterworth, Gaussian
- High-pass filters
- Spectral leakage và window functions
- Convolution theorem
- Phase vs Magnitude

**Áp dụng cho:** Câu 4-7

---

#### 3. Morphological Operations
**File:** `theory/morphological-operations.md`

**Nội dung:**
- Structuring Elements
- Erosion (⊖): Shrinks objects
- Dilation (⊕): Expands objects
- Opening (⊖ → ⊕): Removes small objects
- Closing (⊕ → ⊖): Fills small holes
- Morphological Gradient, Top/Black Hat
- Properties: Duality, Idempotence
- Grayscale morphology
- Connected components relationship

**Áp dụng cho:** Câu 9-18

---

#### 4. Histogram Equalization
**File:** `theory/histogram-equalization.md`

**Nội dung:**
- Định nghĩa histogram và CDF
- Thuật toán Histogram Equalization (4 bước)
- Ví dụ tính toán chi tiết (3×3 → 8 levels)
- Ưu/nhược điểm
- Adaptive Histogram Equalization (CLAHE)
- Histogram Matching
- Color image equalization (HSV, YCbCr)

**Áp dụng cho:** Câu 27-29

---

#### 5. Image Transformations
**File:** `theory/image-transformations.md`

**Nội dung:**
- Log transformation: `s = c × log(1 + r)`
  - Expands dark, compresses bright
- Power-law (Gamma): `s = c × r^γ`
  - γ < 1: Brightens
  - γ > 1: Darkens
- Ảnh hưởng lên histogram
- So sánh các phương pháp
- Gamma correction cho monitors

**Áp dụng cho:** Câu 25-26

---

#### 6. Interpolation Methods
**File:** `theory/interpolation-methods.md`

**Nội dung:**
- Nearest Neighbor:
  - Fastest, blocky, no new values
- Bilinear:
  - 4 neighbors, smooth, weighted average
- Bicubic:
  - 16 neighbors, highest quality
- Area interpolation (downsampling)
- Công thức chi tiết và ví dụ
- So sánh performance và quality
- Edge effects

**Áp dụng cho:** Câu 30-32

---

### ✅ All Answers
**File:** `answers/all_answers.md`

**Nội dung:** Giải chi tiết **32 câu hỏi**, bao gồm:

1. **Câu hỏi gốc** (với input data)
2. **Các options** (A, B, C, D)
3. **Đáp án đúng**
4. **Giải thích chi tiết**:
   - Step-by-step calculation (nếu có)
   - Visual explanation
   - Reference tới theory documents
5. **Key takeaways**

#### Phân Bố Câu Hỏi:

| Chủ Đề | Câu Hỏi | Độ Khó |
|--------|---------|--------|
| **Laplacian** | 1-3, 8 | Trung bình |
| **Fourier & Filtering** | 4-7 | Dễ-Trung bình |
| **Morphology** | 9-18 | Trung bình |
| **Smoothing** | 19 | Dễ |
| **Connected Components** | 20-22 | Dễ |
| **MSE** | 23-24 | Dễ |
| **Image Transforms** | 25-26 | Trung bình |
| **Histogram Equalization** | 27-29 | Khó |
| **Interpolation** | 30-32 | Trung bình |

---

## Cách Sử Dụng

### 1. Học Lý Thuyết
```bash
# Đọc từng theory document theo thứ tự:
1. laplacian-operators.md
2. fourier-transforms.md
3. morphological-operations.md
4. histogram-equalization.md
5. image-transformations.md
6. interpolation-methods.md
```

### 2. Làm Bài Tập
```bash
# Mở all_answers.md
# Đọc câu hỏi → Thử tự giải → Check đáp án
```

### 3. Ôn Tập
```bash
# Quick review:
- Đọc phần "Key Takeaways" trong all_answers.md
- Ôn lại công thức quan trọng
- Practice tính toán tay cho các câu computational
```

---

## Highlights

### 🔑 Key Concepts

#### Laplacian:
- Edge padding mode ảnh hưởng đến kết quả
- Zero-sum kernel → detects rapid changes
- Sharpening = original - Laplacian

#### Fourier:
- **Tần số thấp** (center) = ảnh mượt
- **Tần số cao** (edges) = chi tiết, biên cạnh
- **Butterworth** > Ideal vì giảm ringing

#### Morphology:
- **Erosion**: Shrinks, removes small objects
- **Dilation**: Expands, fills holes
- **Opening**: ⊖ then ⊕ = remove noise
- **Closing**: ⊕ then ⊖ = fill holes

#### Histogram Equalization:
- Algorithm: Histogram → CDF → Normalize → Map
- Spreads out intensity distribution
- Increases global contrast

#### Image Transforms:
- **Log**: Expands dark, compresses bright
- **γ < 1**: Brightens
- **γ > 1**: Darkens

#### Interpolation:
- **Nearest**: Blocky, fast
- **Bilinear**: Smooth, 4 neighbors
- **Bicubic**: Best quality, 16 neighbors

---

## Công Thức Quan Trọng

### Laplacian:
```
Standard kernel:
 0   1   0
 1  -4   1
 0   1   0
```

### MSE:
```
MSE = (1/N) × Σ(A - B)²
```

### Log Transform:
```
s = c × log(1 + r)
```

### Power-Law (Gamma):
```
s = c × r^γ
```

### Histogram Equalization:
```
new_value = round((CDF(old) - CDF_min) / (n - CDF_min) × (L - 1))
```

### Bilinear Interpolation:
```
f(x,y) = (1-dx)(1-dy)×f(x0,y0) + dx(1-dy)×f(x1,y0) +
         (1-dx)dy×f(x0,y1) + dx×dy×f(x1,y1)
```

---

## Tips & Tricks

### Khi Làm Bài Thi:

1. **Đọc kỹ đề:**
   - Padding mode? (zero, edge, replicate)
   - Số levels? (8, 256)
   - Interpolation method? (nearest, bilinear)

2. **Eliminate wrong answers:**
   - Check magnitude (quá lớn/nhỏ?)
   - Check pattern (blocky vs smooth?)
   - Check signs (positive vs negative?)

3. **Visual thinking:**
   - Draw it out nếu cần
   - Morphology: Think about shape changes
   - Interpolation: Smooth vs blocky

4. **Practice calculations:**
   - Laplacian convolution
   - Histogram equalization CDF
   - Bilinear weights

5. **Remember key rules:**
   - Erosion shrinks, dilation expands
   - Low freq = center = smooth
   - γ < 1 brightens, γ > 1 darkens
   - 8-connectivity ≤ 4-connectivity (số vùng)

---

## Tham Khảo

### Textbooks:
- **Digital Image Processing** (Gonzalez & Woods) - Bible của Image Processing
- **Computer Vision: Algorithms and Applications** (Szeliski)
- **The Fourier Transform and Its Applications** (Bracewell)

### Online Resources:
- OpenCV Documentation
- scikit-image Documentation
- Wikipedia: Image Processing topics

### Tools:
- OpenCV: `cv2.filter2D()`, `cv2.morphologyEx()`, `cv2.resize()`
- NumPy: `np.convolve()`, `np.histogram()`, `np.log()`, `np.power()`
- scikit-image: `skimage.morphology`, `skimage.transform`

---

## Status

✅ **Hoàn thành:** 100%
- 6/6 Theory documents
- 32/32 Câu hỏi được giải
- Comprehensive explanations
- Cross-referenced với theory

**Date:** 2025-01-06
**Version:** 1.0

---

## Liên Hệ

Nếu có thắc mắc hoặc phát hiện lỗi, vui lòng tạo issue trong repository.

---

**Good luck với kỳ thi! 🎓**
