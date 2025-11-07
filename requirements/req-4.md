# REQ-4: Đề Tài Cuối Kỳ - Phân Vùng Người & Phát Hiện Xâm Nhập Khu Vực Cấm

## Thông Tin Đề Tài

**Tên Đề Tài**: Phân Vùng Người & Phát Hiện Xâm Nhập Khu Vực Cấm
**Mã Số**: Topic 43
**Môn Học**: Xử Lý Ảnh
**Năm Học**: 2024-2025

---

## Tổng Quan

Đề tài này tập trung vào xây dựng hệ thống **phát hiện và cảnh báo** khi có người xâm nhập vào khu vực bị cấm sử dụng các kỹ thuật xử lý ảnh và computer vision. Hệ thống cần hoạt động hiệu quả trong điều kiện ánh sáng thay đổi và có khả năng phân biệt giữa chuyển động thực và nhiễu.

### Mục Tiêu Chính

1. ✅ **Phân vùng người** (Person Segmentation) từ video/camera
2. ✅ **Xác định khu vực cấm** (Restricted Area Definition)
3. ✅ **Phát hiện xâm nhập** (Intrusion Detection)
4. ✅ **Cảnh báo tự động** (Automated Alert System)
5. ✅ **Xử lý ánh sáng thay đổi** (Adaptive Lighting Handling)

---

## Yêu Cầu Kỹ Thuật

### 1. Phân Vùng Chuyển Động (Motion Segmentation)
- **Frame Differencing**: Phát hiện chuyển động giữa các frame liên tiếp
- **Background Subtraction**: Tách foreground/background
- **Morphological Operations**: Loại bỏ nhiễu, làm mịn vùng phát hiện

### 2. Xử Lý Ánh Sáng Thay Đổi
- **Adaptive Thresholding**: Điều chỉnh threshold động theo điều kiện ánh sáng
- **Histogram Equalization**: Cân bằng độ tương phản
- **Gamma Correction**: Điều chỉnh độ sáng

### 3. Phát Hiện Biên & Vùng
- **Edge Detection**: Sobel, Canny, hoặc Prewitt operators
- **Region Growing**: Mở rộng vùng từ seed points
- **Contour Detection**: Xác định đường viền đối tượng

### 4. Phát Hiện Xâm Nhập
- **ROI (Region of Interest)**: Định nghĩa khu vực cấm
- **Overlap Detection**: Kiểm tra giao giữa đối tượng và ROI
- **Alert Triggering**: Kích hoạt cảnh báo khi phát hiện xâm nhập

### 5. Công Nghệ Sử Dụng
- **Ngôn ngữ**: Python (OpenCV) hoặc MATLAB
- **Libraries**: OpenCV, NumPy, scikit-image
- **Input**: Video files hoặc real-time camera
- **Output**: Video với bounding boxes + alert logs

---

## Cấu Trúc Dự Án

### Folder Structure:

```
req-4-project/
├── code/                           # Code implementation
│   ├── src/
│   │   ├── main.py                # Main application
│   │   ├── motion_detector.py     # Frame differencing & background subtraction
│   │   ├── adaptive_threshold.py  # Adaptive thresholding module
│   │   ├── edge_detector.py       # Edge detection (Sobel/Canny)
│   │   ├── region_grower.py       # Region growing algorithm
│   │   ├── intrusion_detector.py  # ROI & intrusion detection
│   │   ├── alert_system.py        # Alert logging and display
│   │   └── utils.py               # Helper functions
│   ├── config/
│   │   └── config.yaml            # Configuration parameters
│   ├── data/
│   │   ├── input/                 # Input videos
│   │   ├── output/                # Output videos & logs
│   │   └── roi/                   # ROI definitions (JSON/XML)
│   ├── tests/                     # Unit tests
│   │   ├── test_motion.py
│   │   ├── test_threshold.py
│   │   └── test_intrusion.py
│   ├── requirements.txt           # Python dependencies
│   └── README.md                  # Code documentation
│
├── documentation/                 # Báo cáo và tài liệu
│   ├── 01-theory-foundation/
│   │   ├── 1.1-frame-differencing.md
│   │   ├── 1.2-adaptive-thresholding.md
│   │   ├── 1.3-edge-detection.md
│   │   ├── 1.4-region-growing.md
│   │   ├── 1.5-intrusion-detection.md
│   │   └── references.md
│   ├── 02-practical-implementation/
│   │   ├── 2.1-system-architecture.md
│   │   ├── 2.2-algorithm-design.md
│   │   ├── 2.3-implementation-details.md
│   │   ├── 2.4-parameter-tuning.md
│   │   └── 2.5-user-guide.md
│   ├── 03-evaluation/
│   │   ├── 3.1-test-scenarios.md
│   │   ├── 3.2-accuracy-analysis.md
│   │   ├── 3.3-lighting-conditions.md
│   │   ├── 3.4-performance-metrics.md
│   │   └── 3.5-limitations.md
│   ├── 04-deliverables/
│   │   ├── demo-video/
│   │   │   ├── scenario-1-daylight.mp4
│   │   │   ├── scenario-2-lowlight.mp4
│   │   │   └── scenario-3-night.mp4
│   │   ├── screenshots/
│   │   └── report-final.pdf
│   └── README.md
│
├── implementation-guide/          # Hướng dẫn triển khai
│   ├── 1-environment-setup.md
│   ├── 2-data-preparation.md
│   ├── 3-roi-definition.md
│   ├── 4-configuration.md
│   ├── 5-running-system.md
│   └── 6-troubleshooting.md
│
├── knowledge-base/                # Kiến thức nền tảng
│   ├── fundamentals/
│   │   ├── image-basics.md
│   │   ├── video-processing.md
│   │   └── color-spaces.md
│   ├── motion-detection/
│   │   ├── frame-differencing-theory.md
│   │   ├── background-subtraction-methods.md
│   │   └── optical-flow.md
│   ├── segmentation/
│   │   ├── thresholding-methods.md
│   │   ├── edge-based-segmentation.md
│   │   └── region-based-segmentation.md
│   ├── advanced-topics/
│   │   ├── adaptive-algorithms.md
│   │   ├── morphological-processing.md
│   │   └── object-tracking.md
│   └── README.md
│
└── README.md                      # Project overview
```

---

## Chi Tiết Các Thành Phần

### 📂 1. Code Implementation (`code/`)

#### 1.1 Core Modules

##### `main.py`
```python
# Main application entry point
- Load configuration
- Initialize video source (file/camera)
- Load ROI definitions
- Run detection pipeline
- Display results with bounding boxes
- Save output video and logs
```

##### `motion_detector.py`
```python
# Motion detection module
- Frame differencing implementation
- Background subtraction (MOG2, KNN, GMG)
- Temporal filtering
- Morphological operations (erosion, dilation)
```

##### `adaptive_threshold.py`
```python
# Adaptive thresholding module
- Gaussian adaptive thresholding
- Mean adaptive thresholding
- Otsu's method
- Dynamic threshold adjustment
```

##### `edge_detector.py`
```python
# Edge detection module
- Sobel operator (horizontal, vertical, magnitude)
- Canny edge detection (with hysteresis)
- Prewitt operator
- Edge linking and refinement
```

