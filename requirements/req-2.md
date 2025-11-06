# REQ-2: Giải Câu Hỏi Trắc Nghiệm Xử Lý Ảnh

## Context
Giải tất cả các câu hỏi trắc nghiệm từ file "CAU HOI TRAC NGHIEM XU LY ANH-1-1-25(N03).pdf" bao gồm các chủ đề:
- Toán tử Laplacian và đạo hàm
- Biến đổi Fourier
- Lọc ảnh (low-pass, high-pass filters)
- Morphological operations (erosion, dilation)
- Histogram equalization
- Image transformations (logarithmic, power-law)
- Image interpolation (nearest neighbor, bilinear)
- Connected components
- Image quality metrics (MSE, PSNR, SSIM)

## Objectives
1. Phân tích và giải từng câu hỏi trong PDF
2. Giải thích lý thuyết đằng sau mỗi câu hỏi
3. Tạo tài liệu tổng hợp đáp án và giải thích

---

## Danh Sách Câu Hỏi

### Câu 1: Laplacian Operator (2 câu tương tự)
**Đề bài:**
- Cho ảnh A và kernel Laplacian
- Tính giá trị của đạo hàm bậc hai trên toán tử Laplacian
- Sử dụng padding mode = 'edge'

**Input:**
- Ảnh A 1: `[[10,25,30], [30,20,15], [25,60,30]]`
- Ảnh A 2: `[[50,10,10], [45,15,15], [60,20,20]]`
- Kernel: `[[0,1,0], [1,-4,1], [0,1,0]]`

**Options:**
- A, B, C, D (các ma trận kết quả khác nhau)

**Cách giải:**
1. Apply padding 'edge' cho ảnh
2. Áp dụng convolution với kernel Laplacian
3. So sánh kết quả với các options

---

### Câu 2: Biến Đổi Fourier - Tập Trung Phổ
**Đề bài:** Khi thực hiện biến đổi Fourier 2D của một ảnh, nếu ta thấy năng lượng phổ tập trung ở vùng trung tâm, ảnh đó có đặc trưng gì?

**Options:**
- A. Ảnh có nhiều chi tiết nhỏ, nhiều biên cạnh
- B. Ảnh bị nhiễu mạnh
- C. Ảnh có vùng mượt, ít chi tiết
- D. Ảnh đã được làm mượt hơn

**Đáp án:** C (năng lượng tập trung ở tần số thấp → ảnh mượt, ít chi tiết)

---

### Câu 3: Butterworth Low-pass Filter
**Đề bài:** Lý do chính khiến bộ lọc Butterworth được ưa dùng hơn bộ lọc thông thấp lý tưởng (Ideal Low-pass Filter) là gì?

**Options:**
- A. Giữ lại chi tiết tốt hơn ở vùng tần số cao
- B. Có biên cắt gắt hơn
- C. Giảm hiện tượng rung nhờ vùng chuyển tiếp mượt
- D. Tính toán nhanh hơn

**Đáp án:** C (Butterworth có transition mượt, tránh ringing artifact)

---

### Câu 4: Spectral Leakage
**Đề bài:** Hiện tượng "tò n phổ" (spectral leakage) xảy ra khi nào?

**Options:**
- A. Khi ảnh chứa nhiều tần số cao
- B. Khi tín hiệu không được nhận với cửa sổ giới hạn
- C. Khi thực hiện FFT với kích thước nhỏ hơn ảnh
- D. Khi dùng cửa sổ hình chữ nhật (Rectangular window)

**Đáp án:** D (Rectangular window gây spectral leakage)

---

### Câu 5: High-Pass Filter Design
**Đề bài:** Khi thiết kế bộ lọc thông cao bằng DFT, thành phần nào của phổ tần sẽ bị triệt?

**Options:**
- A. Vùng trung tâm phổ
- B. Vùng biên ngoài phổ
- C. Các giá trị pha
- D. Thành phần DC

**Đáp án:** A và D (DC component ở trung tâm phổ, tần số thấp bị triệt)

---

### Câu 6: Laplacian vs Fourier
**Đề bài:** Trong lọc Laplacian, nếu ta cộng ảnh gốc với kết quả Laplacian (thay vì trừ), ảnh sẽ có đặc điểm gì?

**Options:**
- A. Bị mờ đi
- B. Sáng hơn toàn cục
- C. Bi đảo chiều biên
- D. Bi tăng nhiễu

**Đáp án:** B (cộng Laplacian làm sáng toàn cục, tăng cường biên)

---

### Câu 7: Window Functions - FFT
**Đề bài:** Khi ảnh chứa nhiều tần số cao, ảnh đó có đặc trưng gì?

