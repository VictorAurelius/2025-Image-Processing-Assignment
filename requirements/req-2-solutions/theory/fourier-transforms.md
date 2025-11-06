# Biến Đổi Fourier (Fourier Transform)

## Giới Thiệu

Biến đổi Fourier chuyển đổi ảnh từ **miền không gian** (spatial domain) sang **miền tần số** (frequency domain), giúp phân tích và xử lý ảnh hiệu quả hơn.

## Công Thức

### Fourier Transform 2D:
```
F(u,v) = ∫∫ f(x,y) e^(-j2π(ux+vy)) dx dy
```

### Inverse Fourier Transform:
```
f(x,y) = ∫∫ F(u,v) e^(j2π(ux+vy)) du dv
```

### Discrete Fourier Transform (DFT) 2D:
```
F(u,v) = (1/MN) Σ Σ f(x,y) e^(-j2π(ux/M + vy/N))
         x=0..M-1 y=0..N-1
```

## Đặc Điểm Phổ Fourier

### 1. Phổ Tần Số (Frequency Spectrum)
- **Magnitude**: |F(u,v)| = sqrt(Real² + Imag²)
- **Phase**: φ(u,v) = arctan(Imag/Real)

### 2. Phân Bố Năng Lượng

#### Tập trung ở vùng trung tâm (DC component):
- **Ý nghĩa**: Ảnh có nhiều vùng **mượt, ít chi tiết**
- **Tần số thấp** chi phối
- Ví dụ: Ảnh bầu trời, tường trơn

#### Phân tán ra xung quanh:
- **Ý nghĩa**: Ảnh có nhiều **chi tiết nhỏ, biên cạnh, texture**
- **Tần số cao** chi phối
- Ví dụ: Ảnh có nhiều text, pattern phức tạp

### 3. DC Component (u=0, v=0)
- Giá trị trung bình của toàn bộ ảnh
- Tần số thấp nhất
- Nằm ở **trung tâm phổ** sau khi shift

## Frequency Domain Properties

### Tần Số Thấp (Low Frequency)
- **Vị trí**: Gần tâm phổ
- **Ý nghĩa**: Thay đổi chậm trong ảnh
- **Đặc điểm**: Vùng mượt, màu đồng nhất
- **Ví dụ**: Background, vùng không có texture

### Tần Số Cao (High Frequency)
- **Vị trí**: Xa tâm phổ
- **Ý nghĩa**: Thay đổi nhanh trong ảnh
- **Đặc điểm**: Biên cạnh, chi tiết, nhiễu
- **Ví dụ**: Edges, texture, noise

## Filters trong Frequency Domain

### 1. Low-Pass Filter (Lọc Thông Thấp)

**Mục đích**: Giữ tần số thấp, loại bỏ tần số cao

**Hiệu quả**:
- Làm mượt ảnh (smoothing/blurring)
- Giảm nhiễu
- Loại bỏ chi tiết nhỏ

#### a) Ideal Low-Pass Filter (ILPF)
```
H(u,v) = {
  1  if D(u,v) ≤ D₀
  0  if D(u,v) > D₀
}
```
- **Ưu điểm**: Cắt hoàn toàn tần số cao
- **Nhược điểm**: Tạo **ringing artifacts** (hiện tượng rung) do biên cắt gắt

#### b) Butterworth Low-Pass Filter (BLPF)
```
H(u,v) = 1 / (1 + [D(u,v)/D₀]^(2n))
```
- **n**: Order (bậc) của filter
- **n tăng**: Filter càng giống Ideal filter
- **Ưu điểm**:
  - Transition mượt giữa pass và stop band
  - **Giảm ringing artifacts** đáng kể
  - Phù hợp cho hầu hết ứng dụng
- **Lý do được ưa dùng**: Cân bằng giữa hiệu quả và artifacts

#### c) Gaussian Low-Pass Filter (GLPF)
```
H(u,v) = e^(-D²(u,v)/(2D₀²))
```
- **Ưu điểm**: Không có ringing artifacts
- Transition mượt nhất
- Tương ứng với Gaussian blur trong spatial domain

