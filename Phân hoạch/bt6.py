# test_student_title.py
import pytest
from student_title import classify_student

INVALID = "Invalid input"
NONE = "Không đạt danh hiệu nào"
GOOD = "Sinh viên giỏi"
EXCELLENT = "Sinh viên xuất sắc"


@pytest.mark.parametrize(
    "tcid, ec, dht, drl, expected",
    [
        ("TC1", "EC1", 4.50, 50, INVALID),     # dht out of range
        ("TC2", "EC2", 2.50, 60, NONE),        # below both thresholds
        ("TC3", "EC3", 3.40, 85, GOOD),        # giỏi / giỏi
        ("TC4", "EC4", 3.80, 95, EXCELLENT),   # xuất sắc / xuất sắc
        ("TC5", "EC5", 3.40, 95, GOOD),        # ASSUMPTION: lower band wins
        ("TC6", "EC6", 3.80, 85, GOOD),        # ASSUMPTION: lower band wins
    ],
)
def test_student_title(tcid, ec, dht, drl, expected):
    actual = classify_student(dht, drl)
    assert actual == expected, f"{tcid} ({ec}): dht={dht}, drl={drl} -> {actual!r}, expected {expected!r}"