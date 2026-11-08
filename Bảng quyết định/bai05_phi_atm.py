# -*- coding: utf-8 -*-
"""Bài 5: Phí rút tiền tại cây ATM (withdraw, balance, atmCash)."""
import sys
import common

SO_BAI = 5
TEN = "Xác định phí dịch vụ khi rút tiền tại ATM"
DAC_TA = """
Đầu vào : withdraw (số tiền rút) ; balance (số dư) >= 0 ; atmCash ∈ [0 .. 50,000,000]
Đầu ra  : invalid | Số dư không đủ | Số tiền vượt mức trong ATM | Mức phí 1/2/3
Quy tắc :
  - withdraw <= 0 hoặc balance < 0 hoặc atmCash ∉ [0..50,000,000]  -> invalid
  - withdraw > balance                                              -> Số dư không đủ
  - withdraw > atmCash                                              -> Số tiền vượt mức trong ATM
  - (hợp lệ, đủ tiền) withdraw ∈ (0, 1,000,000)                    -> Mức phí 1
  - (hợp lệ, đủ tiền) withdraw ∈ [1,000,000, 10,000,000)           -> Mức phí 2
  - (hợp lệ, đủ tiền) withdraw >= 10,000,000                       -> Mức phí 3
Thứ tự ưu tiên: invalid -> thiếu số dư -> vượt tiền ATM -> mức phí.
Input theo thứ tự (withdraw, balance, atmCash).
"""


def sut(withdraw, balance, atm_cash):
    if withdraw <= 0 or balance < 0 or not (0 <= atm_cash <= 50_000_000):
        return "Invalid"
    if withdraw > balance:
        return "Số dư không đủ"
    if withdraw > atm_cash:
        return "Số tiền vượt mức trong ATM"
    if withdraw < 1_000_000:
        return "Mức phí 1"
    if withdraw < 10_000_000:
        return "Mức phí 2"
    return "Mức phí 3"


DIEU_KIEN = [
    ("C1", "withdraw ≤ 0",          lambda w, b, a: w <= 0),
    ("C2", "balance < 0",           lambda w, b, a: b < 0),
    ("C3", "atmCash ∉ [0;50M]",     lambda w, b, a: not (0 <= a <= 50_000_000)),
    ("C4", "withdraw > balance",    lambda w, b, a: w > b),
    ("C5", "withdraw > atmCash",    lambda w, b, a: w > a),
    ("C6", "withdraw ∈ (0;1M)",     lambda w, b, a: 0 < w < 1_000_000),
    ("C7", "withdraw ∈ [1M;10M)",   lambda w, b, a: 1_000_000 <= w < 10_000_000),
    ("C8", "withdraw ≥ 10M",        lambda w, b, a: w >= 10_000_000),
]
HANH_DONG = [("A1", "Invalid"), ("A2", "Số dư không đủ"),
             ("A3", "Vượt mức ATM"), ("A4", "Mức phí 1"),
             ("A5", "Mức phí 2"), ("A6", "Mức phí 3")]
LUAT = {
    "R1": ("T-------", "A1"),
    "R2": ("FT------", "A1"),
    "R3": ("FFT-----", "A1"),
    "R4": ("FFFT----", "A2"),
    "R5": ("FFFFT---", "A3"),
    "R6": ("FFFFFT--", "A4"),
    "R7": ("FFFFFFT-", "A5"),
    "R8": ("FFFFFFFT", "A6"),
}

CASES = [
    ("TC01", "R1", (0, 1_000_000, 50_000_000),           "Invalid", "withdraw = 0, đúng biên không hợp lệ"),
    ("TC02", "R2", (1, -1, 0),                           "Invalid", "balance = -1, sát dưới biên 0"),
    ("TC03", "R3", (1, 0, 50_000_001),                   "Invalid", "atmCash = 50,000,001, vượt biên trên 50,000,000"),
    ("TC04", "R4", (1_000_000, 999_999, 50_000_000),     "Số dư không đủ", "withdraw lớn hơn balance đúng 1 đơn vị"),
    ("TC05", "R5", (50_000_000, 50_000_000, 49_999_999), "Số tiền vượt mức trong ATM", "withdraw lớn hơn atmCash đúng 1; đủ số dư"),
    ("TC06", "R6", (999_999, 999_999, 999_999),          "Mức phí 1", "withdraw sát dưới 1,000,000; bằng balance và atmCash"),
    ("TC07", "R7", (1_000_000, 10_000_000, 50_000_000),  "Mức phí 2", "withdraw đúng biên 1,000,000"),
    ("TC08", "R8", (10_000_000, 10_000_000, 10_000_000), "Mức phí 3", "withdraw đúng biên 10,000,000"),
]

if __name__ == "__main__":
    sys.exit(common.main(sys.modules[__name__], sys.argv[1:]))
