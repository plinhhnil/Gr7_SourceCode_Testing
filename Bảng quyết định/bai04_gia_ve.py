# -*- coding: utf-8 -*-
"""Bài 4: Giá vé xem phim theo tuổi và ngày trong tuần."""
import sys
import common

SO_BAI = 4
TEN = "Xác định loại vé và giá vé theo tuổi và ngày trong tuần"
DAC_TA = """
Đầu vào : tuổi nguyên ∈ [0..150]; ngày nguyên ∈ [0..6] (0=Thứ Hai ... 6=Chủ Nhật)
Loại vé : tuổi [0,18) hoặc (60,150] -> Vé ưu đãi ; tuổi [18,60] -> Vé tiêu chuẩn
Loại ngày: ngày [0,4] -> Ngày thường ; ngày [5,6] -> Cuối tuần
Bảng giá : Ưu đãi 50.000đ (thường) / 70.000đ (cuối tuần)
           Tiêu chuẩn 80.000đ (thường) / 100.000đ (cuối tuần)
Đầu ra  : Invalid hoặc loại vé + loại ngày + giá
"""


def sut(tuoi, ngay):
    if not (0 <= tuoi <= 150) or not (0 <= ngay <= 6):
        return "Invalid"
    uu_dai = tuoi < 18 or tuoi > 60
    cuoi_tuan = ngay >= 5
    if uu_dai:
        return "Vé ưu đãi cuối tuần - 70.000đ" if cuoi_tuan else "Vé ưu đãi ngày thường - 50.000đ"
    return "Vé tiêu chuẩn cuối tuần - 100.000đ" if cuoi_tuan else "Vé tiêu chuẩn ngày thường - 80.000đ"


DIEU_KIEN = [
    ("C1", "Tuổi ∉ [0,150]",  lambda t, n: not (0 <= t <= 150)),
    ("C2", "Ngày ∉ [0,6]",    lambda t, n: not (0 <= n <= 6)),
    ("C3", "Tuổi ∈ [0,18)",   lambda t, n: 0 <= t < 18),
    ("C4", "Tuổi ∈ [18,60]",  lambda t, n: 18 <= t <= 60),
    ("C5", "Tuổi ∈ (60,150]", lambda t, n: 60 < t <= 150),
    ("C6", "Ngày ∈ [0,4]",    lambda t, n: 0 <= n <= 4),
    ("C7", "Ngày ∈ [5,6]",    lambda t, n: 5 <= n <= 6),
]
HANH_DONG = [("A1", "Invalid"), ("A2", "Ưu đãi ngày thường 50.000đ"),
             ("A3", "Ưu đãi cuối tuần 70.000đ"),
             ("A4", "Tiêu chuẩn ngày thường 80.000đ"),
             ("A5", "Tiêu chuẩn cuối tuần 100.000đ")]
LUAT = {
    "R1": ("T------", "A1"),
    "R2": ("FT-----", "A1"),
    "R3": ("FFTFFTF", "A2"),
    "R4": ("FFTFFFT", "A3"),
    "R5": ("FFFTFTF", "A4"),
    "R6": ("FFFTFFT", "A5"),
    "R7": ("FFFFTTF", "A2"),
    "R8": ("FFFFTFT", "A3"),
}

CASES = [
    ("TC01", "R1", (-1, 0),   "Invalid", "tuổi = -1, sát dưới biên 0"),
    # Bản gốc trong file: (151, 7) -> tuổi cũng ngoài miền nên khớp R1, không khớp R2.
    # Đã sửa tuổi về giá trị hợp lệ để test chỉ thuộc R2.
    ("TC02", "R2", (50, 7),   "Invalid", "ngày = 7, vượt biên 6; tuổi hợp lệ (đã sửa từ (151,7))"),
    ("TC03", "R3", (0, 4),    "Vé ưu đãi ngày thường - 50.000đ", "tuổi biên dưới 0; ngày biên trên của ngày thường 4"),
    ("TC04", "R4", (17, 5),   "Vé ưu đãi cuối tuần - 70.000đ",   "tuổi 17 sát dưới 18; ngày biên dưới cuối tuần 5"),
    ("TC05", "R5", (18, 0),   "Vé tiêu chuẩn ngày thường - 80.000đ", "tuổi đúng biên 18; ngày biên dưới 0"),
    ("TC06", "R6", (60, 6),   "Vé tiêu chuẩn cuối tuần - 100.000đ",  "tuổi đúng biên 60; ngày biên trên 6"),
    ("TC07", "R7", (61, 4),   "Vé ưu đãi ngày thường - 50.000đ", "tuổi 61 vừa qua 60; ngày 4"),
    ("TC08", "R8", (150, 5),  "Vé ưu đãi cuối tuần - 70.000đ",   "tuổi biên trên 150; ngày 5"),
]

if __name__ == "__main__":
    sys.exit(common.main(sys.modules[__name__], sys.argv[1:]))
