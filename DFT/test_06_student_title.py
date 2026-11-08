import unittest

from student_tilte import xet_danh_hieu_sinh_vien
from test_support import assert_cases


CASES = [
    ("TC1", (4.5, 85, 20, 0), "Invalid input"),
    ("TC2", (3.5, 85, 20, 2), "Không đạt danh hiệu"),
    ("TC3", (3.0, 85, 20, 0), "Không đạt danh hiệu"),
    ("TC4", (3.8, 95, 20, 0), "Sinh viên xuất sắc"),
    ("TC5", (3.4, 85, 20, 1), "Sinh viên giỏi"),
]


class TestStudentTitle(unittest.TestCase):
    def test_all_uses_cases(self):
        assert_cases(self, xet_danh_hieu_sinh_vien, CASES)


if __name__ == "__main__":
    unittest.main(verbosity=2)
