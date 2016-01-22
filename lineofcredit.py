
import datetime

class LineOfCredit(object):
    """Implementation of a line of credit product."""
    def __init__(self,limit,APR):
        """Initializes a new LineOfCredit object."""
        self._DATE_OPENED = datetime.datetime.now().date()
        self._APR = APR/100.
        self._current_period = 0
        self._current_limit = limit
        self._current_balance = 0
        self._interest_owed = 0
        self._transaction_history = {}
        self._new_transaction_period()
        
#====== Accessors/getters for variables =========
    @property
    def DATE_OPENED(self):
        """Returns the date the line of credit was first opened,
        as a datetime object."""
        return self._DATE_OPENED
    
    @property
    def APR(self):
        """Returns the APR for the line of credit as a percent.
        For example, an APR of 35% will be returned as 35."""
        return self._APR*100
    
    @property
    def current_period(self):
        """Returns the current pay period as an integer; 0 represents the first
	   pay period."""
        return self._current_period
    
    @property
    def current_limit(self):
        """Returns the curret credit limit available."""
        return self._current_limit
    
    @property
    def current_balance(self):
        """Returns the current balance."""
        return self._current_balance
    
    @property
    def interest_owed(self):
        """Returns the total interest owed."""
        return self._interest_owed
    
    @property
    def transaction_history(self):
        """Returns transaction history as a dictionary object.
           Keys of this dictionary are integers corresponding 
           to particular pay periods. Pay period 0 represents
           the first pay period. Each pay period is 30 days.
           """
        return self._transaction_history
    
    def get_total_amount_owed(self):
        """Returns the total amount owed: 
	   Outstanding balance + interest owed."""
        return round(self._current_balance + self._interest_owed,2)
        
#======== Methods for making transactions ===========
    def withdraw(self, day, amount):
        """Make a withdrawl from the line of credit.
           Raises an exception if the amount exceeds the
           available credit limit."""
        check_day_helper(day)
        if amount > self._current_limit:
            raise ValueError("Withdrawl amount exceeds available credit limit.")
        self._current_limit -= amount
        self._current_balance += amount
        self._log_transaction(day,'withdraw',amount)
        
    def payment(self, day, amount):
        """Make a payment on the line of credit.
        Calls a helper function determine the appropriate
        interest owed, balance and limit values."""
        check_day_helper(day)
        interest = self._interest_owed
        balance = self._current_balance
        limit = self._current_limit
        new_interest, new_balance, new_limit = payment_helper(interest,balance,limit,amount)
        self._interest_owed = new_interest
        self._current_balance = new_balance
        self._current_limit = new_limit
        self._log_transaction(day,'payment',amount)
    
    def _log_transaction(self,day,transaction_type,amount):
        """Logs transaction info for a single transaction. 
	Saves the following info:
        'day' -- The day the transaction took place, as the day number of the
                 current pay period. Day 0 is the first day of a new pay period;
                 Day 29 is the last day of the pay period.
        'transaction_type' -- Either 'withdraw' or 'payment'
        'amount' -- The amount of the transaction.
        'new_balance' -- The new balance after the transaction is processed.
        'new_limit' -- The amount of credit available after the transaction 
	               is processed.
        """
        check_day_helper(day)
        self._transaction_history[self._current_period]['day'].append(day)
        self._transaction_history[self._current_period]['transaction_type'].append(transaction_type)
        self._transaction_history[self._current_period]['amount'].append(amount)
        self._transaction_history[self._current_period]['new_balance'].append(self._current_balance)
        self._transaction_history[self._current_period]['new_limit'].append(self._current_limit)

#======== Methods for closing the pay period and starting a new one ==========
    def close_current_period(self):
        """Closes the current pay period, and starts a new pay period. 
           Updates interest owed, updates the current pay period and
           begins a new transaction history record for the new pay period."""
        interest = self._calculate_interest()
        self._update_interest_owed(interest)
        self._current_period += 1
        self._new_transaction_period()
        
    def _new_transaction_period(self):
        """Creates a new, empty transaction history for the current pay period.
        Raises an error if a transaction history already exists for the pay 
	period."""
        this_period = self._current_period
        found = self._transaction_history.get(this_period,False)
        if found:
            raise KeyError("Transaction history for this pay period already exists.")
        self._transaction_history[this_period] = {'day':[],
                                                  'transaction_type':[],
                                                  'amount':[],
                                                  'new_balance':[],
                                                  'new_limit':[]}
    
#========= Interest Calculation Methods ==================
    def _calculate_interest(self,today = 30):
        """Calculates and returns the interest owed for the current pay period.
        The default behavior assumes the pay period has ended.
        The 'today' variable can be used to calculate interest accrued for days
        less than day 30. It must be an integer, it must be at least as large as 
        the largest day number in the current pay period transaction history,
        and it must not be larger than 30. Raises an exception otherwise."""
        days = self._transaction_history[self._current_period]['day'][::-1]
        balances = self._transaction_history[self._current_period]['new_balance'][::-1]
        apr = self._APR
        interest_total = 0
        if today not in range(max(days),30+1):
            raise ValueError("'today' must be an integer <= 30 or >= largest day number in transaction history.")
        day_start = today
        for i,day in enumerate(days):
            day_end = day
            number_of_days = day_start-day_end
            balance = balances[i]
            interest_total += calculate_interest_helper(number_of_days,balance,apr)
            day_start = day_end
        return round(interest_total,2)

    def _update_interest_owed(self,interest):
        """Updates interest owed to include interest accrued over
           the current pay period."""
        self._interest_owed += interest
        
#====== Helper Functions =================
def check_day_helper(day):
    """Helper function to check if day passed by user is valid.
       Raises an exception if day is not an integer in the 
       range 0 <= day < 30."""
    if not day in range(30):
        raise ValueError("The 'day' argument must be an integer between 0 and 29.")
        
def payment_helper(interest,balance,limit,payment_amount):
    """Helper function to apply payment properly.
       Returns new interest, balance and limit values, given a payment amount.
       Assumes that payments will be applied towards interest first,
       and any remaining amount will be applied towards the balance.
       Raises an exception if payment amount exceeds the amount owed."""
    amount_owed = interest + balance
    if payment_amount > amount_owed:
        raise ValueError("The payment amount exceeds the amount owed.")
    difference = interest - payment_amount
    if difference <= 0:
        interest = 0
        balance += difference
        limit -= difference
    else:
        interest = difference
    return interest, balance, limit

def calculate_interest_helper(number_of_days,balance,apr):
    """Helper function for calculating interest.
       Returns interest accrued given the number days passed,
       the balance over those days, and the APR.
       Assumes 'apr' is a fraction, NOT a percent."""
    interest = number_of_days * balance * apr/365
    return interest

