
import pytest

# Import target function
from delivery_fee import calculate_delivery_fee


@pytest.mark.parametrize(
    "distance, weight, delivery_area, expected_output",
    [
        # TC01 - EC01: Invalid input
        (
            0,
            2.3,
            "NOI_THANH",
            (-1, "KHONG_HOP_LE", "ERROR")
        ),

        # TC02 - EC02: Short distance, standard weight, inner city
        (
            37,
            2.4,
            "NOI_THANH",
            (50000, "TIEU_CHUAN", "OK")
        ),

        # TC03 - EC03: Short distance, standard weight, outer city
        (
            12,
            4.7,
            "NGOAI_THANH",
            (60000, "TIEU_CHUAN", "OK")
        ),

        # TC04 - EC04: Short distance, heavy weight, inner city
        (
            48,
            13.6,
            "NOI_THANH",
            (70000, "HANG_NANG", "OK")
        ),

        # TC05 - EC05: Short distance, heavy weight, outer city
        (
            6,
            8.2,
            "NGOAI_THANH",
            (80000, "HANG_NANG", "OK")
        ),

        # TC06 - EC06: Long distance, standard weight, inner city
        (
            73,
            1.8,
            "NOI_THANH",
            (80000, "TIEU_CHUAN", "OK")
        ),

        # TC07 - EC07: Long distance, standard weight, outer city
        (
            99,
            5.0,
            "NGOAI_THANH",
            (90000, "TIEU_CHUAN", "OK")
        ),

        # TC08 - EC08: Long distance, heavy weight, inner city
        (
            62,
            17.3,
            "NOI_THANH",
            (100000, "HANG_NANG", "OK")
        ),

        # TC09 - EC09: Long distance, heavy weight, outer city
        (
            85,
            6.4,
            "NGOAI_THANH",
            (120000, "HANG_NANG", "OK")
        ),
    ]
)
def test_calculate_delivery_fee(
    distance,
    weight,
    delivery_area,
    expected_output
):
    actual_output = calculate_delivery_fee(
        distance,
        weight,
        delivery_area
    )

    assert actual_output == expected_output
