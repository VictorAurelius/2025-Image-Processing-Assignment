"""
=============================================================================
BÀI 8: K-MEANS (GOM CỤM THEO MÀU/ĐẶC TRƯNG)
=============================================================================
Đề bài: Tách vùng vườn cây, sông, nhà trong ảnh vệ tinh nhỏ nhờ màu/HSV.
Mục tiêu: Gom cụm K=3-5 trên không gian màu (RGB/HSV) để phân mảnh đất.
Yêu cầu: Chuẩn hóa dữ liệu, reshape N×3; hiển thị kết quả theo label.

Tác giả: Ph.D Phan Thanh Toàn
Nguồn: T79-99 Phân vùng ảnh (trang 15-16)
=============================================================================
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os


def create_sample_satellite():
    """Tạo ảnh vệ tinh mẫu với các vùng khác nhau."""
    img = np.zeros((400, 600, 3), dtype=np.uint8)

    # Vùng rừng/cây (xanh lá)
    img[0:200, 0:300] = [34, 139, 34]
    # Thêm biến thể màu
    noise = np.random.randint(-20, 20, (200, 300, 3))
    img[0:200, 0:300] = np.clip(img[0:200, 0:300].astype(np.int16) + noise, 0, 255).astype(np.uint8)

    # Vùng sông/nước (xanh dương)
    img[0:200, 300:600] = [65, 105, 225]
    noise = np.random.randint(-15, 15, (200, 300, 3))
    img[0:200, 300:600] = np.clip(img[0:200, 300:600].astype(np.int16) + noise, 0, 255).astype(np.uint8)

    # Vùng nhà/đất trống (xám/nâu)
    img[200:400, 0:300] = [169, 169, 169]
    noise = np.random.randint(-25, 25, (200, 300, 3))
    img[200:400, 0:300] = np.clip(img[200:400, 0:300].astype(np.int16) + noise, 0, 255).astype(np.uint8)

    # Vùng đất canh tác (vàng/nâu nhạt)
    img[200:400, 300:600] = [210, 180, 140]
    noise = np.random.randint(-20, 20, (200, 300, 3))
    img[200:400, 300:600] = np.clip(img[200:400, 300:600].astype(np.int16) + noise, 0, 255).astype(np.uint8)

    # Thêm một vài đường/công trình
    cv2.line(img, (150, 0), (150, 400), (100, 100, 100), 5)
    cv2.rectangle(img, (250, 250), (320, 320), (150, 150, 150), -1)
    cv2.rectangle(img, (400, 280), (470, 350), (140, 140, 140), -1)

    return img


def kmeans_segmentation(img, K=4, max_iter=20):
    """
    Phân đoạn ảnh bằng K-means clustering.

    Args:
        img: Ảnh RGB đầu vào
        K: Số cụm
        max_iter: Số vòng lặp tối đa

    Returns:
        seg: Ảnh phân đoạn
        labels: Nhãn của mỗi pixel
        centers: Tâm của các cụm
    """
    # Reshape ảnh thành (N, 3) với N là số pixels
    Z = img.reshape((-1, 3)).astype(np.float32)

    # Tiêu chí dừng
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, max_iter, 1.0)

    # K-means clustering
    _, labels, centers = cv2.kmeans(Z, K, None, criteria, 5, cv2.KMEANS_PP_CENTERS)

    # Tạo ảnh phân đoạn với màu của tâm cụm
    seg = centers[labels.flatten()].reshape(img.shape).astype(np.uint8)

    return seg, labels, centers


def main():
    # Kiểm tra ảnh input
    input_path = "../input/satellite.jpg"

    if os.path.exists(input_path):
        print("Đang đọc ảnh từ:", input_path)
        img = cv2.imread(input_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    else:
        print("Không tìm thấy ảnh input, tạo ảnh mẫu...")
        img = create_sample_satellite()
        os.makedirs("../input", exist_ok=True)
        cv2.imwrite(input_path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
        print(f"Đã tạo ảnh mẫu tại: {input_path}")

    print("\n" + "="*60)
    print("K-MEANS CLUSTERING - GOM CỤM MÀU")
    print("="*60)

    # Tham số
    K = 4
    print(f"\nTham số:")
    print(f"  - Số cụm K: {K}")
    print(f"  - Kích thước ảnh: {img.shape}")
    print(f"  - Tổng số pixels: {img.shape[0] * img.shape[1]}")

    # Áp dụng K-means
    print("\nĐang thực hiện K-means clustering...")
    seg, labels, centers = kmeans_segmentation(img, K=K)

    # Thống kê
    print(f"\nTâm các cụm (RGB):")
    unique_labels, counts = np.unique(labels, return_counts=True)
    for i, (label, count) in enumerate(zip(unique_labels, counts)):
        center = centers[label]
        percentage = 100 * count / labels.size
        print(f"  Cụm {label}: RGB({center[0]:.0f}, {center[1]:.0f}, {center[2]:.0f}) - "
              f"{count} pixels ({percentage:.1f}%)")

    # Tạo ảnh với màu label khác nhau
    label_img = labels.reshape(img.shape[:2])

    # Tạo colormap cho labels
    cmap = plt.cm.get_cmap('tab10')
    label_colored = cmap(label_img / K)[:, :, :3]
    label_colored = (label_colored * 255).astype(np.uint8)

    # Test với K khác nhau
    print("\nThử nghiệm với K khác nhau...")
    seg_k3, labels_k3, _ = kmeans_segmentation(img, K=3)
    seg_k5, labels_k5, _ = kmeans_segmentation(img, K=5)
    seg_k6, labels_k6, _ = kmeans_segmentation(img, K=6)

    print(f"  - K=3: {len(np.unique(labels_k3))} cụm")
    print(f"  - K=5: {len(np.unique(labels_k5))} cụm")
    print(f"  - K=6: {len(np.unique(labels_k6))} cụm")

    # Chuyển sang HSV và thử K-means
    print("\nThử K-means trên không gian HSV...")
    img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    seg_hsv, labels_hsv, centers_hsv = kmeans_segmentation(img_hsv, K=K)
    seg_hsv = cv2.cvtColor(seg_hsv, cv2.COLOR_HSV2RGB)

    # Hiển thị kết quả
    plt.figure(figsize=(14, 12))

    plt.subplot(3, 4, 1)
    plt.imshow(img)
    plt.title("Ảnh gốc", fontsize=11, fontweight='bold')
    plt.axis('off')

    plt.subplot(3, 4, 2)
    plt.imshow(seg)
    plt.title(f"K-means RGB (K={K})", fontsize=11, fontweight='bold')
    plt.axis('off')

    plt.subplot(3, 4, 3)
    plt.imshow(label_colored)
    plt.title("Labels (màu phân biệt)", fontsize=11, fontweight='bold')
    plt.axis('off')

    plt.subplot(3, 4, 4)
    plt.imshow(seg_hsv)
    plt.title(f"K-means HSV (K={K})", fontsize=11, fontweight='bold')
    plt.axis('off')

    plt.subplot(3, 4, 5)
    plt.imshow(seg_k3)
    plt.title("K=3", fontsize=11, fontweight='bold')
    plt.axis('off')

    plt.subplot(3, 4, 6)
    plt.imshow(seg)
    plt.title(f"K={K}", fontsize=11, fontweight='bold')
    plt.axis('off')

    plt.subplot(3, 4, 7)
    plt.imshow(seg_k5)
    plt.title("K=5", fontsize=11, fontweight='bold')
    plt.axis('off')

    plt.subplot(3, 4, 8)
    plt.imshow(seg_k6)
    plt.title("K=6", fontsize=11, fontweight='bold')
    plt.axis('off')

    # Histogram màu cho mỗi cụm
    plt.subplot(3, 4, 9)
    colors = ['red', 'green', 'blue', 'orange', 'purple', 'brown'][:K]
    for i in range(K):
        mask = (label_img == i)
        count = np.sum(mask)
        plt.bar(i, count, color=colors[i], alpha=0.7)
    plt.title("Phân bố pixels theo cụm", fontsize=11, fontweight='bold')
    plt.xlabel("Cụm")
    plt.ylabel("Số pixels")
    plt.grid(alpha=0.3)

    # Hiển thị từng cụm riêng lẻ
    for i in range(min(3, K)):
        plt.subplot(3, 4, 10 + i)
        mask = (label_img == i)
        cluster_img = img.copy()
        cluster_img[~mask] = [255, 255, 255]
        plt.imshow(cluster_img)
        plt.title(f"Cụm {i} ({np.sum(mask)} pixels)", fontsize=10, fontweight='bold')
        plt.axis('off')

    plt.tight_layout()

    # Lưu kết quả
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "kmeans_result.png")
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"\nĐã lưu kết quả tại: {output_path}")

    plt.show()

    print("\n" + "="*60)
    print("HOÀN THÀNH!")
    print("="*60)


if __name__ == "__main__":
    main()
