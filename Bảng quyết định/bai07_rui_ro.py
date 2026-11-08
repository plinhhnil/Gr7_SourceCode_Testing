# -*- coding: utf-8 -*-
"""Bài 7: Đánh giá rủi ro gói vay (credit_score, term)."""
import sys
import common

SO_BAI = 7
TEN = "Đánh giá mức độ rủi ro của gói vay tiêu dùng cá nhân"
DAC_TA = """
Đầu vào : credit_score nguyên ∈ [300; 850] ; term (kỳ hạn vay) nguyên ∈ [6; 60]
Đầu ra  : Invalid | Low Risk | High Risk
Quy tắc :
  - credit_score ∉ [300;850] hoặc term ∉ [6;60]                          -> Invalid
  - credit_score ∈ [300;580) hoặc (credit_score ∈ [580;700) và term ∈ [24;60]) -> High Risk
  - (credit_score ∈ [580;700) và term ∈ [6;24)) hoặc credit_score ∈ [700;850]  -> Low Risk
Giả định: đề gốc ghi Low Risk là term ∈ [6;24] nên term = 24 trùng cả hai nhóm.
          Theo bảng quyết định, term = 24 thuộc High Risk, Low Risk dùng [6;24).
"""


def sut(credit_score, term):
    if not (300 <= credit_score <= 850) or not (6 <= term <= 60):
        return "Invalid"
    if credit_score < 580:
        return "High Risk"
    if credit_score < 700:
        return "High Risk" if term >= 24 else "Low Risk"
    return "Low Risk"


# Lưu ý: ở bài này C1, C2 là điều kiện HỢP LỆ (T = hợp lệ), đúng như bảng gốc.
DIEU_KIEN = [
    ("C1", "credit_score ∈ [300;850]", lambda c, t: 300 <= c <= 850),
    ("C2", "term ∈ [6;60]",            lambda c, t: 6 <= t <= 60),
    ("C3", "credit_score ∈ [300;580)", lambda c, t: 300 <= c < 580),
    ("C4", "credit_score ∈ [580;700)", lambda c, t: 580 <= c < 700),
    ("C5", "credit_score ∈ [700;850]", lambda c, t: 700 <= c <= 850),
    ("C6", "term ∈ [6;24)",            lambda c, t: 6 <= t < 24),
    ("C7", "term ∈ [24;60]",           lambda c, t: 24 <= t <= 60),
]
HANH_DONG = [("A1", "Invalid"), ("A2", "High Risk"), ("A3", "Low Risk")]
LUAT = {
    "R1": ("F------", "A1"),
    "R2": ("TF-----", "A1"),
    "R3": ("TTTFF--", "A2"),
    "R4": ("TTFTFFT", "A2"),
    "R5": ("TTFTFTF", "A3"),
    "R6": ("TTFFT--", "A3"),
}

CASES = [
    ("TC01", "R1", (299, 6),   "Invalid",   "credit_score = 299, sát dưới biên 300"),
    ("TC02", "R2", (300, 61),  "Invalid",   "term = 61, vượt biên 60; credit_score đúng biên 300"),
    ("TC03", "R3", (579, 60),  "High Risk", "credit_score sát dưới 580; term biên trên 60"),
    ("TC04", "R4", (580, 24),  "High Risk", "credit_score đúng biên 580; term đúng biên 24"),
    ("TC05", "R5", (699, 23),  "Low Risk",  "credit_score sát dưới 700; term sát dưới 24"),
    ("TC06", "R6", (700, 6),   "Low Risk",  "credit_score đúng biên 700; term biên dưới 6"),
]

if __name__ == "__main__":
    sys.exit(common.main(sys.modules[__name__], sys.argv[1:]))
