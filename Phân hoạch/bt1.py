# test_weekly_salary.py
import pytest

# Điều chỉnh tên module/hàm cho khớp với cài đặt của bạn.
from weekly_salary import calculate_weekly_salary


# (TCID, EC, hours, salary, expected_output)
TEST_CASES = [
    # TC1 - EC1: hours > 60 -> Invalid
    ("TC1", "EC1", 72.35, 85.00, "Invalid"),

    # TC2 - EC2: hours in [0, 40], salary in [30, 200]
    ("TC2", "EC2", 26.50, 94.50, "Lương bình thường"),

    # TC3 - EC3: hours in (40, 60], salary in [30, 200]
    ("TC3", "EC3", 52.40, 161.00, "Lương tăng ca"),
]


@pytest.mark.parametrize(
    "tcid, ec_id, hours, salary, expected",
    TEST_CASES,
    ids=[tc[0] for tc in TEST_CASES],
)
def test_calculate_weekly_salary(tcid, ec_id, hours, salary, expected):
    actual = calculate_weekly_salary(hours, salary)

    assert actual == expected, (
        f"{tcid} [{ec_id}] hours={hours}, salary={salary}: "
        f"expected {expected!r}, got {actual!r}"
    )