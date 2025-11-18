# Đề 2024_KTPM01 - Kiểm Thử Phần Mềm

## Thông tin chung
- **Trường**: DHGTVI - KHOA CNTT - BỘ MÔN CNPM
- **Mã đề**: 2024_KTPM01
- **Thời gian làm bài**: 90 phút
- **Mã bộ môn**: 20410

---

## Đề bài

### Câu 1 (3 điểm)
- **(1.5 điểm)** Tại sao phải kiểm thử phần mềm?
- **(1.5 điểm)** Hãy trình bày hiểu biết của bạn về các quan niệm không đúng trong kiểm thử phần mềm.

### Câu 2 (3.5 điểm)
Cho một hàm trong chương trình sau:

```java
public static int cal(int m1, int d1, int m2, int d2, int y) {
    int numDays; // (1)
    if (m2 == m1) // (2)
        numDays = d2 - d1; // (3)
    else {
        int m4 = y % 4; // (4)
        int m100 = y % 100; // (5)
        int m400 = y % 400; // (6)
        int[] daysIn = { 0, 31, 0, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 }; // (7)
        if ((m4 != 0) || ((m100 == 0) && (m400 != 0))) // (8)
            daysIn[2] = 28; // (8)
        else
            daysIn[2] = 29; // (9)
        numDays = d2 + (daysIn[m1] - d1); // (10)
        int i = m1 + 1; // (11)
        while (i <= m2 - 1) { // (14)
            numDays = numDays + daysIn[i]; // (11)
            i++; // (12)
        }
    }
    return (numDays); // (17)
}
```

Để kiểm thử cho hàm trong chương trình trên, hãy thực hiện các yêu cầu sau đây:
- **(1.0 điểm)** Xây dựng đồ thị luồng điều khiển nhị phân cho hàm trên.
- **(0.5 điểm)** Xác định độ phức tạp của đồ thị.
- **(1.0 điểm)** Xác định các đường thị hành tuyến tính độc lập ứng với đồ thị luồng điều khiển.
- **(1.0 điểm)** Xác định ma trận bao phủ cho các đường thị hành tuyến tính ứng với kiểm thử có bản.

---

## Lời giải

### Câu 1: Tại sao phải kiểm thử phần mềm và các quan niệm sai lầm

#### Phần 1: Tại sao phải kiểm thử phần mềm? (1.5 điểm)

**Phân tích:**
Kiểm thử phần mềm là một giai đoạn quan trọng không thể thiếu trong quy trình phát triển phần mềm.

**Giải đáp:**

**1. Phát hiện lỗi sớm (Early Defect Detection):**
   - Tìm ra lỗi sớm giúp giảm chi phí sửa chữa (chi phí tăng theo cấp số nhân qua các giai đoạn)
   - Lỗi phát hiện ở giai đoạn yêu cầu rẻ hơn 100 lần so với phát hiện sau khi phát hành
   - Ngăn chặn lỗi lan truyền sang các module khác

**2. Đảm bảo chất lượng sản phẩm (Quality Assurance):**
   - Xác nhận phần mềm đáp ứng các yêu cầu chức năng và phi chức năng
   - Đảm bảo phần mềm hoạt động đúng trong các điều kiện khác nhau
   - Kiểm tra tính tương thích, hiệu năng, bảo mật, khả năng sử dụng

**3. Giảm rủi ro (Risk Reduction):**
   - **Rủi ro tài chính**: Tránh tổn thất do phải sửa lỗi sau khi phát hành
   - **Rủi ro pháp lý**: Tránh vi phạm hợp đồng, quy định pháp luật
   - **Rủi ro uy tín**: Bảo vệ thương hiệu, niềm tin khách hàng
   - **Rủi ro an toàn**: Đặc biệt quan trọng với phần mềm y tế, hàng không, tài chính

**4. Xác thực và Xác nhận (Verification & Validation):**
   - **Verification**: "Are we building the product right?" - Xây dựng đúng cách?
   - **Validation**: "Are we building the right product?" - Xây dựng đúng sản phẩm?
   - Đảm bảo sản phẩm đáp ứng nhu cầu thực tế của người dùng

**5. Tuân thủ tiêu chuẩn (Compliance):**
   - Đáp ứng các tiêu chuẩn ngành (ISO, CMMI, FDA, HIPAA, etc.)
   - Yêu cầu bắt buộc trong nhiều lĩnh vực (y tế, tài chính, hàng không)

