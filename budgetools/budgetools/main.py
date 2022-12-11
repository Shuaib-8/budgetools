from pathlib import Path

from budgetools.budget import BaseBudget
from budgetools.forecast import NetWorthSimulation, SalaryExpensesForecasting
from budgetools.investment import (
    investment_inflation_adjustment,
    monthly_amount_to_investment,
)

path = Path(__file__).resolve().parents[1] / "budgetools"


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
    base = BaseBudget(salary=60000, tax_rate=0.3)
    base.rent = 1200
    base.food_daily = 10
    base.entertainment = 200
    base.emergency_expenses = 250
    base.monthly_savings()
    # 1550.0

    # ~~~~~~~~~~~~ Forecast Salary/Cost of Living ~~~~~~~~~~~~
    forecast_living = SalaryExpensesForecasting(years=15, salary=60000, tax_rate=0.3)
    forecast_living.annual_salary_growth = 0.05
    forecast_living.monthly_salary_forecast()
    forecast_living.rent = 1200
    forecast_living.food_daily = 30
    forecast_living.entertainment = 200
    forecast_living.emergency_expenses = 250
    forecast_living.annual_inflation = 0.025
    forecast_living.monthly_expenses_forecast()

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
