# Phép Toán Hình Thái (Morphological Operations)

## Giới Thiệu

Morphological operations là các phép toán xử lý ảnh dựa trên hình dạng (shape), chủ yếu áp dụng cho **ảnh nhị phân** (binary images) nhưng cũng có thể dùng cho ảnh grayscale.

## Khái Niệm Cơ Bản

### Structuring Element (SE hoặc Kernel B)
- Ma trận nhỏ xác định hình dạng và kích thước của phép toán
- Có thể là hình vuông, chữ thập, hình tròn, v.v.
- Có "anchor point" (thường ở giữa)

#### Ví dụ Structuring Elements:
```
3×3 Square:        Cross:           Circle 5×5:
■ ■ ■              . ■ .            . . ■ . .
■ ■ ■              ■ ■ ■            . ■ ■ ■ .
■ ■ ■              . ■ .            ■ ■ ■ ■ ■
                                    . ■ ■ ■ .
                                    . . ■ . .
```

### Padding Modes
- **Zero Padding**: Thêm 0 (black) xung quanh ảnh
- **Replicate**: Sao chép pixel biên
- **Reflect**: Phản xạ ảnh

**Trong đề thi**: Thường dùng **zero padding**

## Hai Phép Toán Cơ Bản

### 1. Erosion (Ăn mòn) - Ký hiệu: A ⊖ B

#### Định nghĩa:
Pixel kết quả = 1 (foreground) **chỉ khi** structuring element fit hoàn toàn trong object

#### Công thức:
```
A ⊖ B = {z | (B)z ⊆ A}
```
Với (B)z là B translated by z

#### Hiệu ứng:
- **Shrinks/thu nhỏ** objects
- **Removes small objects** (nhiễu nhỏ)
- **Breaks narrow connections** (đứt các liên kết mỏng)
- **Smooths boundaries** (làm mượt biên)

#### Ví dụ:

**Input Image A:**
```
0 0 0 0 0
0 1 1 1 0
0 1 1 1 0
0 1 1 1 0
0 0 0 0 0
```

**Structuring Element B (3×3 square):**
```
1 1 1
1 1 1
1 1 1
```

**Result (A ⊖ B):**
```
0 0 0 0 0
0 0 0 0 0
0 0 1 0 0  ← Chỉ còn tâm
0 0 0 0 0
0 0 0 0 0
```

### 2. Dilation (Giãn nở) - Ký hiệu: A ⊕ B

#### Định nghĩa:
Pixel kết quả = 1 nếu structuring element **chạm** ít nhất 1 pixel của object

#### Công thức:
```
A ⊕ B = {z | (B̂)z ∩ A ≠ ∅}
```
Với B̂ là reflection của B

#### Hiệu ứng:
- **Expands/mở rộng** objects
- **Fills small holes** (lấp các lỗ nhỏ)
- **Connects nearby objects** (nối các object gần nhau)
- **Makes boundaries rough** (biên trở nên gồ ghề hơn)

#### Ví dụ:

**Input Image A:**
```
0 0 0 0 0
0 0 1 0 0
0 0 1 0 0
0 0 1 0 0
0 0 0 0 0
```

**Structuring Element B (3×3 square):**
```
1 1 1
1 1 1
1 1 1
```

**Result (A ⊕ B):**
```
0 1 1 1 0
0 1 1 1 0
0 1 1 1 0
0 1 1 1 0
0 1 1 1 0
```

## Phép Toán Phức Hợp

### 3. Opening (Mở) - Ký hiệu: A ∘ B

#### Định nghĩa:
```
A ∘ B = (A ⊖ B) ⊕ B
```
Erosion sau đó Dilation

#### Hiệu ứng:
- **Removes small objects** (loại bỏ nhiễu nhỏ)
- **Smooths contours** (làm mượt đường viền)
- **Breaks thin connections** (ngắt liên kết mỏng)
- **Preserves shape** của large objects

#### Khi nào dùng:
- Loại bỏ noise nhỏ mà vẫn giữ shape chính
- Tách các objects được nối mỏng
- Làm mượt boundaries từ phía ngoài

#### Ví dụ Use Case:
**Input**: Object với small protrusions
**Opening**: Removes protrusions, smooths boundaries

### 4. Closing (Đóng) - Ký hiệu: A • B

#### Định nghĩa:
```
A • B = (A ⊕ B) ⊖ B
```
Dilation sau đó Erosion

#### Hiệu ứng:
- **Fills small holes** (lấp lỗ nhỏ)
- **Smooths contours** (làm mượt đường viền)
- **Connects nearby objects** (nối các object gần)
- **Preserves size** của objects