**6. Cải thiện quy trình phát triển:**
   - Phản hồi giúp cải thiện kỹ năng lập trình viên
   - Phát hiện các vấn đề trong quy trình phát triển
   - Xây dựng văn hóa chất lượng trong tổ chức

**7. Tăng sự tin tưởng (Confidence Building):**
   - Cung cấp thông tin khách quan về mức độ sẵn sàng của phần mềm
   - Hỗ trợ ra quyết định về việc phát hành sản phẩm
   - Tăng niềm tin của stakeholders

**8. Tiết kiệm chi phí dài hạn:**
   - Chi phí kiểm thử << Chi phí sửa lỗi sau khi phát hành
   - Giảm chi phí bảo trì
   - Tăng tuổi thọ của phần mềm

#### Phần 2: Các quan niệm không đúng trong kiểm thử phần mềm (1.5 điểm)

**Quan niệm sai 1: "Kiểm thử hoàn toàn (Complete Testing) là khả thi"**
- **Sự thật**: Không thể kiểm thử tất cả các trường hợp có thể
- **Lý do**:
  - Số lượng đường đi, tổ hợp input là vô hạn hoặc cực lớn
  - Ví dụ: Một chương trình đơn giản với 3 input integer 32-bit có 2^96 tổ hợp
- **Thực tế**: Phải áp dụng kiểm thử dựa trên rủi ro (risk-based testing)

**Quan niệm sai 2: "Kiểm thử có thể chứng minh phần mềm không có lỗi"**
- **Sự thật**: Kiểm thử chỉ có thể chứng minh SỰ HIỆN DIỆN của lỗi, không thể chứng minh SỰ VẮNG MẶT của lỗi
- **Nguyên lý Dijkstra**: "Testing can show the presence of bugs, but never their absence"
- **Thực tế**: Mục tiêu là giảm thiểu lỗi đến mức chấp nhận được

**Quan niệm sai 3: "Kiểm thử chỉ là việc chạy code"**
- **Sự thật**: Kiểm thử bao gồm nhiều hoạt động:
  - Review tài liệu yêu cầu, thiết kế
  - Static analysis (phân tích tĩnh)
  - Code review
  - Test planning và design
  - Test execution
  - Defect tracking và reporting
- **Ước tính**: 30-40% defects có thể tìm thấy mà không cần chạy code

**Quan niệm sai 4: "Kiểm thử bắt đầu sau khi code hoàn thành"**
- **Sự thật**: Kiểm thử nên bắt đầu từ giai đoạn yêu cầu
- **Shift-left testing**: Di chuyển kiểm thử về phía trước trong SDLC
- **Lợi ích**: Tìm lỗi sớm, giảm chi phí

**Quan niệm sai 5: "Kiểm thử tự động thay thế hoàn toàn kiểm thử thủ công"**
- **Sự thật**: Cần kết hợp cả hai
- **Manual testing** cần thiết cho: Exploratory testing, Usability testing, Ad-hoc testing
- **Automated testing** hiệu quả cho: Regression testing, Performance testing, Load testing

**Quan niệm sai 6: "Tester không cần hiểu code"**
- **Sự thật**: Hiểu code giúp tester:
  - Thiết kế test cases hiệu quả hơn
  - Áp dụng white-box testing techniques
  - Hiểu root cause của defects
  - Giao tiếp tốt hơn với developers

**Quan niệm sai 7: "Nhiều test cases = Kiểm thử tốt hơn"**
- **Sự thật**: Chất lượng > Số lượng
- **Pesticide Paradox**: Chạy lại cùng test cases sẽ không tìm thêm lỗi mới
- **Thực tế**: Cần thiết kế test cases thông minh, bao phủ nhiều scenarios

**Quan niệm sai 8: "Nếu build pass qua tất cả tests thì đã sẵn sàng để release"**
- **Sự thật**: Cần xem xét nhiều yếu tố:
  - Test coverage có đủ không?
  - Các defects nghiêm trọng đã được fix chưa?
  - Non-functional requirements (performance, security, usability) đã được kiểm thử chưa?
  - Risk assessment

