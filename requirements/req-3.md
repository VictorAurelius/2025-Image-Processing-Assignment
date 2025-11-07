# REQ-3: Giải Đề Cương Ôn Tập 2024

## Context
Giải tất cả câu hỏi và bài tập từ file "đề-cương-ôn-tập-2024.pdf" bao gồm:
- **Phần 1**: 12 câu hỏi lý thuyết
- **Phần 2**: 7 dạng bài tập với data cụ thể

## Objectives
1. Trả lời chi tiết 12 câu hỏi lý thuyết
2. Giải tất cả 7 bài tập với step-by-step explanation
3. Tạo tài liệu tổng hợp kiến thức ôn tập
4. Cung cấp examples và formulas quan trọng

---

## Phần 1: Câu Hỏi Lý Thuyết (12 câu)

### Câu 1: Mô Hình Màu Cơ Bản
**Yêu cầu**: Trình bày các mô hình màu cơ bản trong xử lý ảnh

**Nội dung cần cover**:
- RGB (Red, Green, Blue)
- CMY/CMYK (Cyan, Magenta, Yellow, Black)
- HSV/HSI (Hue, Saturation, Value/Intensity)
- YCbCr, YUV
- Grayscale
- Chuyển đổi giữa các color spaces
- Ứng dụng của từng model

---

### Câu 2: Tăng/Giảm Độ Sáng Ảnh Đa Mức Xám
**Yêu cầu**: Với ảnh đa mức xám thì tăng giảm độ sáng của ảnh như thế nào? Chúng ta phải sử dụng toán tử loại nào để thực hiện phép toán này?

**Nội dung cần cover**:
- Point operations (phép toán điểm)
- Linear transformation: `I_new = α × I_old + β`
  - α: Contrast factor
  - β: Brightness offset
- Gamma correction: `I_new = c × I_old^γ`
- Logarithmic transform
- Piecewise linear transformation
- Ví dụ cụ thể với các công thức

---

### Câu 3: Cân Bằng Tần Suất (Histogram Equalization)
**Yêu cầu**:
- Cân bằng tần suất là gì?
- Tại sao phải cân bằng tần suất?
- Kỹ thuật cân bằng?

**Nội dung cần cover**:
- Định nghĩa histogram
- Mục đích của histogram equalization
- Thuật toán:
  1. Tính histogram
  2. Tính CDF (Cumulative Distribution Function)
  3. Normalize CDF
  4. Map pixels
- Ưu/nhược điểm
- Adaptive Histogram Equalization (CLAHE)
- Ví dụ tính toán chi tiết

---

### Câu 4: Biến Đổi Cửa Sổ Di Chuyển (Convolution)
**Yêu cầu**: Biến đổi cửa sổ di chuyển hay còn gọi là biến đổi cuộn là biến đổi sử dụng toán tử gì? Ý tưởng cơ bản của biến đổi này là gì?

**Nội dung cần cover**:
- Định nghĩa convolution
- Kernel/mask/filter
- Thuật toán convolution 2D
- Padding modes
- Các loại kernel:
  - Smoothing (averaging, Gaussian)
  - Sharpening (Laplacian)
  - Edge detection (Sobel, Prewitt, Roberts)
- Applications
- Ví dụ minh họa

---

### Câu 5: Mô Hình Nhiễu
**Yêu cầu**: Mô hình nhiễu là gì? Các loại nhiễu?

**Nội dung cần cover**:
- Định nghĩa noise trong ảnh
- Các loại nhiễu:
  - **Gaussian noise**: n(x,y) ~ N(μ, σ²)
  - **Salt-and-pepper noise**: Random black/white pixels
  - **Uniform noise**: Equally distributed
  - **Impulse noise**
  - **Speckle noise**: Multiplicative noise
  - **Periodic noise**: Từ electrical/mechanical interference
- Mô hình toán học
- Phương pháp giảm nhiễu cho từng loại

---

### Câu 6: Biên và Kỹ Thuật Phát Hiện Biên
**Yêu cầu**: Biên là gì? Kỹ thuật phát hiện biên?

**Nội dung cần cover**:
- Định nghĩa edge (biên)
- Các loại edges:
  - Step edge
  - Ramp edge
  - Roof edge
  - Line edge
- Gradient-based methods:
  - **Roberts operator** (2×2)
  - **Prewitt operator** (3×3)
  - **Sobel operator** (3×3)
  - **Canny edge detector**
