import numpy as np
import plotly.graph_objects as go
import streamlit as st

from budgetools.forecast import NetWorthSimulation

# Title to app
st.title(
    """Calculator for forecasting net worth
(considering savings & investment less
expenses) 📊"""
)

years = st.number_input(
    """Enter the number of years to be projected""",
    min_value=1,
    max_value=70,
    key=1,
)

salary = st.number_input(
    """Enter gross yearly salary""",
    min_value=0,
    key=2,
)

salary_growth = st.number_input(
    """Enter estimated annual salary growth e.g. 0.02 for 2%""",
    min_value=0.00,
    max_value=1.00,
    key=3,
)

tax_rate = st.number_input(
    """Enter the tax rate for your income threshold e.g. 0.3 for 30%""",
    min_value=0.00,
    max_value=1.00,
    step=0.01,
    key=4,
)

rent = st.number_input("""Enter your monthly rent""", min_value=0, key=5)

food_daily = st.number_input(
    """Enter your average daily food/grocery expenses""", min_value=0, key=6
)

entertainment = st.number_input(
    """Enter your monthly entertainment expenses""", min_value=0, key=7
)

emergency_expenses = st.number_input(
    """Enter your monthly emergency expenses just in case 😉""", min_value=0, key=8
)

annual_inflation = st.number_input(
    """Enter the annual inflation rate in your locale (CPI collected figures)
       e.g. 0.025 for 2.5%""",
    min_value=0.00,
    max_value=1.00,
    key=9,
)

investment_pct = st.number_input(
    """Enter the monthly pct amount (based on your disposable income less expenses)
       you want to invest in a retirement/investment account e.g. 0.3 for 30%""",
    min_value=0.00,
    max_value=1.00,
    key=10,
)

investment_return = st.number_input(
    """Enter the average annual return on investment (annual growth rate) over a given
       period for which you're invested in e.g. 0.07 for 7% (which is roughly the
       historical average based on popular Global Stock Market indices)""",
    min_value=0.00,
    max_value=1.00,
    key=11,
)

if st.button("Calculate your forecasted net worth i.e. planned savings + investments"):
    forecast_net_worth = NetWorthSimulation(
        years=years,
        salary=salary,
        tax_rate=tax_rate,
        monthly_investment_pct=investment_pct,
    )
    # Take the years and convert to months as a forecast parameter
    forecast_months = 12 * years
    forecast_net_worth.rent = rent
    forecast_net_worth.food_daily = food_daily
    forecast_net_worth.entertainment = entertainment
    forecast_net_worth.emergency_expenses = emergency_expenses
    forecast_net_worth.annual_inflation = annual_inflation
    forecast_net_worth.annual_salary_growth = salary_growth
    forecast_net_worth.annual_investment_return = investment_return
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

    # Create traces
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=np.arange(1, forecast_months + 1, 1),
            y=net_worth,
            mode="lines",
            name="Net Worth",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=np.arange(1, forecast_months + 1, 1),
            y=cumulated_savings_new,
            mode="lines",
            name="Savings",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=np.arange(1, forecast_months + 1, 1),
            y=investment_portfolio,
            mode="lines",
            name="Investment",
        )
    )
    fig.update_layout(
        title=f"""Forecast Net Worth (Investments + Savings) {forecast_months} months
                                <br>
                                <b>({years} years)<b>""",
        xaxis_title="Months",
        yaxis_title="Value",
    )
    # Plot!
    st.plotly_chart(fig, use_container_width=True)
