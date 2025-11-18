# Lý Thuyết: Phân Vùng Dựa Trên Gom Cụm (Clustering Segmentation)

## Tổng Quan

Phân vùng dựa trên gom cụm (clustering segmentation) xem phân vùng ảnh như bài toán phân loại dữ liệu: mỗi pixel là một điểm dữ liệu trong không gian đặc trưng (màu sắc, vị trí, texture), và các pixel thuộc cùng vùng được gom vào cùng một cụm (cluster).

K-means và Mean-shift là hai thuật toán phổ biến nhất. K-means chia pixels thành K cụm với mục tiêu tối thiểu hóa khoảng cách trong cụm, trong khi Mean-shift tìm các mode (đỉnh mật độ) trong không gian đặc trưng mà không cần chỉ định số cụm trước.

Phương pháp clustering đặc biệt hiệu quả cho ảnh vệ tinh (phân loại đất), ảnh y tế (phân vùng mô), và các ứng dụng cần phân loại tự động dựa trên màu sắc và texture.

## Ứng Dụng

- **Bài 8**: K-means Segmentation - Phân vùng ảnh vệ tinh (rừng/sông/nhà/đất)

## Nguyên Lý Toán Học

### 1. K-means Clustering

**Ý tưởng:** Phân K cụm sao cho tổng khoảng cách từ các điểm đến tâm cụm là nhỏ nhất.

**Hàm mục tiêu:**

```
J = Σᵢ₌₁ᴷ Σₓ∈Cᵢ ||x - μᵢ||²
```

Với:
- K: số cụm
- Cᵢ: cụm thứ i
- μᵢ: tâm cụm thứ i
- x: điểm dữ liệu (pixel)

**Thuật toán Lloyd:**

```
1. Khởi tạo K tâm cụm {μ₁, μ₂, ..., μₖ} (random hoặc K-means++)
2. Repeat until convergence:
   a. Assignment step:
      Cᵢ = {x : ||x - μᵢ|| ≤ ||x - μⱼ|| ∀j}
      (Gán mỗi điểm vào cụm gần nhất)

   b. Update step:
      μᵢ = (1/|Cᵢ|) × Σₓ∈Cᵢ x
      (Cập nhật tâm = trung bình các điểm trong cụm)

3. Dừng khi: |μᵢ⁽ᵗ⁺¹⁾ - μᵢ⁽ᵗ⁾| < ε
```

**K-means++ Initialization:**

Chọn tâm ban đầu sao cho cách xa nhau:

```
1. Chọn μ₁ random từ data
2. For i = 2 to K:
   a. Tính D(x) = min distance từ x đến {μ₁, ..., μᵢ₋₁}
   b. Chọn μᵢ với xác suất ∝ D(x)²
```

**Độ phức tạp:**
- Mỗi iteration: O(n × K × d) với n pixels, d dimensions
- Tổng: O(i × n × K × d) với i iterations (thường 10-100)

**Trong phân vùng ảnh:**

```
# RGB space
pixel = [R, G, B]

# RGB + Position space
pixel = [R, G, B, x, y]

# HSV space
pixel = [H, S, V]
```

### 2. Mean-Shift Clustering

**Ý tưởng:** Tìm các mode (local maxima) của hàm mật độ xác suất bằng cách dịch chuyển về hướng gradient.

**Kernel Density Estimation:**

```
f(x) = (1/n) × Σᵢ₌₁ⁿ K((x - xᵢ)/h)
```

Với:
- K: kernel function (thường dùng Gaussian)
- h: bandwidth parameter

**Mean-Shift Vector:**

```
m(x) = (Σᵢ xᵢ × G((x - xᵢ)/h)) / (Σᵢ G((x - xᵢ)/h)) - x
```

Với G là Gaussian kernel:

```
G(x) = exp(-||x||²/2)
```

**Thuật toán:**

```
1. For each pixel x:
   a. Khởi tạo y = x
   b. Repeat:
      - Tính mean-shift vector: m(y)
      - Cập nhật: y ← y + m(y)
   c. Until convergence: ||m(y)|| < ε
   d. Label(x) = mode đã hội tụ

2. Merge các mode gần nhau (< threshold)
```

**Bandwidth selection:**
- Quá nhỏ: nhiều mode, oversegmentation
- Quá lớn: ít mode, undersegmentation

**Độ phức tạp:** O(n² × i) - chậm hơn K-means

### 3. GMM (Gaussian Mixture Model)

