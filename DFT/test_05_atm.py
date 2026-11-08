import unittest

from atm import withdraw_money
from test_support import assert_cases


CASES = [
    ("TC1", (5000000, 10000000, 3000000), "Số tiền vượt mức trong ATM"),
    ("TC2", (500000, 2000000, 10000000), "Mức phí 1"),
    ("TC3", (5000000, 20000000, 30000000), "Mức phí 2"),
    ("TC4", (15000000, 30000000, 40000000), "Mức phí 3"),
]


class TestAtm(unittest.TestCase):
    def test_all_uses_cases(self):
        assert_cases(self, withdraw_money, CASES)


if __name__ == "__main__":
    unittest.main(verbosity=2)
