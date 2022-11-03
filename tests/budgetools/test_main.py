from pytest import approx  # Used for float comparisons
from budgetools.main import monthly_amount_to_investment
from budgetools.main import investment_inflation_adjustment

monthly_amount_to_investment(avg_ror=0.07, years=25, desired_amount=1_000_000)


def test_monthly_to_investment():
    return_value = monthly_amount_to_investment(
        avg_ror=0.07, years=25, desired_amount=1_000_000
    )
    assert isinstance(return_value, float)
    assert return_value == approx(1277.07)


def test_investment_inflation_adjustment():
    return_value = investment_inflation_adjustment(
        avg_inflation=0.03, years=25, desired_amount=1_000_000
    )
    assert isinstance(return_value, float)
    assert return_value == approx(466974.70)