**Options:**
- A. Ảnh chứa nhiều tần số cao
- B. Khi tin hiệu không được nhận với của số giới hạn
- C. Khi thực hiện FFT với kích thước nhỏ hơn ảnh
- D. Khi dùng cửa sổ hình chữ nhật (Rectangular window)

**Đáp án:** A

---

### Câu 8: Window Functions in Image Processing
**Đề bài:** Trong các hàm cửa sổ sau, hàm nào cho độ rò ri phổ thấp nhất nhưng giảm độ phân giải tần số mạnh nhất?

**Options:**
- A. Rectangular
- B. Hamming
- C. Hann
- D. Blackman

**Đáp án:** D (Blackman có spectral leakage thấp nhất nhưng worst frequency resolution)

---

### Câu 9: Morphological Operations - Erosion
**Đề bài:** Xét phần tử cấu trúc B và ảnh A như sau. Kết quả phép A ⊖ B là gì (sử dụng zero padding)?

**Input:**
- Structuring element B (2x2 hoặc pattern)
- Image A (binary image with patterns)

**Cách giải:**
1. Apply erosion với structuring element B
2. So sánh với các options

---

### Câu 10-18: Morphological Operations (Multiple Questions)
**Các phép toán:**
- A ⊖ B (Erosion)
- A ⊕ B (Dilation)
- (A ⊕ B) ⊖ B (Closing)
- (A ⊖ B) ⊕ B (Opening)

**Cách giải chung:**
1. Implement morphological operations
2. Apply với structuring elements khác nhau
3. Verify kết quả

---

### Câu 19: Smoothing Filters
**Đề bài:** Xét ảnh A và bộ lọc làm trơn. Ảnh sau bộ lọc sẽ như thế nào?

**Input:**
- Image A (various matrices)
- Smoothing kernel (averaging filter hoặc Gaussian)

**Options:** Các ma trận kết quả

---

### Câu 20-22: Connected Components
**Đề bài:** Ảnh trên có bao nhiêu vùng liên thông theo kết nối 4 và bao nhiêu vùng theo kết nối 8?

**Input:** Binary images với các connected components

**Options:**
- Số vùng với 4-connectivity
- Số vùng với 8-connectivity

**Cách giải:**
1. Apply connected components labeling
2. Count với 4-connectivity
3. Count với 8-connectivity

---

### Câu 23-24: MSE Calculation
**Đề bài:** Khoảng cách MSE giữa ảnh A và ảnh B bằng bao nhiêu?

**Input:** Hai binary images

**Formula:** MSE = (1/N) × Σ(A - B)²

**Options:** Các giá trị số (0.39, 0.48, 0.52, 0.60, 0.61)

---

### Câu 25: Logarithmic Transformation
**Đề bài:** Một ảnh 8-bit có histogram tập trung ở vùng cường độ thấp (0-70). Nếu áp dụng phép biến đổi logarithmic transformation s = c.log(1+r), điều gì xảy ra với độ tương phản của ảnh?

**Options:**
- A. Độ tương phản ở vùng sáng tăng, vùng tối giảm
- B. Độ tương phản ở vùng tối tăng, vùng sáng giảm
- C. Độ tương phản tăng đều toàn ảnh
- D. Độ tương phản giảm ở mọi vùng

**Đáp án:** B (log transform expands dark regions, compresses bright regions)

---

### Câu 26: Power-Law (Gamma Correction)
**Đề bài:** Cho ảnh gốc r và phép biến đổi power-law (gamma correction): s = c.r^γ. Khi γ = 0.4, kết quả nào dưới đây mô tả ảnh sau biến đổi?

**Options:**
- A. Ảnh tối hơn ảnh gốc
- B. Ảnh sáng hơn ảnh gốc
- C. Ảnh có histogram bị nén về phía giá trị cao
- D. Ảnh có độ tương phân giảm ở vùng sáng

**Đáp án:** B (γ < 1 makes image brighter)

---

### Câu 27: Histogram Equalization
**Đề bài:** Giả sử có ảnh như sau. Khi áp dụng phép cân bằng histogram với số mức xám là 8 thì ảnh mới sẽ như thế nào?

**Input:**
```
1 2 5
6 7 7
1 1 0
```

**Options:** Various transformed matrices

**Cách giải:**
1. Calculate histogram
2. Calculate CDF
3. Apply histogram equalization
4. Map to 8 levels

---

### Câu 28-29: Histogram Equalization (More Examples)
Similar to Câu 27 with different input images

---

### Câu 30: Image Interpolation - Nearest Neighbor
**Đề bài:** Nếu sử dụng phép nội suy Nearest neighbor interpolation để tạo ra ảnh 7x7 thì ảnh mới là gì?

**Input:** Small binary image

**Options:** Enlarged images