##### `region_grower.py`
```python
# Region growing module
- Seed point selection
- Similarity criteria (intensity, gradient)
- Region expansion algorithm
- Connected component labeling
```

##### `intrusion_detector.py`
```python
# Intrusion detection module
- Load ROI polygons/rectangles
- Calculate overlap between detected objects and ROI
- Intrusion validation (time threshold, size filter)
- Generate alerts
```

##### `alert_system.py`
```python
# Alert system module
- Visual alerts (bounding boxes, text overlay)
- Audio alerts (beep sound)
- Log alerts to file (timestamp, location, screenshot)
- Optional: Send notifications (email, SMS)
```

#### 1.2 Configuration (`config/config.yaml`)

```yaml
# Video Input
video:
  source: "data/input/test_video.mp4"  # or 0 for webcam
  fps: 30

# Motion Detection
motion:
  method: "MOG2"  # MOG2, KNN, or frame_diff
  history: 500
  threshold: 16
  detect_shadows: true

# Adaptive Thresholding
threshold:
  method: "gaussian"  # gaussian or mean
  block_size: 11
  C: 2

# Edge Detection
edge:
  method: "canny"  # sobel or canny
  low_threshold: 50
  high_threshold: 150

# Morphological Operations
morphology:
  kernel_size: 5
  iterations: 2

# Intrusion Detection
intrusion:
  roi_file: "data/roi/restricted_area.json"
  overlap_threshold: 0.3  # 30% overlap
  time_threshold: 1.0  # 1 second
  min_object_area: 1000  # pixels

# Alert System
alert:
  visual: true
  audio: true
  log_file: "data/output/alerts.log"
  save_screenshots: true

# Output
output:
  save_video: true
  output_path: "data/output/result.mp4"
  show_realtime: true
```

#### 1.3 ROI Definition (`data/roi/restricted_area.json`)

```json
{
  "restricted_areas": [
    {
      "name": "Area 1",
      "type": "polygon",
      "points": [[100, 100], [400, 100], [400, 300], [100, 300]],
      "color": [255, 0, 0]
    },
    {
      "name": "Area 2",
      "type": "rectangle",
      "x": 500,
      "y": 200,
      "width": 200,
      "height": 150,
      "color": [0, 0, 255]
    }
  ]
}
```

#### 1.4 Dependencies (`requirements.txt`)

```
opencv-python>=4.8.0
numpy>=1.24.0
scikit-image>=0.21.0
matplotlib>=3.7.0
pyyaml>=6.0
pytest>=7.4.0
```

---

### 📚 2. Documentation (`documentation/`)

#### 2.1 Theory Foundation (`01-theory-foundation/`)

##### File: `1.1-frame-differencing.md`
**Nội dung**:
- Định nghĩa và nguyên lý
- Thuật toán frame differencing cơ bản
- Temporal vs spatial differencing
- Ưu/nhược điểm
- Ứng dụng trong motion detection
- So sánh với background subtraction

##### File: `1.2-adaptive-thresholding.md`
**Nội dung**:
- Thresholding cơ bản vs adaptive
- Gaussian adaptive thresholding
- Mean adaptive thresholding
- Otsu's method
- Xử lý ánh sáng không đồng đều
- Parameter tuning strategies

##### File: `1.3-edge-detection.md`
**Nội dung**:
- Edge detection fundamentals
- Gradient operators (Sobel, Prewitt, Scharr)
- Canny edge detection (5 steps)
- Hysteresis thresholding
- Non-maximum suppression
- Edge linking techniques

##### File: `1.4-region-growing.md`
**Nội dung**:
- Region growing algorithm
- Seed selection strategies
- Similarity criteria (intensity, color, texture)
- Region merging và splitting
- Connected components analysis
- 4-connectivity vs 8-connectivity

##### File: `1.5-intrusion-detection.md`
**Nội dung**:
- ROI definition methods
- Overlap calculation (IoU, area percentage)
- Intrusion validation criteria
- False positive reduction
- Temporal consistency checks
- Multi-object tracking

##### File: `references.md`
**Nội dung**:
- Academic papers
- Textbooks
- Online resources
- OpenCV documentation

#### 2.2 Practical Implementation (`02-practical-implementation/`)

##### File: `2.1-system-architecture.md`
**Nội dung**:
```
System Architecture:

[Video Input]
    ↓
[Frame Preprocessing]
    ↓
[Motion Detection] ← [Background Model]
    ↓
[Adaptive Thresholding]
    ↓
[Edge Detection]
    ↓
[Region Growing] → [Object Segmentation]
    ↓
[Intrusion Detection] ← [ROI Database]
    ↓
[Alert System] → [Visual + Audio + Log]
    ↓
[Output Display/Save]
```

- Module interactions
- Data flow diagram
- Processing pipeline
- Real-time considerations

##### File: `2.2-algorithm-design.md`
**Nội dung**:
- Detailed algorithm flowcharts
- Pseudocode for each module
- Decision trees for parameter selection
- Edge case handling

##### File: `2.3-implementation-details.md`
**Nội dung**:
- Code structure explanation
- Key functions and classes
- Design patterns used
- Error handling strategies
- Performance optimizations

##### File: `2.4-parameter-tuning.md`
**Nội dung**:
- Parameter sensitivity analysis
- Tuning guidelines for different scenarios
- Trade-offs (accuracy vs speed)
- Recommended values for various lighting conditions

##### File: `2.5-user-guide.md`
**Nội dung**:
- Installation instructions
- Running the system step-by-step
- GUI/CLI usage
- Defining custom ROIs
- Interpreting results

#### 2.3 Evaluation (`03-evaluation/`)

##### File: `3.1-test-scenarios.md`
**Nội dung**:
- Test case definitions
- Input video descriptions
- Expected outcomes
- Actual results

##### File: `3.2-accuracy-analysis.md`
**Nội dung**:
- Performance metrics:
  - True Positive Rate (TPR)
  - False Positive Rate (FPR)
  - Precision, Recall, F1-score
  - IoU (Intersection over Union)
- Confusion matrix
- ROC curves

##### File: `3.3-lighting-conditions.md`
**Nội dung**:
- **Daylight scenario**: High visibility, clear shadows
- **Low-light scenario**: Reduced contrast, noise increase
- **Night scenario**: Very low light, high noise
- Adaptive parameter adjustments for each
- Accuracy comparison table

##### File: `3.4-performance-metrics.md`
**Nội dung**:
- Processing speed (FPS)
- Memory usage
- CPU/GPU utilization
- Latency analysis
- Scalability tests

##### File: `3.5-limitations.md`
**Nội dung**:
- Current limitations
- Known issues
- False positives/negatives analysis
- Improvement suggestions
- Future work

#### 2.4 Deliverables (`04-deliverables/`)

##### Demo Videos:
- **scenario-1-daylight.mp4**: Outdoor, good lighting
- **scenario-2-lowlight.mp4**: Indoor, dim lighting
- **scenario-3-night.mp4**: Outdoor, night time

Each video should show:
- Original video feed
- Detected motion (highlighted)
- Bounding boxes around persons
- ROI overlay
- Alert triggers (visual + text)

##### Screenshots:
- System GUI/interface
- Alert notifications
- Parameter configuration panels
- Results visualization

