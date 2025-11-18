# Đề 02 - Kiểm Thử Phần Mềm

## Thông tin chung
- **Thời gian**: 90 phút
- **Đề số**: 02
- **Giảng viên**: Nguyễn Trọng Phúc - Bộ môn CNPM - CNTT

---

## Đề bài

### Câu 1 [3đ]
Nêu sự khác biệt giữa hai quá trình: kiểm định và thẩm định trong quy trình kiểm thử phần mềm.

### Câu 2 [7đ]
Để thực hiện tìm kiếm nhanh, người ta xây dựng thuật toán JumpSearch với yêu cầu tìm kiếm cho mảng đã sắp xếp như sau:

```java
public int jumpSearch(int a[], int target){
    int blockSize = (int) Math.sqrt(a.length);
    int start = 0;
    int next = blockSize;

    while( start < a.length && target > a[next-1] )
    {
        start = next;
        next = next + blockSize;
        if ( next >= a.length )
            next = a.length;
    } // while ends

    for( int i=start; i<next; i++ )
    {
        if ( target == a[i])
            return i;
    } // for ends

    return -1;
}
```

Để kiểm thử cho hàm trong chương trình trên, hãy thực hiện các yêu cầu sau đây:
- Xây dựng đồ thị luồng điều khiển nhị phân cho hàm trên.
- Xác định độ phức tạp của đồ thị.
- Xác định các đường thực thị tuyến tính độc lập ứng với đồ thị luồng điều khiển.
- Xây dựng các ca kiểm thử cho bài toán ứng với các đường thực thị tuyến tính trên.
- Xác định các ca kiểm thử cho bài toán ứng với kiểm thử luồng dữ liệu qua trên đồ thị luồng điều khiển ở trên.

---

## Lời giải

### Câu 1: Phân biệt Kiểm định (Verification) và Thẩm định (Validation)

**Phân tích:**
Verification và Validation là hai khái niệm quan trọng trong kiểm thử phần mềm, thường được gọi chung là V&V.

**Giải đáp:**

#### 1. Định nghĩa

**Verification (Kiểm định):**
- Câu hỏi trọng tâm: **"Are we building the product right?"** (Chúng ta có đang xây dựng sản phẩm đúng cách không?)
- Là quá trình đánh giá xem sản phẩm có được phát triển đúng theo đặc tả, thiết kế và tiêu chuẩn không
- Kiểm tra tính nhất quán, đầy đủ và chính xác giữa các giai đoạn phát triển

**Validation (Thẩm định):**
- Câu hỏi trọng tâm: **"Are we building the right product?"** (Chúng ta có đang xây dựng đúng sản phẩm không?)
- Là quá trình đánh giá xem sản phẩm có đáp ứng nhu cầu và mong đợi thực tế của người dùng không
- Kiểm tra xem sản phẩm có giải quyết đúng vấn đề của khách hàng không

#### 2. So sánh chi tiết

| Tiêu chí | Verification (Kiểm định) | Validation (Thẩm định) |
|----------|-------------------------|------------------------|
| **Mục đích** | Đảm bảo sản phẩm được xây dựng đúng theo đặc tả | Đảm bảo sản phẩm đáp ứng nhu cầu người dùng |
| **Câu hỏi** | "Are we building it right?" | "Are we building the right thing?" |
| **Thời điểm** | Trong suốt quá trình phát triển | Sau khi phát triển xong hoặc các giai đoạn quan trọng |
| **Phương pháp** | Static testing (không chạy code) | Dynamic testing (chạy code) |
| **Hoạt động** | Reviews, Inspections, Walkthroughs | Testing, User Acceptance Testing |
| **Đối tượng** | Documents, Design, Code | Actual software product |
| **Tính chất** | Objective (Khách quan) | Subjective (Chủ quan hơn) |
| **Chi phí** | Thấp hơn | Cao hơn |
| **Phát hiện lỗi** | Lỗi trong tài liệu, thiết kế | Lỗi chức năng, usability |

#### 3. Ví dụ minh họa

