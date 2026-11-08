# -*- coding: utf-8 -*-
"""Bài 2: Xét duyệt khoản vay (income, credit, loan)."""
import sys
import common

SO_BAI = 2
TEN = "Xét duyệt khoản vay theo thu nhập, điểm tín dụng, nợ xấu"
DAC_TA = """
Đầu vào : income >= 0 (triệu đồng); credit >= 0; loan ∈ {'TRUE', 'FALSE'} (có nợ xấu)
Đầu ra  : Invalid | Duyệt khoản vay | Từ chối - có nợ xấu |
          Từ chối - điểm tín dụng thấp | Từ chối - hồ sơ xấu | Yêu cầu bổ sung hồ sơ
Quy tắc :
  - income < 0 hoặc credit < 0 hoặc loan ∉ {TRUE, FALSE}   -> Invalid
  - income >= 10, credit >= 200, loan = FALSE               -> Duyệt khoản vay
  - income >= 0,  credit >= 200, loan = TRUE                -> Từ chối - có nợ xấu
  - income >= 0,  credit < 200,  loan = FALSE               -> Từ chối - điểm tín dụng thấp
  - income >= 0,  credit < 200,  loan = TRUE                -> Từ chối - hồ sơ xấu
  - income < 10,  credit >= 200, loan = FALSE               -> Yêu cầu bổ sung hồ sơ
"""


def sut(income, credit, loan):
    if income < 0 or credit < 0 or loan not in ("TRUE", "FALSE"):
        return "Invalid"
    if credit >= 200:
        if loan == "TRUE":
            return "Từ chối khoản vay - có nợ xấu"
        return "Duyệt khoản vay" if income >= 10 else "Yêu cầu bổ sung hồ sơ"
    if loan == "TRUE":
        return "Từ chối khoản vay - hồ sơ xấu"
    return "Từ chối khoản vay - điểm tín dụng thấp"


DIEU_KIEN = [
    ("C1", "income < 0",              lambda i, c, l: i < 0),
    ("C2", "credit < 0",              lambda i, c, l: c < 0),
    ("C3", "loan ∉ ['TRUE';'FALSE']", lambda i, c, l: l not in ("TRUE", "FALSE")),
    ("C4", "loan = 'TRUE'",           lambda i, c, l: l == "TRUE"),
    ("C5", "credit < 200",            lambda i, c, l: c < 200),
    ("C6", "income ≥ 10",             lambda i, c, l: i >= 10),
]
HANH_DONG = [("A1", "Invalid"), ("A2", "Duyệt khoản vay"),
             ("A3", "Từ chối - có nợ xấu"), ("A4", "Từ chối - điểm tín dụng thấp"),
             ("A5", "Từ chối - hồ sơ xấu"), ("A6", "Yêu cầu bổ sung hồ sơ")]
LUAT = {
    "R1": ("T-----", "A1"),
    "R2": ("FT----", "A1"),
    "R3": ("FFT---", "A1"),
    "R4": ("FFFTF-", "A3"),
    "R5": ("FFFTT-", "A5"),
    "R6": ("FFFFT-", "A4"),
    "R7": ("FFFFFT", "A2"),
    "R8": ("FFFFFF", "A6"),
}

CASES = [
    ("TC01", "R1", (-0.01, 200, "FALSE"), "Invalid", "income âm sát 0"),
    ("TC02", "R2", (10.00, -1, "TRUE"),   "Invalid", "credit = -1, sát biên dưới 0"),
    ("TC03", "R3", (0.00, 0, "MAYBE"),    "Invalid", "loan không thuộc {TRUE, FALSE}; income, credit đúng biên dưới 0"),
    ("TC04", "R4", (0.00, 200, "TRUE"),   "Từ chối khoản vay - có nợ xấu", "credit đúng biên 200 (>=200), có nợ xấu"),
    ("TC05", "R5", (10.00, 199, "TRUE"),  "Từ chối khoản vay - hồ sơ xấu", "credit 199 (sát dưới 200) và có nợ xấu"),
    ("TC06", "R6", (9.99, 0, "FALSE"),    "Từ chối khoản vay - điểm tín dụng thấp", "credit thấp, không nợ xấu"),
    ("TC07", "R7", (10.00, 200, "FALSE"), "Duyệt khoản vay", "income đúng biên 10, credit đúng biên 200"),
    ("TC08", "R8", (9.99, 200, "FALSE"),  "Yêu cầu bổ sung hồ sơ", "income 9.99 sát dưới 10, credit đúng biên 200"),
]

if __name__ == "__main__":
    sys.exit(common.main(sys.modules[__name__], sys.argv[1:]))