##### Final Report (`report-final.pdf`):
- Complete documentation compiled
- All sections formatted professionally
- Includes:
  1. Cover page
  2. Table of contents
  3. Theory foundation
  4. Practical implementation
  5. Evaluation results
  6. Conclusion
  7. References
  8. Appendices (code listings, additional charts)

---

### 🛠️ 3. Implementation Guide (`implementation-guide/`)

#### File: `1-environment-setup.md`

**Nội dung**:

```markdown
# Environment Setup

## 1. System Requirements
- **OS**: Windows 10/11, Ubuntu 20.04+, or macOS 11+
- **Python**: 3.8 or higher
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 2GB for code + data
- **Camera**: Optional, for real-time testing

## 2. Install Python
```bash
# Check Python version
python --version  # or python3 --version

# If not installed, download from python.org
```

## 3. Create Virtual Environment
```bash
# Navigate to project directory
cd req-4-project/code

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

## 4. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 5. Verify Installation
```bash
python -c "import cv2; print(cv2.__version__)"
python -c "import numpy; print(numpy.__version__)"
```

## 6. IDE Setup (Optional)
- **VS Code**: Install Python extension
- **PyCharm**: Configure Python interpreter
- **Jupyter**: For experimentation
  ```bash
  pip install jupyter
  jupyter notebook
  ```

## 7. GPU Support (Optional)
For faster processing with CUDA:
```bash
pip install opencv-contrib-python-headless
# Follow CUDA installation guide for your system
```
```

#### File: `2-data-preparation.md`

**Nội dung**:

```markdown
# Data Preparation

## 1. Input Video Requirements
- **Format**: MP4, AVI, MOV, or any OpenCV-supported format
- **Resolution**: 640x480 minimum, 1920x1080 recommended
- **FPS**: 25-30 FPS
- **Duration**: 30 seconds to 5 minutes for testing

## 2. Obtaining Test Videos

### Option A: Download Sample Videos
```bash
# Create data directories
mkdir -p data/input
mkdir -p data/output

# Download sample surveillance videos
# Example sources:
# - Pexels.com (free stock videos)
# - YouTube (Creative Commons)
# - VIRAT Video Dataset (surveillance)
```

### Option B: Record Your Own
- Use smartphone or webcam
- Ensure good coverage of test area
- Include various scenarios:
  - Person entering restricted area
  - Person walking near (but not entering) restricted area
  - No persons present
  - Multiple persons

### Option C: Use Real-time Camera
- Connect USB webcam or IP camera
- Set `source: 0` in config.yaml for default webcam
- Set `source: "rtsp://..."` for IP camera

## 3. Video Preprocessing (Optional)
If videos need adjustment:

```python
import cv2

# Resize video
def resize_video(input_path, output_path, width=1280, height=720):
    cap = cv2.VideoCapture(input_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS)
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        resized = cv2.resize(frame, (width, height))
        out.write(resized)

    cap.release()
    out.release()
```

## 4. Data Organization
```
data/
├── input/
│   ├── test_video_1.mp4
│   ├── test_video_2.mp4
│   └── test_video_3.mp4
├── output/
│   └── (results will be saved here)
└── roi/
    ├── restricted_area.json
    └── (ROI definitions)
```

## 5. Quality Checks
Before running:
- [ ] Videos play correctly in media player
- [ ] Resolution is clear enough to see persons
- [ ] Lighting conditions are representative
- [ ] File paths are correct in config.yaml
```

#### File: `3-roi-definition.md`

**Nội dung**:

```markdown
# ROI (Region of Interest) Definition

## Overview
ROI defines the restricted area(s) where intrusion detection is active.

## Method 1: Manual JSON Editing

Edit `data/roi/restricted_area.json`:

```json
{
  "restricted_areas": [
    {
      "name": "Main Entrance",
      "type": "polygon",
      "points": [[100, 100], [400, 100], [400, 300], [100, 300]],
      "color": [255, 0, 0]
    }
  ]
}
```

### Polygon Points:
- Define vertices in clockwise or counter-clockwise order
- Coordinates are (x, y) in pixels
- Origin (0, 0) is top-left corner

### Rectangle:
```json
{
  "name": "Loading Dock",
  "type": "rectangle",
  "x": 500,
  "y": 200,
  "width": 200,
  "height": 150,
  "color": [0, 0, 255]
}
```

## Method 2: Interactive ROI Selection Tool

Create `tools/roi_selector.py`:

```python
import cv2
import json

class ROISelector:
    def __init__(self, video_path):
        self.video_path = video_path
        self.points = []
        self.rois = []

    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.points.append([x, y])
            print(f"Point added: ({x}, {y})")
        elif event == cv2.EVENT_RBUTTONDOWN:
            if len(self.points) >= 3:
                roi = {
                    "name": f"Area {len(self.rois) + 1}",
                    "type": "polygon",
                    "points": self.points.copy(),
                    "color": [255, 0, 0]
                }
                self.rois.append(roi)
                print(f"ROI saved: {len(self.points)} points")
                self.points = []

    def run(self):
        cap = cv2.VideoCapture(self.video_path)
        ret, frame = cap.read()
        cap.release()

        if not ret:
            print("Error: Cannot read video")
            return

        cv2.namedWindow("ROI Selector")
        cv2.setMouseCallback("ROI Selector", self.mouse_callback)

        print("Instructions:")
        print("- Left click: Add point")
        print("- Right click: Finish current ROI")
        print("- Press 's': Save and exit")
        print("- Press 'c': Clear current points")
        print("- Press 'q': Quit without saving")

        while True:
            display = frame.copy()

            # Draw current points
            for pt in self.points:
                cv2.circle(display, tuple(pt), 5, (0, 255, 0), -1)

            # Draw lines between points
            if len(self.points) > 1:
                for i in range(len(self.points) - 1):
                    cv2.line(display, tuple(self.points[i]),
                            tuple(self.points[i+1]), (0, 255, 0), 2)

            # Draw saved ROIs
            for roi in self.rois:
                pts = roi["points"]
                for i in range(len(pts)):
                    cv2.line(display, tuple(pts[i]),
                            tuple(pts[(i+1) % len(pts)]), tuple(roi["color"]), 2)

            cv2.imshow("ROI Selector", display)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('s'):
                self.save_rois()
                break
            elif key == ord('c'):
                self.points = []
                print("Points cleared")
            elif key == ord('q'):
                break

        cv2.destroyAllWindows()

    def save_rois(self):
        output = {"restricted_areas": self.rois}
        with open("data/roi/restricted_area.json", "w") as f:
            json.dump(output, f, indent=2)
        print(f"Saved {len(self.rois)} ROI(s) to restricted_area.json")

if __name__ == "__main__":
    selector = ROISelector("data/input/test_video.mp4")
    selector.run()
```

### Usage:
```bash
python tools/roi_selector.py
```

## Method 3: Use First Frame
For quick testing, use entire frame or simple coordinates:

```json
{
  "restricted_areas": [
    {
      "name": "Full Frame",
      "type": "rectangle",
      "x": 0,
      "y": 0,
      "width": 1280,
      "height": 720,
      "color": [255, 0, 0]
    }
  ]
}
```

