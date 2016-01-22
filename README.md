This repository includes an implementation of a line of credit product and an ipython notebook session demonstrating its use.

Notes about the implementation:

- It follows the convention that leading underscores imply private access to variables and methods. For instance, the `self.withdraw()` method is public and the `self._log_transaction()` method is private. All variables have been marked as private to prevent external changes, but they have read-only access via the @property decorator. 

- It uses day numbers (integers) to represent which day in the current pay period transactions occur. The first day of a pay period is 0 and the last day is 29. A `_DATE_OPENED` variable is initialized to store the date that the line of credit was opened. This is a `datetime` object and can be used calculate transaction dates when necessary.

- Transaction history is segmented based on pay period. Each segment is a dictionary object containing transaction information. These segments are stored in a dictionary object using their corresponding pay period as a key. The pay periods are integers representing the number of previous pay periods since opening the line of credit. Pay period 0 is the first pay period. The pay period is incremented when the current pay period is closed. The beginning pay period dates can be calculated using the `_DATE_OPENED` variable.

- Payments made are assumed to be applied towards interest first, then outstanding balance. It's assumed that interest is only calculated on outstanding balance throughout the lifetime of the line of credit, and that interest owed is not added to the outstanding balance when a new pay period begins. The current credit limit is only based on outstanding balance; total interest owed is not used to determine the available credit limit. Interest owed and balance are kept separate for these reasons. Behavior can be easily adjusted by modifying the `payment_helper()` method.

- To maintain it's flexibility, no assumptions have been made about the external use of this implementation. For this reason, variables and values are passed “as is” when being accessed. For instance, the `_transaction_history` variable will be passed as a dictionary object, rather than a formatted table. It's assumed that external applications will modify the data as needed for the application.