**Mô hình:** Dữ liệu được sinh từ K phân bố Gaussian:

```
p(x) = Σₖ₌₁ᴷ πₖ × N(x | μₖ, Σₖ)
```

Với:
- πₖ: mixing coefficient (Σπₖ = 1)
- N(x|μₖ,Σₖ): Gaussian với mean μₖ và covariance Σₖ

**EM Algorithm:**

```
E-step: Tính posterior probability
γₖ(xᵢ) = (πₖ × N(xᵢ|μₖ,Σₖ)) / Σⱼ(πⱼ × N(xᵢ|μⱼ,Σⱼ))

M-step: Cập nhật tham số
Nₖ = Σᵢ γₖ(xᵢ)
πₖ = Nₖ/n
μₖ = (1/Nₖ) × Σᵢ γₖ(xᵢ) × xᵢ
Σₖ = (1/Nₖ) × Σᵢ γₖ(xᵢ) × (xᵢ - μₖ)(xᵢ - μₖ)ᵀ
```

**Độ phức tạp:** O(i × n × K × d²)

## Code Examples (OpenCV)

### 1. K-means Segmentation (OpenCV)

```python
import cv2
import numpy as np

def kmeans_segmentation(img, K=4, max_iter=100):
    """
    Phân vùng ảnh bằng K-means.

    Args:
        img: Ảnh RGB (H×W×3)
        K: Số cụm
        max_iter: Số iteration tối đa

    Returns:
        seg: Ảnh phân vùng
        labels: Nhãn của mỗi pixel
        centers: Tâm các cụm
    """
    # Reshape ảnh thành (n_pixels, 3)
    pixels = img.reshape((-1, 3)).astype(np.float32)

    # Tiêu chí dừng
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
                max_iter, 1.0)

    # K-means
    _, labels, centers = cv2.kmeans(
        pixels, K, None,
        criteria, 10,
        cv2.KMEANS_PP_CENTERS  # K-means++ initialization
    )

    # Tạo ảnh phân vùng với màu tâm cụm
    seg = centers[labels.flatten()].reshape(img.shape).astype(np.uint8)

    return seg, labels, centers

# Sử dụng
img = cv2.imread('satellite.jpg')
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

seg, labels, centers = kmeans_segmentation(img_rgb, K=4)

print(f"Tâm các cụm (RGB):")
for i, center in enumerate(centers):
    print(f"  Cụm {i}: RGB({center[0]:.0f}, {center[1]:.0f}, {center[2]:.0f})")
```

### 2. K-means với RGB + Position

```python
def kmeans_color_spatial(img, K=4, spatial_weight=0.1):
    """
    K-means kết hợp màu sắc và vị trí không gian.

    Feature vector: [R, G, B, w×x, w×y]
    """
    H, W, _ = img.shape

    # Tạo feature vector 5D
    y_coords, x_coords = np.mgrid[0:H, 0:W]
    features = np.dstack([
        img[:, :, 0],  # R
        img[:, :, 1],  # G
        img[:, :, 2],  # B
        x_coords * spatial_weight,  # x position
        y_coords * spatial_weight   # y position
    ])

    pixels = features.reshape((-1, 5)).astype(np.float32)

    # K-means
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 1.0)
    _, labels, centers = cv2.kmeans(pixels, K, None, criteria, 10,
                                     cv2.KMEANS_PP_CENTERS)

    # Tạo ảnh phân vùng (chỉ lấy RGB từ centers)
    seg = centers[labels.flatten(), :3].reshape(img.shape).astype(np.uint8)

    return seg, labels.reshape((H, W))

# Sử dụng
seg, label_img = kmeans_color_spatial(img_rgb, K=5, spatial_weight=0.5)
```

### 3. K-means trên không gian HSV

```python
def kmeans_hsv(img, K=4):
    """K-means trên không gian HSV."""

    # Chuyển sang HSV
    img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    # Reshape
    pixels = img_hsv.reshape((-1, 3)).astype(np.float32)

    # K-means
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 1.0)
    _, labels, centers = cv2.kmeans(pixels, K, None, criteria, 10,
                                     cv2.KMEANS_PP_CENTERS)

    # Tạo ảnh phân vùng
    seg_hsv = centers[labels.flatten()].reshape(img_hsv.shape).astype(np.uint8)
    seg_rgb = cv2.cvtColor(seg_hsv, cv2.COLOR_HSV2RGB)

    return seg_rgb, labels, centers

# Sử dụng
seg_hsv, labels_hsv, centers_hsv = kmeans_hsv(img_rgb, K=4)
```

