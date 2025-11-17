# Hướng Dẫn Chuẩn Bị Ảnh Input

## 📋 Tổng Quan

Folder này chứa ảnh đầu vào cho các bài tập về **Tách Biên** (T21-40).

## 🎯 Các Cách Chuẩn Bị Ảnh

### Cách 1: Tự Động Tạo Ảnh Mẫu (Khuyến Nghị)

Chạy script tự động tạo tất cả ảnh mẫu cần thiết:

```bash
cd input
python generate_samples.py
```

Script sẽ tạo 10 ảnh mẫu trong folder `sample-images/`.

### Cách 2: Tự Chuẩn Bị Ảnh

Đặt ảnh của bạn vào `input/sample-images/` với tên tương ứng:

| Bài | Tên File | Mô Tả | Yêu Cầu |
|-----|----------|-------|---------|
| 1 | `building.jpg` | Tòa nhà/đường phố | Ảnh có nhiều cạnh rõ nét |
| 2 | `doc.jpg` | Giấy A4 chụp nghiêng | Nền tương phản với giấy |
| 3 | `road.jpg` | Đường cao tốc | Camera hành trình, có làn |
| 4 | `surface.jpg` | Bề mặt kim loại/nhựa | Có vài vết xước mảnh |
| 5 | `coins.jpg` | Đồng xu/bi tròn | Từ trên xuống, ít chồng lấn |
| 6 | `product.jpg` | Sản phẩm trên nền | Nền đơn giản (trắng/xám) |
| 7 | `surface_crack.jpg` | Bê tông có vết nứt | Vết nứt mảnh, ánh sáng đều |
| 8 | `leaf.jpg` | Lá cây trên nền | Nền tương phản |
| 9 | `measure.jpg` | Vật thể + đồng xu | Đồng xu làm chuẩn đo |
| 10 | `receipt.jpg` | Hoá đơn/biên bản | Bị nghiêng 5-15 độ |

### Cách 3: Để Code Tự Tạo (Fallback)

Nếu không tìm thấy ảnh, mỗi script sẽ tự động tạo ảnh mẫu khi chạy.

## 📝 Lưu Ý

- **Định dạng**: JPG hoặc PNG
- **Kích thước**: 600x800 hoặc lớn hơn (khuyến nghị)
- **Chất lượng**: Tốt, ít nhiễu, ánh sáng đều
- **Nền**: Đơn giản, tương phản với đối tượng

## 🔧 Yêu Cầu Đặc Biệt

### Bài 2 (Document Scanning)
- Giấy A4 trắng trên nền tối HOẶC ngược lại
- Góc chụp: Nghiêng 15-30 độ
- 4 góc giấy phải rõ ràng

### Bài 3 (Lane Detection)
- Đường cao tốc với làn rõ ràng
- Camera nhìn từ xe, góc khoảng 30-45 độ xuống
- Ánh sáng ban ngày

### Bài 5 (Coin Counting)
- Đồng xu không chồng lấn quá nhiều
- Chụp từ trên xuống (overhead)
- Kích thước đồng xu tương đối đồng đều

### Bài 9 (Object Measurement)
- BẮT BUỘC có đồng xu hoặc vật chuẩn với kích thước đã biết
- Vật thể cần đo và đồng xu cùng nằm trên mặt phẳng
- Camera gần vuông góc với mặt phẳng

## ✅ Kiểm Tra

Sau khi chuẩn bị ảnh, kiểm tra:

```bash
ls -lh sample-images/
```

Nên thấy 10 file ảnh.

## 🆘 Troubleshooting

**Lỗi: "File not found"**
→ Chạy `python generate_samples.py` hoặc để code tự tạo

**Lỗi: "Cannot read image"**
→ Kiểm tra định dạng file (JPG/PNG)

**Kết quả kém**:
→ Thử ảnh với chất lượng tốt hơn, ánh sáng đều hơn
