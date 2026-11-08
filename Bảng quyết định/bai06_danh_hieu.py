# -*- coding: utf-8 -*-
"""Bài 6: Danh hiệu sinh viên (dht, drl)."""
import sys
import common

SO_BAI = 6
TEN = "Xác định danh hiệu sinh viên theo điểm học tập và điểm rèn luyện"
DAC_TA = """
Đầu vào : dht (điểm học tập) ∈ [0.00 .. 4.00] ; drl (điểm rèn luyện) nguyên ∈ [0 .. 100]
Đầu ra  : Invalid input | Không đạt danh hiệu nào | Sinh viên giỏi | Sinh viên xuất sắc
Quy tắc :
  - dht ∉ [0..4] hoặc drl ∉ [0..100]               -> Invalid input
  - dht ∈ [0.00, 3.20) và drl ∈ [0, 80)            -> Không đạt danh hiệu nào
  - dht ∈ [3.20, 3.60) và drl ∈ [80, 90)           -> Sinh viên giỏi
  - dht ∈ [3.60, 4.00] và drl ∈ [90, 100]          -> Sinh viên xuất sắc
Lỗ hổng của đề: các tổ hợp còn lại (ví dụ dht 3.19 nhưng drl 80) đề không nêu đầu ra.
Bảng quyết định gán cho các tổ hợp này hành động A5 = "Không xác định".
"""


def sut(dht, drl):
    if not (0.0 <= dht <= 4.0) or not (0 <= drl <= 100):
        return "Invalid input"
    if dht < 3.20 and drl < 80:
        return "Không đạt danh hiệu nào"
    if 3.20 <= dht < 3.60 and 80 <= drl < 90:
        return "Sinh viên giỏi"
    if dht >= 3.60 and drl >= 90:
        return "Sinh viên xuất sắc"
    return "Không xác định"


DIEU_KIEN = [
    ("C1", "dht ∉ [0;4]",        lambda d, r: not (0 <= d <= 4)),
    ("C2", "drl ∉ [0;100]",      lambda d, r: not (0 <= r <= 100)),
    ("C3", "dht ∈ [0;3.20)",     lambda d, r: 0 <= d < 3.20),
    ("C4", "dht ∈ [3.20;3.60)",  lambda d, r: 3.20 <= d < 3.60),
    ("C5", "dht ∈ [3.60;4.00]",  lambda d, r: 3.60 <= d <= 4.00),
    ("C6", "drl ∈ [0;80)",       lambda d, r: 0 <= r < 80),
    ("C7", "drl ∈ [80;90)",      lambda d, r: 80 <= r < 90),
    ("C8", "drl ∈ [90;100]",     lambda d, r: 90 <= r <= 100),
]
HANH_DONG = [("A1", "Invalid input"), ("A2", "Không đạt danh hiệu nào"),
             ("A3", "Sinh viên giỏi"), ("A4", "Sinh viên xuất sắc"),
             ("A5", "Không xác định (đề chưa nêu)")]
LUAT = {
    "R1":  ("T-------", "A1"),
    "R2":  ("FT------", "A1"),
    "R3":  ("FFTFFTFF", "A2"),
    "R4":  ("FFTFFFTF", "A5"),
    "R5":  ("FFTFFFFT", "A5"),
    "R6":  ("FFFTFTFF", "A5"),
    "R7":  ("FFFTFFTF", "A3"),
    "R8":  ("FFFTFFFT", "A5"),
    "R9":  ("FFFFTTFF", "A5"),
    "R10": ("FFFFTFTF", "A5"),
    "R11": ("FFFFTFFT", "A4"),
}

CASES = [
    ("TC01", "R1",  (-0.01, 100), "Invalid input", "dht = -0.01, sát dưới biên 0"),
    ("TC02", "R2",  (4.00, 101),  "Invalid input", "drl = 101, vượt biên 100; dht đúng biên 4.00"),
    ("TC03", "R3",  (0.00, 0),    "Không đạt danh hiệu nào", "cả hai biến ở biên dưới"),
    ("TC04", "R4",  (3.19, 80),   "Không xác định", "dht sát dưới 3.20 nhưng drl đúng biên 80"),
    ("TC05", "R5",  (0.00, 100),  "Không xác định", "dht thấp nhất, drl cao nhất"),
    ("TC06", "R6",  (3.20, 79),   "Không xác định", "dht đúng biên 3.20 nhưng drl sát dưới 80"),
    ("TC07", "R7",  (3.59, 89),   "Sinh viên giỏi", "cả hai sát biên trên của nhóm giỏi"),
    ("TC08", "R8",  (3.20, 90),   "Không xác định", "dht đúng biên 3.20 nhưng drl đã tới 90"),
    ("TC09", "R9",  (3.60, 0),    "Không xác định", "dht đúng biên 3.60 nhưng drl thấp nhất"),
    ("TC10", "R10", (4.00, 80),   "Không xác định", "dht cao nhất nhưng drl chỉ 80"),
    ("TC11", "R11", (3.60, 90),   "Sinh viên xuất sắc", "cả hai đúng biên dưới của nhóm xuất sắc"),
]

if __name__ == "__main__":
    sys.exit(common.main(sys.modules[__name__], sys.argv[1:]))
