# Đề 03 - Kiểm Thử Phần Mềm

## Thông tin chung
- **Thời gian**: 60 phút
- **Đề số**: 03

---

## Đề bài

### Câu 1
Hãy phân biệt các khái niệm "Errors", "Faults" và "Failures" trong kiểm thử phần mềm.

Hãy trình bày khái niệm về mục đích của một kiểu thử vấn đề trong kiểm thử phần mềm.

### Câu 2
Cho một hàm trong chương trình sau:

```c
double average(int value, int step, int min, int max){
    double res = 0.0; // (1)
    int i = 0; // (2)
    int k = 0; // (3)
    int count = 0; // (4)
    int sum = 0; // (5)
    double temp = 0.0; // (6)
    while (k < step){ // (7)
        k++; // (8)
        temp = value * k; // (9)
        if (temp >= min && temp <= max){ // (10)
            count++; // (11)
            sum += temp; // (11)
        }
        if (temp > max) break; // (12)
    }
    if (count > 0){ // (14)
        res = sum / count; // (15)
    }
    return res; // (16)
}
```

Để kiểm thử cho hàm trong chương trình trên, hãy thực hiện các yêu cầu sau đây:

A. Xây dựng ca kiểm thử
- Xây dựng đồ thị luồng điều khiển nhị phân cho hàm trên.
- Xác định độ phức tạp của đồ thị.
- Xác định các đường thị hành tuyến tính độc lập ứng với đồ thị luồng điều khiển.
- Xác định ma trận bao phủ cho các đường thị hành tuyến tính ứng với các ca kiểm thử có bản.

---

## Lời giải

### Câu 1: Phân biệt Errors, Faults và Failures

**Phân tích:**
Câu hỏi yêu cầu phân biệt ba khái niệm cơ bản trong kiểm thử phần mềm và giải thích mục đích của kiểm thử.

**Giải đáp:**

#### Phân biệt Errors, Faults và Failures:

1. **Error (Lỗi/Sai lầm):**
   - Là sai lầm do con người gây ra trong quá trình phát triển phần mềm
   - Nguyên nhân: do thiếu hiểu biết, nhầm lẫn, hoặc không cẩn thận của lập trình viên
   - Ví dụ: Lập trình viên hiểu sai yêu cầu, viết sai công thức tính toán, logic sai

2. **Fault (Lỗi trong code/Defect):**
   - Là biểu hiện của Error trong code, thiết kế hoặc tài liệu
   - Là kết quả trực tiếp của Error
   - Có thể tồn tại trong code nhưng chưa được kích hoạt
   - Ví dụ: Một câu lệnh if có điều kiện sai, một vòng lặp thiếu điều kiện dừng

3. **Failure (Hỏng hóc/Lỗi thực thi):**
   - Là sự sai lệch giữa kết quả thực tế và kết quả mong đợi khi chạy chương trình
   - Xảy ra khi Fault được kích hoạt trong quá trình thực thi
   - Là biểu hiện bên ngoài mà người dùng có thể quan sát được
   - Ví dụ: Chương trình crash, hiển thị kết quả sai, không phản hồi

**Mối quan hệ:**
```
Error (sai lầm của con người)
  → Fault (lỗi trong code)
    → Failure (lỗi khi thực thi)
```

**Lưu ý quan trọng:**
- Không phải mọi Error đều dẫn đến Fault
- Không phải mọi Fault đều dẫn đến Failure (fault có thể không được kích hoạt)
- Một Error có thể tạo ra nhiều Faults
- Một Fault có thể gây ra nhiều Failures khác nhau

#### Mục đích của kiểm thử phần mềm:

1. **Phát hiện lỗi (Defect Detection):**
   - Tìm ra các Faults trong code trước khi phần mềm được phát hành
   - Giảm thiểu Failures trong môi trường production

2. **Đảm bảo chất lượng (Quality Assurance):**
   - Xác nhận phần mềm đáp ứng các yêu cầu đã định
   - Đảm bảo phần mềm hoạt động đúng như mong đợi

3. **Xác thực và Xác nhận (Verification & Validation):**
   - Verification: "Are we building the product right?" (Xây dựng đúng không?)
   - Validation: "Are we building the right product?" (Xây dựng đúng sản phẩm không?)

4. **Tăng độ tin cậy:**
   - Cung cấp thông tin về mức độ tin cậy của phần mềm
   - Giúp đưa ra quyết định về việc phát hành sản phẩm

5. **Giảm rủi ro:**
   - Giảm thiểu rủi ro về tài chính, uy tín và pháp lý
   - Tránh các sự cố nghiêm trọng khi triển khai

---

### Câu 2: Kiểm thử hàm average()

**Phân tích:**
Hàm `average()` tính giá trị trung bình của các số thỏa mãn điều kiện: `min <= value*k <= max` với k từ 1 đến step.

**A. Xây dựng đồ thị luồng điều khiển (Control Flow Graph - CFG)**

#### Bước 1: Xác định các node

```
Node 1:  Entry point
Node 2:  double res = 0.0; int i = 0; int k = 0; int count = 0; int sum = 0; double temp = 0.0;
Node 3:  while (k < step) - Decision node
Node 4:  k++; temp = value * k;
Node 5:  if (temp >= min && temp <= max) - Decision node
Node 6:  count++; sum += temp;
Node 7:  if (temp > max) - Decision node
Node 8:  break;
Node 9:  Back to while condition (Node 3)
Node 10: if (count > 0) - Decision node
Node 11: res = sum / count;
Node 12: return res;
Node 13: Exit point
```

#### Bước 2: Vẽ đồ thị luồng điều khiển nhị phân

