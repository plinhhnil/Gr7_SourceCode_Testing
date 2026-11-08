
import pytest

from atm import withdraw_money


# Test cases generated using Output-Based
# Equivalence Partitioning (EP)
#
# Format:
# (TCID, EC_ID, withdraw, balance, atmCash, expected_output)

test_cases = [
    # EC1: Invalid
    ("TC01", "EC1", 0, 2_000_000, 3_000_000, "invalid"),

    # EC2: Insufficient balance
    ("TC02", "EC2", 2_000_000, 1_000_000, 3_000_000,
     "Số dư không đủ"),

    # EC3: Insufficient ATM cash
    ("TC03", "EC3", 2_000_000, 3_000_000, 1_000_000,
     "Số tiền vượt mức trong ATM"),

    # EC4: Fee level 1
    ("TC04", "EC4", 500_000, 2_000_000, 3_000_000,
     "Mức phí 1"),

    # EC5: Fee level 2
    ("TC05", "EC5", 3_000_000, 5_000_000, 4_000_000,
     "Mức phí 2"),

    # EC6: Fee level 3
    ("TC06", "EC6", 12_000_000, 15_000_000, 20_000_000,
     "Mức phí 3"),
]


@pytest.mark.parametrize(
    "tcid, ec_id, withdraw, balance, atmCash, expected",
    test_cases
)
def test_withdraw_money(
    tcid, ec_id, withdraw, balance, atmCash, expected
):
    actual = withdraw_money(withdraw, balance, atmCash)

    assert actual == expected, (
        f"\nTest Case: {tcid}"
        f"\nEquivalence Class: {ec_id}"
        f"\nInput: withdraw={withdraw}, "
        f"balance={balance}, atmCash={atmCash}"
        f"\nExpected: {expected}"
        f"\nActual: {actual}"
    )
