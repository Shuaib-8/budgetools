import streamlit as st

from budgetools.investment import investment_inflation_adjustment

# Title to app
st.title("Calculator for inflation adjusted savings/investment goal 📉")

inflation_rate = st.number_input(
    """Enter assumed (annual) average rate of inflation (e.g. Inflation
    rate measured from Consumer Price Index (CPI) in your location)""",
    min_value=0.00,
    max_value=1.00,
)

years = st.number_input(
    "Enter the number of years you would like to invest/save for",
    min_value=1,
    max_value=50,
)

target_amount = st.number_input(
    """Enter the target investment/savings
     amount that you would like to aim for""",
    min_value=1000,
    step=1000,
)

if st.button("Calculate the inflation adjusted investment/savings target amount"):

    inflation_adjusted_amount = investment_inflation_adjustment(
        inflation_rate, years, target_amount
    )
    st.markdown(
        f"""**The investment/savings amount adjusted for inflation is:** \n\n
                {inflation_adjusted_amount:.2f}"""
    )