```
        [1 Start]
            ↓
    [2 Initialization]
            ↓
        [3 while(k<step)]
         ↙         ↘
    True           False
      ↓               ↓
[4 k++,temp=value*k]  [10 if(count>0)]
      ↓               ↙        ↘
[5 if(temp>=min      True      False
   &&temp<=max)]      ↓          ↓
   ↙      ↘       [11 res=     [12 return res]
True    False      sum/count]     ↓
  ↓        ↓           ↓        [13 Exit]
[6 count++, [7 if(temp>max)]
 sum+=temp]  ↙        ↘
     ↓    True      False
     ↓     ↓          ↓
[7 if(temp>max)] [9 goto 3]
   ↙      ↘
True    False
  ↓        ↓
[8 break] [9 goto 3]
  ↓
[10 if(count>0)]
```

#### Bước 3: Xác định độ phức tạp vòng tròn (Cyclomatic Complexity)

**Công thức tính:**
- V(G) = E - N + 2 (E: số cạnh, N: số node)
- V(G) = P + 1 (P: số điểm quyết định/predicate nodes)
- V(G) = Số vùng khép kín + 1

**Đếm số điểm quyết định:**
1. `while (k < step)` - Node 3
2. `if (temp >= min && temp <= max)` - Node 5
3. `if (temp > max)` - Node 7
4. `if (count > 0)` - Node 10

**Tính toán:**
- V(G) = P + 1 = 4 + 1 = **5**

**Kết luận:** Độ phức tạp vòng tròn = 5, có nghĩa là cần ít nhất 5 đường đi độc lập để kiểm thử đầy đủ.

#### Bước 4: Xác định các đường đi độc lập (Independent Paths)

**Đường đi 1 (Path 1):** Không vào vòng lặp, count = 0
```
1 → 2 → 3 → 10 → 12 → 13
Điều kiện: step <= 0
Test case: average(5, 0, 0, 100) = 0.0
```

**Đường đi 2 (Path 2):** Vào vòng lặp 1 lần, temp trong khoảng [min, max]
```
1 → 2 → 3 → 4 → 5 → 6 → 7 → 9 → 3 → 10 → 11 → 12 → 13
Điều kiện: step = 1, min <= value*1 <= max
Test case: average(10, 1, 5, 15) = 10.0
```

**Đường đi 3 (Path 3):** Vào vòng lặp, temp không trong khoảng [min, max], không break
```
1 → 2 → 3 → 4 → 5 → 7 → 9 → 3 → 10 → 12 → 13
Điều kiện: step >= 1, temp < min hoặc (temp > max nhưng không thỏa điều kiện break)
Test case: average(2, 2, 20, 30) = 0.0 (temp = 2, 4 đều < 20)
```

**Đường đi 4 (Path 4):** Vào vòng lặp, temp > max, break sớm
```
1 → 2 → 3 → 4 → 5 → 7 → 8 → 10 → 12 → 13
Điều kiện: temp > max trong lần lặp đầu tiên
Test case: average(100, 5, 10, 50) = 0.0 (temp = 100 > 50, break)
```

**Đường đi 5 (Path 5):** Vòng lặp nhiều lần, có cả temp trong và ngoài khoảng
```
1 → 2 → 3 → 4 → 5 → 6 → 7 → 9 → 3 → 4 → 5 → 7 → 9 → 3 → 10 → 11 → 12 → 13
Điều kiện: step > 1, một số giá trị temp trong [min, max]
Test case: average(5, 3, 10, 20)
  - k=1: temp=5 (< 10, không count)
  - k=2: temp=10 (trong [10,20], count)
  - k=3: temp=15 (trong [10,20], count)
  - result = (10+15)/2 = 12.5
```

#### Bước 5: Ma trận bao phủ (Coverage Matrix)

| Test Case | Path | value | step | min | max | Expected Result | Node Coverage |
|-----------|------|-------|------|-----|-----|----------------|---------------|
| TC1 | 1 | 5 | 0 | 0 | 100 | 0.0 | 1,2,3,10,12,13 |
| TC2 | 2 | 10 | 1 | 5 | 15 | 10.0 | 1,2,3,4,5,6,7,9,3,10,11,12,13 |
| TC3 | 3 | 2 | 2 | 20 | 30 | 0.0 | 1,2,3,4,5,7,9,3,10,12,13 |
| TC4 | 4 | 100 | 5 | 10 | 50 | 0.0 | 1,2,3,4,5,7,8,10,12,13 |
| TC5 | 5 | 5 | 3 | 10 | 20 | 12.5 | All nodes |

**Ma trận bao phủ các nhánh (Branch Coverage Matrix):**

| Decision Point | True Path | False Path | TC Coverage |
|----------------|-----------|------------|-------------|
| while (k < step) | TC2,3,4,5 | TC1 | All |
| if (temp >= min && temp <= max) | TC2,5 | TC3,4 | All |
| if (temp > max) | TC4 | TC2,3,5 | All |
| if (count > 0) | TC2,5 | TC1,3,4 | All |

**Kết luận:**
- Tất cả 5 test cases đạt 100% statement coverage
- Đạt 100% branch coverage
- Đạt 100% path coverage cho các đường đi độc lập
- Đủ để thỏa mãn tiêu chí kiểm thử cơ sở (basis path testing)

**Giải thích thuật toán:**
Hàm `average()` tính trung bình của các giá trị `value * k` (với k từ 1 đến step) mà nằm trong khoảng [min, max]. Nếu tìm thấy giá trị nào lớn hơn max, vòng lặp sẽ dừng sớm (break). Nếu không có giá trị nào thỏa mãn, trả về 0.0.
