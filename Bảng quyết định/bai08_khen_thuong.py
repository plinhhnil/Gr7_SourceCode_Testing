# -*- coding: utf-8 -*-
"""Bài 8: Phân loại khen thưởng (kpi, td, thang)."""
import sys
import common

SO_BAI = 8
TEN = "Phân loại khen thưởng của công ty"
DAC_TA = """
Đầu vào : kpi (thực) ∈ [0.0; 100.0] ; td (điểm thái độ, nguyên) ∈ [0; 100] ;
          thang (số tháng làm việc, nguyên) ∈ [1; 12]
Đầu ra  : Invalid | Khong | Tieu chuan | Xuat sac
Quy tắc :
  - kpi ∉ [0;100] hoặc td ∉ [0;100] hoặc thang ∉ [1;12]    -> Invalid
  - kpi ∈ [0;75) hoặc td ∈ [0;80) hoặc thang ∈ [1;6)       -> Khong
  - kpi ∈ [75;90) và td ∈ [80;100] và thang ∈ [6;12]       -> Tieu chuan
  - kpi ∈ [90;100] và td ∈ [80;100] và thang ∈ [6;12]      -> Xuat sac
"""


def sut(kpi, td, thang):
    if not (0.0 <= kpi <= 100.0) or not (0 <= td <= 100) or not (1 <= thang <= 12):
        return "Invalid"
    if kpi < 75.0 or td < 80 or thang < 6:
        return "Khong"
    return "Tieu chuan" if kpi < 90.0 else "Xuat sac"


DIEU_KIEN = [
    ("C1",  "kpi ∉ [0.0;100.0]", lambda k, t, m: not (0 <= k <= 100)),
    ("C2",  "td ∉ [0;100]",      lambda k, t, m: not (0 <= t <= 100)),
    ("C3",  "thang ∉ [1;12]",    lambda k, t, m: not (1 <= m <= 12)),
    ("C4",  "kpi ∈ [0.0;75.0)",  lambda k, t, m: 0 <= k < 75),
    ("C5",  "td ∈ [0;80)",       lambda k, t, m: 0 <= t < 80),
    ("C6",  "thang ∈ [1;6)",     lambda k, t, m: 1 <= m < 6),
    ("C7",  "kpi ∈ [75.0;90.0)", lambda k, t, m: 75 <= k < 90),
    ("C8",  "kpi ∈ [90.0;100.0]", lambda k, t, m: 90 <= k <= 100),
    ("C9",  "td ∈ [80;100]",     lambda k, t, m: 80 <= t <= 100),
    ("C10", "thang ∈ [6;12]",    lambda k, t, m: 6 <= m <= 12),
]
HANH_DONG = [("A1", "Invalid"), ("A2", "Khong"),
             ("A3", "Tieu chuan"), ("A4", "Xuat sac")]
LUAT = {
    "R1": ("T---------", "A1"),
    "R2": ("FT--------", "A1"),
    "R3": ("FFT-------", "A1"),
    "R4": ("FFFT------", "A2"),
    "R5": ("FFFFT-----", "A2"),
    "R6": ("FFFFFT----", "A2"),
    "R7": ("FFFFFFTFTT", "A3"),
    "R8": ("FFFFFFFTTT", "A4"),
}

CASES = [
    ("TC01", "R1", (-0.1, 50, 6),    "Invalid",    "kpi = -0.1, sát dưới biên 0.0"),
    ("TC02", "R2", (80.0, 101, 6),   "Invalid",    "td = 101, vượt biên 100"),
    ("TC03", "R3", (80.0, 80, 13),   "Invalid",    "thang = 13, vượt biên 12"),
    ("TC04", "R4", (74.9, 100, 12),  "Khong",      "kpi sát dưới 75.0; td, thang ở biên trên"),
    ("TC05", "R5", (75.0, 79, 12),   "Khong",      "td sát dưới 80; kpi đúng biên 75.0"),
    ("TC06", "R6", (90.0, 80, 5),    "Khong",      "thang sát dưới 6; kpi đúng biên 90.0, td đúng biên 80"),
    ("TC07", "R7", (89.9, 80, 6),    "Tieu chuan", "kpi sát dưới 90; td đúng biên 80; thang đúng biên 6"),
    # Bản gốc trong file: (100.0, 100, 12). Đã đổi kpi về đúng biên 90.0 để bắt lỗi biên
    # (nếu code viết kpi <= 90 thay vì kpi < 90 thì test này sẽ FAIL).
    ("TC08", "R8", (90.0, 80, 6),    "Xuat sac",   "kpi đúng biên 90.0; td, thang đúng biên dưới (đã sửa từ (100.0,100,12))"),
]

if __name__ == "__main__":
    sys.exit(common.main(sys.modules[__name__], sys.argv[1:]))
