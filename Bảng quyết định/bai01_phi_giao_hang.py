# -*- coding: utf-8 -*-
"""Bài 1: Tính phí giao hàng (price, distance, member)."""
import sys
import common

SO_BAI = 1
TEN = "Tính phí giao hàng theo giá đơn, khoảng cách, loại khách hàng"
DAC_TA = """
Đầu vào : price >= 0 (nghìn đồng); distance ∈ [0 .. 30] (km); member ∈ {VIP, NORMAL}
Đầu ra  : Invalid | Freeship | 10.000đ | 20.000đ | 30.000đ
Quy tắc :
  - price < 0 hoặc distance ∉ [0..30] hoặc member ∉ {VIP, NORMAL}  -> Invalid
  - price >= 500,000 (hợp lệ)                                      -> Freeship
  - price < 500,000, distance ∈ [0..10],  VIP     -> 10.000đ
  - price < 500,000, distance ∈ [0..10],  NORMAL  -> 20.000đ
  - price < 500,000, distance ∈ (10..30], VIP     -> 20.000đ
  - price < 500,000, distance ∈ (10..30], NORMAL  -> 30.000đ
"""


# ------------------------------------------------------------ code cần test
def sut(price, distance, member):
    if price < 0 or not (0 <= distance <= 30) or member not in ("VIP", "NORMAL"):
        return "Invalid"
    if price >= 500000:
        return "Freeship"
    if distance <= 10:
        return "10.000đ" if member == "VIP" else "20.000đ"
    return "20.000đ" if member == "VIP" else "30.000đ"


# ------------------------------------------------------------ bảng quyết định
DIEU_KIEN = [
    ("C1", "price < 0",                lambda p, d, m: p < 0),
    ("C2", "distance ∉ [0..30]",       lambda p, d, m: not (0 <= d <= 30)),
    ("C3", "member ∉ [VIP; NORMAL]",   lambda p, d, m: m not in ("VIP", "NORMAL")),
    ("C4", "price ≥ 500,000",          lambda p, d, m: p >= 500000),
    ("C5", "distance ∈ [0..10]",       lambda p, d, m: 0 <= d <= 10),
    ("C6", "distance ∈ (10..30]",      lambda p, d, m: 10 < d <= 30),
    ("C7", "member = VIP",             lambda p, d, m: m == "VIP"),
    ("C8", "member = NORMAL",          lambda p, d, m: m == "NORMAL"),
]
HANH_DONG = [("A1", "Invalid"), ("A2", "Freeship"), ("A3", "10.000đ"),
             ("A4", "20.000đ"), ("A5", "30.000đ")]
LUAT = {
    "R1": ("T-------", "A1"),
    "R2": ("FT------", "A1"),
    "R3": ("FFT-----", "A1"),
    "R4": ("FFFT----", "A2"),
    "R5": ("FFFFTFTF", "A3"),
    "R6": ("FFFFTFFT", "A4"),
    "R7": ("FFFFFTTF", "A4"),
    "R8": ("FFFFFTFT", "A5"),
}

# ------------------------------------------------------------ test case
CASES = [
    ("TC01", "R1", (-0.001, 15.00, "VIP"),    "Invalid",  "price âm ngay sát 0 (biên dưới của price)"),
    ("TC02", "R2", (100000, 30.01, "VIP"),    "Invalid",  "distance vượt biên trên 30 một chút"),
    ("TC03", "R3", (100000, 10.00, "GOLD"),   "Invalid",  "member không thuộc {VIP, NORMAL}"),
    ("TC04", "R4", (500000, 30.00, "NORMAL"), "Freeship", "price đúng biên 500,000 và distance đúng biên 30"),
    ("TC05", "R5", (499999, 0.00, "VIP"),     "10.000đ",  "price sát dưới 500,000; distance biên dưới 0; VIP"),
    ("TC06", "R6", (0, 10.00, "NORMAL"),      "20.000đ",  "price biên dưới 0; distance biên trên của nhóm gần = 10"),
    ("TC07", "R7", (499999, 10.01, "VIP"),    "20.000đ",  "distance vừa qua 10 (vào nhóm xa); VIP"),
    ("TC08", "R8", (499999, 30.00, "NORMAL"), "30.000đ",  "distance biên trên 30; NORMAL"),
]

if __name__ == "__main__":
    sys.exit(common.main(sys.modules[__name__], sys.argv[1:]))
