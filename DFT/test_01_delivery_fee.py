import unittest

from deliveryFee import deliveryFee
from test_support import assert_cases


CASES = [
    ("TC01", (-1, 5.0, "VIP"), "Invalid"),
    ("TC02", (600000, 5.0, "VIP"), "Freeship"),
    ("TC03", (100000, 5.0, "VIP"), "10.000đ"),
    ("TC04", (100000, 20.0, "VIP"), "20.000đ"),
    ("TC05", (100000, 5.0, "NORMAL"), "20.000đ"),
    ("TC06", (100000, 20.0, "NORMAL"), "30.000đ"),
]


class TestDeliveryFee(unittest.TestCase):
    def test_all_uses_cases(self):
        assert_cases(self, deliveryFee, CASES)


if __name__ == "__main__":
    unittest.main(verbosity=2)
