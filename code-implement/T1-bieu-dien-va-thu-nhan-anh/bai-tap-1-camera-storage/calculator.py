"""
Bài tập 1 - Tính dung lượng & băng thông cho hệ thống camera
Bối cảnh: Thiết kế hệ thống giám sát hành lang trường học

Tác giả: TS. Phan Thanh Toàn
"""

import math

def calculate_storage(width, height, channels, bit_depth, fps, duration_days):
    """
    Tính dung lượng lưu trữ cho hệ thống camera

    Args:
        width: Chiều rộng ảnh (pixels)
        height: Chiều cao ảnh (pixels)
        channels: Số kênh màu (1=xám, 3=RGB)
        bit_depth: Độ sâu bit (8, 10, 12)
        fps: Số khung hình/giây
        duration_days: Thời gian lưu trữ (ngày)

    Returns:
        dict: Kích thước ảnh, dung lượng, băng thông
    """
    # Tính kích thước 1 frame (bytes)
    pixels_per_frame = width * height
    bits_per_pixel = channels * bit_depth
    bytes_per_frame = (pixels_per_frame * bits_per_pixel) / 8

    # Tính dung lượng theo thời gian
    frames_per_second = fps
    frames_per_day = frames_per_second * 60 * 60 * 24
    frames_total = frames_per_day * duration_days

    bytes_total = bytes_per_frame * frames_total

    # Quy đổi đơn vị
    kb_total = bytes_total / 1024
    mb_total = kb_total / 1024
    gb_total = mb_total / 1024
    tb_total = gb_total / 1024

    # Tính băng thông (Mbps)
    bits_per_second = bytes_per_frame * fps * 8
    mbps = bits_per_second / (1024 * 1024)

    return {
        'frame_size_bytes': bytes_per_frame,
        'frame_size_kb': bytes_per_frame / 1024,
        'frame_size_mb': bytes_per_frame / (1024 * 1024),
        'total_bytes': bytes_total,
        'total_kb': kb_total,
        'total_mb': mb_total,
        'total_gb': gb_total,
        'total_tb': tb_total,
        'bandwidth_bps': bits_per_second,
        'bandwidth_mbps': mbps,
        'bandwidth_gbps': mbps / 1024
    }

def print_scenario(name, width, height, bit_depth, fps, days=30):
    """In kết quả một kịch bản"""
    print(f"\n{'='*60}")
    print(f"Kịch bản: {name}")
    print(f"{'='*60}")
    print(f"Độ phân giải: {width}x{height}")
    print(f"Độ sâu bit: {bit_depth} bit")
    print(f"FPS: {fps}")
    print(f"Thời gian lưu: {days} ngày")

    # Tính cho ảnh xám
    result_gray = calculate_storage(width, height, 1, bit_depth, fps, days)
    print(f"\n--- ẢNH XÁM (1 kênh) ---")
    print(f"Kích thước 1 frame: {result_gray['frame_size_kb']:.2f} KB ({result_gray['frame_size_mb']:.4f} MB)")
    print(f"Dung lượng {days} ngày: {result_gray['total_gb']:.2f} GB ({result_gray['total_tb']:.3f} TB)")
    print(f"Băng thông cần thiết: {result_gray['bandwidth_mbps']:.2f} Mbps")

    # Tính cho ảnh RGB
    result_rgb = calculate_storage(width, height, 3, bit_depth, fps, days)
    print(f"\n--- ẢNH RGB (3 kênh) ---")
    print(f"Kích thước 1 frame: {result_rgb['frame_size_kb']:.2f} KB ({result_rgb['frame_size_mb']:.4f} MB)")
    print(f"Dung lượng {days} ngày: {result_rgb['total_gb']:.2f} GB ({result_rgb['total_tb']:.3f} TB)")
    print(f"Băng thông cần thiết: {result_rgb['bandwidth_mbps']:.2f} Mbps ({result_rgb['bandwidth_gbps']:.3f} Gbps)")

if __name__ == "__main__":
    print("TÍNH TOÁN DUNG LƯỢNG & BĂNG THÔNG HỆ THỐNG CAMERA GIÁM SÁT")
    print("="*60)

    # (a) 1080p – 8 bit – 15 fps
    print_scenario("(a) 1080p – 8 bit – 15 fps", 1920, 1080, 8, 15)

    # (b) 720p – 10 bit – 25 fps
    print_scenario("(b) 720p – 10 bit – 25 fps", 1280, 720, 10, 25)

    # (c) 4K – 8 bit – 5 fps
    print_scenario("(c) 4K – 8 bit – 5 fps", 3840, 2160, 8, 5)

    # So sánh
    print(f"\n{'='*60}")
    print("NHẬN XÉT & TRADE-OFF")
    print(f"{'='*60}")
    print("""
Trade-off giữa độ phân giải không gian và độ phân giải mức xám:

1. Độ phân giải không gian (Spatial Resolution):
   - 4K > 1080p > 720p
   - Ảnh hưởng: Chi tiết không gian, khả năng phóng to
   - Tăng độ phân giải → tăng dung lượng theo tỷ lệ bình phương

2. Độ phân giải mức xám (Gray-level Resolution):
   - 12-bit > 10-bit > 8-bit
   - Ảnh hưởng: Độ chi tiết sắc độ, khả năng phân biệt màu
   - Tăng bit depth → tăng dung lượng tuyến tính

3. Lựa chọn tối ưu:
   - Giám sát thông thường: 720p/1080p - 8 bit - 15-25 fps
   - Cần chi tiết cao: 4K - 8 bit - 5-10 fps
   - Điều kiện ánh sáng thay đổi: 1080p - 10 bit - 15 fps
   - Quan trọng: Sử dụng nén (H.264/H.265) giảm 90-95% dung lượng
""")
