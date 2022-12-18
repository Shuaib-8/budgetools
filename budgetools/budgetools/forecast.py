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
        >>> forecast_living.food_daily = 30
        >>> forecast_living.entertainment = 200
        >>> forecast_living.rent = 1200
        >>> forecast_living.entertainment = 200
        >>> forecast_living.emergency_expenses = 250
        >>> forecast_living.monthly_expenses_forecast()
        array([2555.25, 2560.52, 2565.79, 2571.08, 2576.37, 2581.68, 2587,
        2592.32, 2597.66, 2603.02, 2608.38, 2613.75, ...])
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
    """
    Forecasting instance class for estimating future projections for net worth for each
    given month across the defined period

    1. Salary - Salary growth over given period.
    2. Expenses - Expenses (cost of living) over given period.
    3. Investment - the pct to invest from  net income (salary - expenses). It's
    attached with the compound growth across each period i.e. `annual_investment_return`
    based on financial market conditions.

    Attributes
    ----------
    `years` : int
        The number of years (period) to estimate forecasts for.
    `salary` : int
        Annual salary (gross).
    `tax_rate` : float
        Tax rate percentage as a decimal e.g. 30% = 0.3.
    `monthly_investment_pct`
        How much from one's net income is to be used for investment e.g. 30% = 0.3.

    Methods
    -------
    `savings_forecast`
        Computes an estimate of the final net worth and an array containing
        cumulative saving flows respectively for the given period.
    `monthly_income_investment`
        Computes an array containing investment deposit forecast flows, an array
        containing savings forecast which is now considered in tandem with investment,
        and an array containing cumulative savings which is the modified total savings.
    `net_worth_savings_investments`
        Computes an an array containing cumulative savings which is the modified total
        savings, an array containing investment portfolio growth forecast based on
        estimated annual investment return, and an array containing overall net worth
        i.e. total investment portfolio flows + cumulative saving flows over the defined
        period.
    """

    def __init__(
        self, years: int, salary: int, tax_rate: float, monthly_investment_pct: float
    ):
        """
        Instantiates the attributes for the NetWorthSimulation object.

        Parameters
        ----------
        `years` : int
            Sets the number of years of the NetWorthSimulation object.
        `salary` : int
            Sets salary of the NetWorthSimulation object.
        `tax_rate` : float
            Sets tax rate of the NetWorthSimulation object.
        `monthly_investment_pct` : float
            Sets monthly investment percentage of the NetWorthSimulation object.
        """
        super().__init__(years, salary, tax_rate)
        self.monthly_investment_pct = monthly_investment_pct
        self._annual_investment_return = 0

    @property
    def annual_investment_return(self) -> float:
        """
        The 'annual_investment_return' property. Get or set the annual investment rate
        of return property value.
        The suitable value lies between 0-1.

        Returns
        -------
        float
            The annual investment rate of return.
        """
        return self._annual_investment_return

    @annual_investment_return.setter
    def annual_investment_return(self, investment_return_value: float):
        if investment_return_value < 0:
            raise ValueError("The inflation rate should be 0 or between 0-1")
        self._annual_investment_return = investment_return_value

    def savings_forecast(self) -> tuple[float | int, np.ndarray]:
        """
        Computes the final net worth (last element of the cumulative savings for the
        defined period) and the cumulative savings flows across the entire period.

        Returns
        -------
            - float | int \n
                The final total savings from the cumulative savings forecast, which
                is the last element in the array.
            - np.ndarray \n
                Returns the array of cumulative savings flows, where each element in the
                array is an estimate of the forecasted savings (cumulated since the
                initial period), starting from month 1 until end of array which is equal
                to length of years value converted into months e.g. 15 years is equal to
                180 months = 180 elements in the array.

        Examples
        --------
        >>> from budgetools.forecast import NetWorthSimulation
        >>> forecast_net_worth = NetWorthSimulation(years=25, salary=60000, tax_rate=0.3,
        monthly_investment_pct=0.3
        )
        >>> forecast_net_worth.rent = 1200
        >>> forecast_net_worth.food_daily = 30
        >>> forecast_net_worth.entertainment = 200
        >>> forecast_net_worth.emergency_expenses = 250
        >>> forecast_net_worth.annual_inflation = 0.025
        >>> forecast_net_worth.annual_salary_growth = 0.05
        >>> final_net_worth, cumulative_savings = forecast_net_worth.savings_forecast()
        >>> final_net_worth
        999094.6900000005
        >>> cumulative_savings
        array([959.01, 1927.07, 2904.23, 3890.54, 4886.05, 5890.8,
        6904.84, 7928.24, 8961.03, 10003.25, 11054.96, 12116.21, ...])
        """

        # Calculate savings for each month
        savings_forecast = (
            self.monthly_salary_forecast() - self.monthly_expenses_forecast()
        )

        # Calculate cumulative savings over time
        cumulative_savings = np.cumsum(savings_forecast)

        # Final cumulative savings
        final_net_worth = cumulative_savings[-1]

        return final_net_worth, cumulative_savings

    def monthly_income_investment(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Computes the investment deposit projected flows, the savings forecast modified
        due to a fixed percentage going into investments simultaneously, and cumulated
        savings now factoring in some percentage of savings going into investing.

        Returns
        -------
            - np.ndarray \n
                Returns the array of investment deposit flows, where each element in the
                array is an estimate of the forecasted investment deposits
                (cumulated since the initial period), starting from month 1 until end of
                array which is equal to length of years value converted into months e.g.
                15 years is equal to 180 months = 180 elements in the array.
            - np.ndarray \n
                Returns the array of cumulative savings flows, where each element in the
                array is an estimate of the forecasted savings (cumulated since the
                initial period), starting from month 1 until end of array which is equal
                to length of years value converted into months e.g. 15 years is equal to
                180 months = 180 elements in the array.
            - np.ndarray \n
                Returns the array of modified cumulative savings flows, where each
                element in the array is an estimate of the forecasted savings while
                investing a percentage of income (cumulated since the initial period),
                starting from month 1 until end of array which is equal to length of
                years value converted into months e.g. 15 years is equal to
                180 months = 180 elements in the array.

        Examples
        --------
        >>> from budgetools.forecast import NetWorthSimulation
        >>> forecast_net_worth = NetWorthSimulation(years=25, salary=60000,
        tax_rate=0.3, monthly_investment_pct=0.3
        )
        >>> forecast_net_worth.rent = 1200
        >>> forecast_net_worth.food_daily = 30
        >>> forecast_net_worth.entertainment = 200
        >>> forecast_net_worth.emergency_expenses = 250
        >>> forecast_net_worth.annual_inflation = 0.025
        >>> forecast_net_worth.annual_salary_growth = 0.05
        >>> (
                investment_deposit_forecast,
                savings_forecast_post_investment,
                cumulative_savings_new,
            ) = forecast_net_worth.monthly_income_investment()
        >>> investment_deposit_forecast
        array([287.703, 290.418, 293.148, 295.893, 298.653, 301.425, 304.212,
        307.02 , 309.837, 312.666, 315.513, 318.375, ...])
        >>> savings_forecast_post_investment
        array([671.307, 677.642, 684.012, 690.417, 696.857, 703.325, 709.828,
        716.38 , 722.953, 729.554, 736.197, 742.875, ...])
        >>> cumulative_savings_new
        array([ 671.307, 1348.949, 2032.961, 2723.378, 3420.235, 4123.56,
        4833.388, 5549.768, 6272.721, 7002.275, 7738.472, 8481.347, ...])
        """

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

    def net_worth_savings_investments(
        self,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Computes cumulated savings now factoring in some percentage of savings going
        into investing, the investment portfolio flows which are projected based on
        annual investment rate or return, and the net worth which is cumulated savings
        + the cumulated investment portfolio.

        Returns
        -------
            - np.ndarray \n
                Returns the array of modified cumulative savings flows, where each
                element in the array is an estimate of the forecasted savings while
                investing a percentage of income (cumulated since the initial period),
                starting from month 1 until end of array which is equal to length of
                years value converted into months e.g. 15 years is equal to
                180 months = 180 elements in the array.
            - np.ndarray \n
                Returns the array of cumulative investment portfolio flows, where each
                element in the array is an estimate of the forecasted investment
                rate of returns post investment deposit flows (cumulated since the
                initial period), starting from month 1 until end of array which is equal
                to length of years value converted into months e.g. 15 years is equal
                to 180 months = 180 elements in the array.
            - np.ndarray \n
                Returns the array of cumulative net worth (cumulative savings +
                cumulative investment returns), where each element in the array is an
                estimate of the forecasted net worth flows (cumulated since the initial
                period), starting from month 1 until end of array which is equal to
                length of years value converted into months e.g. 15 years is equal to
                180 months = 180 elements in the array.

        Examples
        --------
        >>> from budgetools.forecast import NetWorthSimulation
        >>> forecast_net_worth = NetWorthSimulation(years=25, salary=60000,
        tax_rate=0.3, monthly_investment_pct=0.3
        )
        >>> forecast_net_worth.rent = 1200
        >>> forecast_net_worth.food_daily = 30
        >>> forecast_net_worth.entertainment = 200
        >>> forecast_net_worth.emergency_expenses = 250
        >>> forecast_net_worth.annual_inflation = 0.025
        >>> forecast_net_worth.annual_salary_growth = 0.05
        >>> forecast_net_worth.annual_investment_return = 0.07
        >>> (
                cumulated_savings_new,
                investment_portfolio,
                net_worth,
            ) = forecast_net_worth.net_worth_savings_investments()
        >>> investment_portfolio
        array([287.703, 579.74771459, 876.17369246, 1177.0207059,
        1482.32875209, 1792.13505437, 2106.48004652, 2425.41039096,
        2748.96101393, 3077.17003917, 3410.08180595, 3747.73790427, ...])
        >>> net_worth
        array([959.01, 1928.69671459, 2909.13469246, 3900.3987059,
        4902.56375209, 5915.69505437, 6939.86804652, 7975.17839096,
        9021.68201393, 10079.44503917, 11148.55380595, 12229.08490427, ...])
        """
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

        # Create initial (empty) NumPy arrays the size of forecast months
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
