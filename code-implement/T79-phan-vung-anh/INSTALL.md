# HƯỚNG DẪN CÀI ĐẶT

## Yêu cầu

- **Python:** 3.8 trở lên
- **pip:** Package installer for Python

## Cài đặt thư viện

### Cách 1: Từ requirements.txt (Khuyến nghị)

```bash
pip install -r requirements.txt
```

### Cách 2: Cài từng thư viện

```bash
pip install opencv-python
pip install numpy
pip install matplotlib
pip install scipy
pip install scikit-image
```

### Cách 3: Dùng conda

```bash
conda install -c conda-forge opencv numpy matplotlib scipy scikit-image
```

## Kiểm tra cài đặt

Chạy lệnh sau để kiểm tra:

```python
python3 -c "import cv2, numpy, matplotlib, scipy, skimage; print('All libraries installed!')"
```

Nếu không có lỗi → Cài đặt thành công!

## Lỗi thường gặp

### Lỗi: pip không tìm thấy

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install python3-pip
```

**macOS:**
```bash
brew install python3
```

**Windows:**
- Download Python từ python.org
- Chọn "Add Python to PATH" khi cài

### Lỗi: Permission denied

**Linux/Mac:**
```bash
pip install --user -r requirements.txt
```

**Hoặc dùng sudo:**
```bash
sudo pip install -r requirements.txt
```

### Lỗi: opencv-python không cài được

Thử phiên bản headless:
```bash
pip install opencv-python-headless
```

### Lỗi: matplotlib backend

**Linux WSL:**
```bash
export MPLBACKEND=Agg
```

Hoặc edit code, thêm dòng này trước `import matplotlib.pyplot`:
```python
import matplotlib
matplotlib.use('Agg')
```

## Virtual Environment (Khuyến nghị)

Tạo môi trường ảo để tránh xung đột:

```bash
# Tạo venv
python3 -m venv venv

# Kích hoạt
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Cài thư viện
pip install -r requirements.txt

# Chạy code
python bai-1-global-thresholding/threshold.py
```

## Kiểm tra phiên bản

```bash
python3 --version    # Nên >= 3.8
pip --version
```

## Test chạy

Sau khi cài xong, test ngay:

```bash
cd bai-1-global-thresholding
python3 threshold.py
```

Nếu thấy:
- "Đang đọc ảnh..." → Code chạy OK!
- Hiện biểu đồ → matplotlib OK!
- "Đã lưu kết quả..." → Hoàn hảo!

---

**Nếu gặp lỗi khác, vui lòng tạo issue!**