**Verification:**
- Review tài liệu yêu cầu để đảm bảo đầy đủ, rõ ràng, không mâu thuẫn
- Review thiết kế để đảm bảo phù hợp với yêu cầu
- Code review để đảm bảo tuân thủ coding standards
- Static analysis để tìm lỗi cú pháp, logic issues
- Unit testing để kiểm tra từng module hoạt động đúng theo thiết kế

**Validation:**
- System testing để kiểm tra toàn bộ hệ thống
- Integration testing để kiểm tra các module tích hợp đúng
- User Acceptance Testing (UAT) với khách hàng
- Beta testing với người dùng thực tế
- Performance testing, Security testing, Usability testing

#### 4. Mối quan hệ

```
Requirements → Verification → Design → Verification → Code → Verification → Product
     ↓                                                                         ↓
     └─────────────────────── Validation ──────────────────────────────────────┘
```

**Verification** kiểm tra từng bước một (step-by-step):
- Requirements ← (verified by) → Design
- Design ← (verified by) → Code
- Code ← (verified by) → Build

**Validation** kiểm tra toàn bộ (end-to-end):
- Requirements ← (validated by) → Final Product

#### 5. Kỹ thuật sử dụng

**Verification Techniques:**
- Inspections
- Reviews
- Walkthroughs
- Desk-checking
- Static analysis tools (linters, code analyzers)

**Validation Techniques:**
- Black box testing
- White box testing
- Non-functional testing
- User acceptance testing

#### 6. Tầm quan trọng

**Tại sao cần cả hai?**
- **Chỉ có Verification**: Có thể xây dựng sai sản phẩm nhưng xây dựng đúng kỹ thuật
  - Ví dụ: Xây dựng một ứng dụng mobile hoàn hảo nhưng người dùng lại cần web app
- **Chỉ có Validation**: Có thể xây dựng đúng sản phẩm nhưng chất lượng kém
  - Ví dụ: Sản phẩm đúng chức năng nhưng code chất lượng kém, khó bảo trì

**Kết luận:**
- Verification và Validation bổ sung cho nhau
- Cần áp dụng cả hai trong suốt vòng đời phát triển phần mềm
- Verification giúp tiết kiệm chi phí bằng cách phát hiện lỗi sớm
- Validation đảm bảo sản phẩm cuối cùng có giá trị thực tế với người dùng

---

### Câu 2: Kiểm thử thuật toán Jump Search

**Phân tích:**
Jump Search là thuật toán tìm kiếm trên mảng đã sắp xếp. Ý tưởng: nhảy theo block size = √n, tìm block chứa target, sau đó tìm kiếm tuyến tính trong block đó.

**Độ phức tạp**: O(√n)

#### A. Xây dựng đồ thị luồng điều khiển (CFG)

**Xác định các node:**

```
Node 1:  Entry point
Node 2:  int blockSize = (int) Math.sqrt(a.length);
         int start = 0; int next = blockSize;
Node 3:  while(start < a.length && target > a[next-1]) - Decision node
Node 4:  start = next; next = next + blockSize;
Node 5:  if (next >= a.length) - Decision node
Node 6:  next = a.length;
Node 7:  Back to while condition (Node 3)
Node 8:  for(int i=start; i<next; i++) - Decision node
Node 9:  if (target == a[i]) - Decision node
Node 10: return i;
Node 11: Continue for loop (Node 8)
Node 12: return -1;
Node 13: Exit point
```

**Đồ thị CFG:**

```
            [1 Entry]
                ↓
    [2 blockSize, start=0, next=blockSize]
                ↓
    [3 while(start<a.length && target>a[next-1])]
         ↙                              ↘
      True                             False
       ↓                                  ↓
[4 start=next, next+=blockSize]     [8 for(i=start; i<next)]
       ↓                              ↙         ↘
[5 if(next >= a.length)]          True        False
   ↙         ↘                      ↓            ↓
True        False               [9 if(target   [12 return -1]
  ↓            ↓                  ==a[i])]        ↓
[6 next=     [7 goto 3]          ↙      ↘       [13 Exit]
 a.length]                    True    False
  ↓                             ↓        ↓
[7 goto 3]                  [10 return [11 i++,
                                i]      goto 8]
                               ↓
                            [13 Exit]
```

#### B. Xác định độ phức tạp vòng tròn (Cyclomatic Complexity)

