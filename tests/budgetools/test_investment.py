from dataclasses import dataclass

import pytest
from pytest import approx  # Used for float comparisons

from budgetools.investment import (
    investment_inflation_adjustment,
    monthly_amount_to_investment,
)


@dataclass
class Params:
    rate_of_return: float = 0.0
    inflation_rate: float = 0.0
    years: int = 1
    target: float = 0.0


@pytest.fixture()
def params_7pc_25yrs_million():
    result = Params(rate_of_return=0.07, years=25, target=1_000_000)
    return result


@pytest.fixture()
def params_3pcinf_25yrs_million():
    result = Params(inflation_rate=0.03, years=25, target=1_000_000)
    return result


def test_monthly_to_investment(params_7pc_25yrs_million):
    return_value = monthly_amount_to_investment(
        avg_ror=params_7pc_25yrs_million.rate_of_return,
        years=params_7pc_25yrs_million.years,
        desired_amount=params_7pc_25yrs_million.target,
    )
    assert params_7pc_25yrs_million.rate_of_return == approx(0.07)
    assert params_7pc_25yrs_million.years == 25
    assert params_7pc_25yrs_million.target == 1_000_000
    assert params_7pc_25yrs_million.inflation_rate == 0.00
    assert isinstance(return_value, float)
    assert return_value == approx(1277.07)


def test_investment_inflation_adjustment(params_3pcinf_25yrs_million):
    return_value = investment_inflation_adjustment(
        avg_inflation=params_3pcinf_25yrs_million.inflation_rate,
        years=params_3pcinf_25yrs_million.years,
        desired_amount=params_3pcinf_25yrs_million.target,
    )
    assert params_3pcinf_25yrs_million.rate_of_return == 0.00
    assert params_3pcinf_25yrs_million.years == 25
    assert params_3pcinf_25yrs_million.target == 1_000_000
    assert params_3pcinf_25yrs_million.inflation_rate == approx(0.03)
    assert isinstance(return_value, float)
    assert return_value == approx(477605.57)


@pytest.mark.parametrize(
    "test_negative_rate, test_negative_years, test_negative_target",
    [(-0.05, -10, -1000), (0.05, -10, -1000), (0.05, 10, -1000)],
)
def test_negative_values_for_invalid_inputs_monthly_investment(
    test_negative_rate, test_negative_years, test_negative_target
):

    with pytest.raises(RuntimeError) as excinfo:
        monthly_amount_to_investment(
            avg_ror=test_negative_rate,
            years=test_negative_years,
            desired_amount=test_negative_target,
        )
    excinfo.match(
        "No arguments in the equation should be negative, \
            please redefine"
    )


@pytest.mark.parametrize(
    "test_negative_inflation_rate, test_negative_years, test_negative_target",
    [(-0.05, -10, -1000), (0.05, -10, -1000), (0.05, 10, -1000)],
)
def test_negative_values_for_invalid_inputs_inflation_adjustment(
    test_negative_inflation_rate, test_negative_years, test_negative_target
):

    with pytest.raises(RuntimeError) as excinfo:
        investment_inflation_adjustment(
            avg_inflation=test_negative_inflation_rate,
            years=test_negative_years,
            desired_amount=test_negative_target,
        )
    excinfo.match(
        "No arguments in the equation should be negative, \
            please redefine"
    )