**Cách giải:**
1. Apply nearest neighbor interpolation
2. Scale from original size to 7x7

---

### Câu 31: Image Interpolation - Bilinear (7x7)
**Đề bài:** Nếu sử dụng phép nội suy Bilinear interpolation để tạo ra ảnh 7x7 thì ảnh mới là gì?

**Input:** Small binary image

---

### Câu 32: Image Interpolation - Bilinear (3x3)
**Đề bài:** Nếu sử dụng phép nội suy Bilinear interpolation để tạo ra ảnh 3x3 thì ảnh mới là gì?

**Input:** Small binary image (2x2 or similar)

---

## Task Breakdown

### Phase 1: Setup Project Structure
```
requirements/
└── req-2-solutions/
    ├── theory/
    │   ├── laplacian-operators.md
    │   ├── fourier-transforms.md
    │   ├── morphological-operations.md
    │   ├── histogram-equalization.md
    │   ├── image-transformations.md
    │   └── interpolation-methods.md
    └── answers/
        └── all_answers.md
```

### Phase 2: Theory Documentation

**File:** `theory/laplacian-operators.md`
```markdown
# Toán Tử Laplacian

## Định nghĩa
Laplacian là toán tử đạo hàm bậc hai, phát hiện biên trong ảnh.

## Kernel chuẩn
```
0   1   0
1  -4   1
0   1   0
```

## Padding Modes
- zero: Pad với 0
- edge: Pad với giá trị biên
- reflect: Pad phản xạ
- wrap: Pad wrap-around

## Ứng dụng
- Edge detection
- Image sharpening
- Feature enhancement
```

**File:** `theory/fourier-transforms.md`
```markdown
# Biến Đổi Fourier

## Năng lượng tập trung vùng trung tâm
- Tần số thấp → Ảnh mượt, ít chi tiết
- Tần số cao → Ảnh nhiều chi tiết, biên cạnh

## Low-pass vs High-pass Filters
- Low-pass: Giữ tần số thấp, loại tần số cao → Làm mượt
- High-pass: Giữ tần số cao, loại tần số thấp → Tăng cường biên

## Butterworth Filter
- Transition mượt hơn Ideal filter
- Tránh ringing artifacts
- Order càng cao càng giống Ideal filter
```

**File:** `theory/morphological-operations.md`
```markdown
# Morphological Operations

## Erosion (⊖)
- Shrinks objects
- Removes small objects
- Breaks narrow connections

## Dilation (⊕)
- Expands objects
- Fills holes
- Connects nearby objects

## Opening: (A ⊖ B) ⊕ B
- Removes small objects
- Smooths boundaries

## Closing: (A ⊕ B) ⊖ B
- Fills holes
- Connects nearby objects
```

**File:** `theory/histogram-equalization.md`
```markdown
# Histogram Equalization

## Algorithm
1. Calculate histogram
2. Calculate CDF (Cumulative Distribution Function)
3. Normalize CDF: CDF_norm = (CDF - CDF_min) / (total_pixels - CDF_min) × (L - 1)
4. Map old values to new values using CDF_norm

## Effect
- Spreads out intensity values
- Increases global contrast
- May amplify noise
```

**File:** `theory/image-transformations.md`
```markdown
# Image Transformations

## Logarithmic: s = c × log(1 + r)
- Expands dark regions
- Compresses bright regions
- Good for images with large dynamic range

## Power-law (Gamma): s = c × r^γ
- γ < 1: Brightens image (expands dark, compresses bright)
- γ > 1: Darkens image (compresses dark, expands bright)
- γ = 1: No change
```

**File:** `theory/interpolation-methods.md`
```markdown
# Image Interpolation Methods

## Nearest Neighbor
- Fastest
- Blocky results
- No new pixel values created

## Bilinear
- Smoother than nearest neighbor
- Averages 4 nearest pixels
- May blur edges

## Bicubic
- Smoothest
- Uses 16 nearest pixels
- Best quality but slowest
```

### Phase 3: Compile All Answers

**File:** `answers/all_answers.md`

Create comprehensive answer sheet with:
1. Question number
2. Correct answer (A, B, C, or D)
3. Brief explanation
4. Reference to theory documentation

---

## Summary Checklist

### Theory Documentation
- [ ] Laplacian operators
- [ ] Fourier transforms
- [ ] Morphological operations
- [ ] Histogram equalization
- [ ] Image transformations
- [ ] Interpolation methods

### Answer Compilation
- [ ] All 32 questions answered
- [ ] Explanations provided
- [ ] Cross-referenced with theory

---

## Notes
- Focus on understanding the theory behind each question
- Provide clear explanations for each answer
- Reference relevant theory documentation for deeper understanding
