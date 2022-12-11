# `budgetools`
---

`budgetools` is an App/project to demonstrate the utilities of budgeting, saving, and investing.
 The idea is to share the principles of budgeting and financial planning, as a means for assessing one's financial future and decision making.

1. How much to save/invest every month to reach a monetary amount in a given number of years
2. Inflation adjusted considerations for a given monetary amount i.e. **purchasing power**
3. Basic monthly budget considerations 
4. Forecasting salary/income growth and cost of living (expenses due to inflation) growth i.e. living standards
5. Forecasting savings accumulation
6. Forecasting investing alongside savings accumulation
7. Forecasting net worth - savings (#5) and investment (#6)

## Installation
---

The project/app is compatible with `python 3.x` (optimal results for `3.10`).

It's first recommended to clone the repo 

```bash
$ git clone https://github.com/Shuaib-8/budgetools.git
```

After cloning, within the root of the repo, you can install requirements in the following two ways

1. You can install the project/package directly using `pip` like so:

```bash
$ python -m pip install "git+https://github.com/Shuaib-8/finance-budget-app.git#egg=budgetools&subdirectory=budgetools"
```

2. You can install via `conda` environment (if installed) or create a virtual environment (venv) and install dependencies via `requirements.txt`

```bash
$ conda env create -f env.yml
```
Once environment is created run the following

```bash
$ conda activate finance-app
```

You can create a venv beforehand and install

```bash
$ python -m pip install -r requirements.txt
```
### **App Access**
<br>
Finally, if you want to run the app, then perform the following
<br>
Move to the app location if not already

```bash
$ cd app
$ streamlit run 1_🤑_main_page.py
```


A `Docker` install is also possible (assuming you're in the root of this repo where the `Dockerfile` is located)

```bash
$ docker build -t streamlit_budgetools .
```

After the containerisation process is finished, the app can be accessed through 

```bash
$ docker run -p 8501:8501 streamlit_budgetools
```

The app is then available to view online via: 

```bash
http://0.0.0.0:8501
```

## How to use
---
As this is also a native `python` project, it is structured like so

```
├── budgetools
│   ├── budgetools
│   │   ├── __init__.py
│   │   ├── budget.py # access budget utilities
│   │   ├── forecast.py # access forecast/simulations of utilities for savings/investing and overall net worth
│   │   ├── investment.py # access investment utilities to show avenues towards monetary target
│   │   └── main.py # access example workflow for these given functions
│   └── setup.py
```

The best place to start is with **investment utilities** to answer the following:
- How much do I need to save monthly to reach a monetary target?
```python
from budgetools.investment import monthly_amount_to_investment

# avg_ror - average annual rate of returns from a given stock index e.g. S&P 500
# years - number of years to invest for 
# desired_amount - monetary target 

monthly_amount_to_investment(
        avg_ror=0.07, years=25, desired_amount=1_000_000
)

> 1277.07
```

- How much is the monetary target really worth in real terms by the end of the period? 
```python
from budgetools.investment import investment_inflation_adjustment

# avg_inflation - average inflation rate over a given period, which is usually shown by an economy's Consumer Price Index (CPI) rate

investment_inflation_adjustment(
        avg_inflation=0.03, years=25, desired_amount=1_000_000
)

> 477605.57
```

Afterwards, a **basic budget** is sensible to contemplate on a given future monetary goal:

- How much do I have leftover at the end of a typical month based on income (after tax) and common expenses?
```python
from budgetools.budget import BaseBudget

# salary - annual gross amount 
# tax_rate - tax rate in your domicile (if known)

base = BaseBudget(salary=60000, tax_rate=0.4)

base.rent = 1200 # monthly
base.food_daily = 10 # daily (below function call extends to monthly)
base.entertainment = 200 # monthly
base.emergency_expenses = 250 # monthly

base.monthly_savings()
> 1550
```

It's also to important to consider how **salary and cost of living** can be affected based on apparent trends and to see how one can be affected by given trends being extended in the **future**:

- How does my salary growth prospects and cost of living (based on economic conditions) affect my income and expenses in the future (per month until end of period)?
```python
from budgetools.forecast import SalaryExpensesForecasting

forecast_living = SalaryExpensesForecasting(years=15, salary=60000, tax_rate=0.3)
forecast_living.annual_salary_growth = 0.05

salary_forecast = forecast_living.monthly_salary_forecast()
salary_forecast 
# Returns a NumPy array that is equal to length of years e.g. 15 years = 180 months = 180 elements representing salary forecast
> array([3514.26, 3528.58, 3542.95, 3557.39, 3571.88, 3586.43, 3601.04,
       3615.72, 3630.45, 3645.24, 3660.09, 3675., ...])

forecast_living.rent = 1200
forecast_living.food_daily = 30
forecast_living.entertainment = 200
forecast_living.emergency_expenses = 250
forecast_living.annual_inflation = 0.025

expenses_forecast = forecast_living.monthly_expenses_forecast()

expenses_forecast
# Returns a NumPy array that is equal to length of years e.g. 15 years = 180 months = 180 elements representing expenses forecast
> array([2555.25, 2560.52, 2565.79, 2571.08, 2576.37, 2581.68, 2587.,
       2592.32, 2597.66, 2603.02, 2608.38, 2613.75, ...])
```

Finally, it's worth considering a sustainable solution alongside earning income to reach a monetary target (net worth) as indicated earlier. Savings in a standard savings account aggresively may not be feasible to reach a given goal quicker. However, introducing **long-term investment** strategies such as in a retirement account or in a broad/diversified stock market index such as the S&P 500 every so often can allow one to take advantage of ***compound growth***, which could build up savings in a more efficient manner:

- How does my final net worth and cumulative savings look like over a given period - standard savings and no investment?
```python
from budgetools.forecast import NetWorthSimulation

forecast_net_worth = NetWorthSimulation(
    years=25, salary=60000, tax_rate=0.3, monthly_investment_pct=0.3
)

forecast_net_worth.rent = 1200
forecast_net_worth.food_daily = 30
forecast_net_worth.entertainment = 200
forecast_net_worth.emergency_expenses = 250
forecast_net_worth.annual_inflation = 0.025
forecast_net_worth.annual_salary_growth = 0.05

final_net_worth, cumulative_savings = forecast_net_worth.savings_forecast()

final_net_worth 
> 999094.69
cumulative_savings
# Returns a NumPy array that is equal to length of years e.g. 25 years = 300 months = 300 elements representing cumulative savings schedule
> array([  959.01,  1927.07,  2904.23,  3890.54,  4886.05,  5890.8,
        6904.84,  7928.24,  8961.03, 10003.25, 11054.96, 12116.21, ...])
```

Now if we factor in some of our savings towards **investment** (30% in this case), we can see how a savings/investment forecast schedule could look like: 

- How does my savings and investment schedule look like - corresponding with cumulative savings in this setup?
```python
from budgetools.forecast import NetWorthSimulation

forecast_net_worth = NetWorthSimulation(
    years=25, salary=60000, tax_rate=0.3, monthly_investment_pct=0.3
)

forecast_net_worth.rent = 1200
forecast_net_worth.food_daily = 30
forecast_net_worth.entertainment = 200
forecast_net_worth.emergency_expenses = 250
forecast_net_worth.annual_inflation = 0.025
forecast_net_worth.annual_salary_growth = 0.05

(
    investment_deposit_forecast,
    savings_forecast_post_investment,
    cumulative_savings_new,
) = forecast_net_worth.monthly_income_investment()

investment_deposit_forecast 
# Returns a NumPy array that is equal to length of years e.g. 25 years = 300 months = 300 elements representing investment deposit forecast
> array([287.703, 290.418, 293.148, 295.893, 298.653, 301.425, 304.212,
       307.02 , 309.837, 312.666, 315.513, 318.375, ...])
savings_forecast_post_investment
# Returns a NumPy array that is equal to length of years e.g. 25 years = 300 months = 300 elements representing savings forecast while considering investing
> array([671.307, 677.642, 684.012, 690.417, 696.857, 703.325, 709.828,
       716.38 , 722.953, 729.554, 736.197, 742.875, ...])
cumulative_savings_new
# Returns a NumPy array that is equal to length of years e.g. 25 years = 300 months = 300 elements representing a modified cumulative savings schedule (wrt investing)
> array([671.307, 1348.949, 2032.961, 2723.378, 3420.235, 4123.56 ,
       4833.388, 5549.768, 6272.721, 7002.275, 7738.472, 8481.347, ...])
```

Now that it can be shown how savings/investment can look like for accumulating savings, finally we can show how **net worth** is impacted:

- How does my net worth look like when considering savings alongside investment?
```python
from budgetools.forecast import NetWorthSimulation

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

(
    cumulated_savings_new,
    investment_portfolio,
    net_worth,
) = forecast_net_worth.net_worth_savings_investments()

investment_portfolio 
# Returns a NumPy array that is equal to length of years e.g. 25 years = 300 months = 300 elements representing an approximate investment portfolio growth schedule 
> array([287.703, 579.74771459, 876.17369246, 1177.0207059,
       1482.32875209, 1792.13505437, 2106.48004652, 2425.41039096,
       2748.96101393, 3077.17003917, 3410.08180595, 3747.73790427, ...])
net_worth 
# Returns a NumPy array that is equal to length of years e.g. 25 years = 300 months = 300 elements representing an approximate net worth (savings + investment) growth schedule 
> array([959.01, 1928.69671459, 2909.13469246, 3900.3987059,
        4902.56375209, 5915.69505437, 6939.86804652, 7975.17839096,
        9021.68201393, 10079.44503917, 11148.55380595, 12229.08490427, ...])
# Returns predicted net worth by the end of the period
final_net_worth = f'Final net worth: {net_worth[-1]:,.2f}'
print(final_net_worth)
> Final net worth: 1,299,150.94
```

Hence, within the same time frame, there's a gain to be made from **long-term** investing alongside saving.

## Testing
---
To run and also test that everything is working within this project, it's also recommended to check `tests`. 
<br>
From the top level/root of the directory, run the following command:

```bash
pytest
```

### References 

Special thanks to **Dakota Wixom** who developed the course [**Introduction to Financial Concepts in Python**](https://app.datacamp.com/learn/courses/introduction-to-financial-concepts-in-python) via **DataCamp**. The course has helped inspire and develop this project, where I have adapted the given material from the code/exercises within the course.