#### Khi nào dùng:
- Lấp các lỗ nhỏ trong objects
- Nối các objects bị ngắt quãng
- Làm mượt boundaries từ phía trong

#### Ví dụ Use Case:
**Input**: Object with small holes
**Closing**: Fills holes, connects gaps

## So Sánh Opening vs Closing

| Đặc điểm | Opening (⊖ → ⊕) | Closing (⊕ → ⊖) |
|----------|-----------------|-----------------|
| **Loại bỏ** | Small bright regions | Small dark regions |
| **Hiệu ứng** | Shrinks then expands | Expands then shrinks |
| **Smoothing** | Bên ngoài (external) | Bên trong (internal) |
| **Ứng dụng** | Remove noise | Fill holes |
| **Shape** | Slightly smaller | Slightly larger |

## Các Phép Toán Khác

### 5. Morphological Gradient

```
Gradient = Dilation - Erosion
         = (A ⊕ B) - (A ⊖ B)
```

**Hiệu ứng**: Phát hiện **outline/boundary** của objects

### 6. Top Hat Transform

```
Top Hat = Original - Opening
        = A - (A ∘ B)
```

**Hiệu ứng**: Trích xuất **small bright features**

### 7. Black Hat Transform

```
Black Hat = Closing - Original
          = (A • B) - A
```

**Hiệu ứng**: Trích xuất **small dark features**

### 8. Hit-or-Miss Transform

Phát hiện specific patterns trong ảnh

## Properties (Tính Chất)

### Duality:
```
(A ⊖ B)ᶜ = Aᶜ ⊕ B̂
(A ⊕ B)ᶜ = Aᶜ ⊖ B̂
```

### Idempotence:
```
(A ∘ B) ∘ B = A ∘ B
(A • B) • B = A • B
```

Opening và Closing là idempotent (áp dụng nhiều lần = áp dụng 1 lần)

### Monotonicity:
```
If A ⊆ C, then:
  A ⊖ B ⊆ C ⊖ B
  A ⊕ B ⊆ C ⊕ B
```

## Ví Dụ Thực Tế

### Bài toán 1: Remove Salt Noise
**Input**: Ảnh có nhiễu muối (white spots)
**Solution**: Opening với SE nhỏ
**Giải thích**: Erosion loại bỏ white spots, dilation phục hồi shape

### Bài toán 2: Fill Holes in Objects
**Input**: Objects có lỗ nhỏ
**Solution**: Closing với SE vừa
**Giải thích**: Dilation lấp lỗ, erosion trả về size gốc

### Bài toán 3: Separate Touching Objects
**Input**: Hai objects chạm nhau
**Solution**: Opening với SE phù hợp
**Giải thích**: Erosion ngắt connection, dilation phục hồi

### Bài toán 4: Extract Boundaries
**Input**: Binary object
**Solution**: Morphological Gradient
**Giải thích**: Dilation - Erosion = chỉ giữ boundary

## Chọn Structuring Element

### Size:
- **Nhỏ (3×3)**: Chỉnh sửa nhỏ, preserve details
- **Vừa (5×5, 7×7)**: Cân bằng giữa effect và preservation
- **Lớn (>7×7)**: Thay đổi lớn, có thể mất details

### Shape:
- **Square**: General purpose, isotropic
- **Cross**: Nhấn mạnh 4-connectivity
- **Circle**: Isotropic nhất, natural shape
- **Line**: Phát hiện features theo hướng cụ thể

## Connected Components Relationship

Morphology thường được dùng như preprocessing cho connected components:

1. **Noise Removal**: Opening/Closing
2. **Separation**: Opening để tách objects
3. **Connection**: Closing để nối objects
4. **Labeling**: Sau khi morphology, apply connected components

## Grayscale Morphology

Erosion và Dilation cũng có thể áp dụng cho grayscale images:

### Grayscale Erosion:
```
(A ⊖ B)(x,y) = min{A(x+s, y+t) - B(s,t)}
```

### Grayscale Dilation:
```
(A ⊕ B)(x,y) = max{A(x-s, y-t) + B(s,t)}
```

## Tips & Tricks

1. **Chọn SE phù hợp với features cần xử lý**
2. **Iterative operations**: Có thể apply nhiều lần
3. **Combine operations**: Opening + Closing thường tốt hơn riêng lẻ
4. **Preprocessing**: Morphology trước khi feature extraction
5. **Postprocessing**: Clean up sau thresholding

## Tham Khảo

- Digital Image Processing (Gonzalez & Woods) - Chapter 9
- Mathematical Morphology (Serra)
- OpenCV Documentation: `cv2.erode()`, `cv2.dilate()`, `cv2.morphologyEx()`
- scikit-image: `skimage.morphology`