### 4. Mean-Shift Segmentation (OpenCV)

```python
def meanshift_segmentation(img, spatial_radius=20, color_radius=40, min_size=100):
    """
    Mean-shift segmentation.

    Args:
        spatial_radius: Spatial window radius
        color_radius: Color window radius
        min_size: Minimum region size
    """
    # pyrMeanShiftFiltering
    seg = cv2.pyrMeanShiftFiltering(img, spatial_radius, color_radius)

    return seg

# Sử dụng
img_bgr = cv2.imread('satellite.jpg')
seg_meanshift = meanshift_segmentation(img_bgr, spatial_radius=21,
                                        color_radius=51)

cv2.imshow('Mean-Shift', seg_meanshift)
cv2.waitKey(0)
```

### 5. GMM với scikit-learn

```python
from sklearn.mixture import GaussianMixture
import numpy as np

def gmm_segmentation(img, n_components=4):
    """Phân vùng bằng Gaussian Mixture Model."""

    # Reshape
    pixels = img.reshape((-1, 3))

    # Fit GMM
    gmm = GaussianMixture(n_components=n_components, covariance_type='full',
                          max_iter=100, random_state=42)
    labels = gmm.fit_predict(pixels)

    # Tạo ảnh phân vùng
    seg = gmm.means_[labels].reshape(img.shape).astype(np.uint8)

    return seg, labels, gmm

# Sử dụng
seg_gmm, labels_gmm, model = gmm_segmentation(img_rgb, n_components=5)

# Thống kê
print(f"Weights: {model.weights_}")
print(f"Means:\n{model.means_}")
```

## So Sánh Các Phương Pháp

| Phương pháp | Độ phức tạp | Số cụm | Khởi tạo | Ưu điểm | Nhược điểm |
|------------|-------------|--------|----------|---------|------------|
| **K-means** | O(n×K×i) | Cần K | Quan trọng | Nhanh, đơn giản | Local minima, cần K |
| **K-means++** | O(n×K×i) | Cần K | Tốt hơn | Robust hơn | Vẫn cần K |
| **Mean-Shift** | O(n²×i) | Tự động | Không cần | Không cần K | Rất chậm |
| **GMM-EM** | O(n×K×d²×i) | Cần K | Quan trọng | Mô hình xác suất | Chậm, phức tạp |

## Ưu Nhược Điểm

### K-means

**Ưu điểm:**
- Đơn giản, dễ hiểu và cài đặt
- Nhanh O(n×K×i), scale tốt với dữ liệu lớn
- K-means++ cải thiện khởi tạo
- OpenCV hỗ trợ sẵn, tối ưu

**Nhược điểm:**
- Cần chỉ định K trước
- Nhạy với khởi tạo (local minima)
- Giả định cụm hình cầu, kích thước tương đương
- Nhạy với outliers

### Mean-Shift

**Ưu điểm:**
- Không cần chỉ định số cụm K
- Tìm được cụm hình dạng bất kỳ
- Robust với outliers
- Không giả định về phân bố

**Nhược điểm:**
- Rất chậm O(n²)
- Cần chọn bandwidth h
- Không scale với dữ liệu lớn
- Kết quả phụ thuộc nhiều vào h

### GMM

**Ưu điểm:**
- Mô hình xác suất, có posterior probabilities
- Cụm có thể hình ellipse (covariance)
- Soft clustering (mỗi điểm thuộc nhiều cụm)
- Có thể sử dụng BIC/AIC để chọn K

**Nhược điểm:**
- Chậm hơn K-means
- Phức tạp hơn (covariance matrix)
- Vẫn nhạy với khởi tạo
- Có thể singular covariance

## Kỹ Thuật Nâng Cao

### 1. Elbow Method để chọn K

```python
def find_optimal_k(img, k_range=range(2, 11)):
    """Tìm K tối ưu bằng Elbow method."""

    pixels = img.reshape((-1, 3)).astype(np.float32)
    inertias = []

    for k in k_range:
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 1.0)
        compactness, _, _ = cv2.kmeans(pixels, k, None, criteria, 10,
                                        cv2.KMEANS_PP_CENTERS)
        inertias.append(compactness)

    # Vẽ elbow curve
    import matplotlib.pyplot as plt
    plt.plot(k_range, inertias, 'bo-')
    plt.xlabel('Số cụm K')
    plt.ylabel('Inertia (Within-cluster sum of squares)')
    plt.title('Elbow Method')
    plt.grid(True)
    plt.show()

    return inertias
```