- Laplacian-based methods:
  - Laplacian operator
  - LoG (Laplacian of Gaussian)
- So sánh các phương pháp
- Ví dụ với kernels cụ thể

---

### Câu 7: Nén Ảnh
**Yêu cầu**: Tại sao chúng ta phải nén ảnh? Các kỹ thuật nén ảnh?

**Nội dung cần cover**:
- **Lý do nén**:
  - Giảm dung lượng storage
  - Tăng tốc transmission
  - Bandwidth constraints
- **Phân loại**:
  - **Lossless compression**: Không mất dữ liệu
    - Run-Length Encoding (RLE)
    - Huffman coding
    - LZW (Lempel-Ziv-Welch)
    - Arithmetic coding
  - **Lossy compression**: Có mất dữ liệu
    - JPEG (DCT-based)
    - JPEG2000 (Wavelet-based)
    - Fractal compression
- **Compression ratio**
- **Quality metrics**: PSNR, SSIM
- So sánh các phương pháp

---

### Câu 8: Phương Pháp Lọc Ảnh
**Yêu cầu**: Các phương pháp lọc ảnh trên miền không gian? Lọc trên miền tần số?

**Nội dung cần cover**:

#### Lọc Miền Không Gian (Spatial Domain):
- **Linear filters**:
  - Mean filter (averaging)
  - Gaussian filter
  - Weighted average
- **Non-linear filters**:
  - Median filter
  - Max/Min filters
  - Order-statistic filters
- Convolution với kernels

#### Lọc Miền Tần Số (Frequency Domain):
- Fourier Transform
- **Low-pass filters**:
  - Ideal LPF
  - Butterworth LPF
  - Gaussian LPF
- **High-pass filters**:
  - Ideal HPF
  - Butterworth HPF
  - Gaussian HPF
- **Band-pass/Band-reject filters**
- Convolution theorem: Spatial convolution = Frequency multiplication

---

### Câu 9: Phân Vùng Ảnh
**Yêu cầu**: Khái niệm, ý nghĩa của phân vùng ảnh? Các kỹ thuật phân vùng ảnh?

**Nội dung cần cover**:
- **Định nghĩa**: Image segmentation là quá trình chia ảnh thành các regions có ý nghĩa
- **Mục đích**:
  - Object detection
  - Feature extraction
  - Image analysis
  - Region of interest identification

- **Các kỹ thuật**:
  1. **Thresholding-based**:
     - Global thresholding
     - Adaptive thresholding
     - **Otsu's method** (tự động tìm threshold)
     - Multi-level thresholding

  2. **Region-based**:
     - Region growing
     - Region splitting and merging
     - Watershed algorithm

  3. **Edge-based**:
     - Edge detection → boundary tracing

  4. **Clustering-based**:
     - K-means clustering
     - Mean-shift
     - DBSCAN

  5. **Advanced methods**:
     - Graph cuts
     - Active contours (Snakes)
     - Level sets
     - Deep learning (U-Net, Mask R-CNN)

---

### Câu 10: Các Phương Pháp Mã Hóa
**Yêu cầu**: Trình bày một số phương pháp mã hóa

**Nội dung cần cover**:

#### 1. Run-Length Encoding (RLE):
- Mã hóa chuỗi giá trị lặp lại
- Example: `AAAABBBB → 4A4B`
- Hiệu quả cho ảnh có nhiều vùng đồng nhất

#### 2. Huffman Coding:
- Variable-length coding
- Dựa trên frequency của symbols
- Build Huffman tree
- Optimal prefix code
- Example chi tiết

#### 3. LZW (Lempel-Ziv-Welch):
- Dictionary-based compression
- Build dictionary dynamically
- Sử dụng trong GIF, TIFF
- Example với ảnh 1×3 blocks

#### 4. Arithmetic Coding:
- Encode entire message thành một số thực
- Better compression ratio than Huffman
- More complex

#### 5. Transform Coding:
- DCT (Discrete Cosine Transform) - JPEG
- DWT (Discrete Wavelet Transform) - JPEG2000
- KLT (Karhunen-Loève Transform)

---

### Câu 11: Biến Đổi Cosine trong JPEG
**Yêu cầu**: Biến đổi Cosine trong nén JPEG nhằm mục đích gì? Và bước nào trong nén JPEG sẽ làm cho quá trình nén ảnh là không bảo toàn?

