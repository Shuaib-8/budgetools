import numpy as np
import plotly.graph_objects as go
import streamlit as st

from budgetools.forecast import SalaryExpensesForecasting

# Title to app
st.title("Calculator for forecasting income and expenses growth over time 🔮")

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

if st.button("Calculate your forecasted income and expenses"):
    forecast_living = SalaryExpensesForecasting(
        years=years, salary=salary, tax_rate=tax_rate
    )
    forecast_living.annual_salary_growth = salary_growth
    # Take the years and convert to months as a forecast parameter
    forecast_months = 12 * years
    salary_forecast = forecast_living.monthly_salary_forecast()

    forecast_living.rent = rent
    forecast_living.food_daily = food_daily
    forecast_living.entertainment = entertainment
    forecast_living.emergency_expenses = emergency_expenses
    forecast_living.annual_inflation = annual_inflation
    expenses_forecast = forecast_living.monthly_expenses_forecast()

    # Create traces
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=np.arange(1, forecast_months + 1, 1),
            y=salary_forecast,
            mode="lines",
            name="Salary",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=np.arange(1, forecast_months + 1, 1),
            y=expenses_forecast,
            mode="lines",
            name="Expenses",
        )
    )
    fig.update_layout(
        title=f"""Forecast Living Situation over {forecast_months} months
                                <br>
                                <b>({years} years)<b>""",
        xaxis_title="Months",
        yaxis_title="Value",
    )
    # Plot!
    st.plotly_chart(fig, use_container_width=True)