### 2. Silhouette Score

```python
from sklearn.metrics import silhouette_score

def evaluate_clustering(img, k_range=range(2, 11)):
    """Đánh giá clustering bằng Silhouette score."""

    pixels = img.reshape((-1, 3))
    scores = []

    for k in k_range:
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 1.0)
        _, labels, _ = cv2.kmeans(pixels.astype(np.float32), k, None,
                                   criteria, 10, cv2.KMEANS_PP_CENTERS)

        score = silhouette_score(pixels, labels.flatten())
        scores.append(score)
        print(f"K={k}: Silhouette = {score:.4f}")

    return scores
```

### 3. Superpixel SLIC + K-means

```python
from skimage.segmentation import slic

def superpixel_kmeans(img, n_segments=100, K=4):
    """
    Kết hợp SLIC superpixels với K-means.

    1. SLIC tạo superpixels
    2. K-means trên features của superpixels
    """
    # Bước 1: SLIC
    segments = slic(img, n_segments=n_segments, compactness=10,
                    sigma=1, start_label=1)

    # Bước 2: Tính feature cho mỗi superpixel
    n_sp = segments.max() + 1
    features = np.zeros((n_sp, 3))

    for i in range(n_sp):
        mask = (segments == i)
        if np.sum(mask) > 0:
            features[i] = np.mean(img[mask], axis=0)

    # Bước 3: K-means trên superpixels
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 1.0)
    _, sp_labels, centers = cv2.kmeans(features.astype(np.float32), K, None,
                                        criteria, 10, cv2.KMEANS_PP_CENTERS)

    # Bước 4: Map labels từ superpixels về pixels
    label_img = sp_labels[segments]
    seg = centers[label_img].reshape(img.shape).astype(np.uint8)

    return seg, label_img

# Ưu điểm: Nhanh hơn, preserve boundaries tốt hơn
```

### 4. Mini-Batch K-means cho ảnh lớn

```python
from sklearn.cluster import MiniBatchKMeans

def fast_kmeans(img, K=4, batch_size=1000):
    """Mini-batch K-means cho ảnh lớn."""

    pixels = img.reshape((-1, 3))

    # Mini-batch K-means
    mbkmeans = MiniBatchKMeans(n_clusters=K, batch_size=batch_size,
                                max_iter=100, random_state=42)
    labels = mbkmeans.fit_predict(pixels)

    # Tạo ảnh phân vùng
    seg = mbkmeans.cluster_centers_[labels].reshape(img.shape).astype(np.uint8)

    return seg, labels

# Nhanh gấp 10-100 lần với ảnh lớn
```

## Tài Liệu Tham Khảo

1. **MacQueen, J.** (1967). "Some methods for classification and analysis of multivariate observations." Proceedings of the Fifth Berkeley Symposium on Mathematical Statistics and Probability, 1(14), 281-297.

2. **Arthur, D., & Vassilvitskii, S.** (2007). "k-means++: The advantages of careful seeding." Proceedings of the Eighteenth Annual ACM-SIAM Symposium on Discrete Algorithms, 1027-1035.

3. **Comaniciu, D., & Meer, P.** (2002). "Mean shift: A robust approach toward feature space analysis." IEEE Transactions on Pattern Analysis and Machine Intelligence, 24(5), 603-619.

4. **Dempster, A. P., Laird, N. M., & Rubin, D. B.** (1977). "Maximum likelihood from incomplete data via the EM algorithm." Journal of the Royal Statistical Society: Series B, 39(1), 1-22.

## Liên Kết

- **Code thực hành:**
  - [Bài 8: K-means Clustering](/code-implement/T79-phan-vung-anh/bai-8-kmeans/)

- **Lý thuyết liên quan:**
  - [01: Thresholding Methods](01-thresholding-methods.md)
  - [02: Region-based Segmentation](02-region-based-segmentation.md)
  - [06: Segmentation Evaluation](06-segmentation-evaluation.md)

- **Tài liệu gốc:** T79-99 Phân vùng ảnh (trang 15-16)

---

**Tác giả:** Ph.D Phan Thanh Toàn
**Cập nhật:** 2025-11-17
**Phiên bản:** 1.0