**Nội dung cần cover**:

#### Mục đích của DCT trong JPEG:
1. **Energy Compaction**: Tập trung năng lượng vào low-frequency coefficients
2. **Decorrelation**: Giảm correlation giữa các pixels
3. **Quantization-friendly**: Dễ dàng loại bỏ high-frequency components

#### Các Bước JPEG:
1. **Color space conversion**: RGB → YCbCr
2. **Block division**: 8×8 blocks
3. **DCT**: Transform to frequency domain
4. **Quantization**: ⚠️ **LOSSY STEP** - Chia cho quantization matrix và round
5. **Zigzag scanning**: Arrange coefficients
6. **Entropy encoding**: Huffman/Arithmetic coding (lossless)

#### Bước Không Bảo Toàn (Lossy):
**QUANTIZATION (Bước 4)**:
- Chia DCT coefficients cho quantization table
- Round to integers
- Information loss occurs here
- Quality factor controls quantization table values
- Cannot recover exact original values

---

### Câu 12: Xử Lý Hình Thái
**Yêu cầu**: Khái niệm, ý nghĩa, các phép xử lý hình thái

**Nội dung cần cover**:

#### Định Nghĩa:
- Morphological operations là các phép toán dựa trên shape
- Chủ yếu cho binary images
- Sử dụng Structuring Element (SE)

#### Các Phép Toán Cơ Bản:

1. **Erosion (Co, ⊖)**:
   - Shrinks objects
   - Removes small objects
   - Formula: A ⊖ B

2. **Dilation (Giãn, ⊕)**:
   - Expands objects
   - Fills holes
   - Formula: A ⊕ B

3. **Opening (Mở, ∘)**:
   - Erosion then Dilation
   - Removes small bright spots
   - Formula: A ∘ B = (A ⊖ B) ⊕ B

4. **Closing (Đóng, •)**:
   - Dilation then Erosion
   - Fills small dark holes
   - Formula: A • B = (A ⊕ B) ⊖ B

#### Các Phép Toán Khác:
- Morphological Gradient
- Top-hat transform
- Black-hat transform
- Hit-or-miss transform

#### Ứng Dụng:
- Noise removal
- Shape analysis
- Feature extraction
- Object separation/connection

---

## Phần 2: Bài Tập (7 bài)

### Bài 1: Tìm Biên với Roberts, Prewitt, Sobel

**Input Image (8×8):**
```
2  4  2  4  4  3  3  3
4  3  1  4  2  1  3  1
2  3  1  2  1  1  3  2
4  1  1  2  2  2  2  3
1  4  1  2  1  4  3  4
2  3  1  4  1  1  2  1
1  2  2  2  4  1  3  4
1  3  1  1  4  1  1  4
```

**Yêu cầu**: Tìm biên sử dụng:
- Roberts operator
- Prewitt operator
- Sobel operator

**Cần thực hiện**:
1. Trình bày kernels của từng operator
2. Apply convolution (xử lý padding)
3. Tính magnitude: `G = sqrt(Gx² + Gy²)`
4. Output kết quả gradient magnitude

---

### Bài 2: Tăng Cường Ảnh với Gaussian Filter

**Input Image (8×8):**
```
4  4  1  1  2  0  1  0
4  1  4  2  2  3  4  4
2  4  2  0  0  1  0  0
0  1  2  0  1  3  4  3
0  0  4  2  0  3  2  4
1  1  1  3  3  3  4  4
4  3  3  4  1  2  0  0
1  2  3  0  2  0  2  1
```

**Yêu cầu**:
1. Cho biết kết quả sau khi tăng cường sử dụng các hàm biến đổi mức xám
2. Kỹ thuật lọc không gian
3. Lọc thông thấp Gaussian cửa sổ 3×3

**Gaussian Kernel 3×3 (normalized):**
```
1   2   1
2   4   2
1   2   1
────────
   16
```

**Cần thực hiện**:
1. Apply Gaussian filter với zero padding
2. Tính convolution cho từng pixel
3. Output ảnh đã làm mượt

---

### Bài 3: Cân Bằng Histogram

**Input Image I (5×4):**
```
1  2  0  4
1  0  0  7
2  2  1  0
4  1  2  1
2  0  1  1
```

