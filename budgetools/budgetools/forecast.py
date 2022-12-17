import numpy as np

from budgetools.budget import BaseBudget


class SalaryExpensesForecasting(BaseBudget):
    """
    Forecasting instance class for estimate future flows for
    1. Salary - Salary growth over given period.
    2. Expenses - Expenses (cost of living) over given period.

    Attributes
    ----------
    `years` : int
        The number of years (period) to estimate forecasts for.
    `salary` : int
        Annual salary (gross).
    `tax_rate` : float
        Tax rate percentage as a decimal e.g. 30% = 0.3.

    Methods
    -------
    `monthly_salary_forecast`
        Computes an estimate of prospective monthly salary flows.
    `monthly_expenses_forecast`
        Computes an estimate of prospective monthly expenses (cost of living) flows.
    """

    def __init__(self, years, salary, tax_rate):
        """
        Instantiates the attributes for the SalaryExpensesForecasting object.

        Parameters
        ----------
        `years` : int
            Sets the number of years of the SalaryExpensesForecasting object.
        `salary` : int
            Sets salary of the SalaryExpensesForecasting object.
        `tax_rate` : float
            Sets tax rate of the SalaryExpensesForecasting object.
        """
        super().__init__(salary, tax_rate)
        self.years = years
        self._annual_salary_growth = 0
        self._annual_inflation = 0

    @property
    def annual_salary_growth(self) -> float:
        """
        The 'annual_salary_growth' property. Get or set the annual salary growth
        property value.
        The suitable value lies between 0-1.

        Returns
        -------
        float
            The annual salary growth rate.
        """
        return self._annual_salary_growth

    @annual_salary_growth.setter
    def annual_salary_growth(self, salary_growth_value: float):
        if salary_growth_value < 0:
            raise ValueError("The salary growth rate should be 0 or between 0-1")
        self._annual_salary_growth = salary_growth_value

    @property
    def annual_inflation(self) -> float:
        """
        The 'annual_inflation' property. Get or set the annual inflation rate
        property value.
        The suitable value lies between 0-1.

        Returns
        -------
        float
            The annual (CPI) inflation rate.
        """
        return self._annual_inflation

    @annual_inflation.setter
    def annual_inflation(self, inflation_value: float):
        if inflation_value < 0:
            raise ValueError("The inflation rate should be 0 or between 0-1")
        self._annual_inflation = inflation_value

    def monthly_salary_forecast(self) -> np.ndarray:
        """
        Projects the flows for the monthly salary forecast over the defined period and
        estimated (average) annual salary growth.

        Returns
        -------
        numpy.ndarray
            Returns the flow of monthly salary forecast, where each element in the array
            is an estimate of the forecasted salary value, starting from month 1 until
            end of array which is equal to length of years value converted into months
            e.g. 15 years is equal to 180 months = 180 elements in the array.

        Examples
        --------
        >>> from budgetools.forecast import SalaryExpensesForecasting
        >>> forecast_living = SalaryExpensesForecasting(years=15, salary=60000,
                                                        tax_rate=0.3)
        >>> forecast_living.annual_salary_growth = 0.05
        >>> forecast_living.monthly_salary_forecast()
        array([3514.26, 3528.58, 3542.95, 3557.39, 3571.88, 3586.43, 3601.04, \
        3615.72, 3630.45, 3645.24, 3660.09, 3675, ...])
        """
        MONTHS_PER_YEAR = 12
        # Take the years and convert to months as a forecast parameter
        forecast_months = MONTHS_PER_YEAR * self.years

        # Converting from an annual rate to a periodic rate
        monthly_salary_growth = (1 + self._annual_salary_growth) ** (
            1 / MONTHS_PER_YEAR
        ) - 1

        # Forecast cumulative salary growth (monthly)
        cumulative_salary_growth_forecast = np.cumprod(
            np.repeat(1 + monthly_salary_growth, forecast_months)
        )

        # Finally calculate the salary forecast
        salary_forecast = np.round(
            cumulative_salary_growth_forecast * self.monthly_salary_after_tax(), 2
        )

        return salary_forecast

    def monthly_expenses_forecast(self) -> np.ndarray:
        """
        Projects the flows for the monthly expenses (cost of living) forecast over the
        defined period and given expense categories.

        Returns
        -------
        numpy.ndarray
            Returns the flow of monthly expenses forecast, where each element in the
            array is an estimate of the forecasted salary value, starting from month 1
            until end of array which is equal to length of years value converted into
            months e.g. 15 years is equal to 180 months = 180 elements in the array.

        Examples
        --------
        >>> from budgetools.forecast import SalaryExpensesForecasting
        >>> forecast_living = SalaryExpensesForecasting(years=15, salary=60000,
                                                        tax_rate=0.3)
        >>> forecast_living.annual_inflation = 0.025
        >>> forecast_living.food_daily = 10
        >>> forecast_living.entertainment = 200
        >>> forecast_living.rent = 1200
        >>> forecast_living.entertainment = 200
        >>> forecast_living.emergency_expenses = 250
        >>> forecast_living.monthly_expenses_forecast()
        array([1954.02, 1958.04, 1962.07, 1966.12, 1970.17, 1974.22, 1978.29, \
        1982.37, 1986.45, 1990.54, 1994.64, 1998.75, ...])
        """
        MONTHS_PER_YEAR = 12
        # Take the years and convert to months as a forecast parameter
        forecast_months = MONTHS_PER_YEAR * self.years

        # Converting from an annual rate to a periodic rate
        monthly_inflation = (1 + self.annual_inflation) ** (1 / MONTHS_PER_YEAR) - 1

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
        MONTHS_PER_YEAR = 12
        # gather the years as distinct months
        forecast_months = MONTHS_PER_YEAR * self.years

        # Set the annual investment return
        investment_rate_annual = self.annual_investment_return

        # Compute the monthly investment return
        investment_rate_monthly = (1 + investment_rate_annual) ** (
            1 / MONTHS_PER_YEAR
        ) - 1

        # Retrieve the cumulated savings
        (
            investment_deposit_forecast,
            _,
            cumulative_savings_new,
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
