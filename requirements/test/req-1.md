# Plan Task: Xử lý và Giải đề thi từ hình ảnh

## Mục tiêu
Đọc các file ảnh đề thi (de1.jpg, de2.jpg, de3.jpg, de4.jpg), trích xuất nội dung đề bài, và cung cấp lời giải chi tiết cho từng câu hỏi.

## Các bước thực hiện

### Bước 1: Xử lý de1.jpg
1. **Đọc file ảnh**: `requirements/test/de1.jpg`
2. **Trích xuất nội dung đề bài**:
   - Đọc kỹ toàn bộ văn bản trong ảnh
   - Ghi chép lại đề bài một cách chính xác, bao gồm:
     - Tiêu đề đề thi
     - Thời gian làm bài
     - Tất cả các câu hỏi (Câu 1, Câu 2, ...)
     - Code mẫu (nếu có)
     - Các yêu cầu cụ thể
3. **Tạo file markdown**: `requirements/test/de1-solution.md`
   - Phần 1: Ghi lại đề bài đầy đủ
   - Phần 2: Lời giải chi tiết cho từng câu hỏi
4. **Yêu cầu về lời giải**:
   - Giải thích rõ ràng, dễ hiểu
   - Cung cấp ví dụ minh họa (nếu cần)
   - Code solution (nếu câu hỏi yêu cầu code)
   - Phân tích test cases (nếu có)

### Bước 2: Xử lý de2.jpg
1. **Đọc file ảnh**: `requirements/test/de2.jpg`
2. **Trích xuất nội dung đề bài** (tương tự Bước 1)
3. **Tạo file markdown**: `requirements/test/de2-solution.md`
4. **Viết lời giải chi tiết**

### Bước 3: Xử lý de3.jpg
1. **Đọc file ảnh**: `requirements/test/de3.jpg`
2. **Trích xuất nội dung đề bài** (tương tự Bước 1)
3. **Tạo file markdown**: `requirements/test/de3-solution.md`
4. **Viết lời giải chi tiết**

### Bước 4: Xử lý de4.jpg
1. **Đọc file ảnh**: `requirements/test/de4.jpg`
2. **Trích xuất nội dung đề bài** (tương tự Bước 1)
3. **Tạo file markdown**: `requirements/test/de4-solution.md`
4. **Viết lời giải chi tiết**

## Cấu trúc file markdown output

Mỗi file `deX-solution.md` sẽ có cấu trúc như sau:

```markdown
# Đề [Số đề] - [Tên môn học]

## Thông tin chung
- **Thời gian**: [X phút]
- **Ngày thi**: [nếu có]
- **Mã đề**: [nếu có]

---

## Đề bài

### Câu 1
[Nội dung câu hỏi 1]

### Câu 2
[Nội dung câu hỏi 2]

...

---

## Lời giải

### Câu 1: [Tóm tắt nội dung câu hỏi]

**Phân tích:**
[Phân tích yêu cầu của câu hỏi]

**Giải đáp:**
[Lời giải chi tiết]

**Code (nếu có):**
\`\`\`[language]
[code solution]
\`\`\`

**Giải thích:**
[Giải thích code/lời giải]

### Câu 2: [Tóm tắt nội dung câu hỏi]

...
```

## Lưu ý quan trọng

1. **Độ chính xác**: Đảm bảo đọc và ghi chép đề bài chính xác 100%, không sai sót
2. **Định dạng**: Sử dụng markdown formatting đúng chuẩn
3. **Code blocks**: Sử dụng syntax highlighting phù hợp (C, C++, Java, Python, etc.)
4. **Lời giải**:
   - Phải rõ ràng, logic, dễ hiểu
   - Giải thích từng bước
   - Cung cấp test cases nếu câu hỏi về testing/debugging
5. **Đường dẫn lưu file**: Tất cả file output lưu tại `requirements/test/`

## Checklist hoàn thành

- [ ] Đọc và xử lý de1.jpg → Tạo de1-solution.md
- [ ] Đọc và xử lý de2.jpg → Tạo de2-solution.md
- [ ] Đọc và xử lý de3.jpg → Tạo de3-solution.md
- [ ] Đọc và xử lý de4.jpg → Tạo de4-solution.md
- [ ] Kiểm tra lại tất cả các file output
- [ ] Đảm bảo format markdown đúng chuẩn
- [ ] Đảm bảo lời giải đầy đủ và chính xác

## Ghi chú
- Nếu ảnh không rõ ràng ở một số phần, ghi chú lại và cố gắng suy luận hợp lý
- Nếu có công thức toán học, sử dụng LaTeX notation trong markdown
- Đối với bảng biểu, sử dụng markdown table format
