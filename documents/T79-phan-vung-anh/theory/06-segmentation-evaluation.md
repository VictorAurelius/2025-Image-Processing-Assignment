# Lý Thuyết: Đánh Giá Phân Vùng Ảnh (Segmentation Evaluation)

## Tổng Quan

Đánh giá chất lượng phân vùng ảnh là bước quan trọng để so sánh các phương pháp và tinh chỉnh tham số. Không giống classification có ground truth rõ ràng, segmentation evaluation phức tạp hơn vì ranh giới vùng có thể subjective và phụ thuộc vào ứng dụng.

Có hai nhóm metrics chính: **Supervised metrics** (có ground truth - Dice, IoU, Precision/Recall) và **Unsupervised metrics** (không cần ground truth - Dunn Index, Silhouette). Supervised metrics đánh giá độ chính xác so với nhãn thủ công, trong khi unsupervised metrics đánh giá chất lượng clustering.

Việc lựa chọn metric phù hợp phụ thuộc vào ứng dụng: IoU cho object detection, Dice cho medical imaging, F-measure cho edge detection.

## Metrics Chính

### 1. Confusion Matrix

**Định nghĩa:**

```
                Predicted
              Positive | Negative
        _____|__________|__________
Actual  Pos  |   TP    |    FN
        Neg  |   FP    |    TN
```

Với:
- TP (True Positive): Pixels được phân đúng là foreground
- FP (False Positive): Pixels bị phân nhầm là foreground
- TN (True Negative): Pixels được phân đúng là background
- FN (False Negative): Pixels bị bỏ sót (should be foreground)

### 2. Precision, Recall, F-measure

**Precision (Độ chính xác):**

```
Precision = TP / (TP + FP)
```

Tỷ lệ pixels được phân đúng trong tất cả pixels được phân là foreground.

**Recall (Độ phủ - Sensitivity):**

```
Recall = TP / (TP + FN)
```

Tỷ lệ pixels foreground thực tế được phát hiện.

**F-measure (F1-score):**

```
F₁ = 2 × (Precision × Recall) / (Precision + Recall)
```

Harmonic mean của Precision và Recall.

**F-beta score:**

```
Fᵦ = (1 + β²) × (Precision × Recall) / (β² × Precision + Recall)
```

- β > 1: Ưu tiên Recall
- β < 1: Ưu tiên Precision

### 3. IoU (Intersection over Union)

**Jaccard Index:**

```
IoU = |A ∩ B| / |A ∪ B| = TP / (TP + FP + FN)
```

Với A = predicted, B = ground truth.

**Ý nghĩa:** IoU = 1 (perfect), IoU > 0.5 (acceptable), IoU > 0.7 (good)

**mIoU (mean IoU):** Trung bình IoU của tất cả các classes.

### 4. Dice Coefficient

**Sørensen-Dice Coefficient:**

```
Dice = 2 × |A ∩ B| / (|A| + |B|) = 2TP / (2TP + FP + FN)
```

**Quan hệ với IoU:**

```
Dice = 2 × IoU / (1 + IoU)
```

**Ưu điểm:** Dice đánh giá cao overlap hơn IoU, phù hợp medical imaging.

### 5. Pixel Accuracy

**Global Accuracy:**

```
PA = (TP + TN) / (TP + TN + FP + FN)
```

**Mean Pixel Accuracy (mPA):**

```
mPA = (1/K) × Σₖ TPₖ / (TPₖ + FNₖ)
```

K là số classes.

### 6. Boundary-based Metrics

**Boundary F1 (BF):**

Đánh giá chất lượng biên thay vì toàn bộ vùng.

```
BF = 2 × (Pᵦ × Rᵦ) / (Pᵦ + Rᵦ)
```

Với:
- Pᵦ: Precision của boundary pixels
- Rᵦ: Recall của boundary pixels

**Hausdorff Distance:**

```
H(A, B) = max{h(A,B), h(B,A)}
h(A,B) = max{min{d(a,b) | b ∈ B} | a ∈ A}
```

Đo khoảng cách tối đa giữa 2 biên.

### 7. Unsupervised Metrics

**Dunn Index:**

```
D = min{δ(Cᵢ, Cⱼ)} / max{Δ(Cₖ)}
```

Với:
- δ(Cᵢ, Cⱼ): Inter-cluster distance
- Δ(Cₖ): Intra-cluster distance

D càng cao → clustering càng tốt.

**Silhouette Coefficient:**

```
s(i) = (b(i) - a(i)) / max{a(i), b(i)}
```

Với:
- a(i): Trung bình khoảng cách đến cùng cluster
- b(i): Trung bình khoảng cách đến cluster gần nhất

s ∈ [-1, 1], s → 1 là tốt.

**Davies-Bouldin Index:**

```
DB = (1/K) × Σᵢ max{(Δᵢ + Δⱼ) / δᵢⱼ}
```

DB càng nhỏ → clustering càng tốt.

## Code Examples

### 1. Confusion Matrix và Basic Metrics