## Tips
- Test ROI on a static frame first
- Use contrasting colors for visibility
- Avoid overly complex polygons (3-6 points ideal)
- Multiple smaller ROIs > one large complex ROI
```

#### File: `4-configuration.md`

**Nội dung**:

```markdown
# Configuration Guide

## Configuration File: `config/config.yaml`

### Video Input
```yaml
video:
  source: "data/input/test_video.mp4"  # Path or camera index
  fps: 30                              # Frame rate (if reading from file)
```

**Options:**
- File path: `"path/to/video.mp4"`
- Webcam: `0` (default camera) or `1, 2, ...` for additional cameras
- IP camera: `"rtsp://username:password@ip:port/stream"`

### Motion Detection
```yaml
motion:
  method: "MOG2"        # Options: "MOG2", "KNN", "frame_diff"
  history: 500          # Number of frames for background learning
  threshold: 16         # Sensitivity (lower = more sensitive)
  detect_shadows: true  # Detect and mark shadows
```

**Tuning:**
- **Daylight**: `threshold: 16-25`, `history: 500`
- **Low-light**: `threshold: 10-15`, `history: 300`
- **Night**: `threshold: 8-12`, `history: 200`

### Adaptive Thresholding
```yaml
threshold:
  method: "gaussian"    # Options: "gaussian", "mean"
  block_size: 11        # Neighborhood size (must be odd)
  C: 2                  # Constant subtracted from mean
```

**Tuning:**
- **High contrast**: `block_size: 7-11`, `C: 2-5`
- **Low contrast**: `block_size: 15-21`, `C: 1-3`
- **Noisy**: `block_size: 15-25`, `C: 5-10`

### Edge Detection
```yaml
edge:
  method: "canny"           # Options: "canny", "sobel"
  low_threshold: 50         # Canny lower threshold
  high_threshold: 150       # Canny upper threshold
```

**Tuning:**
- **Sharp edges only**: `low: 100`, `high: 200`
- **More edges**: `low: 30`, `high: 100`
- **Sobel**: Use magnitude threshold instead

### Morphological Operations
```yaml
morphology:
  kernel_size: 5        # Size of structuring element
  iterations: 2         # Number of times to apply
```

**Purpose:**
- Remove noise (erosion → dilation)
- Fill holes (dilation → erosion)
- Smooth boundaries

### Intrusion Detection
```yaml
intrusion:
  roi_file: "data/roi/restricted_area.json"
  overlap_threshold: 0.3   # Min overlap ratio to trigger (30%)
  time_threshold: 1.0      # Seconds object must be in ROI
  min_object_area: 1000    # Min pixel area to consider
```

**Tuning:**
- **Strict detection**: `overlap: 0.5`, `time: 2.0`
- **Lenient detection**: `overlap: 0.2`, `time: 0.5`
- **Filter small objects**: Increase `min_object_area`

### Alert System
```yaml
alert:
  visual: true                          # Show on video
  audio: true                           # Play sound
  log_file: "data/output/alerts.log"   # Log file path
  save_screenshots: true                # Save frame on alert
```

### Output
```yaml
output:
  save_video: true                      # Save output video
  output_path: "data/output/result.mp4"
  show_realtime: true                   # Display while processing
```

## Quick Presets

### Preset 1: Outdoor Daylight
```yaml
motion:
  threshold: 20
threshold:
  block_size: 11
  C: 2
edge:
  low_threshold: 50
  high_threshold: 150
```

### Preset 2: Indoor Low-Light
```yaml
motion:
  threshold: 12
threshold:
  block_size: 15
  C: 3
edge:
  low_threshold: 30
  high_threshold: 100
```

### Preset 3: Night
```yaml
motion:
  threshold: 10
threshold:
  block_size: 21
  C: 5
edge:
  low_threshold: 20
  high_threshold: 80
```
```

#### File: `5-running-system.md`

**Nội dung**:

```markdown
# Running the System

## Step-by-Step Execution

### 1. Activate Environment
```bash
cd req-4-project/code
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

### 2. Verify Setup
```bash
# Check files
ls data/input/           # Input videos present?
ls data/roi/             # ROI file present?
cat config/config.yaml   # Config correct?
```

### 3. Run Main Program
```bash
python src/main.py
```

### 4. Command-Line Arguments (Optional)

```bash
# Use custom config
python src/main.py --config custom_config.yaml

# Override video source
python src/main.py --source data/input/another_video.mp4

# Use webcam
python src/main.py --source 0

# Skip display (headless)
python src/main.py --no-display

# Save output only
python src/main.py --output-only
```

### 5. Expected Output

**Console:**
```
[INFO] Loading configuration...
[INFO] Initializing video source...
[INFO] Video: 1280x720 @ 30 FPS
[INFO] Loading ROI definitions...
[INFO] ROI: 2 restricted areas loaded
[INFO] Starting detection pipeline...
[INFO] Processing frame 1/900...
[ALERT] Intrusion detected at 00:05 in Area 1!
[INFO] Processing frame 2/900...
...
[INFO] Processing complete. Saved to data/output/result.mp4
[INFO] Total alerts: 3
[INFO] Alert log: data/output/alerts.log
```

**Display Window:**
- Original video with overlays:
  - Red polygons: ROI areas
  - Green boxes: Detected persons (no intrusion)
  - Red boxes: Persons in restricted area (intrusion)
  - Text: "ALERT - INTRUSION DETECTED"
  - Frame counter, FPS

### 6. Reviewing Results

#### Output Video:
```bash
# Open with default player
open data/output/result.mp4  # Mac
xdg-open data/output/result.mp4  # Linux
start data/output/result.mp4  # Windows
```

#### Alert Log:
```bash
cat data/output/alerts.log
```

Example log:
```
2025-01-06 14:32:15 | ALERT | Area 1 | Intrusion detected | Frame 150 | Screenshot: alert_001.png
2025-01-06 14:32:18 | ALERT | Area 1 | Intrusion detected | Frame 240 | Screenshot: alert_002.png
2025-01-06 14:33:02 | ALERT | Area 2 | Intrusion detected | Frame 890 | Screenshot: alert_003.png
```

#### Screenshots:
```bash
ls data/output/screenshots/
# alert_001.png, alert_002.png, ...
```

## Interactive Mode

For real-time tuning, use interactive mode:

```bash
python src/main.py --interactive
```

**Controls:**
- `p`: Pause/resume
- `s`: Save current frame
- `r`: Reset background model
- `+/-`: Adjust threshold
- `q`: Quit

## Batch Processing

Process multiple videos:

```bash
python src/batch_process.py --input-dir data/input/ --output-dir data/output/
```

## Troubleshooting During Run

| Issue | Solution |
|-------|----------|
| No video display | Check `show_realtime: true` in config |
| Too many false alerts | Increase `overlap_threshold` or `min_object_area` |
| Missing real intrusions | Decrease `motion.threshold`, increase sensitivity |
| Slow processing | Reduce resolution, disable `save_video` |
| Camera not opening | Check source index, permissions, cable |

## Performance Monitoring

```bash
# With FPS counter
python src/main.py --show-fps

# With resource monitoring
python src/main.py --profile
```

## Stopping the System

- Press `q` in display window
- `Ctrl+C` in terminal (graceful shutdown)
- Kills background processes automatically
```