**Quan niệm sai 9: "Kiểm thử là trách nhiệm của tester"**
- **Sự thật**: Chất lượng là trách nhiệm của cả team
- **Developers**: Unit testing, code review
- **Testers**: Test planning, execution, automation
- **Business Analysts**: Requirements validation
- **DevOps**: Integration testing, deployment testing

**Quan niệm sai 10: "Tìm thấy và fix tất cả bugs"**
- **Sự thật**: Không thực tế và không cần thiết
- **80-20 rule**: 80% defects nằm trong 20% modules
- **Risk-based approach**: Tập trung vào critical areas

---

### Câu 2: Kiểm thử hàm cal()

**Phân tích:**
Hàm `cal()` tính số ngày giữa hai ngày trong cùng một năm. Nếu hai ngày cùng tháng, tính đơn giản bằng d2 - d1. Nếu khác tháng, tính số ngày còn lại của tháng đầu, cộng các tháng giữa, cộng số ngày của tháng cuối. Hàm cũng xử lý năm nhuận.

#### A. Xây dựng đồ thị luồng điều khiển (CFG)

**Xác định các node:**

```
Node 1:  Entry point
Node 2:  int numDays; // (1)
Node 3:  if (m2 == m1) // (2) - Decision node
Node 4:  numDays = d2 - d1; // (3)
Node 5:  int m4 = y % 4; int m100 = y % 100; int m400 = y % 400;
         int[] daysIn = {...}; // (4-7)
Node 6:  if ((m4 != 0) || ((m100 == 0) && (m400 != 0))) // (8) - Decision node
Node 7:  daysIn[2] = 28; // (8)
Node 8:  daysIn[2] = 29; // (9)
Node 9:  numDays = d2 + (daysIn[m1] - d1); int i = m1 + 1; // (10-11)
Node 10: while (i <= m2 - 1) // (14) - Decision node
Node 11: numDays = numDays + daysIn[i]; i++; // (11-12)
Node 12: return numDays; // (17)
Node 13: Exit point
```

**Đồ thị CFG:**

```
           [1 Entry]
               ↓
          [2 int numDays]
               ↓
       [3 if(m2 == m1)]
         ↙           ↘
      True          False
       ↓               ↓
[4 numDays=d2-d1]  [5 m4, m100, m400, daysIn[]]
       ↓               ↓
       |         [6 if(m4!=0 || ...)]
       |           ↙         ↘
       |        True        False
       |         ↓            ↓
       |    [7 daysIn[2]=28] [8 daysIn[2]=29]
       |         ↓            ↓
       |         └────┬───────┘
       |              ↓
       |         [9 numDays=..., i=m1+1]
       |              ↓
       |         [10 while(i <= m2-1)]
       |           ↙         ↘
       |        True        False
       |         ↓            ↓
       |    [11 numDays+=    [12 return numDays]
       |     daysIn[i], i++]  ↓
       |         ↓         [13 Exit]
       |         └→[10]
       |              ↓
       └──────────→[12 return numDays]
                      ↓
                  [13 Exit]
```

#### B. Xác định độ phức tạp vòng tròn (Cyclomatic Complexity)

**Đếm các điểm quyết định (Decision Points):**
1. `if (m2 == m1)` - Node 3
2. `if ((m4 != 0) || ((m100 == 0) && (m400 != 0)))` - Node 6
3. `while (i <= m2 - 1)` - Node 10

**Tính toán:**
- **V(G) = P + 1** (P = số điểm quyết định)
- V(G) = 3 + 1 = **4**

**Kết luận:** Độ phức tạp vòng tròn = 4, cần ít nhất 4 đường đi độc lập để kiểm thử đầy đủ.

#### C. Xác định các đường đi độc lập (Independent Paths)

**Đường đi 1 (Path 1):** Cùng tháng
```
1 → 2 → 3 → 4 → 12 → 13
Điều kiện: m1 == m2
Test case: cal(5, 10, 5, 25, 2024) = 15
          (Tháng 5 ngày 10 → Tháng 5 ngày 25)
```

