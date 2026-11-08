import unittest

from QuangLinh_Tinh_phi_gui_xe import calculate_parking_fee
from test_support import assert_cases


INVALID = (-1, "KHONG_HOP_LE")

CASES = [
    ("TC01", (0, "XE_MAY", "NGOAI_TROI"), INVALID),
    ("TC02", (5, "XE_DAP", "NGOAI_TROI"), INVALID),
    ("TC03", (5, "XE_MAY", "TRONG_NHA"), INVALID),
    ("TC04", (5, "XE_MAY", "NGOAI_TROI"), (10000, "NGAN_HAN")),
    ("TC05", (12, "OTO", "CO_MAI"), (100000, "DAI_HAN")),
]


class TestParkingFee(unittest.TestCase):
    def test_all_uses_cases(self):
        assert_cases(self, calculate_parking_fee, CASES)


if __name__ == "__main__":
    unittest.main(verbosity=2)
