import unittest

from QuangLinh_Tinh_phi_giao_hang import calculate_delivery_fee
from test_support import assert_cases


INVALID = (-1, "KHONG_HOP_LE", "ERROR")

CASES = [
    ("TC01", (10.5, 2.0, "NOI_THANH"), INVALID),
    ("TC02", (10, "abc", "NOI_THANH"), INVALID),
    ("TC03", (101, 2.0, "NOI_THANH"), INVALID),
    ("TC04", (10, 25.0, "NOI_THANH"), INVALID),
    ("TC05", (10, 2.0, "TINH_KHAC"), INVALID),
    ("TC06", (10, 2.0, "NGOAI_THANH"), (60000, "TIEU_CHUAN", "OK")),
    ("TC07", (60, 10.0, "NOI_THANH"), (100000, "HANG_NANG", "OK")),
]


class TestDeliveryCalculation(unittest.TestCase):
    def test_all_uses_cases(self):
        assert_cases(self, calculate_delivery_fee, CASES)


if __name__ == "__main__":
    unittest.main(verbosity=2)
