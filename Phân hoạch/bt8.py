# test_reward_classifier.py
import pytest

from reward_classifier import phan_loai_khen_thuong


@pytest.mark.parametrize(
    "tcid, kpi, td, thang, expected",
    [
        ("TC1", 105.5, 85, 8,  "Invalid"),     # EC1: kpi > 100.0
        ("TC2", 62.3,  91, 9,  "Khong"),       # EC2: kpi < 75.0
        ("TC3", 82.7,  88, 10, "Tieu chuan"),  # EC3: kpi in [75, 90)
        ("TC4", 95.4,  93, 7,  "Xuat sac"),    # EC4: kpi in [90, 100]
    ],
)
def test_phan_loai_khen_thuong(tcid, kpi, td, thang, expected):
    actual = phan_loai_khen_thuong(kpi, td, thang)
    assert actual == expected, (
        f"{tcid}: input=({kpi}, {td}, {thang}) "
        f"expected={expected!r}, got={actual!r}"
    )