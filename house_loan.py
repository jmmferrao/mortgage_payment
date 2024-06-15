import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter, FuncAnimation

class LoanDetails:
    
    def __init__(self, principal: float = 0, annual_rates: list = [], years: list = []):
        
        """
        A class to represent the details of a loan and calculate the monthly payment amounts.

        Parameters:
        ----------
        - principal: float.
        The initial amount of the loan.
        - annual_rates : list.
        A list of annual interest rates for different periods of the loan.
        - years : list
        A list of time periods (in years) corresponding to the annual interest rates.
        """
        
        self.principal = principal
        self.annual_rates = annual_rates
        self.years = years

    
    def monthly_payment_amount(self) -> list:
        
        """
        Calculates the monthly payment amounts for each period specified in annual_rates and years.

        The calculation takes into account the principal, the annual interest rates, and the time periods.
        It returns a list of monthly payment amounts for each period.

        Returns:
        -------
        -list.
            A list of monthly payment amounts for each period.
        """
        
        monthly_rates = [rate / 12 / 100 for rate in self.annual_rates]
        n_payments_list = [years * 12 for years in self.years]
        total_payments = sum(n_payments_list)
        
        remaining_principal = self.principal
        final_amount = []
            
        for i, rate in enumerate(monthly_rates):
            monthly_payment_numerator = remaining_principal * rate * (1 + rate) ** total_payments
            monthly_payment_denominator = (1 + rate) ** total_payments - 1
            monthly_payment = monthly_payment_numerator / monthly_payment_denominator
            final_amount.append(monthly_payment)
            
            # Compute remaining principal after the current rate period
            remaining_principal = remaining_principal * (1 + rate)**n_payments_list[i] - (monthly_payment / rate) * ((1 + rate)**n_payments_list[i] - 1)
            
            # Update total payments left by subtracting the number of payments already processed
            current_payments = n_payments_list[i]
            total_payments -= current_payments

        return final_amount

    def payment_decomposition(self) -> pd.DataFrame:
        
        """
        Decomposes each monthly payment into interest and principal parts over the life of the loan.

        It considers  interest rates and time periods and calculates the payment breakdown
        for each month, returning the details as a pandas DataFrame.

        Returns:
        -------
        pd.DataFrame
            A DataFrame containing the breakdown of each monthly payment into interest and principal parts, along with their respective percentages, and the remaining principal after each payment.
            The columns are:
            - 'Month': The month number.
            - 'Payment': The total payment amount for the month.
            - 'Interest part (€)': The portion of the payment that goes towards interest.
            - 'Interest percentage': The percentage of the payment that goes towards interest.
            - 'Capital part (€)': The portion of the payment that goes towards the principal.
            - 'Capital percentage': The percentage of the payment that goes towards the principal.
            - 'Principal left': The remaining principal after the payment.
            - 'Interest Accumulated (€)': The total amount of interest already paid at each period.
        """
        
        monthly_payment = LoanDetails.monthly_payment_amount(self) 
        
        principal_left = self.principal
        month_list = []
        payment_list = []
        interest_list = []
        interest_percentage_list = []
        capital_list = []
        capital_percentage_list = []
        principal_left_list = []
        interest_accumulated_list = []
    
        monthly_rate = [rate  / 12 / 100 for rate in self.annual_rates]
        periods = [year * 12 for year in self.years]
        total_months = sum([year * 12 for year in self.years])
        
        #we need to make the periods list accumulative. for example [12, 6] should become [12, 18]
        
        current_sum = 0
        accumulative_periods = []

        for num in periods:
            current_sum += num
            accumulative_periods.append(current_sum)
        
        #initially we apply the first rate
        monthly_payment_value = monthly_payment[0]
        monthly_rate_value = monthly_rate[0]
        c = 0
        principal_left = self.principal
        interest_accumulated = 0
        
        for month_number in np.arange(1, total_months+1):
            interest = principal_left * monthly_rate_value
            interest_percentage = round(interest * 100 / monthly_payment_value,2)
            capital = monthly_payment_value - interest
            capital_percentage =  round(capital * 100 / monthly_payment_value,2)
            principal_left -= capital
            interest_accumulated += interest
            
            month_list.append(month_number)
            payment_list.append(monthly_payment_value)
            interest_list.append(interest)
            interest_percentage_list.append(interest_percentage)
            capital_list.append(capital)
            capital_percentage_list.append(capital_percentage)
            principal_left_list.append(principal_left if principal_left > 0 else 0)
            interest_accumulated_list.append(interest_accumulated)
            
            #we need to update to variable rate components once rate period has elapsed, except in the last period
            if month_number == accumulative_periods[c] and c < len(accumulative_periods) -  1:
                c += 1
                monthly_payment_value = monthly_payment[c]
                monthly_rate_value = monthly_rate[c]
        
        
        df = pd.DataFrame({'Month': month_list,
                        'Payment (€)': payment_list,
                        'Interest part (€)': interest_list,
                        'Interest percentage': interest_percentage_list,
                        'Capital part (€)': capital_list,
                        'Capital percentage': capital_percentage_list,
                        'Principal left (€)': principal_left_list,
                        'Interest Accumulated (€)': interest_accumulated_list})
        
        return df
    
    def total_amount_to_repay(self) -> float:
        
        """
        Calculate and print the total amount to be repaid over the life of the loan.

        This method calculates the total repayment amount for the loan based on its type.
        
        :return: float
        """

        monthly_payment_list = LoanDetails.monthly_payment_amount(self)
        
        final_value = []
           
        for rate, period in zip(monthly_payment_list, self.years):
            final_value.append(rate * period * 12)
            
        final_value = sum(final_value)
        
        return final_value
        
        #print(f"The total amount to repay the bank (capital + interest) is equal to EUR: {final_value:,.2f}")

