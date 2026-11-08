import unittest

from Khai_PhanLoaiSucKhoe import classify_health
from test_support import assert_cases


CASES = [
    ("TC01", (30, 98), "Invalid"),
    ("TC02", (80, 88), "Nguy hiểm"),
    ("TC03", (110, 98), "Cảnh báo"),
    ("TC04", (80, 98), "Bình thường"),
]


class TestHealthClassification(unittest.TestCase):
    def test_all_uses_cases(self):
        assert_cases(self, classify_health, CASES)


if __name__ == "__main__":
    unittest.main(verbosity=2)
