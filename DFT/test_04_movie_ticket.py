import unittest

from Khai_PhanLoaiVe import classify_ticket
from test_support import assert_cases


CASES = [
    ("TC01", (-5, 2), "Invalid"),
    ("TC02", (10, 2), "Ve uu dai ngay thuong - 50000d"),
    ("TC03", (70, 5), "Ve uu dai cuoi tuan - 70000d"),
    ("TC04", (30, 0), "Ve tieu chuan ngay thuong - 80000d"),
    ("TC05", (30, 6), "Ve tieu chuan cuoi tuan - 100000d"),
]


class TestMovieTicket(unittest.TestCase):
    def test_all_uses_cases(self):
        assert_cases(self, classify_ticket, CASES)


if __name__ == "__main__":
    unittest.main(verbosity=2)
