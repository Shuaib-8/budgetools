import numpy_financial as npf


def monthly_amount_to_investment(
    avg_ror: float, years: int, desired_amount: int
) -> float:
    """
    A function utility that computes the sum of money needed to be
    invested (every month) to reach a desired
    target amount after a given period of time.

    Parameters
    ----------
    avg_ror : float
        Average rate of return (RoR) that is assumed for the given investment
        allocation to be growing over a period of time (years).
    years : int
        Number of years an individual will consistently invest.
    desired_amount : int
        The sum of money accumulated (at the end of the term) that an
        individual aims to achieve.

    Returns
    -------
    float
       The monthly amount needed to consistently invest based on setting of
       years, ror, and target investment amount.
    """
    MONTHS_PER_YEAR = 12
    fv = desired_amount

    if avg_ror < 0 or years < 0 or desired_amount < 0:
        raise RuntimeError(
            "No arguments in the equation should be negative, \
            please redefine"
        )

    return -1 * (
        npf.pmt(
            rate=((1 + avg_ror) ** (1 / MONTHS_PER_YEAR) - 1),
            nper=MONTHS_PER_YEAR * years,
            pv=0,
            fv=fv,
        )
    )


def investment_inflation_adjustment(
    avg_inflation: float, years: int, desired_amount: int
) -> float:
    """
    A function utility that computes the inflation adjusted target investment amount
    over a given defined period of time.
    The average inflation rate can be assumed from indicators such as
    the Consumer Price Index (CPI)
    for the given time period and the country of which the currency unit is denominated
    in e.g assuming the investment is in USD, you'll want to take the CPI figures
    published by the U.S Central Bank or a given Statistical Agency.

    Parameters
    ----------
    avg_inflation : float
        Average rate of inflation. Assumed to be taken from a price index e.g. CPI
        over a period of time (years).
    years : int
        Number of years an individual will consistently invest.
    desired_amount : int
        The sum of money accumulated (at the end of the term) that an
        individual aims to achieve.

    Returns
    -------
    float
        The real (future) value (adjusted for inflation) of the target investment amount
        over the defined period.
    """
    fv = -1 * desired_amount
    rate = avg_inflation

    if avg_inflation < 0 or years < 0 or desired_amount < 0:
        raise RuntimeError(
            "No arguments in the equation should be negative, \
            please redefine"
        )

    return npf.pv(rate=rate, nper=years, pmt=0, fv=fv)
