from pathlib import Path
import numpy_financial as npf

path = Path(__file__).resolve().parents[1] / 'src'

def monthly_amount_to_investment(avg_ror: float, years: int, desired_amount: int) -> float:
    """
    A function utility that computes the sum of money needed to be invested (every month) to reach a desired 
    target amount after a given period of time.

    Average 

    Parameters
    ----------
    avg_ror : float
        Average rate of return (RoR) that is assumed for the given investment allocation to be growing over a period of time (years).
    years : int
        Number of years an individual will consistently invest.
    desired_amount : int
        The sum of money accumulated (at the end of the term) that an individual aims to achieve.

    Returns
    -------
    float
       The monthly amount needed to consistently invest based on setting of years, ror, and target amount
    """
    rate = 0.07
    period = years
    fv = desired_amount
    return -1 * (npf.pmt(rate=((1+rate)**(1/12) - 1), nper=12*period, pv=0, fv=fv))

if __name__ == '__main__':
    amount = monthly_amount_to_investment(0.07, years=25, desired_amount=1000000)
    # 1277.07
    print(amount)