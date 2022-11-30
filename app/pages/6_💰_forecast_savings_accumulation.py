import numpy as np
import plotly.graph_objects as go
import streamlit as st

from budgetools.forecast import NetWorthSimulation

# Title to app
st.title("Calculator for forecasting savings accumulation over time 💰")

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
    """Enter you average daily food/grocery expenses""", min_value=0, key=6
)

entertainment = st.number_input(
    """Enter you monthly entertainment expenses""", min_value=0, key=7
)

emergency_expenses = st.number_input(
    """Enter you monthly emergency expenses just in case 😉""", min_value=0, key=8
)

annual_inflation = st.number_input(
    """Enter annual inflation rate in your locale (CPI collected figures)
       e.g. 0.025 for 2.5%""",
    min_value=0.00,
    max_value=1.00,
    key=9,
)

if st.button("Calculate your forecasted savings accumulation"):
    forecast_savings = NetWorthSimulation(
        years=years, salary=salary, tax_rate=tax_rate, monthly_investment_pct=0
    )
    # Take the years and convert to months as a forecast parameter
    forecast_months = 12 * years
    forecast_savings.rent = rent
    forecast_savings.food_daily = food_daily
    forecast_savings.entertainment = entertainment
    forecast_savings.emergency_expenses = emergency_expenses
    forecast_savings.annual_inflation = annual_inflation
    forecast_savings.annual_salary_growth = salary_growth
    final_net_worth, cumulative_savings = forecast_savings.savings_forecast()

    st.markdown(
        f"""**Final net worth based on savings simulation:** \n\n
        {final_net_worth:,.0f}"""
    )

    # Create traces
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=np.arange(1, forecast_months + 1, 1),
            y=cumulative_savings,
            mode="lines",
            name="Salary",
        )
    )
    fig.update_layout(
        title=f"""Forecast Savings accumulation over {forecast_months} months
                                <br>
                                <b>({years} years)<b>""",
        xaxis_title="Months",
        yaxis_title="Savings value",
    )
    # Plot!
    st.plotly_chart(fig, use_container_width=True)