**Yêu cầu**:
- Vẽ lược đồ xám và thực hiện cân bằng lược đồ xám
- Tìm ảnh I' sau khi đã cân bằng lược đồ xám

**Cần thực hiện**:
1. Tính histogram h(g)
2. Tính CDF
3. Normalize CDF với L levels (có thể L=8)
4. Map old values → new values
5. Reconstruct image I'
6. Vẽ histogram trước và sau

---

### Bài 4: Xử Lý Hình Thái

**Input Image X (8×8 binary):**
```
0  1  1  0  0  1  0  0
1  1  0  0  0  1  1  0
0  1  1  0  1  1  1  1
1  1  0  1  1  1  1  1
1  0  1  1  1  1  0  0
1  0  0  1  0  1  1  1
1  0  1  1  1  0  1  0
1  0  0  0  1  1  1  1
```

**Structuring Element B (3×3):**
```
1  0  0
0  1  1
1  0  0
```

**Yêu cầu**: Tìm kết quả của phép:
1. **Giãn** (Dilation): X ⊕ B
2. **Co** (Erosion): X ⊖ B
3. **Đóng** (Closing): (X ⊕ B) ⊖ B
4. **Mở** (Opening): (X ⊖ B) ⊕ B

**Cần thực hiện**:
- Áp dụng từng phép toán với zero padding
- Show kết quả từng bước
- Giải thích sự khác biệt giữa các operations

---

### Bài 5: Phân Vùng Ảnh

#### Bài 5a: Tìm Ngưỡng Tự Động

**Histogram:**
```
g    | 0   1   2   3    4    5    6    7     8     9
h(g) | 20  40  30  50   70   60   120  250   100   20
```

**Yêu cầu**: Thực hiện tìm ngưỡng tự động với thuật toán đẳng điều cho bức ảnh I có biểu đồ tần suất sau.

**Thuật Toán**:
1. Chọn initial threshold T₀ (e.g., mean)
2. Segment image thành 2 groups: G₁ (≤T) và G₂ (>T)
3. Tính mean của G₁ và G₂: μ₁, μ₂
4. New threshold: T_new = (μ₁ + μ₂) / 2
5. Repeat until convergence

**Note**: Đã biết ảnh có 10 mức xám (0-9)

---

#### Bài 5b: Tìm Ngưỡng với Độ Chính Xác 88%

**Histogram:**
```
g    | 0   1   2   3   4    5    6   7   8   9
h(g) | 39  45  53  72  40   112  25  34  23  13
```

**Yêu cầu**: Thực hiện tìm ngưỡng tự động với thuật toán đối xứng nền cho bức ảnh I' có biểu đồ tần suất sau. Được biết độ chính xác cần tính là 88%.

**Cần thực hiện**:
1. Total pixels: Σh(g)
2. Target: 88% of total
3. Find threshold T such that cumulative sum reaches 88%

---

#### Bài 5c: Thuật Toán Otsu

**Input Image I (5×6):**
```
0  1  2  3  4  5
0  0  1  2  3  4
0  0  0  1  2  3
0  0  0  0  1  2
0  0  0  0  0  1
```

**Yêu cầu**: Tìm ngưỡng tự động cục bộ theo thuật toán Otsu

**Thuật Toán Otsu**:
1. Tính histogram
2. For each possible threshold k:
   - Chia thành 2 classes: C₀ (0..k) và C₁ (k+1..L-1)
   - Tính probability: ω₀, ω₁
   - Tính mean: μ₀, μ₁
   - Tính between-class variance: σ²ᵦ = ω₀ω₁(μ₁ - μ₀)²
3. Choose k that maximizes σ²ᵦ

---

### Bài 6: Nén LZW

**Input Image I (4×9 binary):**
```
1  0  0  1  1  1  0  1  0
0  0  0  1  0  1  1  1  0
0  0  1  0  1  1  1  1  1
1  1  1  0  0  0  1  1  0
```

**Initial Dictionary**: Blocks 1×3 với giá trị 0-7
```
Code | Pattern
-----|--------
 0   | 0 0 0
 1   | 0 0 1
 2   | 0 1 0
 3   | 0 1 1
 4   | 1 0 0
 5   | 1 0 1
 6   | 1 1 0
 7   | 1 1 1
```

**Yêu cầu**:
1. Mã hóa ảnh bằng LZW
2. Giải mã để verify