def plot_capital_evolution(df: pd.DataFrame):
    plt.figure(figsize=(12,8))
    plt.plot(df['Month'], df['Principal left'], label = 'Principal left', color = 'blue')
    plt.xlabel('Month')
    plt.ylabel('Principal left (€)')
    plt.title('Evolution of capital to be repaid')
    plt.grid(True)
    plt.show()
    
def plot_payment_decomposition(df: pd.DataFrame):
    fig, ax1 = plt.subplots(figsize=(12, 8))
    
    # Plotting the interest part on the primary y-axis
    ax1.plot(df['Month'], df['Interest part'], label='Interest Part', color='blue')
    ax1.set_xlabel('Month')
    ax1.set_ylabel('Interest part (€)', color = 'blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    
    # Creating a secondary y-axis
    ax2 = ax1.twinx()
    ax2.plot(df['Month'], df['Capital part'], label='Principal Left', color='green')
    ax2.set_ylabel('Capital part (€)', color = 'green')
    ax2.tick_params(axis='y', labelcolor='green')
    
    plt.title('Evolution of Interest and Capital to be Repaid')
    fig.tight_layout()  # Adjust layout to prevent overlap
    plt.grid(True)
    plt.show()
    
def plot_payment_decomposition_animated(filename: str, x: pd.Series, y1 = pd.Series, y2 = pd.Series):
    fig, ax1 = plt.subplots(figsize=(12, 8))

    # Initialize the primary y-axis plot
    line1, = ax1.plot([], [], 'b-', label='Interest Paid 1')
    ax1.set_xlabel('Month')
    ax1.set_ylabel('Variable rates each 5 years: 0.01%, 2.5%, 3.5%, 4%, 2.5%', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Create a secondary y-axis
    ax2 = ax1.twinx()
    line2, = ax2.plot([], [], 'g-', label='Interest Paid 2')
    ax2.set_ylabel('Fixed 1.5% rate', color='green')
    ax2.tick_params(axis='y', labelcolor='green')

    plt.title('Interest payment comparison between fixed and variable rates')
    fig.tight_layout()  # Adjust layout to prevent overlap
    plt.grid(True)

    # Initialize data lists
    xdata, ydata1, ydata2 = [], [], []


    # Set axis limits
    
    min_y1_y2 = min(min(y1), min(y2))
    max_y1_y2 = max(max(y1), max(y2))
    
    ax1.set_xlim(min(x), max(x))
    ax1.set_ylim(min_y1_y2 - 10, max_y1_y2 + 500)
    ax2.set_ylim(min_y1_y2 - 10, max_y1_y2 + 500)
    
    # Update function for animation
    def update(frame):
        xdata.append(x[frame])
        ydata1.append(y1[frame])
        ydata2.append(y2[frame])

        line1.set_data(xdata, ydata1)
        line2.set_data(xdata, ydata2)

        return line1, line2

    # Create animation
    ani = FuncAnimation(fig, update, frames=range(len(x)), blit=True)

    # Save the animation
    metadata = dict(title='Loan Repayment Evolution', artist='Matplotlib')
    writer = PillowWriter(fps=15, metadata=metadata)
    ani.save(filename, writer=writer)

    plt.close()