### 2. High-Pass Filter (Lọc Thông Cao)

**Mục đích**: Giữ tần số cao, loại bỏ tần số thấp

**Hiệu quả**:
- Tăng cường biên (edge enhancement)
- Sharpening
- Phát hiện chi tiết nhỏ

**Design**: `H_HP(u,v) = 1 - H_LP(u,v)`

**Thành phần bị triệt**:
- **DC component** (tần số = 0)
- **Vùng trung tâm phổ** (tần số thấp)

### 3. Band-Pass & Band-Reject Filters

**Band-Pass**: Chỉ giữ một dải tần số nhất định

**Band-Reject (Notch)**: Loại bỏ một dải tần số cụ thể

## Hiện Tượng Spectral Leakage

### Định Nghĩa
Spectral leakage (tò n phổ) là hiện tượng năng lượng của một tần số "rò rỉ" sang các tần số lân cận.

### Nguyên Nhân
1. **Rectangular Window**:
   - Khi lấy một đoạn tín hiệu hữu hạn
   - Tương đương với nhân với rectangular window
   - **Đây là nguyên nhân chính trong đề thi**

2. **Truncation**: Cắt ngắn tín hiệu không đúng chu kỳ

3. **Discontinuities**: Gián đoạn tại biên

### Giải Pháp

#### Window Functions:
Các hàm cửa sổ làm mượt biên để giảm leakage:

| Window | Spectral Leakage | Frequency Resolution | Ứng dụng |
|--------|------------------|---------------------|----------|
| **Rectangular** | Cao nhất | Tốt nhất | Đơn giản nhưng nhiều leakage |
| **Hann** | Trung bình | Trung bình | Cân bằng tốt |
| **Hamming** | Thấp | Khá | Phổ biến trong audio |
| **Blackman** | Thấp nhất | Kém nhất | Khi cần minimize leakage |

**Trade-off**:
- Leakage thấp ↔ Frequency resolution kém
- Blackman: Leakage thấp nhất nhưng độ phân giải tần số kém nhất

## FFT (Fast Fourier Transform)

### Ưu Điểm
- **Tốc độ**: O(N log N) thay vì O(N²) của DFT
- Hiệu quả cho ảnh lớn

### Lưu Ý
- Kích thước tốt nhất: 2^n (512, 1024, 2048, ...)
- Zero padding nếu kích thước không phù hợp
- Kích thước nhỏ hơn ảnh → loss of information

## Ứng Dụng Thực Tế

### 1. Image Filtering
- Design filter trong frequency domain
- Faster cho kernel lớn

### 2. Compression
- JPEG sử dụng DCT (Discrete Cosine Transform)
- Loại bỏ tần số cao ít quan trọng

### 3. Pattern Recognition
- Phân tích texture
- Feature extraction

### 4. Image Restoration
- Deblurring
- Noise removal

### 5. Watermarking
- Embed watermark trong frequency domain
- Robust hơn spatial domain

## Mối Quan Hệ với Spatial Domain

### Convolution Theorem:
```
f * g ↔ F · G
Convolution trong spatial domain
= Multiplication trong frequency domain
```

**Ứng dụng**:
- Filtering nhanh hơn trong frequency domain cho kernel lớn
- FFT → Multiply → IFFT thay vì convolution trực tiếp

## Phase vs Magnitude

### Magnitude Spectrum:
- Thể hiện năng lượng tại mỗi tần số
- Quan trọng cho filtering

### Phase Spectrum:
- Chứa thông tin về vị trí trong ảnh
- **Quan trọng hơn cho reconstruction**
- Ảnh reconstruct từ phase thường nhận diện được
- Ảnh reconstruct từ magnitude thường không nhận diện được

## Tham Khảo

- Digital Image Processing (Gonzalez & Woods) - Chapter 4
- The Fourier Transform and Its Applications (Bracewell)
- Understanding Digital Signal Processing (Lyons) - Chapter 3
- numpy.fft documentation
- OpenCV: `cv2.dft()`, `cv2.idft()`
