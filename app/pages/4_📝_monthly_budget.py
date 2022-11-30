import streamlit as st

from budgetools.budget import BaseBudget

# Title to app
st.title("Calculator for a basic monthly budget 📝")

salary = st.number_input(
    """Enter gross yearly salary""",
    min_value=0,
    key=1,
)

tax_rate = st.number_input(
    """Enter the tax rate for your income threshold e.g. 0.3 for 30%""",
    min_value=0.00,
    max_value=1.00,
    step=0.01,
    key=2,
)

rent = st.number_input("""Enter your monthly rent""", min_value=0, key=3)

food_daily = st.number_input(
    """Enter you average daily food/grocery expenses""", min_value=0, key=4
)

entertainment = st.number_input(
    """Enter you monthly entertainment expenses""", min_value=0, key=5
)

emergency_expenses = st.number_input(
    """Enter you monthly emergency expenses just in case 😉""", min_value=0, key=6
)

if st.button("Calculate your monthly disposable income and savings"):

    base = BaseBudget(salary=salary, tax_rate=tax_rate)
    base.rent = rent
    base.food_daily = food_daily
    base.entertainment = entertainment
    base.emergency_expenses = emergency_expenses

    st.markdown(
        f"""**Monthly salary after tax is:** \n\n
        {base.monthly_salary_after_tax():.0f}"""
    )

    st.markdown(
        f"""**Monthly expenses is:** \n\n
        {base.monthly_expenses():.0f}"""
    )

    st.markdown(
        f"""**Monthly savings is:** \n\n
        {base.monthly_savings():.0f}"""
    )