#### File: `6-troubleshooting.md`

**Nội dung**:

```markdown
# Troubleshooting Guide

## Installation Issues

### Issue: `pip install` fails
**Symptoms:**
```
ERROR: Could not find a version that satisfies the requirement opencv-python
```

**Solutions:**
1. Update pip: `pip install --upgrade pip`
2. Check Python version: `python --version` (need 3.8+)
3. Try: `pip install opencv-python-headless`
4. Install from wheel file

### Issue: Import errors
**Symptoms:**
```
ModuleNotFoundError: No module named 'cv2'
```

**Solutions:**
1. Ensure virtual environment is activated
2. Reinstall: `pip uninstall opencv-python && pip install opencv-python`
3. Check installation: `pip list | grep opencv`

## Runtime Issues

### Issue: Video not opening
**Symptoms:**
```
[ERROR] Cannot open video source
```

**Solutions:**
1. Check file path is correct
2. Verify video file is not corrupted (play in VLC)
3. For webcam: Try different indices (0, 1, 2)
4. For webcam: Check permissions (especially macOS)
5. Install additional codecs: `pip install opencv-contrib-python`

### Issue: ROI file not found
**Symptoms:**
```
FileNotFoundError: data/roi/restricted_area.json
```

**Solutions:**
1. Create directory: `mkdir -p data/roi`
2. Create minimal ROI file (see `3-roi-definition.md`)
3. Check `roi_file` path in `config.yaml`

### Issue: No motion detected
**Symptoms:**
- Video plays but no bounding boxes appear
- No alerts even when person clearly visible

**Solutions:**
1. Lower `motion.threshold` in config (try 10)
2. Check background subtraction method (try "MOG2" → "frame_diff")
3. Verify `min_object_area` not too high
4. Print debug info: Add `--debug` flag

### Issue: Too many false alerts
**Symptoms:**
- Constant alerts with no persons
- Shadows/lighting triggering alerts

**Solutions:**
1. Increase `overlap_threshold` (0.3 → 0.5)
2. Increase `time_threshold` (1.0 → 2.0)
3. Enable shadow detection: `detect_shadows: true`
4. Increase `min_object_area` to filter noise
5. Adjust `motion.threshold` higher (16 → 25)

### Issue: Slow processing
**Symptoms:**
- Low FPS (<5 FPS)
- High CPU usage

**Solutions:**
1. Reduce video resolution:
   ```python
   frame = cv2.resize(frame, (640, 360))
   ```
2. Skip frames:
   ```python
   if frame_count % 2 == 0:  # Process every 2nd frame
   ```
3. Disable real-time display: `show_realtime: false`
4. Use GPU acceleration (requires CUDA)
5. Simplify ROI (fewer points)

### Issue: Out of memory
**Symptoms:**
```
MemoryError: Unable to allocate array
```

**Solutions:**
1. Process shorter video segments
2. Reduce history: `history: 500` → `200`
3. Release unused variables
4. Use `frame_diff` instead of `MOG2/KNN`

## Detection Quality Issues

### Issue: Edges not detected properly
**Symptoms:**
- Incomplete object boundaries
- Missing edges in low light

**Solutions:**
1. Adjust Canny thresholds:
   - Lower both thresholds for more edges
   - Maintain 1:2 or 1:3 ratio (low:high)
2. Try Sobel instead of Canny
3. Apply Gaussian blur before edge detection
4. Increase contrast with histogram equalization

### Issue: Segmentation errors
**Symptoms:**
- Person split into multiple regions
- Background included in person region

**Solutions:**
1. Adjust morphology:
   - Increase `kernel_size` (5 → 7)
   - Increase `iterations` (2 → 3)
2. Use closing operation to fill holes
3. Apply median filter to reduce noise
4. Tune region growing similarity threshold

### Issue: Lighting changes cause issues
**Symptoms:**
- Sudden lighting change triggers false alerts
- System fails in shadows

**Solutions:**
1. Use adaptive thresholding (already in pipeline)
2. Increase `history` for background model (500 → 1000)
3. Apply gamma correction:
   ```python
   frame = np.power(frame/255.0, 0.7) * 255
   ```
4. Use histogram equalization per frame
5. Consider CLAHE (Contrast Limited AHE)

## Configuration Issues

### Issue: YAML syntax error
**Symptoms:**
```
yaml.scanner.ScannerError: mapping values are not allowed here
```

**Solutions:**
1. Check indentation (use spaces, not tabs)
2. Quote string values: `"value"`
3. Validate YAML online: yamllint.com

### Issue: JSON ROI syntax error
**Symptoms:**
```
json.decoder.JSONDecodeError: Expecting property name
```

**Solutions:**
1. Validate JSON online: jsonlint.com
2. Check commas, brackets, quotes
3. Use ROI selector tool instead of manual editing

## Platform-Specific Issues

### macOS:
- **Camera permission**: System Preferences → Security & Privacy → Camera
- **File permissions**: Check `chmod` on directories

### Windows:
- **Path separators**: Use `/` or `\\` (not single `\`)
- **Antivirus**: May block camera access, whitelist Python

### Linux:
- **Camera device**: May be `/dev/video0`, `/dev/video1`
- **Permissions**: Add user to `video` group:
  ```bash
  sudo usermod -a -G video $USER
  ```

## Getting Help

### Enable Debug Mode
```bash
python src/main.py --debug
```
Shows detailed logs for each processing step.

### Generate Debug Report
```bash
python src/debug_report.py
```
Outputs system info, config, sample frames.

### Check Logs
```bash
tail -f data/output/alerts.log
```

### Test Individual Modules
```bash
# Test motion detection only
python tests/test_motion.py

# Test threshold only
python tests/test_threshold.py
```

### Common Commands for Diagnosis
```bash
# Check OpenCV build info
python -c "import cv2; print(cv2.getBuildInformation())"

# Test video file
python -c "import cv2; cap=cv2.VideoCapture('video.mp4'); print(cap.isOpened())"

# Test camera
python -c "import cv2; cap=cv2.VideoCapture(0); print(cap.isOpened())"
```

## Still Stuck?

1. Check project README.md
2. Review example outputs in `documentation/04-deliverables/`
3. Compare your config with preset configurations
4. Simplify: Start with minimal config, add complexity gradually
5. Test with different input video (ensure input is valid)
```

---

### 🧠 4. Knowledge Base (`knowledge-base/`)

#### 4.1 Fundamentals (`fundamentals/`)

##### File: `image-basics.md`
**Nội dung**:
- Digital image representation (matrix, pixels, channels)
- Color spaces (RGB, BGR, Grayscale, HSV)
- Image resolution and dimensions
- Pixel intensity values (0-255 for 8-bit)
- Image formats (PNG, JPEG, BMP)
- Reading/writing images with OpenCV
- Basic operations (crop, resize, flip, rotate)

##### File: `video-processing.md`
**Nội dung**:
- Video as sequence of frames
- Frame rate (FPS) và temporal resolution
- Video codecs and containers
- Reading frames with VideoCapture
- Writing videos with VideoWriter
- Frame extraction techniques
- Temporal vs spatial information

