import unittest

from homeCredit import homeCredit
from test_support import assert_cases


CASES = [
    ("TC01", (-1, 300, "FALSE"), "Invalid"),
    (
        "TC02",
        (5, 100, "TRUE"),
        "Từ chối khoản vay - hồ sơ xấu",
    ),
    (
        "TC03",
        (5, 100, "FALSE"),
        "Từ chối khoản vay - điểm tín dụng thấp",
    ),
    (
        "TC04",
        (20, 300, "TRUE"),
        "Từ chối khoản vay - có nợ xấu",
    ),
    ("TC05", (20, 300, "FALSE"), "Duyệt khoản vay"),
    ("TC06", (5, 300, "FALSE"), "Yêu cầu bổ sung hồ sơ"),
]


class TestHomeCredit(unittest.TestCase):
    def test_all_uses_cases(self):
        assert_cases(self, homeCredit, CASES)


if __name__ == "__main__":
    unittest.main(verbosity=2)
