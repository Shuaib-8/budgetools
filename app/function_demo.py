import streamlit as st
from budgetools.main import monthly_amount_to_investment

# Title to app
st.title("Welcome to a calculator for monthly savings given financial target")

rate = st.number_input(
    "Enter assumed average rate of return (RoR)", min_value=0.00, max_value=1.00
)

years = st.number_input(
    "Enter the number of years you would like to invest for", min_value=1, max_value=50
)

target_amount = st.number_input(
    "Enter the target amount that you would like to aim for", min_value=1000, step=1000
)

if st.button("Calculate the amount to invest per month"):

    amount = monthly_amount_to_investment(rate, years, target_amount)
    st.markdown(f"**The amount to invest (per month) is:** \n\n{amount:.2f}")