```python
import numpy as np

def compute_metrics(pred, gt):
    """
    Tính các metrics cơ bản.

    Args:
        pred: Predicted binary mask (0/255)
        gt: Ground truth binary mask (0/255)

    Returns:
        dict: Metrics
    """
    # Chuyển về binary
    pred = (pred > 127).astype(np.uint8)
    gt = (gt > 127).astype(np.uint8)

    # Confusion matrix
    TP = np.sum((pred == 1) & (gt == 1))
    FP = np.sum((pred == 1) & (gt == 0))
    TN = np.sum((pred == 0) & (gt == 0))
    FN = np.sum((pred == 0) & (gt == 1))

    # Metrics
    precision = TP / (TP + FP + 1e-7)
    recall = TP / (TP + FN + 1e-7)
    f1 = 2 * precision * recall / (precision + recall + 1e-7)
    accuracy = (TP + TN) / (TP + TN + FP + FN)

    # IoU
    iou = TP / (TP + FP + FN + 1e-7)

    # Dice
    dice = 2 * TP / (2*TP + FP + FN + 1e-7)

    return {
        'TP': TP, 'FP': FP, 'TN': TN, 'FN': FN,
        'Precision': precision,
        'Recall': recall,
        'F1': f1,
        'Accuracy': accuracy,
        'IoU': iou,
        'Dice': dice
    }

# Sử dụng
pred = cv2.imread('predicted.png', 0)
gt = cv2.imread('ground_truth.png', 0)

metrics = compute_metrics(pred, gt)
for k, v in metrics.items():
    if k not in ['TP', 'FP', 'TN', 'FN']:
        print(f"{k}: {v:.4f}")
```

### 2. mIoU (Multi-class)

```python
def mean_iou(pred_labels, gt_labels, num_classes):
    """
    Tính mean IoU cho multi-class segmentation.

    Args:
        pred_labels: Predicted labels (H×W)
        gt_labels: Ground truth labels (H×W)
        num_classes: Số classes

    Returns:
        miou: Mean IoU
        ious: IoU của từng class
    """
    ious = []

    for cls in range(num_classes):
        pred_cls = (pred_labels == cls)
        gt_cls = (gt_labels == cls)

        intersection = np.sum(pred_cls & gt_cls)
        union = np.sum(pred_cls | gt_cls)

        if union == 0:
            iou = float('nan')  # Bỏ qua class không có
        else:
            iou = intersection / union

        ious.append(iou)

    # Mean IoU (bỏ qua NaN)
    miou = np.nanmean(ious)

    return miou, ious

# Sử dụng
pred_labels = np.array([[0, 0, 1], [1, 2, 2], [2, 2, 2]])
gt_labels = np.array([[0, 0, 1], [1, 1, 2], [2, 2, 2]])

miou, ious = mean_iou(pred_labels, gt_labels, num_classes=3)
print(f"mIoU: {miou:.4f}")
for i, iou in enumerate(ious):
    print(f"  Class {i}: {iou:.4f}")
```

### 3. Boundary F1

```python
from scipy.ndimage import distance_transform_edt

def boundary_f1(pred, gt, threshold=2):
    """
    Tính Boundary F1 score.

    Args:
        pred: Predicted binary mask
        gt: Ground truth binary mask
        threshold: Distance threshold (pixels)

    Returns:
        bf1: Boundary F1 score
    """
    # Tìm biên
    pred_boundary = cv2.Canny(pred.astype(np.uint8) * 255, 50, 150) > 0
    gt_boundary = cv2.Canny(gt.astype(np.uint8) * 255, 50, 150) > 0

    # Distance transform
    dist_pred = distance_transform_edt(~gt_boundary)
    dist_gt = distance_transform_edt(~pred_boundary)

    # Precision: Phần trăm boundary predicted gần ground truth
    precision = np.sum(dist_pred[pred_boundary] <= threshold) / (np.sum(pred_boundary) + 1e-7)

    # Recall: Phần trăm ground truth boundary được phát hiện
    recall = np.sum(dist_gt[gt_boundary] <= threshold) / (np.sum(gt_boundary) + 1e-7)

    # F1
    bf1 = 2 * precision * recall / (precision + recall + 1e-7)

    return bf1, precision, recall

# Sử dụng
bf1, bp, br = boundary_f1(pred, gt, threshold=2)
print(f"Boundary F1: {bf1:.4f} (P={bp:.4f}, R={br:.4f})")
```

### 4. Hausdorff Distance

```python
from scipy.spatial.distance import directed_hausdorff

def hausdorff_distance(pred, gt):
    """Tính Hausdorff distance giữa 2 biên."""

    # Tìm biên
    pred_boundary = cv2.Canny(pred.astype(np.uint8) * 255, 50, 150) > 0
    gt_boundary = cv2.Canny(gt.astype(np.uint8) * 255, 50, 150) > 0

    # Tọa độ pixels biên
    pred_points = np.argwhere(pred_boundary)
    gt_points = np.argwhere(gt_boundary)

    # Hausdorff distance
    h1 = directed_hausdorff(pred_points, gt_points)[0]
    h2 = directed_hausdorff(gt_points, pred_points)[0]

    hd = max(h1, h2)

    return hd

# Sử dụng
hd = hausdorff_distance(pred, gt)
print(f"Hausdorff Distance: {hd:.2f} pixels")
```

