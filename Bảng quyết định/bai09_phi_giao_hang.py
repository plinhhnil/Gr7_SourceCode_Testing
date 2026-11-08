# -*- coding: utf-8 -*-
"""Bài 9: Tính phí giao hàng (distance, weight, delivery_area)."""
import sys
import common

SO_BAI = 9
TEN = "Tính phí giao hàng theo khoảng cách, cân nặng, khu vực"
DAC_TA = """
Đầu vào : distance nguyên ∈ [1..100] (km) ;
          weight thực ∈ [0.1 .. 20.0] (kg), phải là bội của 0.1 (weight % 0.1 = 0) ;
          delivery_area ∈ {NOI_THANH, NGOAI_THANH}
Đầu ra  : (delivery_fee, service_type, message)
Quy tắc :
  - vi phạm bất kỳ điều kiện hợp lệ nào  -> (-1, KHONG_HOP_LE, ERROR)
  distance ∈ [1..51) (tức 1..50):
      weight ∈ [0.1..5.1): NOI_THANH (50.000, TIEU_CHUAN, OK) | NGOAI_THANH (60.000, TIEU_CHUAN, OK)
      weight ∈ [5.1..20.0]: NOI_THANH (70.000, HANG_NANG, OK) | NGOAI_THANH (80.000, HANG_NANG, OK)
  distance ∈ [51..100]:
      weight ∈ [0.1..5.1): NOI_THANH (80.000, TIEU_CHUAN, OK) | NGOAI_THANH (90.000, TIEU_CHUAN, OK)
      weight ∈ [5.1..20.0]: NOI_THANH (100.000, HANG_NANG, OK) | NGOAI_THANH (120.000, HANG_NANG, OK)
"""

EPS = 1e-9


def sut(distance, weight, delivery_area):
    err = (-1, "KHONG_HOP_LE", "ERROR")
    if not (1 <= distance <= 100):
        return err
    w10 = round(weight * 10)                    # đổi sang số bước 0.1, tránh sai số float
    if abs(weight * 10 - w10) > 1e-6:           # weight % 0.1 != 0
        return err
    if not (1 <= w10 <= 200):                   # [0.1 .. 20.0]
        return err
    if delivery_area not in ("NOI_THANH", "NGOAI_THANH"):
        return err

    noi = delivery_area == "NOI_THANH"
    gan = distance <= 50                        # distance ∈ [1..51)
    nhe = w10 < 51                              # weight ∈ [0.1..5.1)
    bang = {
        (True, True, True): (50_000, "TIEU_CHUAN"),
        (True, True, False): (60_000, "TIEU_CHUAN"),
        (True, False, True): (70_000, "HANG_NANG"),
        (True, False, False): (80_000, "HANG_NANG"),
        (False, True, True): (80_000, "TIEU_CHUAN"),
        (False, True, False): (90_000, "TIEU_CHUAN"),
        (False, False, True): (100_000, "HANG_NANG"),
        (False, False, False): (120_000, "HANG_NANG"),
    }
    fee, svc = bang[(gan, nhe, noi)]
    return (fee, svc, "OK")


DIEU_KIEN = [
    ("C1",  "distance < 1",                lambda d, w, a: d < 1),
    ("C2",  "distance > 100",              lambda d, w, a: d > 100),
    ("C3",  "weight < 0.1",                lambda d, w, a: w < 0.1 - EPS),
    ("C4",  "weight > 20.0",               lambda d, w, a: w > 20.0 + EPS),
    ("C5",  "weight % 0.1 != 0",           lambda d, w, a: abs(w * 10 - round(w * 10)) > 1e-6),
    ("C6",  "delivery_area ∉ {NOI,NGOAI}", lambda d, w, a: a not in ("NOI_THANH", "NGOAI_THANH")),
    ("C7",  "distance ∈ [1..51)",          lambda d, w, a: 1 <= d < 51),
    ("C8",  "distance ∈ [51..100]",        lambda d, w, a: 51 <= d <= 100),
    ("C9",  "weight ∈ [0.1..5.1)",         lambda d, w, a: 0.1 - EPS <= w < 5.1 - EPS),
    ("C10", "weight ∈ [5.1..20.0]",        lambda d, w, a: 5.1 - EPS <= w <= 20.0 + EPS),
    ("C11", "area = NOI_THANH",            lambda d, w, a: a == "NOI_THANH"),
    ("C12", "area = NGOAI_THANH",          lambda d, w, a: a == "NGOAI_THANH"),
]
HANH_DONG = [("A0", "(-1, KHONG_HOP_LE, ERROR)"),
             ("A1", "(50.000, TIEU_CHUAN, OK)"), ("A2", "(60.000, TIEU_CHUAN, OK)"),
             ("A3", "(70.000, HANG_NANG, OK)"),  ("A4", "(80.000, HANG_NANG, OK)"),
             ("A5", "(80.000, TIEU_CHUAN, OK)"), ("A6", "(90.000, TIEU_CHUAN, OK)"),
             ("A7", "(100.000, HANG_NANG, OK)"), ("A8", "(120.000, HANG_NANG, OK)")]