**Đếm các điểm quyết định:**
1. `while(start < a.length && target > a[next-1])` - Node 3
2. `if (next >= a.length)` - Node 5
3. `for(int i=start; i<next; i++)` - Node 8
4. `if (target == a[i])` - Node 9

**Tính toán:**
- **V(G) = P + 1** = 4 + 1 = **5**

**Kết luận:** Độ phức tạp vòng tròn = 5

#### C. Xác định các đường đi độc lập (Independent Paths)

**Đường đi 1 (Path 1):** Target ở block đầu tiên, tìm thấy ngay
```
1 → 2 → 3 → 8 → 9 → 10 → 13
Điều kiện: target <= a[next-1] và target == a[start]
```

**Đường đi 2 (Path 2):** Target ở block đầu, không tìm thấy
```
1 → 2 → 3 → 8 → 9 → 11 → 8 → 12 → 13
Điều kiện: target <= a[next-1] nhưng không có trong [start, next)
```

**Đường đi 3 (Path 3):** Nhảy qua blocks, không điều chỉnh next, tìm thấy
```
1 → 2 → 3 → 4 → 5 → 7 → 3 → 8 → 9 → 10 → 13
Điều kiện: target > a[next-1], next < a.length, tìm thấy sau khi nhảy
```

**Đường đi 4 (Path 4):** Nhảy đến cuối mảng, điều chỉnh next, tìm thấy
```
1 → 2 → 3 → 4 → 5 → 6 → 7 → 3 → 8 → 9 → 10 → 13
Điều kiện: next >= a.length, phải điều chỉnh next = a.length
```

**Đường đi 5 (Path 5):** Tìm kiếm toàn bộ, không tìm thấy
```
1 → 2 → 3 → 4 → 5 → 7 → 3 → 8 → 9 → 11 → 8 → 12 → 13
Điều kiện: Không tìm thấy target trong mảng
```

#### D. Xây dựng các ca kiểm thử

**Test Case 1: Tìm thấy ở đầu mảng**
```java
Input:
  a[] = {1, 3, 5, 7, 9, 11, 13, 15, 17}
  target = 3
Expected: 1
Giải thích:
  - blockSize = sqrt(9) = 3
  - start = 0, next = 3
  - while(0 < 9 && 3 > a[2]=5): false → không vào vòng lặp
  - for(i=0; i<3): i=0, target(3) == a[0]=1? No
                   i=1, target(3) == a[1]=3? Yes → return 1
Path: 1→2→3→8→9→11→8→9→10→13
```

**Test Case 2: Tìm thấy ở giữa mảng sau khi nhảy**
```java
Input:
  a[] = {1, 3, 5, 7, 9, 11, 13, 15, 17}
  target = 11
Expected: 5
Giải thích:
  - blockSize = 3
  - Lần 1: start=0, next=3, while(0<9 && 11>a[2]=5): true
    - start=3, next=6, if(6>=9): false
  - Lần 2: while(3<9 && 11>a[5]=11): false → thoát
  - for(i=3; i<6): i=3, 11==a[3]=7? No
                   i=4, 11==a[4]=9? No
                   i=5, 11==a[5]=11? Yes → return 5
Path: 1→2→3→4→5→7→3→8→9→11→8→9→11→8→9→10→13
```

**Test Case 3: Tìm thấy ở cuối mảng, cần điều chỉnh next**
```java
Input:
  a[] = {2, 4, 6, 8, 10, 12, 14, 16, 18, 20}
  target = 18
Expected: 8
Giải thích:
  - blockSize = sqrt(10) = 3
  - Lần 1: start=0, next=3, while(0<10 && 18>a[2]=6): true
    - start=3, next=6
  - Lần 2: while(3<10 && 18>a[5]=12): true
    - start=6, next=9
  - Lần 3: while(6<10 && 18>a[8]=18): false → thoát
  - for(i=6; i<9): i=6, 18==a[6]=14? No
                   i=7, 18==a[7]=16? No
                   i=8, 18==a[8]=18? Yes → return 8
```