### 5. Unsupervised Metrics

```python
from sklearn.metrics import silhouette_score, davies_bouldin_score

def evaluate_clustering(img, labels):
    """
    Đánh giá unsupervised clustering.

    Args:
        img: Ảnh gốc (H×W×3)
        labels: Labels (H×W)

    Returns:
        metrics: Dict of scores
    """
    # Flatten
    pixels = img.reshape((-1, 3))
    labels_flat = labels.flatten()

    # Silhouette score
    sil = silhouette_score(pixels, labels_flat)

    # Davies-Bouldin index
    db = davies_bouldin_score(pixels, labels_flat)

    return {
        'Silhouette': sil,
        'Davies-Bouldin': db
    }

# Sử dụng
img = cv2.imread('image.jpg')
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# K-means
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=4, random_state=42)
labels = kmeans.fit_predict(img_rgb.reshape(-1, 3)).reshape(img_rgb.shape[:2])

metrics = evaluate_clustering(img_rgb, labels)
print(f"Silhouette: {metrics['Silhouette']:.4f}")
print(f"Davies-Bouldin: {metrics['Davies-Bouldin']:.4f}")
```

## So Sánh Metrics

| Metric | Phạm vi | Supervised? | Ưu điểm | Nhược điểm |
|--------|---------|-------------|---------|------------|
| **IoU** | [0,1] | Có | Standard, dễ hiểu | Bias với class imbalance |
| **Dice** | [0,1] | Có | Medical imaging | Tương tự IoU |
| **F1** | [0,1] | Có | Balance P&R | Cần threshold |
| **BF** | [0,1] | Có | Tập trung biên | Tính toán chậm |
| **Hausdorff** | [0,∞) | Có | Đo max error | Nhạy outliers |
| **Silhouette** | [-1,1] | Không | Không cần GT | Chậm với n lớn |

## Kỹ Thuật Nâng Cao

### 1. Per-class Metrics

```python
def per_class_metrics(pred_labels, gt_labels, num_classes):
    """Tính metrics chi tiết cho từng class."""

    results = []

    for cls in range(num_classes):
        pred_cls = (pred_labels == cls).astype(np.uint8)
        gt_cls = (gt_labels == cls).astype(np.uint8)

        metrics = compute_metrics(pred_cls * 255, gt_cls * 255)
        metrics['class'] = cls

        results.append(metrics)

    return results

# Hiển thị bảng
import pandas as pd
df = pd.DataFrame(results)
print(df[['class', 'Precision', 'Recall', 'F1', 'IoU']])
```

### 2. Confusion Matrix Visualization

```python
import matplotlib.pyplot as plt
import seaborn as sns

def plot_confusion_matrix(pred_labels, gt_labels, num_classes, class_names=None):
    """Vẽ confusion matrix cho multi-class."""

    cm = np.zeros((num_classes, num_classes), dtype=np.int64)

    for i in range(num_classes):
        for j in range(num_classes):
            cm[i, j] = np.sum((gt_labels == i) & (pred_labels == j))

    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=class_names or range(num_classes),
                yticklabels=class_names or range(num_classes))
    plt.ylabel('Ground Truth')
    plt.xlabel('Predicted')
    plt.title('Confusion Matrix')
    plt.show()
```

### 3. Precision-Recall Curve

```python
def precision_recall_curve(pred_prob, gt):
    """Vẽ PR curve với nhiều thresholds."""

    thresholds = np.linspace(0, 1, 100)
    precisions = []
    recalls = []

    for thresh in thresholds:
        pred = (pred_prob > thresh).astype(np.uint8)
        metrics = compute_metrics(pred * 255, gt)

        precisions.append(metrics['Precision'])
        recalls.append(metrics['Recall'])

    plt.figure(figsize=(8, 6))
    plt.plot(recalls, precisions, 'b-', linewidth=2)
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall Curve')
    plt.grid(True)
    plt.show()

    # AP (Average Precision)
    ap = np.trapz(precisions, recalls)
    return ap
```

## Tài Liệu Tham Khảo

1. **Dice, L. R.** (1945). "Measures of the amount of ecologic association between species." Ecology, 26(3), 297-302.

2. **Jaccard, P.** (1912). "The distribution of the flora in the alpine zone." New Phytologist, 11(2), 37-50.

3. **Martin, D., et al.** (2004). "Learning to detect natural image boundaries using local brightness, color, and texture cues." IEEE TPAMI, 26(5), 530-549.

4. **Rousseeuw, P. J.** (1987). "Silhouettes: a graphical aid to the interpretation and validation of cluster analysis." Journal of Computational and Applied Mathematics, 20, 53-65.

## Liên Kết

- **Lý thuyết:**
  - [01: Thresholding](01-thresholding-methods.md)
  - [02: Region-based](02-region-based-segmentation.md)
  - [03: Clustering](03-clustering-segmentation.md)

---

**Tác giả:** Ph.D Phan Thanh Toàn | **Cập nhật:** 2025-11-17
