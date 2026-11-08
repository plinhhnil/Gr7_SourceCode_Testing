
import pytest

from health import classify_health


# Test case structure:
# (test_id, HR, SpO2, expected_output)

test_cases = [
    # EC1: Invalid
    ("TC01", 39, 97, "Invalid"),

    # EC2: Nguy hiểm
    ("TC02", 45, 97, "Nguy hiểm"),

    # EC3: Cảnh báo
    ("TC03", 55, 98, "Cảnh báo"),

    # EC4: Bình thường
    ("TC04", 80, 98, "Bình thường"),
]


@pytest.mark.parametrize(
    "test_id, hr, spo2, expected",
    test_cases
)
def test_classify_health(
    test_id, hr, spo2, expected
):
    actual = classify_health(hr, spo2)

    assert actual == expected, (
        f"{test_id} FAILED: "
        f"HR={hr}, SpO2={spo2}, "
        f"Expected={expected}, Actual={actual}"
    )
