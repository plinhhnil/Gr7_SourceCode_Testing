# test_booking.py
import pytest
from booking import check_booking


@pytest.mark.parametrize(
    "tcid, age, slot, expected",
    [
        ("TC1", 150, 3, "Invalid"),                      # EC1
        ("TC2", 3,   7, "Không đủ tuổi xem phim"),       # EC2
        ("TC3", 12,  4, "Vé trẻ em"),                    # EC3
        ("TC4", 45,  8, "Vé người lớn"),                 # EC4
    ],
)
def test_check_booking(tcid, age, slot, expected):
    actual = check_booking(age, slot)
    assert actual == expected, (
        f"{tcid}: check_booking({age}, {slot}) returned {actual!r}, "
        f"expected {expected!r}"
    )