**Đường đi 2 (Path 2):** Khác tháng, năm không nhuận, không vào vòng lặp
```
1 → 2 → 3 → 5 → 6 → 7 → 9 → 10 → 12 → 13
Điều kiện: m2 = m1 + 1 (hai tháng liền kề), năm không nhuận
Test case: cal(1, 15, 2, 10, 2023)
          - Năm 2023 không nhuận (2023 % 4 != 0)
          - daysIn[2] = 28
          - numDays = 10 + (31 - 15) = 26
          - i = 2, while(2 <= 1) = false, không vào vòng lặp
          = 26 ngày
```

**Đường đi 3 (Path 3):** Khác tháng, năm nhuận, không vào vòng lặp
```
1 → 2 → 3 → 5 → 6 → 8 → 9 → 10 → 12 → 13
Điều kiện: m2 = m1 + 1, năm nhuận
Test case: cal(1, 15, 2, 10, 2024)
          - Năm 2024 nhuận (2024 % 4 = 0, 2024 % 100 != 0)
          - daysIn[2] = 29
          - numDays = 10 + (31 - 15) = 26
          - i = 2, while(2 <= 1) = false
          = 26 ngày
```

**Đường đi 4 (Path 4):** Khác tháng, có vòng lặp (nhiều tháng giữa)
```
1 → 2 → 3 → 5 → 6 → 7 → 9 → 10 → 11 → 10 → 12 → 13
Điều kiện: m2 > m1 + 1 (có ít nhất 1 tháng ở giữa)
Test case: cal(1, 15, 4, 10, 2023)
          - Từ 15/1 đến 10/4
          - Năm 2023 không nhuận → daysIn[2] = 28
          - numDays = 10 + (31 - 15) = 26
          - i = 2:
            - while(2 <= 3): true
            - numDays = 26 + 28 = 54, i = 3
            - while(3 <= 3): true
            - numDays = 54 + 31 = 85, i = 4
            - while(4 <= 3): false
          = 85 ngày
```

#### D. Ma trận bao phủ (Coverage Matrix)

| Test Case | Path | m1 | d1 | m2 | d2 | y | Expected | Giải thích |
|-----------|------|----|----|----|----|------|----------|------------|
| TC1 | 1 | 5 | 10 | 5 | 25 | 2024 | 15 | Cùng tháng 5 |
| TC2 | 2 | 1 | 15 | 2 | 10 | 2023 | 26 | Khác tháng, không nhuận |
| TC3 | 3 | 1 | 15 | 2 | 10 | 2024 | 26 | Khác tháng, năm nhuận |
| TC4 | 4 | 1 | 15 | 4 | 10 | 2023 | 85 | Nhiều tháng, vòng lặp |

**Tính toán chi tiết TC4:**
- Ngày còn lại tháng 1: 31 - 15 = 16 ngày
- Tháng 2 (2023 không nhuận): 28 ngày
- Tháng 3: 31 ngày
- Ngày đầu tháng 4: 10 ngày
- **Tổng: 16 + 28 + 31 + 10 = 85 ngày**

**Ma trận bao phủ nhánh (Branch Coverage):**

| Decision Node | True Path | False Path | TC Coverage |
|---------------|-----------|------------|-------------|
| if (m2 == m1) | TC1 | TC2, TC3, TC4 | All |
| if (năm không nhuận) | TC2, TC4 | TC3 | All |
| while (i <= m2-1) | TC4 | TC1, TC2, TC3 | All |

**Phân tích năm nhuận:**
- Năm nhuận khi: (chia hết cho 4) VÀ (không chia hết cho 100 HOẶC chia hết cho 400)
- Điều kiện trong code: `(m4 != 0) || ((m100 == 0) && (m400 != 0))` → **năm KHÔNG nhuận**
- 2024: 2024%4=0, 2024%100=24, 2024%400=24 → (0!=0 false) || ((24==0 false) && (24!=0 true)) → false → **nhuận**
- 2023: 2023%4=3, → (3!=0 true) || ... → true → **không nhuận**

**Kết luận:**
- 4 test cases đạt 100% statement coverage
- Đạt 100% branch coverage
- Đạt 100% path coverage cho các đường độc lập
- Thỏa mãn basis path testing

**Lưu ý về bugs tiềm ẩn:**
1. Hàm giả định m2 >= m1 (không kiểm tra)
2. Không kiểm tra tính hợp lệ của tháng (1-12) và ngày (1-31)
3. Array daysIn có index 0 không sử dụng (lãng phí)
4. Biến `i` được khai báo ở line 2 nhưng không sử dụng
