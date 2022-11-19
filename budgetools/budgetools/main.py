from pathlib import Path
import numpy_financial as npf
import numpy as np

path = Path(__file__).resolve().parents[1] / "src"


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
    fv = desired_amount

    if avg_ror < 0 or years < 0 or desired_amount < 0:
        raise RuntimeError(
            "No arguments in the equation should be negative, \
            please redefine"
        )

    return -1 * (
        npf.pmt(rate=((1 + avg_ror) ** (1 / 12) - 1), nper=12 * years, pv=0, fv=fv)
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


class BaseBudget:
    def __init__(self, salary, tax_rate):
        self.salary: int = salary
        self.tax_rate: float = tax_rate
        self._rent: int = 0
        self._food_daily: int = 0
        self._entertainment: int = 0
        self._emergency_expenses: int = 0

    def monthly_salary_after_tax(self):
        salary_disposable = self.salary * (1 - self.tax_rate)

        monthly_salary_disposable = salary_disposable / 12

        return monthly_salary_disposable

    @property
    def rent(self) -> int:
        return self._rent

    @rent.setter
    def rent(self, rent_value: int):
        if rent_value < 0:
            raise ValueError("Your rent should be 0 or above")
        self._rent = rent_value

    @property
    def food_daily(self) -> int:
        return self._food_daily

    @food_daily.setter
    def food_daily(self, food_value: int):
        if food_value < 0:
            raise ValueError("Your food expenses should be 0 or above")
        self._food_daily = food_value

    @property
    def entertainment(self) -> int:
        return self._entertainment

    @entertainment.setter
    def entertainment(self, entertainment_value: int):
        if entertainment_value < 0:
            raise ValueError("Sorry your entertainment expenses should be 0 or above")
        self._entertainment = entertainment_value

    @property
    def emergency_expenses(self) -> int:

        return self._emergency_expenses

    @emergency_expenses.setter
    def emergency_expenses(self, emergency_value: int):
        if emergency_value < 0:
            raise ValueError("Sorry your emergency expenses should be 0 or above")
        self._emergency_expenses = emergency_value

    def monthly_expenses(self):

        expenses_per_month = (
            self._rent
            + (self._food_daily * 30)
            + self._entertainment
            + self._emergency_expenses
        )

        return expenses_per_month

    def monthly_savings(self):

        monthly_savings_income = (
            self.monthly_salary_after_tax() - self.monthly_expenses()
        )

        return monthly_savings_income


class SalaryExpensesForecasting(BaseBudget):
    def __init__(self, years, salary, tax_rate):
        super().__init__(salary, tax_rate)
        self.years = years
        self._annual_salary_growth = 0
        self._annual_inflation = 0

    @property
    def annual_salary_growth(self) -> float:
        return self._annual_salary_growth

    @annual_salary_growth.setter
    def annual_salary_growth(self, salary_growth_value: float):
        if salary_growth_value < 0:
            raise ValueError("The salary growth rate should be 0 or between 0-1")
        self._annual_salary_growth = salary_growth_value

    @property
    def annual_inflation(self) -> float:
        return self._annual_inflation

    @annual_inflation.setter
    def annual_inflation(self, inflation_value: float):
        if inflation_value < 0:
            raise ValueError("The inflation rate should be 0 or between 0-1")
        self._annual_inflation = inflation_value

    def monthly_salary_forecast(self):

        # Take the years and convert to months as a forecast parameter
        forecast_months = 12 * self.years

        # Converting from an annual rate to a periodic rate
        monthly_salary_growth = (1 + self._annual_salary_growth) ** (1 / 12) - 1

        # Forecast cumulative salary growth (monthly)
        cumulative_salary_growth_forecast = np.cumprod(
            np.repeat(1 + monthly_salary_growth, forecast_months)
        )

        # Finally calculate the salary forecast
        salary_forecast = np.round(
            cumulative_salary_growth_forecast * self.monthly_salary_after_tax(), 2
        )

        return salary_forecast

    def monthly_expenses_forecast(self):

        # Take the years and convert to months as a forecast parameter
        forecast_months = 12 * self.years

        # Converting from an annual rate to a periodic rate
        monthly_inflation = (1 + self.annual_inflation) ** (1 / 12) - 1

        # Forecast cumulative expenses growth (monthly)
        cumulative_inflation_forecast = np.cumprod(
            np.repeat(1 + monthly_inflation, forecast_months)
        )

        # Finally calculate the expenses forecast
        expenses_forecast = np.round(
            cumulative_inflation_forecast * self.monthly_expenses(), 2
        )

        return expenses_forecast


class NetWorthSimulation(SalaryExpensesForecasting):
    def __init__(self, years, salary, tax_rate, monthly_investment_pct):
        super().__init__(years, salary, tax_rate)
        self.monthly_investment_pct = monthly_investment_pct
        self._annual_investment_return = 0

    @property
    def annual_investment_return(self) -> float:
        return self._annual_investment_return

    @annual_investment_return.setter
    def annual_investment_return(self, investment_return_value: float):
        if investment_return_value < 0:
            raise ValueError("The inflation rate should be 0 or between 0-1")
        self._annual_investment_return = investment_return_value

    def savings_forecast(self):

        # Calculate savings for each month
        savings_forecast = (
            self.monthly_salary_forecast() - self.monthly_expenses_forecast()
        )

        # Calculate cuulative savings over time
        cumulative_savings = np.cumsum(savings_forecast)

        # Final cumulative savings
        final_net_worth = cumulative_savings[-1]

        return final_net_worth, cumulative_savings

    def monthly_income_investment(self):

        # Compute monthly deposit for investment account
        investment_deposit_forecast = (
            self.monthly_salary_forecast() - self.monthly_expenses_forecast()
        ) * self.monthly_investment_pct

        # Rest goes into savings account
        savings_forecast_new = (
            self.monthly_salary_forecast() - self.monthly_expenses_forecast()
        ) * (1 - self.monthly_investment_pct)

        # Calculate cumulative savings over time
        cumulative_savings_new = np.cumsum(savings_forecast_new)

        return investment_deposit_forecast, savings_forecast_new, cumulative_savings_new

    def net_worth_savings_investments(self):

        # gather the years as distinct months
        forecast_months = self.years * 12

        # Set the annual investment return
        investment_rate_annual = self.annual_investment_return

        # Compute the monthly investment return
        investment_rate_monthly = (1 + investment_rate_annual) ** (1 / 12) - 1

        # Retrieve the cumulated savings
        (
            investment_deposit_forecast,
            _,
            cumulated_savings_new,
        ) = self.monthly_income_investment()

        # Create intial (empty) NumPy arrays the size of forecast months
        investment_portfolio, net_worth = np.zeros(shape=(forecast_months,)), np.zeros(
            shape=(forecast_months,)
        )

        for i in range(forecast_months):
            # Find the previous investment deposit amount
            if i == 0:
                previous_investment = 0
            else:
                previous_investment = investment_portfolio[i - 1]

            # Calculate the value of your previous investments, which have grown
            previous_investment_growth = previous_investment * (
                1 + investment_rate_monthly
            )

            # Add your new deposit to your investment portfolio
            investment_portfolio[i] = (
                previous_investment_growth + investment_deposit_forecast[i]
            )

            # Calculate your net worth at each point in time
            net_worth[i] = cumulative_savings_new[i] + investment_portfolio[i]

        return cumulative_savings_new, investment_portfolio, net_worth


if __name__ == "__main__":
    # ~~~~~~~~~~~~ Investment Utilities ~~~~~~~~~~~~
    amount = monthly_amount_to_investment(
        avg_ror=0.07, years=25, desired_amount=1_000_000
    )
    # 1277.07

    inflation_adjusted_target = investment_inflation_adjustment(
        avg_inflation=0.03, years=25, desired_amount=1_000_000
    )
    # 477605.57

    # ~~~~~~~~~~~~ Basic Budget ~~~~~~~~~~~~
    base = BaseBudget(salary=60000, tax_rate=0.4)
    base.rent = 1200
    base.food_daily = 10
    base.entertainment = 200
    base.emergency_expenses = 250

    # ~~~~~~~~~~~~ Forecast Salary/Cost of Living ~~~~~~~~~~~~
    forecast_living = SalaryExpensesForecasting(years=15, salary=60000, tax_rate=0.3)
    forecast_living.annual_salary_growth = 0.05
    forecast_living.rent = 1200
    forecast_living.food_daily = 30
    forecast_living.entertainment = 200
    forecast_living.emergency_expenses = 250
    forecast_living.annual_inflation = 0.025

    # ~~~~~~~~~~~~ Investing a Pct of Income & Net Worth ~~~~~~~~~~~~
    forecast_net_worth = NetWorthSimulation(
        years=25, salary=60000, tax_rate=0.3, monthly_investment_pct=0.3
    )
    forecast_net_worth.rent = 1200
    forecast_net_worth.food_daily = 30
    forecast_net_worth.entertainment = 200
    forecast_net_worth.emergency_expenses = 250
    forecast_net_worth.annual_inflation = 0.025
    forecast_net_worth.annual_salary_growth = 0.05
    forecast_net_worth.annual_investment_return = 0.07
    final_net_worth, cumulative_savings = forecast_net_worth.savings_forecast()

    (
        investment_deposit_forecast,
        savings_forecast_post_investment,
        cumulative_savings_new,
    ) = forecast_net_worth.monthly_income_investment()

    (
        cumulated_savings_new,
        investment_portfolio,
        net_worth,
    ) = forecast_net_worth.net_worth_savings_investments()