**Test Case 4: Không tìm thấy, target nhỏ hơn phần tử đầu**
```java
Input:
  a[] = {5, 10, 15, 20, 25, 30}
  target = 3
Expected: -1
Giải thích:
  - blockSize = sqrt(6) = 2
  - start=0, next=2
  - while(0<6 && 3>a[1]=10): false
  - for(i=0; i<2): i=0, 3==a[0]=5? No
                   i=1, 3==a[1]=10? No
  - return -1
```

**Test Case 5: Không tìm thấy, target lớn hơn phần tử cuối**
```java
Input:
  a[] = {1, 3, 5, 7, 9}
  target = 15
Expected: -1
Giải thích:
  - blockSize = sqrt(5) = 2
  - Lần 1: start=0, next=2, while(0<5 && 15>a[1]=3): true
    - start=2, next=4
  - Lần 2: while(2<5 && 15>a[3]=7): true
    - start=4, next=6, if(6>=5): true → next=5
  - Lần 3: while(4<5 && 15>a[4]=9): true
    - start=5, next=7, if(7>=5): true → next=5
  - Lần 4: while(5<5): false → thoát
  - for(i=5; i<5): false → không vào
  - return -1
```

**Test Case 6: Không tìm thấy, target nằm giữa hai phần tử**
```java
Input:
  a[] = {2, 4, 8, 16, 32}
  target = 10
Expected: -1
Giải thích:
  - blockSize = 2
  - Lần 1: start=0, next=2, while(0<5 && 10>a[1]=4): true
    - start=2, next=4
  - Lần 2: while(2<5 && 10>a[3]=16): false → thoát
  - for(i=2; i<4): i=2, 10==a[2]=8? No
                   i=3, 10==a[3]=16? No
  - return -1
```

**Test Case 7: Mảng có 1 phần tử, tìm thấy**
```java
Input:
  a[] = {42}
  target = 42
Expected: 0
Giải thích:
  - blockSize = sqrt(1) = 1
  - start=0, next=1
  - while(0<1 && 42>a[0]=42): false
  - for(i=0; i<1): i=0, 42==a[0]=42? Yes → return 0
```

**Test Case 8: Mảng có 1 phần tử, không tìm thấy**
```java
Input:
  a[] = {42}
  target = 10
Expected: -1
```

#### E. Ma trận bao phủ các đường đi

| TC | Array | Target | Result | Path | Coverage |
|----|-------|--------|--------|------|----------|
| TC1 | [1,3,5,7,9,11,13,15,17] | 3 | 1 | 1→2→3→8→9→10 | while:F, if(next>=):-, for:T, if(==):T |
| TC2 | [1,3,5,7,9,11,13,15,17] | 11 | 5 | 1→2→3→4→5→7→3→8→9→10 | while:T→F, if(next>=):F, for:T, if(==):T |
| TC3 | [2,4,6,8,10,12,14,16,18,20] | 18 | 8 | 1→2→3→4→5→7→3→8→9→10 | while:T→F, if(next>=):F, for:T, if(==):T |
| TC4 | [5,10,15,20,25,30] | 3 | -1 | 1→2→3→8→9→11→8→12 | while:F, for:T→F, if(==):F |
| TC5 | [1,3,5,7,9] | 15 | -1 | 1→2→3→4→5→6→7→3→8→12 | while:T→F, if(next>=):T, for:F |
| TC6 | [2,4,8,16,32] | 10 | -1 | 1→2→3→4→5→7→3→8→9→11→8→12 | while:T→F, if(next>=):F, for:T→F, if(==):F |
| TC7 | [42] | 42 | 0 | 1→2→3→8→9→10 | Edge case: single element found |
| TC8 | [42] | 10 | -1 | 1→2→3→8→9→11→8→12 | Edge case: single element not found |

#### F. Kiểm thử luồng dữ liệu (Data Flow Testing)

**Biến cần theo dõi:**
- `blockSize`, `start`, `next`, `i`, `target`, `a[]`

**Định nghĩa-Sử dụng (Def-Use Chains):**

1. **blockSize:**
   - Def: Node 2
   - Use: Node 4 (next = next + blockSize)
   - Paths: 2 → 3 → 4