LUAT = {
    "R1":  ("T-----------", "A0"),
    "R2":  ("FT----------", "A0"),
    "R3":  ("FFT---------", "A0"),
    "R4":  ("FFFT--------", "A0"),
    "R5":  ("FFFFT-------", "A0"),
    "R6":  ("FFFFFT------", "A0"),
    "R7":  ("FFFFFFTFTFTF", "A1"),
    "R8":  ("FFFFFFTFTFFT", "A2"),
    "R9":  ("FFFFFFTFFTTF", "A3"),
    "R10": ("FFFFFFTFFTFT", "A4"),
    "R11": ("FFFFFFFTTFTF", "A5"),
    "R12": ("FFFFFFFTTFFT", "A6"),
    "R13": ("FFFFFFFTFTTF", "A7"),
    "R14": ("FFFFFFFTFTFT", "A8"),
}

LOI = (-1, "KHONG_HOP_LE", "ERROR")
CASES = [
    ("TC01", "R1",  (0, 10.0, "NOI_THANH"),    LOI, "distance = 0, sát dưới biên 1"),
    ("TC02", "R2",  (101, 10.0, "NOI_THANH"),  LOI, "distance = 101, vượt biên 100"),
    ("TC03", "R3",  (50, 0.0, "NOI_THANH"),    LOI, "weight = 0.0, dưới biên 0.1"),
    ("TC04", "R4",  (50, 20.1, "NOI_THANH"),   LOI, "weight = 20.1, vượt biên 20.0"),
    ("TC05", "R5",  (50, 0.15, "NOI_THANH"),   LOI, "weight nằm trong miền nhưng không là bội của 0.1"),
    ("TC06", "R6",  (50, 10.0, "HA_NOI"),      LOI, "delivery_area không thuộc {NOI_THANH, NGOAI_THANH}"),
    ("TC07", "R7",  (1, 0.1, "NOI_THANH"),     (50_000, "TIEU_CHUAN", "OK"),  "distance, weight đều biên dưới"),
    ("TC08", "R8",  (50, 5.0, "NGOAI_THANH"),  (60_000, "TIEU_CHUAN", "OK"),  "distance biên trên nhóm gần 50; weight sát dưới 5.1"),
    ("TC09", "R9",  (50, 5.1, "NOI_THANH"),    (70_000, "HANG_NANG", "OK"),   "weight đúng biên 5.1 (vào nhóm nặng)"),
    ("TC10", "R10", (1, 20.0, "NGOAI_THANH"),  (80_000, "HANG_NANG", "OK"),   "weight biên trên 20.0; distance biên dưới"),
    ("TC11", "R11", (51, 0.1, "NOI_THANH"),    (80_000, "TIEU_CHUAN", "OK"),  "distance đúng biên 51 (vào nhóm xa)"),
    ("TC12", "R12", (100, 5.0, "NGOAI_THANH"), (90_000, "TIEU_CHUAN", "OK"),  "distance biên trên 100; weight sát dưới 5.1"),
    ("TC13", "R13", (51, 20.0, "NOI_THANH"),   (100_000, "HANG_NANG", "OK"),  "distance 51; weight biên trên 20.0"),
    ("TC14", "R14", (100, 5.1, "NGOAI_THANH"), (120_000, "HANG_NANG", "OK"),  "distance 100; weight đúng biên 5.1"),
]

if __name__ == "__main__":
    sys.exit(common.main(sys.modules[__name__], sys.argv[1:]))
