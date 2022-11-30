import numpy as np

from budgetools.budget import BaseBudget


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