**Thuật Toán LZW Encoding**:
1. Initialize dictionary với codes 0-7
2. Read first pattern → output code
3. Read next pattern:
   - If current+next in dictionary → extend current
   - Else:
     - Output code for current
     - Add current+next to dictionary (code 8, 9, ...)
     - Current = next
4. Continue until end

---

### Bài 7: Nén Huffman

**Input Image I (4×4):**
```
12  15  12  15
15  12  15  18
18  12  18  12
15  18  15  12
```

**Yêu cầu**: Hãy nén và giải nén ảnh bằng thuật toán Huffman

**Cần thực hiện**:

1. **Count Frequency**:
   - 12: ? occurrences
   - 15: ? occurrences
   - 18: ? occurrences

2. **Build Huffman Tree**:
   - Sort by frequency
   - Combine two smallest nodes
   - Repeat until one root

3. **Generate Codes**:
   - Traverse tree: left=0, right=1
   - Assign codes to symbols

4. **Encode**:
   - Replace each pixel với Huffman code

5. **Decode**:
   - Use tree to decode bit stream back to pixels

6. **Calculate Compression Ratio**:
   - Original bits vs Encoded bits

---

## Task Breakdown

### Phase 1: Tài Liệu Lý Thuyết

**Folder structure:**
```
requirements/
└── req-3-solutions/
    ├── theory/
    │   ├── 01-color-models.md
    │   ├── 02-brightness-adjustment.md
    │   ├── 03-histogram-equalization.md
    │   ├── 04-convolution.md
    │   ├── 05-noise-models.md
    │   ├── 06-edge-detection.md
    │   ├── 07-image-compression.md
    │   ├── 08-filtering-methods.md
    │   ├── 09-image-segmentation.md
    │   ├── 10-encoding-methods.md
    │   ├── 11-jpeg-dct.md
    │   └── 12-morphology.md
    ├── exercises/
    │   ├── bai-1-edge-detection.md
    │   ├── bai-2-gaussian-filter.md
    │   ├── bai-3-histogram-equalization.md
    │   ├── bai-4-morphology.md
    │   ├── bai-5a-auto-threshold.md
    │   ├── bai-5b-threshold-88.md
    │   ├── bai-5c-otsu.md
    │   ├── bai-6-lzw.md
    │   └── bai-7-huffman.md
    └── README.md
```

### Phase 2: Giải Bài Tập

Mỗi bài tập cần:
1. **Problem statement** (rõ ràng)
2. **Input data** (formatted)
3. **Theory background** (ngắn gọn)
4. **Step-by-step solution**
5. **Final answer**
6. **Verification** (nếu có thể)

### Phase 3: Tổng Hợp

**README.md** bao gồm:
- Overview của đề cương
- Quick reference cho từng topic
- Công thức quan trọng
- Tips & tricks cho thi
- Cross-references

---

## Summary Checklist

### Theory (12 câu)
- [ ] Câu 1: Mô hình màu
- [ ] Câu 2: Tăng/giảm độ sáng
- [ ] Câu 3: Cân bằng tần suất
- [ ] Câu 4: Convolution
- [ ] Câu 5: Mô hình nhiễu
- [ ] Câu 6: Edge detection
- [ ] Câu 7: Image compression
- [ ] Câu 8: Filtering methods
- [ ] Câu 9: Image segmentation
- [ ] Câu 10: Encoding methods
- [ ] Câu 11: JPEG DCT
- [ ] Câu 12: Morphology

### Exercises (7 bài)
- [ ] Bài 1: Edge detection (Roberts, Prewitt, Sobel)
- [ ] Bài 2: Gaussian filtering
- [ ] Bài 3: Histogram equalization
- [ ] Bài 4: Morphological operations
- [ ] Bài 5a: Auto threshold
- [ ] Bài 5b: Threshold with 88% accuracy
- [ ] Bài 5c: Otsu's method
- [ ] Bài 6: LZW compression
- [ ] Bài 7: Huffman coding

---

## Notes

- Tất cả bài tập có data cụ thể từ PDF
- Cần tính toán chi tiết, step-by-step
- Ưu tiên clarity và correctness
- Provide formulas và examples
- Cross-reference với theory khi cần
- Sử dụng tables và diagrams để minh họa

---

**Expected Output**:
- 12 theory documents (comprehensive)
- 9 exercise solutions (detailed)
- 1 README (tổng hợp)
- Total: ~22 markdown files