2. **start:**
   - Def: Node 2 (start = 0)
   - Def: Node 4 (start = next)
   - Use: Node 3 (while condition)
   - Use: Node 8 (for initialization)
   - Paths:
     - 2 → 3 (du-path)
     - 2 → 3 → 4 → 5 → 7 → 3 (du-path với redefinition)
     - 4 → 5 → 7 → 3 → 8 (du-path)

3. **next:**
   - Def: Node 2 (next = blockSize)
   - Def: Node 4 (next = next + blockSize)
   - Def: Node 6 (next = a.length)
   - Use: Node 3 (a[next-1])
   - Use: Node 5 (if condition)
   - Use: Node 8 (for condition)
   - Paths:
     - 2 → 3 (du-path)
     - 4 → 5 (du-path)
     - 4 → 5 → 7 → 3 (du-path với reuse)
     - 6 → 7 → 3 (du-path sau redefinition)

4. **i:**
   - Def: Node 8 (for init, i++)
   - Def: Node 11 (i++)
   - Use: Node 8 (for condition)
   - Use: Node 9 (a[i])
   - Paths:
     - 8 → 9 (du-path)
     - 11 → 8 → 9 (du-path)

5. **target:**
   - Def: Node 1 (parameter)
   - Use: Node 3 (comparison)
   - Use: Node 9 (comparison)
   - Paths:
     - 1 → 2 → 3 (du-path)
     - 1 → 2 → 3 → ... → 8 → 9 (du-path)

**All-Defs Coverage:** Test cases phải bao phủ tất cả định nghĩa của biến
- TC1-TC8 đã cover tất cả defs

**All-Uses Coverage:** Test cases phải bao phủ tất cả uses từ mỗi def
- TC2, TC3, TC5: Cover def-use của next với cả 3 defs
- TC1, TC4: Cover def-use của start với def ban đầu
- TC2, TC3, TC6: Cover def-use của start với redefinition

**All-DU-Paths Coverage:**

| Variable | Def Node | Use Node | Test Cases | Path |
|----------|----------|----------|------------|------|
| blockSize | 2 | 4 | TC2,TC3,TC5,TC6 | 2→3→4 |
| start | 2 | 3 | All | 2→3 |
| start | 2 | 8 | TC1,TC4,TC7,TC8 | 2→3→8 |
| start | 4 | 3 | TC2,TC3,TC5,TC6 | 4→5→7→3 |
| start | 4 | 8 | TC2,TC3,TC6 | 4→...→3→8 |
| next | 2 | 3 | TC1,TC4,TC7,TC8 | 2→3 |
| next | 4 | 5 | TC2,TC3,TC5,TC6 | 4→5 |
| next | 6 | 7 | TC5 | 6→7 |
| i | 8 | 9 | All (có for) | 8→9 |
| i | 11 | 8 | TC1,TC2,TC3,TC4,TC6 | 11→8 |
| target | 1 | 3 | TC2,TC3,TC5,TC6 | 1→2→3 |
| target | 1 | 9 | All | 1→...→9 |

**Kết luận:**
- Test suite đạt 100% All-Defs coverage
- Đạt 100% All-Uses coverage
- Đạt 100% All-DU-Paths coverage
- Coverage đầy đủ cho kiểm thử luồng dữ liệu

**Lưu ý về bugs tiềm ẩn:**
1. **ArrayIndexOutOfBoundsException**: Nếu mảng rỗng (a.length = 0), blockSize = 0, next = 0, truy cập a[next-1] = a[-1] sẽ lỗi
2. **Mảng không sắp xếp**: Thuật toán giả định mảng đã sắp xếp, không kiểm tra
3. **Null pointer**: Không kiểm tra a == null

**Cải tiến đề xuất:**
```java
public int jumpSearch(int a[], int target){
    if (a == null || a.length == 0) return -1; // Fix bug 1

    int blockSize = (int) Math.sqrt(a.length);
    int start = 0;
    int next = Math.min(blockSize, a.length); // Fix bug 2

    while( start < a.length && target > a[next-1] ) {
        start = next;
        next = next + blockSize;
        if ( next >= a.length )
            next = a.length;
    }

    for( int i=start; i<next; i++ ) {
        if ( target == a[i])
            return i;
    }

    return -1;
}
```
