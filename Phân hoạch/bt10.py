
import pytest

# Import target function from the module
# Replace module/function names if your implementation differs.
from parking import calculate_parking_fee


@pytest.mark.parametrize(
    "tcid, hours, vehicle_type, parking_area, expected",
    [
        # EC01: Invalid input
        (
            "TC01",
            0,
            "XE_MAY",
            "NGOAI_TROI",
            (-1, "KHONG_HOP_LE")
        ),

        # EC02: Short-term, Motorcycle, Outdoor
        (
            "TC02",
            5,
            "XE_MAY",
            "NGOAI_TROI",
            (10000, "NGAN_HAN")
        ),

        # EC03: Short-term, Motorcycle, Covered
        (
            "TC03",
            7,
            "XE_MAY",
            "CO_MAI",
            (15000, "NGAN_HAN")
        ),

        # EC04: Short-term, Car, Outdoor
        (
            "TC04",
            3,
            "OTO",
            "NGOAI_TROI",
            (40000, "NGAN_HAN")
        ),

        # EC05: Short-term, Car, Covered
        (
            "TC05",
            8,
            "OTO",
            "CO_MAI",
            (55000, "NGAN_HAN")
        ),

        # EC06: Long-term, Motorcycle, Outdoor
        (
            "TC06",
            12,
            "XE_MAY",
            "NGOAI_TROI",
            (20000, "DAI_HAN")
        ),

        # EC07: Long-term, Motorcycle, Covered
        (
            "TC07",
            20,
            "XE_MAY",
            "CO_MAI",
            (30000, "DAI_HAN")
        ),

        # EC08: Long-term, Car, Outdoor
        (
            "TC08",
            15,
            "OTO",
            "NGOAI_TROI",
            (80000, "DAI_HAN")
        ),

        # EC09: Long-term, Car, Covered
        (
            "TC09",
            24,
            "OTO",
            "CO_MAI",
            (100000, "DAI_HAN")
        ),
    ],
    ids=[
        "TC01_Invalid",
        "TC02_Short_Motorcycle_Outdoor",
        "TC03_Short_Motorcycle_Covered",
        "TC04_Short_Car_Outdoor",
        "TC05_Short_Car_Covered",
        "TC06_Long_Motorcycle_Outdoor",
        "TC07_Long_Motorcycle_Covered",
        "TC08_Long_Car_Outdoor",
        "TC09_Long_Car_Covered",
    ]
)


def test_calculate_parking_fee(
    tcid,
    hours,
    vehicle_type,
    parking_area,
    expected
):
    """
    Test parking fee calculation using
    Output-Based Equivalence Partitioning.
    """

    actual = calculate_parking_fee(
        hours,
        vehicle_type,
        parking_area
    )

    assert actual == expected, (
        f"\nTest Case: {tcid}"
        f"\nInput: hours={hours}, "
        f"vehicle_type={vehicle_type}, "
        f"parking_area={parking_area}"
        f"\nExpected: {expected}"
        f"\nActual: {actual}"
    )