##### File: `color-spaces.md`
**Nội dung**:
- RGB: Standard color model
- BGR: OpenCV default
- Grayscale: Single channel intensity
- HSV: Hue, Saturation, Value (better for segmentation)
- YCbCr: Luminance and chrominance
- Color space conversion với `cv2.cvtColor()`
- When to use which color space

#### 4.2 Motion Detection (`motion-detection/`)

##### File: `frame-differencing-theory.md`

**Nội dung**:

```markdown
# Frame Differencing Theory

## Definition
Frame differencing là kỹ thuật phát hiện chuyển động bằng cách so sánh các frame liên tiếp trong video.

## Basic Algorithm

### 1. Consecutive Frame Differencing
```
D(t) = |F(t) - F(t-1)|
```
- F(t): Current frame
- F(t-1): Previous frame
- D(t): Difference image

### 2. Thresholding
```
Binary(t) = {
  255 if D(t) > threshold
  0   otherwise
}
```

### 3. Steps:
1. Read frame F(t)
2. Convert to grayscale
3. Compute difference with previous frame
4. Apply threshold
5. Morphological operations (optional)
6. Find contours
7. Draw bounding boxes

## Variants

### A. Two-Frame Difference
```python
diff = cv2.absdiff(frame_t, frame_t_1)
```
**Pros**: Simple, fast
**Cons**: Sensitive to noise

### B. Three-Frame Difference
```python
diff1 = cv2.absdiff(frame_t, frame_t_1)
diff2 = cv2.absdiff(frame_t_1, frame_t_2)
motion = cv2.bitwise_and(diff1, diff2)
```
**Pros**: More robust
**Cons**: Slower, may miss fast motion

### C. Weighted Difference
```python
diff = cv2.absdiff(frame_t, alpha*frame_t_1 + (1-alpha)*frame_t_2)
```
**Pros**: Temporal smoothing
**Cons**: More complex

## Threshold Selection

### Fixed Threshold:
```python
threshold = 25
_, binary = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
```

### Adaptive Threshold:
```python
binary = cv2.adaptiveThreshold(diff, 255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY, 11, 2)
```

### Otsu's Method:
```python
_, binary = cv2.threshold(diff, 0, 255,
    cv2.THRESH_BINARY + cv2.THRESH_OTSU)
```

## Morphological Post-Processing

```python
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

# Remove noise
opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

# Fill holes
closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)

# Smooth boundaries
dilated = cv2.dilate(closed, kernel, iterations=2)
```

## Advantages
✅ Simple to implement
✅ Fast computation
✅ No training required
✅ Works well for static cameras

## Disadvantages
❌ Sensitive to noise
❌ Affected by illumination changes
❌ Camera jitter causes false detections
❌ Moving objects only (not stationary objects)
❌ Ghost effect (holes in moving objects)

## Improvements

### 1. Gaussian Blur
```python
frame = cv2.GaussianBlur(frame, (5, 5), 0)
```
Reduces noise before differencing.

### 2. Background Subtraction
Instead of F(t-1), use learned background model.

### 3. Multi-Scale
Compute differences at multiple resolutions.

### 4. Temporal Median
Use median of last N frames instead of single previous frame.

## Applications
- Motion detection in surveillance
- Activity recognition
- Change detection
- Video compression (motion estimation)
- Sports analysis

## Comparison with Background Subtraction

| Feature | Frame Diff | Background Subtraction |
|---------|------------|------------------------|
| **Complexity** | Low | Medium-High |
| **Speed** | Fast | Medium |
| **Accuracy** | Medium | High |
| **Lighting** | Sensitive | Adaptive |
| **Setup** | None | Learning period |
| **Stationary** | ❌ | ✅ |

## Example Code

```python
import cv2
import numpy as np

def frame_difference(video_path):
    cap = cv2.VideoCapture(video_path)
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()

    while cap.isOpened():
        # Convert to grayscale
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        # Compute difference
        diff = cv2.absdiff(gray1, gray2)

        # Apply Gaussian blur
        diff = cv2.GaussianBlur(diff, (5, 5), 0)

        # Threshold
        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

        # Morphology
        kernel = np.ones((5, 5), np.uint8)
        thresh = cv2.dilate(thresh, kernel, iterations=2)

        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)

        # Draw bounding boxes
        for contour in contours:
            if cv2.contourArea(contour) > 1000:  # Filter small areas
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame2, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Display
        cv2.imshow("Frame Difference", frame2)
        cv2.imshow("Threshold", thresh)

        # Update frames
        frame1 = frame2
        ret, frame2 = cap.read()

        if not ret or cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
```

## Further Reading
- "Background and Foreground Modeling" (Piccardi, 2004)
- "Adaptive Background Mixture Models" (Stauffer & Grimson, 1999)
- OpenCV Documentation: Background Subtraction
```

##### File: `background-subtraction-methods.md`

**Nội dung**:
- Difference from frame differencing
- Background modeling concepts
- MOG (Mixture of Gaussians)
- MOG2 (Improved MOG)
- KNN (K-Nearest Neighbors)
- GMG (Geometric Multigrid)
- Comparison of methods
- Learning rate and history
- Shadow detection
- OpenCV implementation với `cv2.createBackgroundSubtractor*()`

##### File: `optical-flow.md`

**Nội dung**:
- Optical flow definition (motion vectors)
- Dense vs sparse optical flow
- Lucas-Kanade method
- Farneback method
- Applications in motion tracking
- Visualization techniques
- Comparison with frame differencing

#### 4.3 Segmentation (`segmentation/`)

##### File: `thresholding-methods.md`

**Nội dung**:

```markdown
# Thresholding Methods

## Overview
Thresholding converts grayscale image → binary image by comparing pixel intensities to threshold value(s).

## 1. Global Thresholding

### Basic Thresholding
```
Binary(x,y) = {
  maxval  if I(x,y) > threshold
  0       otherwise
}
```

### OpenCV Types:
```python
_, binary = cv2.threshold(gray, thresh, maxval, cv2.THRESH_BINARY)
```

- `THRESH_BINARY`: value = maxval if > thresh, else 0
- `THRESH_BINARY_INV`: Inverse of binary
- `THRESH_TRUNC`: value = thresh if > thresh, else unchanged
- `THRESH_TOZERO`: value = unchanged if > thresh, else 0
- `THRESH_TOZERO_INV`: Inverse of tozero

### Otsu's Method (Automatic Threshold Selection)
```python
_, binary = cv2.threshold(gray, 0, 255,
    cv2.THRESH_BINARY + cv2.THRESH_OTSU)
```

**How it works:**
- Computes histogram
- Tries all possible thresholds
- Selects threshold that minimizes intra-class variance
- Optimal for bimodal histograms

## 2. Adaptive Thresholding

### Why Adaptive?
- **Problem**: Global threshold fails with non-uniform lighting
- **Solution**: Calculate threshold for small regions

### Adaptive Mean
```python
binary = cv2.adaptiveThreshold(gray, 255,
    cv2.ADAPTIVE_THRESH_MEAN_C,
    cv2.THRESH_BINARY, block_size, C)
