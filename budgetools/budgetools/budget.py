class BaseBudget:
    def __init__(self, salary, tax_rate):
        self.salary: int = salary
        self.tax_rate: float = tax_rate
        self._rent: int = 0
        self._food_daily: int = 0
        self._entertainment: int = 0
        self._emergency_expenses: int = 0

    def monthly_salary_after_tax(self):
        MONTHS_PER_YEAR = 12
        salary_disposable = self.salary * (1 - self.tax_rate)

        monthly_salary_disposable = salary_disposable / MONTHS_PER_YEAR

        return monthly_salary_disposable

    @property
    def rent(self) -> int:
        return self._rent

    @rent.setter
    def rent(self, rent_value: int):
        if rent_value < 0:
            raise ValueError("Your rent should be 0 or above")
        self._rent = rent_value

    @property
    def food_daily(self) -> int:
        return self._food_daily

    @food_daily.setter
    def food_daily(self, food_value: int):
        if food_value < 0:
            raise ValueError("Your food expenses should be 0 or above")
        self._food_daily = food_value

    @property
    def entertainment(self) -> int:
        return self._entertainment

    @entertainment.setter
    def entertainment(self, entertainment_value: int):
        if entertainment_value < 0:
            raise ValueError("Sorry your entertainment expenses should be 0 or above")
        self._entertainment = entertainment_value

    @property
    def emergency_expenses(self) -> int:

        return self._emergency_expenses

    @emergency_expenses.setter
    def emergency_expenses(self, emergency_value: int):
        if emergency_value < 0:
            raise ValueError("Sorry your emergency expenses should be 0 or above")
        self._emergency_expenses = emergency_value

    def monthly_expenses(self):
        DAYS_PER_MONTH = 30
        expenses_per_month = (
            self._rent
            + (self._food_daily * DAYS_PER_MONTH)
            + self._entertainment
            + self._emergency_expenses
        )

        return expenses_per_month

    def monthly_savings(self):

        monthly_savings_income = (
            self.monthly_salary_after_tax() - self.monthly_expenses()
        )

        return monthly_savings_income
