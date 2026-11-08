# test_ticket_ep.py
import pytest
from ticket import calculate_ticket_price  # Đổi tên module/hàm nếu khác


@pytest.mark.parametrize(
    "tcid, age, day, expected",
    [
        # EC1: tuổi hoặc ngày ngoài miền hợp lệ
        ("TC1", 200, 3, "Invalid"),
        # EC2: ưu đãi + ngày thường
        ("TC2", 10, 2, "Vé ưu đãi ngày thường – 50.000đ"),
        # EC3: ưu đãi + cuối tuần
        ("TC3", 75, 6, "Vé ưu đãi cuối tuần – 70.000đ"),
        # EC4: tiêu chuẩn + ngày thường
        ("TC4", 35, 0, "Vé tiêu chuẩn ngày thường – 80.000đ"),
        # EC5: tiêu chuẩn + cuối tuần
        ("TC5", 45, 5, "Vé tiêu chuẩn cuối tuần – 100.000đ"),
    ],
)
def test_ticket_price_ep(tcid, age, day, expected):
    actual = calculate_ticket_price(age, day)
    assert actual == expected, (
        f"{tcid}: input(age={age}, day={day}) -> "
        f"expected '{expected}', got '{actual}'"
    )