class BaseBudget:
    """
    Foundational budget instance class for computing a simple
    budget on a monthly basis (income - expenses).

    Attributes
    ----------
    `salary` : int
        Annual salary (gross).
    `tax_rate` : float
        Tax rate percentage as a decimal e.g. 30% = 0.3.

    Methods
    -------
    `monthly_salary_after_tax`
        Salary leftover after tax on a monthly basis.
    `monthly_expenses`
        Expenses on a monthly basis.
    `monthly_savings`
        Monthly salary after tax (monthly_salary_after_tax)
        subtract monthly expenses (monthly_expenses).
    """

    def __init__(self, salary: int, tax_rate: float):
        """
        Instantiates the attributes for the BaseBudget object.

        Parameters
        ----------
        `salary` : int
            Sets Annual salary (gross) of the BaseBudget object.
        `tax_rate` : float
            Sets Tax rate (decimal) of the BaseBudget object.
        """
        self.salary: int = salary
        self.tax_rate: float = tax_rate
        self._rent: int = 0
        self._food_daily: int = 0
        self._entertainment: int = 0
        self._emergency_expenses: int = 0

    def monthly_salary_after_tax(self) -> int | float:
        """
        The monthly salary after tax computation.

        Returns
        -------
        int | float
            Returns the monthly salary after tax value.

        Examples
        --------
        >>> from budgetools.budget import BaseBudget
        >>> base = BaseBudget(salary=60000, tax_rate=0.3)
        >>> base.monthly_salary_after_tax()
        3500
        """
        MONTHS_PER_YEAR = 12
        salary_disposable = self.salary * (1 - self.tax_rate)

        monthly_salary_disposable = salary_disposable / MONTHS_PER_YEAR

        return monthly_salary_disposable

    @property
    def rent(self) -> int:
        """
        The 'rent' expense property. Get or set the monthly rent value.

        Returns
        -------
        int
            The monthly rent expense.
        """
        return self._rent

    @rent.setter
    def rent(self, rent_value: int):
        if rent_value < 0:
            raise ValueError("Your rent should be 0 or above")
        self._rent = rent_value

    @property
    def food_daily(self) -> int:
        """
        The 'food_daily' property. Get or set the daily (average) food expense value.

        Returns
        -------
        int
            The daily food expense.
        """
        return self._food_daily

    @food_daily.setter
    def food_daily(self, food_value: int):
        if food_value < 0:
            raise ValueError("Your food expenses should be 0 or above")
        self._food_daily = food_value

    @property
    def entertainment(self) -> int:
        """
        The 'entertainment' property. Get or set the monthly entertainment value.

        Returns
        -------
        int
            The monthly entertainment expense.
        """
        return self._entertainment

    @entertainment.setter
    def entertainment(self, entertainment_value: int):
        if entertainment_value < 0:
            raise ValueError("Sorry your entertainment expenses should be 0 or above")
        self._entertainment = entertainment_value

    @property
    def emergency_expenses(self) -> int:
        """
        The 'emergency_expenses' property. Get or set the monthly emergency
        expenses value.

        Returns
        -------
        int
            The monthly emergency expenses value.
        """

        return self._emergency_expenses

    @emergency_expenses.setter
    def emergency_expenses(self, emergency_value: int):
        if emergency_value < 0:
            raise ValueError("Sorry your emergency expenses should be 0 or above")
        self._emergency_expenses = emergency_value

    def monthly_expenses(self) -> int | float:
        """
        Computes the total monthly expenses based on properties defined beforehand:
        - rent
        - food
        - entertainment
        - emergency

        Returns
        -------
        int | float
            Expenses on a monthly basis.

        Examples
        --------
        >>> from budgetools.budget import BaseBudget
        >>> base = BaseBudget(salary=60000, tax_rate=0.3)
        >>> base.rent = 1200
        >>> base.food_daily = 10
        >>> base.entertainment = 200
        >>> base.emergency_expenses = 250
        >>> base.monthly_expenses()
        1950
        """
        DAYS_PER_MONTH = 30
        expenses_per_month = (
            self._rent
            + (self._food_daily * DAYS_PER_MONTH)
            + self._entertainment
            + self._emergency_expenses
        )

        return expenses_per_month

    def monthly_savings(self) -> int | float:
        """
        Computes the monthly savings by subtracting monthly_expenses from
        monthly_salary_after_tax based on properties defined beforehand:
        - rent
        - food
        - entertainment
        - emergency

        Returns
        -------
        int | float
            Monthly savings (which takes into income post tax and expenses).

        Examples
        --------
        >>> from budgetools.budget import BaseBudget
        >>> base = BaseBudget(salary=60000, tax_rate=0.3)
        >>> base.rent = 1200
        >>> base.food_daily = 10
        >>> base.entertainment = 200
        >>> base.emergency_expenses = 250
        >>> base.monthly_savings()
        1550
        """
        monthly_savings_income = (
            self.monthly_salary_after_tax() - self.monthly_expenses()
        )

        return monthly_savings_income
