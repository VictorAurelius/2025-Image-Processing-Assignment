# Input Images Directory

Thư mục này chứa ảnh đầu vào cho các bài tập xử lý hình thái.

## Cấu trúc thư mục

```
input/
├── docs/           # Ảnh tài liệu/văn bản
│   ├── noisy_scan.png    # Bài 1: Văn bản có nhiễu
│   └── uneven.jpg        # Bài 9: Chiếu sáng không đều
├── parts/          # Ảnh linh kiện
│   └── gapped.png        # Bài 2: Linh kiện có khe hở
├── objects/        # Ảnh vật thể
│   └── sample.png        # Bài 3: Các vật thể mẫu
├── coins/          # Ảnh đồng xu/viên nén
│   └── touching.jpg      # Bài 4: Các đồng xu chạm nhau
├── plates/         # Ảnh biển số
│   └── plate.jpg         # Bài 5: Biển số xe
├── surface/        # Ảnh bề mặt
│   └── holes.png         # Bài 6: Bề mặt có lỗ
├── edges/          # Ảnh biên
│   └── jagged.png        # Bài 7: Biên có gai
└── conveyor/       # Ảnh băng chuyền
    └── items.png         # Bài 8: Vật thể trên băng chuyền
```

## Lưu ý

- Nếu thiếu ảnh input, chương trình sẽ **TỰ ĐỘNG TẠO** ảnh mẫu
- Bạn có thể thay thế bằng ảnh thực tế của mình
- Định dạng hỗ trợ: PNG, JPG, JPEG
- Khuyến nghị kích thước: 400x600 đến 800x1000 pixels

## Tạo ảnh mẫu

Chạy script để tạo tất cả ảnh mẫu:

```bash
python generate_samples.py
```

Hoặc mỗi bài tập sẽ tự động tạo ảnh khi chạy nếu thiếu input.