```

**Threshold** = mean of (block_size × block_size) neighborhood - C

### Adaptive Gaussian
```python
binary = cv2.adaptiveThreshold(gray, 255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY, block_size, C)
```

**Threshold** = Gaussian-weighted mean - C

### Parameters:
- **block_size**: Neighborhood size (must be odd, e.g., 11, 15, 21)
  - Smaller → more local adaptation
  - Larger → smoother, less noise
- **C**: Constant subtracted from mean (fine-tuning)
  - Positive C → lower threshold → more foreground
  - Negative C → higher threshold → less foreground

## 3. Multi-Level Thresholding

For multiple regions:
```python
_, level1 = cv2.threshold(gray, thresh1, 255, cv2.THRESH_BINARY)
_, level2 = cv2.threshold(gray, thresh2, 255, cv2.THRESH_BINARY)
multi_level = level1 - level2  # Pixels between thresh1 and thresh2
```

## 4. Color-Based Thresholding

In HSV space:
```python
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
lower = np.array([hue_min, sat_min, val_min])
upper = np.array([hue_max, sat_max, val_max])
mask = cv2.inRange(hsv, lower, upper)
```

**Use case**: Segment specific colors (e.g., red objects)

## Comparison

| Method | Best For | Pros | Cons |
|--------|----------|------|------|
| **Global** | Uniform lighting | Simple, fast | Fails with gradients |
| **Otsu** | Bimodal histogram | Automatic | Not adaptive |
| **Adaptive Mean** | Variable lighting | Handles gradients | Slower |
| **Adaptive Gaussian** | Smooth gradients | Best quality | Slowest |
| **Color** | Colored objects | Robust to lighting | Needs color tuning |

## Tips for Intrusion Detection

1. **Pre-processing:**
   - Gaussian blur to reduce noise
   - Histogram equalization if too dark/bright

2. **Choose method:**
   - **Daylight (uniform)**: Otsu
   - **Indoor (variable light)**: Adaptive Gaussian
   - **Night (low contrast)**: Adaptive Mean with larger block_size

3. **Post-processing:**
   - Morphological opening: Remove noise
   - Morphological closing: Fill holes

4. **Parameter tuning:**
   - Start with block_size=11, C=2
   - Increase block_size if too noisy
   - Adjust C if too much/little foreground

## Example for Person Detection

```python
def adaptive_person_threshold(frame):
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Adaptive thresholding
    binary = cv2.adaptiveThreshold(blurred, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,  # Inverse: person = white
        block_size=15,
        C=3)

    # Morphological operations
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    return binary
```

## Further Reading
- Otsu's original paper (1979)
- "Adaptive Thresholding for the DigitalDesk" (Wellner, 1993)
- Digital Image Processing (Gonzalez & Woods) - Chapter 10
```

##### File: `edge-based-segmentation.md`
**Nội dung**:
- Edge detection fundamentals
- Gradient-based methods (Sobel, Prewitt, Scharr)
- Canny edge detection (detailed 5-step algorithm)
- Laplacian of Gaussian (LoG)
- Edge linking và boundary tracing
- Integration with region growing
- Applications in object segmentation

##### File: `region-based-segmentation.md`
**Nội dung**:
- Region growing algorithm
- Seeded region growing
- Similarity predicates (intensity, color, texture)
- Region merging and splitting
- Watershed algorithm
- Connected components analysis
- Application to person segmentation

#### 4.4 Advanced Topics (`advanced-topics/`)

##### File: `adaptive-algorithms.md`
**Nội dung**:
- Adaptive thresholding in depth
- Adaptive background modeling
- Learning rate adjustment
- Handling gradual lighting changes
- Sudden change detection
- Parameter self-tuning strategies

##### File: `morphological-processing.md`
**Nội dung**:
- Structuring elements
- Erosion and dilation
- Opening and closing
- Morphological gradient
- Top-hat and black-hat transforms
- Application to noise removal and hole filling
- Choosing kernel size and shape

##### File: `object-tracking.md`
**Nội dung**:
- Tracking vs detection
- Centroid tracking
- Kalman filtering
- Mean-shift and CAMShift
- Optical flow tracking
- Multi-object tracking (MOT)
- Handling occlusions
- Track association và ID assignment

---

### 📋 5. Main README (`README.md`)

**Nội dung**:

```markdown
# REQ-4 Project: Person Segmentation & Intrusion Detection

## Overview
This project implements an intelligent surveillance system that detects persons entering restricted areas using computer vision techniques. The system works in various lighting conditions and provides real-time alerts.

## Project Structure

```
req-4-project/
├── code/                      # Implementation
├── documentation/             # Reports and theory
├── implementation-guide/      # Setup and usage instructions
├── knowledge-base/           # Learning resources
└── README.md                 # This file
```

## Quick Start

### 1. Setup Environment
```bash
cd code
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 2. Prepare Data
- Place test videos in `code/data/input/`
- Define ROI in `code/data/roi/restricted_area.json`
  (Use `python tools/roi_selector.py` for interactive selection)

### 3. Configure
Edit `code/config/config.yaml` to match your scenario.

### 4. Run
```bash
cd code
python src/main.py
```

## Features
✅ Motion-based person detection (frame differencing + background subtraction)
✅ Adaptive thresholding for variable lighting
✅ Edge detection and region growing for segmentation
✅ Custom ROI definition (polygons/rectangles)
✅ Real-time intrusion alerts (visual + audio + logging)
✅ Output video with bounding boxes and overlays
✅ Works in daylight, low-light, and night conditions

## Technical Stack
- **Language**: Python 3.8+
- **Libraries**: OpenCV, NumPy, scikit-image
- **Algorithms**:
  - Motion Detection: MOG2, KNN, Frame Differencing
  - Segmentation: Adaptive Thresholding, Canny Edge Detection
  - Region Growing with seed-based expansion
  - Intrusion Detection: IoU-based overlap calculation

## Documentation

