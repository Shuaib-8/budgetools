# `budgetools`
---

`budgetools` is an App/project to demonstrate the utilities of budgeting, saving, and investing.
 The idea is to share the principles of budgeting and financial planning, as a means for assessing one's financial future and decision making.

1. How much to save/invest every month to reach a monetary amount in a given number of years
2. Inflation adjusted considerations for a given monetary amount i.e. **purchasing power**
3. Basic monthly budget considerations 
4. Forecasting salary/income growth and cost of living (expenses due to inflation) growth i.e. living standards
5. Forecasting savings accumulation
6. Forecasting investing along savings accumulation
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
