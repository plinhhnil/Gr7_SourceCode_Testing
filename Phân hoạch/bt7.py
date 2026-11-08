
import pytest

from credit_risk import evaluate_credit_risk


@pytest.mark.parametrize(
    "credit_score, term, expected",
    [
        # EC1: Invalid credit_score
        (250, 36, "Invalid"),

        # EC2: Invalid term
        (650, 5, "Invalid"),

        # EC3: credit_score in [300, 580)
        (450, 36, "High Risk"),

        # EC4: credit_score in [580, 700), term in [24, 60]
        (620, 36, "High Risk"),

        # EC5: credit_score in [580, 700), term in [6, 24)
        (620, 12, "Low Risk"),

        # EC6: credit_score in [700, 850]
        (750, 48, "Low Risk"),
    ],
)
def test_evaluate_credit_risk(credit_score, term, expected):
    actual = evaluate_credit_risk(credit_score, term)

    assert actual == expected
