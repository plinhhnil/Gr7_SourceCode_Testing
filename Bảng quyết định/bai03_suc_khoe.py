# -*- coding: utf-8 -*-
"""Bài 3: Phân loại sức khỏe theo HR và SpO2."""
import sys
import common

SO_BAI = 3
TEN = "Phân loại tình trạng sức khỏe theo nhịp tim (HR) và SpO2"
DAC_TA = """
Đầu vào : HR nguyên ∈ [40..180] (bpm); SpO2 nguyên ∈ [85..100] (%)
Ngưỡng HR   : [40,50) Nguy hiểm | [50,60) Cảnh báo | [60,100] Bình thường
              (100,120] Cảnh báo | (120,180] Nguy hiểm
Ngưỡng SpO2 : [85,90) Nguy hiểm | [90,95) Cảnh báo | [95,100] Bình thường
Đầu ra  : Invalid | Nguy hiểm (có ít nhất 1 chỉ số nguy hiểm) |
          Cảnh báo (có chỉ số cảnh báo, không có nguy hiểm) | Bình thường
"""


def sut(hr, spo2):
    if not (40 <= hr <= 180) or not (85 <= spo2 <= 100):
        return "Invalid"
    if hr < 50 or hr > 120 or spo2 < 90:
        return "Nguy hiểm"
    if hr < 60 or hr > 100 or spo2 < 95:
        return "Cảnh báo"
    return "Bình thường"


DIEU_KIEN = [
    ("C1",  "HR ∉ [40,180]",    lambda h, s: not (40 <= h <= 180)),
    ("C2",  "SpO2 ∉ [85,100]",  lambda h, s: not (85 <= s <= 100)),
    ("C3",  "HR ∈ [40,50)",     lambda h, s: 40 <= h < 50),
    ("C4",  "HR ∈ (120,180]",   lambda h, s: 120 < h <= 180),
    ("C5",  "SpO2 ∈ [85,90)",   lambda h, s: 85 <= s < 90),
    ("C6",  "HR ∈ [50,60)",     lambda h, s: 50 <= h < 60),
    ("C7",  "HR ∈ (100,120]",   lambda h, s: 100 < h <= 120),
    ("C8",  "SpO2 ∈ [90,95)",   lambda h, s: 90 <= s < 95),
    ("C9",  "HR ∈ [60,100]",    lambda h, s: 60 <= h <= 100),
    ("C10", "SpO2 ∈ [95,100]",  lambda h, s: 95 <= s <= 100),
]
HANH_DONG = [("A1", "Invalid"), ("A2", "Nguy hiểm"),
             ("A3", "Cảnh báo"), ("A4", "Bình thường")]
LUAT = {
    "R1": ("T---------", "A1"),
    "R2": ("FT--------", "A1"),
    "R3": ("FFT-------", "A2"),
    "R4": ("FFFT------", "A2"),
    "R5": ("FFFFT-----", "A2"),
    "R6": ("FFFFFT----", "A3"),
    "R7": ("FFFFFFT---", "A3"),
    "R8": ("FFFFFFFT--", "A3"),
    "R9": ("FFFFFFFFTT", "A4"),
}

CASES = [
    ("TC01", "R1", (39, 84),   "Invalid",     "HR = 39, sát dưới biên 40 (SpO2 cũng sát dưới 85 nhưng R1 xét trước)"),
    # Bản gốc trong file: (181, 101) -> HR cũng ngoài miền nên khớp R1, không khớp R2.
    # Đã sửa HR về giá trị hợp lệ để test chỉ thuộc R2.
    ("TC02", "R2", (60, 101),  "Invalid",     "SpO2 = 101 vượt biên 100; HR hợp lệ (đã sửa từ (181,101))"),
    ("TC03", "R3", (49, 100),  "Nguy hiểm",   "HR = 49 sát dưới 50 (nhóm [40,50))"),
    ("TC04", "R4", (121, 85),  "Nguy hiểm",   "HR = 121 vừa qua 120; SpO2 biên dưới 85"),
    ("TC05", "R5", (60, 89),   "Nguy hiểm",   "SpO2 = 89 sát dưới 90; HR biên dưới nhóm bình thường 60"),
    ("TC06", "R6", (50, 95),   "Cảnh báo",    "HR đúng biên 50; SpO2 biên dưới nhóm bình thường 95"),
    ("TC07", "R7", (101, 90),  "Cảnh báo",    "HR = 101 vừa qua 100; SpO2 đúng biên 90"),
    ("TC08", "R8", (100, 94),  "Cảnh báo",    "SpO2 = 94 sát dưới 95; HR đúng biên trên 100 (vẫn bình thường)"),
    ("TC09", "R9", (60, 95),   "Bình thường", "HR và SpO2 đều đúng biên dưới của nhóm bình thường"),
]

if __name__ == "__main__":
    sys.exit(common.main(sys.modules[__name__], sys.argv[1:]))
