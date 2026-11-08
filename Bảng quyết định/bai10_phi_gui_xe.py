# -*- coding: utf-8 -*-
"""Bài 10: Tính phí gửi xe (hours, vehicle_type, parking_area)."""
import sys
import common

SO_BAI = 10
TEN = "Tính phí gửi xe theo số giờ, loại xe, khu vực đỗ"
DAC_TA = """
Đầu vào : hours nguyên ∈ [1..24] ; vehicle_type ∈ {XE_MAY, OTO} ;
          parking_area ∈ {NGOAI_TROI, CO_MAI}
Đầu ra  : (parking_fee, parking_type)
Quy tắc :
  - hours ∉ [1..24] hoặc vehicle_type, parking_area ngoài tập cho phép -> (-1, KHONG_HOP_LE)
  hours ∈ [1..9) -> NGAN_HAN:
      XE_MAY: NGOAI_TROI 10.000 | CO_MAI 15.000
      OTO   : NGOAI_TROI 40.000 | CO_MAI 55.000
  hours ∈ [9..24] -> DAI_HAN:
      XE_MAY: NGOAI_TROI 20.000 | CO_MAI 30.000
      OTO   : NGOAI_TROI 80.000 | CO_MAI 100.000
"""


def sut(hours, vehicle_type, parking_area):
    err = (-1, "KHONG_HOP_LE")
    if not (1 <= hours <= 24):
        return err
    if vehicle_type not in ("XE_MAY", "OTO"):
        return err
    if parking_area not in ("NGOAI_TROI", "CO_MAI"):
        return err

    ngan_han = hours < 9
    bang = {
        (True, "XE_MAY", "NGOAI_TROI"): 10_000,
        (True, "XE_MAY", "CO_MAI"): 15_000,
        (True, "OTO", "NGOAI_TROI"): 40_000,
        (True, "OTO", "CO_MAI"): 55_000,
        (False, "XE_MAY", "NGOAI_TROI"): 20_000,
        (False, "XE_MAY", "CO_MAI"): 30_000,
        (False, "OTO", "NGOAI_TROI"): 80_000,
        (False, "OTO", "CO_MAI"): 100_000,
    }
    fee = bang[(ngan_han, vehicle_type, parking_area)]
    return (fee, "NGAN_HAN" if ngan_han else "DAI_HAN")


DIEU_KIEN = [
    ("C1",  "hours < 1",                      lambda h, v, a: h < 1),
    ("C2",  "hours > 24",                     lambda h, v, a: h > 24),
    ("C3",  "vehicle_type ∉ {XE_MAY, OTO}",   lambda h, v, a: v not in ("XE_MAY", "OTO")),
    ("C4",  "parking_area ∉ {NGOAI_TROI,CO_MAI}", lambda h, v, a: a not in ("NGOAI_TROI", "CO_MAI")),
    ("C5",  "hours ∈ [1..9)",                 lambda h, v, a: 1 <= h < 9),
    ("C6",  "hours ∈ [9..24]",                lambda h, v, a: 9 <= h <= 24),
    ("C7",  "vehicle_type = XE_MAY",          lambda h, v, a: v == "XE_MAY"),
    ("C8",  "vehicle_type = OTO",             lambda h, v, a: v == "OTO"),
    ("C9",  "parking_area = NGOAI_TROI",      lambda h, v, a: a == "NGOAI_TROI"),
    ("C10", "parking_area = CO_MAI",          lambda h, v, a: a == "CO_MAI"),
]
HANH_DONG = [("A0", "(-1, KHONG_HOP_LE)"),
             ("A1", "(10.000, NGAN_HAN)"), ("A2", "(15.000, NGAN_HAN)"),
             ("A3", "(40.000, NGAN_HAN)"), ("A4", "(55.000, NGAN_HAN)"),
             ("A5", "(20.000, DAI_HAN)"),  ("A6", "(30.000, DAI_HAN)"),
             ("A7", "(80.000, DAI_HAN)"),  ("A8", "(100.000, DAI_HAN)")]
LUAT = {
    "R1":  ("T---------", "A0"),
    "R2":  ("FT--------", "A0"),
    "R3":  ("FFT-------", "A0"),
    "R4":  ("FFFT------", "A0"),
    "R5":  ("FFFFTFTFTF", "A1"),
    "R6":  ("FFFFTFTFFT", "A2"),
    "R7":  ("FFFFTFFTTF", "A3"),
    "R8":  ("FFFFTFFTFT", "A4"),
    "R9":  ("FFFFFTTFTF", "A5"),
    "R10": ("FFFFFTTFFT", "A6"),
    "R11": ("FFFFFTFTTF", "A7"),
    "R12": ("FFFFFTFTFT", "A8"),
}

LOI = (-1, "KHONG_HOP_LE")
CASES = [
    ("TC01", "R1",  (0, "XE_MAY", "NGOAI_TROI"),   LOI, "hours = 0, sát dưới biên 1"),
    ("TC02", "R2",  (25, "XE_MAY", "NGOAI_TROI"),  LOI, "hours = 25, vượt biên 24"),
    ("TC03", "R3",  (12, "XE_DAP", "NGOAI_TROI"),  LOI, "vehicle_type không thuộc {XE_MAY, OTO}"),
    ("TC04", "R4",  (12, "XE_MAY", "NHA_XE"),      LOI, "parking_area không thuộc {NGOAI_TROI, CO_MAI}"),
    ("TC05", "R5",  (1, "XE_MAY", "NGOAI_TROI"),   (10_000, "NGAN_HAN"),  "hours biên dưới 1"),
    ("TC06", "R6",  (8, "XE_MAY", "CO_MAI"),       (15_000, "NGAN_HAN"),  "hours = 8, sát dưới biên 9"),
    ("TC07", "R7",  (1, "OTO", "NGOAI_TROI"),      (40_000, "NGAN_HAN"),  "hours biên dưới 1; ô tô"),
    ("TC08", "R8",  (8, "OTO", "CO_MAI"),          (55_000, "NGAN_HAN"),  "hours = 8; ô tô có mái"),
    ("TC09", "R9",  (9, "XE_MAY", "NGOAI_TROI"),   (20_000, "DAI_HAN"),   "hours đúng biên 9 (vào dài hạn)"),
    ("TC10", "R10", (24, "XE_MAY", "CO_MAI"),      (30_000, "DAI_HAN"),   "hours biên trên 24"),
    ("TC11", "R11", (9, "OTO", "NGOAI_TROI"),      (80_000, "DAI_HAN"),   "hours đúng biên 9; ô tô ngoài trời"),
    ("TC12", "R12", (24, "OTO", "CO_MAI"),         (100_000, "DAI_HAN"),  "hours biên trên 24; ô tô có mái"),
]

if __name__ == "__main__":
    sys.exit(common.main(sys.modules[__name__], sys.argv[1:]))