### For Implementation:
1. **implementation-guide/**: Step-by-step setup and usage
2. **code/README.md**: Code structure and module details

### For Understanding:
1. **knowledge-base/**: Theory and concepts
2. **documentation/01-theory-foundation/**: Detailed explanations

### For Evaluation:
1. **documentation/03-evaluation/**: Test results and analysis
2. **documentation/04-deliverables/**: Demo videos and reports

## Results

### Performance Metrics:
- **Processing Speed**: ~25-30 FPS (1280x720)
- **Detection Accuracy**: 92% (daylight), 85% (low-light), 78% (night)
- **False Positive Rate**: <5%
- **Memory Usage**: ~200MB

### Test Scenarios:
1. **Daylight**: Clear visibility, high accuracy
2. **Low-light**: Moderate visibility, adaptive threshold performs well
3. **Night**: Low visibility, challenges with dark clothing

## Limitations
- Requires relatively static camera
- Struggles with very crowded scenes
- False positives during sudden lighting changes (lightning, car headlights)
- Cannot distinguish between authorized/unauthorized persons (no face recognition)

## Future Improvements
- Deep learning integration (YOLO, Faster R-CNN)
- Person re-identification
- Multi-camera support
- Cloud connectivity for remote monitoring
- Mobile app for alerts

## References
- Digital Image Processing (Gonzalez & Woods)
- OpenCV Documentation: https://docs.opencv.org/
- Background Subtraction: Piccardi (2004)
- Canny Edge Detection: Canny (1986)

## License
Educational project for Image Processing course.

## Author
[Your Name]
[Your Student ID]
[Your University]

---

**Date**: January 2025
**Version**: 1.0
**Course**: Image Processing (Xử Lý Ảnh)
```

---

## Thực Hiện Theo Các Phase

### Phase 1: Chuẩn Bị Môi Trường (1-2 giờ)
1. ✅ Tạo folder structure
2. ✅ Setup virtual environment
3. ✅ Install dependencies
4. ✅ Prepare test videos
5. ✅ Create initial config files

### Phase 2: Implement Core Modules (4-6 giờ)
1. ✅ `motion_detector.py` - Frame differencing + MOG2
2. ✅ `adaptive_threshold.py` - Adaptive thresholding
3. ✅ `edge_detector.py` - Sobel + Canny
4. ✅ `region_grower.py` - Region growing
5. ✅ `intrusion_detector.py` - ROI overlap detection
6. ✅ `alert_system.py` - Visual/audio alerts + logging

### Phase 3: Integration (2-3 giờ)
1. ✅ `main.py` - Pipeline integration
2. ✅ Testing với real videos
3. ✅ Parameter tuning
4. ✅ Bug fixes

### Phase 4: Documentation - Theory (3-4 giờ)
1. ✅ Write 6 theory documents trong `01-theory-foundation/`
2. ✅ Add diagrams và examples
3. ✅ Cross-reference với code

### Phase 5: Documentation - Practice (2-3 giờ)
1. ✅ System architecture diagram
2. ✅ Algorithm design documentation
3. ✅ Implementation details explanation
4. ✅ User guide

### Phase 6: Evaluation (2-3 giờ)
1. ✅ Run tests in 3 lighting conditions
2. ✅ Collect metrics (accuracy, FPS, etc.)
3. ✅ Record demo videos
4. ✅ Analyze limitations

### Phase 7: Knowledge Base (3-4 giờ)
1. ✅ Write fundamental concepts (9 documents)
2. ✅ Add code examples
3. ✅ Create reference materials

### Phase 8: Implementation Guide (2-3 giờ)
1. ✅ Environment setup guide
2. ✅ Data preparation guide
3. ✅ Configuration guide
4. ✅ Troubleshooting guide

### Phase 9: Final Deliverables (2-3 giờ)
1. ✅ Compile final report PDF
2. ✅ Prepare demo videos với annotations
3. ✅ Create screenshots
4. ✅ Final code review và cleanup

### Phase 10: Testing & QA (1-2 giờ)
1. ✅ Run full system test
2. ✅ Verify all documentation links
3. ✅ Ensure reproducibility
4. ✅ Final presentation slides (optional)

---

## Estimated Total Time: 22-33 giờ

### Breakdown:
- **Code Implementation**: 8-11 giờ (35-40%)
- **Documentation**: 12-17 giờ (50-55%)
- **Testing & QA**: 2-5 giờ (10-15%)

---

## Success Criteria

### Code (35%):
- [ ] All modules implemented và functional
- [ ] System runs without errors
- [ ] Real-time processing (>20 FPS)
- [ ] Configurable parameters
- [ ] Clean, documented code

### Documentation (40%):
- [ ] Complete theory foundation (6 documents)
- [ ] Practical implementation guide (5 documents)
- [ ] Evaluation report với metrics (5 documents)
- [ ] Final report compiled (PDF)

### Deliverables (25%):
- [ ] 3 demo videos (daylight, low-light, night)
- [ ] Screenshots of system
- [ ] Alert logs
- [ ] Accuracy analysis report

---

## Yêu Cầu Báo Cáo

Theo format chuẩn, báo cáo cuối kỳ cần bao gồm:

### 1. Cơ Sở Lý Thuyết (Theory Foundation)
**Folder**: `documentation/01-theory-foundation/`

- [ ] Giải thích các thuật toán sử dụng
- [ ] Công thức toán học
- [ ] Diagrams và flowcharts
- [ ] References to textbooks/papers

### 2. Thực Hành (Practical Implementation)
**Folder**: `documentation/02-practical-implementation/`

- [ ] System architecture
- [ ] Algorithm design
- [ ] Implementation details
- [ ] Parameter tuning
- [ ] User guide

### 3. Đánh Giá & Kết Luận (Evaluation & Conclusion)
**Folder**: `documentation/03-evaluation/`

- [ ] Test scenarios
- [ ] Accuracy metrics
- [ ] Performance analysis
- [ ] Limitations và challenges
- [ ] Conclusions

### 4. Sản Phẩm (Deliverables)
**Folder**: `documentation/04-deliverables/`

- [ ] Demo videos
- [ ] Screenshots
- [ ] Final report PDF
- [ ] Source code (với README)

---

## Checklist Hoàn Thành

### Trước Khi Bắt Đầu:
- [ ] Đọc kỹ yêu cầu đề tài
- [ ] Chuẩn bị video input samples
- [ ] Xác định ROI (restricted areas)
- [ ] Setup development environment

### Trong Quá Trình:
- [ ] Commit code thường xuyên (Git)
- [ ] Test từng module riêng lẻ trước khi integrate
- [ ] Document code bằng docstrings
- [ ] Save intermediate results (screenshots, videos)

### Trước Khi Nộp:
- [ ] Run full system test
- [ ] Verify tất cả file paths đúng
- [ ] Check spelling và grammar trong documentation
- [ ] Compile final report PDF
- [ ] Create backup (zip archive)

---

## Tips & Best Practices

### Code:
1. **Modular design**: Mỗi module làm 1 việc cụ thể
2. **Configuration file**: Không hardcode parameters
3. **Error handling**: Try-except cho file I/O, video capture
4. **Logging**: Use Python logging module, không chỉ print()
5. **Performance**: Profile code, optimize bottlenecks

### Documentation:
1. **Clear structure**: Headings, subheadings, bullet points
2. **Visuals**: Diagrams > text khi có thể
3. **Examples**: Code snippets với comments
4. **Cross-reference**: Link giữa các documents
5. **Consistent format**: Markdown hoặc LaTeX

### Testing:
1. **Multiple videos**: Test nhiều scenarios
2. **Edge cases**: Very dark, very bright, fast motion, no motion
3. **Parameter sweep**: Try different configs
4. **Baseline comparison**: Compare với simple methods
5. **User testing**: Ask someone else to run your code

---

## Resources

### Learning Materials:
- **knowledge-base/**: Tất cả concepts cần thiết
- **OpenCV Tutorials**: https://docs.opencv.org/4.x/d9/df8/tutorial_root.html
- **Gonzalez & Woods**: Digital Image Processing (Chapter 10: Image Segmentation)

### Sample Datasets:
- **VIRAT Video Dataset**: Surveillance videos
- **ChangeDetection.net**: Background subtraction benchmark
- **Pexels/Pixabay**: Free stock videos

### Tools:
- **ROI Selector**: `tools/roi_selector.py` (trong code)
- **Video Annotation**: LabelImg, CVAT
- **Performance Profiling**: cProfile, line_profiler

---

## Contact & Support

Nếu gặp vấn đề:
1. Check `implementation-guide/6-troubleshooting.md`
2. Review `knowledge-base/` for concepts
3. Test individual modules in `tests/`
4. Check code examples trong theory documents

---

**Good luck với đề tài! 🎓🚀**
