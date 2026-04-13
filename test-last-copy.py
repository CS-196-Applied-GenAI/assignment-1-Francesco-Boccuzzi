class BankAccount:
    """A simple bank account with deposits, withdrawals, and a transfer feature."""
 
    # The minimum balance the account is allowed to reach.
    MINIMUM_BALANCE = 0.0
 
    def __init__(self, owner: str, initial_balance: float = 0.0):
        """
        Create a new BankAccount.
 
        Parameters
        ----------
        owner : str
            The name of the account holder.  Must be a non-empty string.
        initial_balance : float
            Starting balance.  Must be >= MINIMUM_BALANCE.
 
        Raises
        ------
        ValueError
            If owner is empty or initial_balance is negative.
        """
        if not owner or not owner.strip():
            raise ValueError("Owner name cannot be empty.")
        if initial_balance < self.MINIMUM_BALANCE:
            raise ValueError(
                f"Initial balance cannot be negative (got {initial_balance})."
            )
 
        self._owner = owner.strip()
        self._balance = float(initial_balance)
        self._transactions: list[str] = []  # human-readable log
 
    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------
 
    @property
    def owner(self) -> str:
        """The account holder's name (read-only)."""
        return self._owner
 
    @property
    def balance(self) -> float:
        """Current account balance (read-only)."""
        return self._balance
 
    # ------------------------------------------------------------------
    # Core operations
    # ------------------------------------------------------------------
 
    def deposit(self, amount: float) -> float:
        """
        Add money to the account.
 
        Parameters
        ----------
        amount : float
            The amount to deposit.  Must be strictly greater than 0.
 
        Returns
        -------
        float
            The new balance after the deposit.
 
        Raises
        ------
        ValueError
            If amount is zero or negative.
        """
        if amount <= 0:
            raise ValueError(f"Deposit amount must be positive (got {amount}).")
        self._balance += amount
        self._transactions.append(f"deposit  +{amount:.2f}  -> {self._balance:.2f}")
        return self._balance
 
    def withdraw(self, amount: float) -> float:
        """
        Remove money from the account.
 
        Parameters
        ----------
        amount : float
            The amount to withdraw.  Must be strictly greater than 0 and
            no larger than the current balance.
 
        Returns
        -------
        float
            The new balance after the withdrawal.
 
        Raises
        ------
        ValueError
            If amount is zero or negative.
        InsufficientFundsError
            If amount exceeds the current balance.
        """
        if amount <= 0:
            raise ValueError(f"Withdrawal amount must be positive (got {amount}).")
        if amount > self._balance:
            raise InsufficientFundsError(
                f"Cannot withdraw {amount:.2f}; "
                f"current balance is only {self._balance:.2f}."
            )
        self._balance -= amount
        self._transactions.append(f"withdraw -{amount:.2f}  -> {self._balance:.2f}")
        return self._balance
 
    def transfer(self, amount: float, target: "BankAccount") -> None:
        """
        Move money from this account to another BankAccount.
 
        This is equivalent to:
            self.withdraw(amount)
            target.deposit(amount)
 
        Parameters
        ----------
        amount : float
            The amount to transfer.  Same rules as withdraw().
        target : BankAccount
            The destination account.  Must not be this same account.
 
        Raises
        ------
        ValueError
            If target is the same object as self, or if amount is invalid.
        InsufficientFundsError
            If this account does not have enough funds.
        """
        if target is self:
            raise ValueError("Cannot transfer money to the same account.")
        # withdraw() and deposit() handle their own validation.
        self.withdraw(amount)
        target.deposit(amount)
        self._transactions.append(
            f"transfer -{amount:.2f} to {target.owner}"
        )
 
    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------
 
    def get_transaction_count(self) -> int:
        """Return the total number of transactions recorded."""
        return len(self._transactions)
 
    def get_history(self) -> list[str]:
        """Return a copy of the transaction log (oldest first)."""
        return list(self._transactions)
 
    def __repr__(self) -> str:
        return f"BankAccount(owner={self._owner!r}, balance={self._balance:.2f})"
 
 
# ---------------------------------------------------------------------------
# Custom exception
# ---------------------------------------------------------------------------
 
class InsufficientFundsError(Exception):
    """Raised when a withdrawal or transfer would drop the balance below zero."""
 
 
# ---------------------------------------------------------------------------
# Comprehensive Test Suite
# ---------------------------------------------------------------------------

import unittest
from decimal import Decimal


class TestBankAccountInitialization(unittest.TestCase):
    """Test cases for BankAccount initialization."""

    def test_init_with_valid_owner_and_balance(self):
        """Test creating an account with a valid owner and balance."""
        account = BankAccount("Alice", 500.0)
        self.assertEqual(account.owner, "Alice")
        self.assertEqual(account.balance, 500.0)

    def test_init_with_default_balance(self):
        """Test creating an account with default (zero) initial balance."""
        account = BankAccount("Bob")
        self.assertEqual(account.owner, "Bob")
        self.assertEqual(account.balance, 0.0)

    def test_init_with_whitespace_owner_stripped(self):
        """Test that owner name is stripped of leading/trailing whitespace."""
        account = BankAccount("  Charlie  ")
        self.assertEqual(account.owner, "Charlie")

    def test_init_with_zero_balance(self):
        """Test creating an account with explicitly zero balance."""
        account = BankAccount("David", 0.0)
        self.assertEqual(account.balance, 0.0)

    def test_init_with_large_balance(self):
        """Test creating an account with a large balance."""
        account = BankAccount("Eve", 999999999.99)
        self.assertEqual(account.balance, 999999999.99)

    def test_init_rejects_empty_owner(self):
        """Test that empty string owner raises ValueError."""
        with self.assertRaises(ValueError) as context:
            BankAccount("", 100.0)
        self.assertIn("Owner name cannot be empty", str(context.exception))

    def test_init_rejects_whitespace_only_owner(self):
        """Test that whitespace-only owner raises ValueError."""
        with self.assertRaises(ValueError) as context:
            BankAccount("   ", 100.0)
        self.assertIn("Owner name cannot be empty", str(context.exception))

    def test_init_rejects_negative_balance(self):
        """Test that negative initial balance raises ValueError."""
        with self.assertRaises(ValueError) as context:
            BankAccount("Frank", -100.0)
        self.assertIn("Initial balance cannot be negative", str(context.exception))

    def test_init_balance_converted_to_float(self):
        """Test that integer balance is converted to float."""
        account = BankAccount("Grace", 100)
        self.assertEqual(account.balance, 100.0)
        self.assertIsInstance(account.balance, float)


class TestDeposit(unittest.TestCase):
    """Test cases for the deposit() method."""

    def setUp(self):
        """Create a fresh account for each test."""
        self.account = BankAccount("Tester", 100.0)

    def test_deposit_positive_amount(self):
        """Test depositing a positive amount."""
        new_balance = self.account.deposit(50.0)
        self.assertEqual(self.account.balance, 150.0)
        self.assertEqual(new_balance, 150.0)

    def test_deposit_small_amount(self):
        """Test depositing a very small amount."""
        new_balance = self.account.deposit(0.01)
        self.assertAlmostEqual(self.account.balance, 100.01)
        self.assertAlmostEqual(new_balance, 100.01)

    def test_deposit_large_amount(self):
        """Test depositing a large amount."""
        new_balance = self.account.deposit(5000000.0)
        self.assertEqual(self.account.balance, 5000100.0)
        self.assertEqual(new_balance, 5000100.0)

    def test_deposit_multiple_times(self):
        """Test making multiple deposits in sequence."""
        self.account.deposit(50.0)
        self.account.deposit(75.0)
        self.account.deposit(25.0)
        self.assertEqual(self.account.balance, 250.0)

    def test_deposit_to_zero_balance_account(self):
        """Test depositing to an account with zero balance."""
        account = BankAccount("Zero Account", 0.0)
        new_balance = account.deposit(100.0)
        self.assertEqual(account.balance, 100.0)
        self.assertEqual(new_balance, 100.0)

    def test_deposit_zero_rejected(self):
        """Test that depositing zero raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.deposit(0.0)
        self.assertIn("Deposit amount must be positive", str(context.exception))

    def test_deposit_negative_rejected(self):
        """Test that depositing negative amount raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.deposit(-50.0)
        self.assertIn("Deposit amount must be positive", str(context.exception))

    def test_deposit_recorded_in_history(self):
        """Test that deposits are recorded in transaction history."""
        self.account.deposit(25.0)
        history = self.account.get_history()
        self.assertEqual(len(history), 1)
        self.assertIn("deposit", history[0])
        self.assertIn("+25.00", history[0])


class TestWithdraw(unittest.TestCase):
    """Test cases for the withdraw() method."""

    def setUp(self):
        """Create a fresh account for each test."""
        self.account = BankAccount("Tester", 500.0)

    def test_withdraw_valid_amount(self):
        """Test withdrawing a valid amount."""
        new_balance = self.account.withdraw(100.0)
        self.assertEqual(self.account.balance, 400.0)
        self.assertEqual(new_balance, 400.0)

    def test_withdraw_entire_balance(self):
        """Test withdrawing the entire balance."""
        new_balance = self.account.withdraw(500.0)
        self.assertEqual(self.account.balance, 0.0)
        self.assertEqual(new_balance, 0.0)

    def test_withdraw_small_amount(self):
        """Test withdrawing a very small amount."""
        new_balance = self.account.withdraw(0.01)
        self.assertAlmostEqual(self.account.balance, 499.99)

    def test_withdraw_multiple_times(self):
        """Test making multiple withdrawals in sequence."""
        self.account.withdraw(100.0)
        self.account.withdraw(150.0)
        self.account.withdraw(50.0)
        self.assertEqual(self.account.balance, 200.0)

    def test_withdraw_zero_rejected(self):
        """Test that withdrawing zero raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.withdraw(0.0)
        self.assertIn("Withdrawal amount must be positive", str(context.exception))

    def test_withdraw_negative_rejected(self):
        """Test that withdrawing negative amount raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.withdraw(-50.0)
        self.assertIn("Withdrawal amount must be positive", str(context.exception))

    def test_withdraw_more_than_balance_rejected(self):
        """Test that withdrawing more than balance raises InsufficientFundsError."""
        with self.assertRaises(InsufficientFundsError) as context:
            self.account.withdraw(501.0)
        self.assertIn("Cannot withdraw", str(context.exception))
        self.assertIn("501.00", str(context.exception))
        self.assertEqual(self.account.balance, 500.0)  # Balance unchanged

    def test_withdraw_slightly_more_than_balance_rejected(self):
        """Test that withdrawing even slightly more than balance is rejected."""
        with self.assertRaises(InsufficientFundsError):
            self.account.withdraw(500.01)

    def test_withdraw_from_zero_balance_rejected(self):
        """Test that withdrawing from a zero balance account is rejected."""
        account = BankAccount("Zero Account", 0.0)
        with self.assertRaises(InsufficientFundsError):
            account.withdraw(1.0)

    def test_withdraw_recorded_in_history(self):
        """Test that withdrawals are recorded in transaction history."""
        self.account.withdraw(75.0)
        history = self.account.get_history()
        self.assertEqual(len(history), 1)
        self.assertIn("withdraw", history[0])
        self.assertIn("-75.00", history[0])


class TestTransfer(unittest.TestCase):
    """Test cases for the transfer() method."""

    def setUp(self):
        """Create two fresh accounts for each test."""
        self.account_a = BankAccount("Alice", 500.0)
        self.account_b = BankAccount("Bob", 200.0)

    def test_transfer_valid_amount(self):
        """Test transferring a valid amount between accounts."""
        self.account_a.transfer(100.0, self.account_b)
        self.assertEqual(self.account_a.balance, 400.0)
        self.assertEqual(self.account_b.balance, 300.0)

    def test_transfer_entire_balance(self):
        """Test transferring an entire balance."""
        self.account_a.transfer(500.0, self.account_b)
        self.assertEqual(self.account_a.balance, 0.0)
        self.assertEqual(self.account_b.balance, 700.0)

    def test_transfer_small_amount(self):
        """Test transferring a very small amount."""
        self.account_a.transfer(0.01, self.account_b)
        self.assertAlmostEqual(self.account_a.balance, 499.99)
        self.assertAlmostEqual(self.account_b.balance, 200.01)

    def test_transfer_multiple_times(self):
        """Test making multiple transfers in sequence."""
        self.account_a.transfer(100.0, self.account_b)
        self.account_a.transfer(50.0, self.account_b)
        self.assertEqual(self.account_a.balance, 350.0)
        self.assertEqual(self.account_b.balance, 350.0)

    def test_transfer_to_self_rejected(self):
        """Test that transferring to same account raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account_a.transfer(100.0, self.account_a)
        self.assertIn("Cannot transfer money to the same account", str(context.exception))
        self.assertEqual(self.account_a.balance, 500.0)  # Balance unchanged

    def test_transfer_zero_rejected(self):
        """Test that transferring zero raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account_a.transfer(0.0, self.account_b)
        self.assertIn("must be positive", str(context.exception))

    def test_transfer_negative_rejected(self):
        """Test that transferring negative amount raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account_a.transfer(-50.0, self.account_b)
        self.assertIn("must be positive", str(context.exception))

    def test_transfer_insufficient_funds_rejected(self):
        """Test that transferring more than balance raises InsufficientFundsError."""
        with self.assertRaises(InsufficientFundsError):
            self.account_a.transfer(501.0, self.account_b)
        self.assertEqual(self.account_a.balance, 500.0)  # Balance unchanged
        self.assertEqual(self.account_b.balance, 200.0)  # Balance unchanged

    def test_transfer_recorded_in_both_histories(self):
        """Test that transfers are recorded in transaction histories."""
        self.account_a.transfer(150.0, self.account_b)
        
        history_a = self.account_a.get_history()
        history_b = self.account_b.get_history()
        
        self.assertIn("transfer", history_a[-1])
        self.assertIn("-150.00", history_a[-1])
        self.assertIn("Bob", history_a[-1])
        
        self.assertIn("deposit", history_b[-1])
        self.assertIn("+150.00", history_b[-1])


class TestTransactionHistory(unittest.TestCase):
    """Test cases for transaction history tracking."""

    def test_get_transaction_count_empty(self):
        """Test transaction count for a new account."""
        account = BankAccount("New", 0.0)
        self.assertEqual(account.get_transaction_count(), 0)

    def test_get_transaction_count_after_operations(self):
        """Test transaction count increases after operations."""
        account = BankAccount("Tester", 100.0)
        self.assertEqual(account.get_transaction_count(), 0)
        
        account.deposit(50.0)
        self.assertEqual(account.get_transaction_count(), 1)
        
        account.withdraw(25.0)
        self.assertEqual(account.get_transaction_count(), 2)

    def test_get_history_empty(self):
        """Test history is empty for a new account."""
        account = BankAccount("New", 0.0)
        history = account.get_history()
        self.assertEqual(history, [])
        self.assertIsInstance(history, list)

    def test_get_history_returns_copy(self):
        """Test that get_history returns a copy, not the original list."""
        account = BankAccount("Tester", 100.0)
        account.deposit(50.0)
        
        history1 = account.get_history()
        history2 = account.get_history()
        
        self.assertEqual(history1, history2)
        self.assertIsNot(history1, history2)  # Different list objects

    def test_get_history_order(self):
        """Test that transaction history is in order (oldest first)."""
        account = BankAccount("Tester", 100.0)
        account.deposit(50.0)
        account.withdraw(25.0)
        account.deposit(10.0)
        
        history = account.get_history()
        self.assertEqual(len(history), 3)
        self.assertIn("deposit", history[0])
        self.assertIn("withdraw", history[1])
        self.assertIn("deposit", history[2])

    def test_history_includes_balance_after_transaction(self):
        """Test that history includes the new balance after each transaction."""
        account = BankAccount("Tester", 100.0)
        account.deposit(50.0)
        history = account.get_history()
        self.assertIn("150.00", history[0])

    def test_transfer_adds_to_count(self):
        """Test that transfers increment the transaction count."""
        account_a = BankAccount("A", 100.0)
        account_b = BankAccount("B", 0.0)
        
        self.assertEqual(account_a.get_transaction_count(), 0)
        account_a.transfer(50.0, account_b)
        # Transfer records a withdrawal and an additional transfer log entry
        self.assertEqual(account_a.get_transaction_count(), 2)


class TestProperties(unittest.TestCase):
    """Test cases for read-only properties."""

    def test_owner_property_readonly(self):
        """Test that owner property is read-only."""
        account = BankAccount("Alice", 100.0)
        with self.assertRaises(AttributeError):
            account.owner = "Bob"

    def test_balance_property_readonly(self):
        """Test that balance property is read-only."""
        account = BankAccount("Alice", 100.0)
        with self.assertRaises(AttributeError):
            account.balance = 200.0

    def test_owner_returns_correct_value(self):
        """Test that owner property returns the correct value."""
        account = BankAccount("CharlieBrown", 0.0)
        self.assertEqual(account.owner, "CharlieBrown")

    def test_balance_reflects_operations(self):
        """Test that balance property reflects all operations."""
        account = BankAccount("Tester", 100.0)
        self.assertEqual(account.balance, 100.0)
        
        account.deposit(50.0)
        self.assertEqual(account.balance, 150.0)
        
        account.withdraw(30.0)
        self.assertEqual(account.balance, 120.0)


class TestRepr(unittest.TestCase):
    """Test cases for string representation."""

    def test_repr_format(self):
        """Test that __repr__ returns a properly formatted string."""
        account = BankAccount("Alice", 123.45)
        repr_str = repr(account)
        self.assertIn("BankAccount", repr_str)
        self.assertIn("Alice", repr_str)
        self.assertIn("123.45", repr_str)

    def test_repr_with_zero_balance(self):
        """Test __repr__ with zero balance."""
        account = BankAccount("Bob", 0.0)
        repr_str = repr(account)
        self.assertIn("0.00", repr_str)

    def test_repr_with_large_balance(self):
        """Test __repr__ with a large balance."""
        account = BankAccount("Rich", 1000000.50)
        repr_str = repr(account)
        self.assertIn("1000000.50", repr_str)


class TestComplexScenarios(unittest.TestCase):
    """Test cases for complex real-world scenarios."""

    def test_joint_account_simulation(self):
        """Test simulating a joint account with transfers."""
        shared = BankAccount("Joint", 1000.0)
        person_a = BankAccount("Alice", 0.0)
        person_b = BankAccount("Bob", 0.0)
        
        shared.transfer(300.0, person_a)
        shared.transfer(350.0, person_b)
        person_a.transfer(50.0, person_b)
        
        self.assertEqual(shared.balance, 350.0)
        self.assertEqual(person_a.balance, 250.0)
        self.assertEqual(person_b.balance, 400.0)

    def test_full_transaction_log(self):
        """Test a complete transaction log from multiple operations."""
        account = BankAccount("Logger", 500.0)
        
        account.deposit(100.0)
        account.withdraw(50.0)
        account.deposit(25.0)
        
        history = account.get_history()
        self.assertEqual(len(history), 3)
        
        # Check that balances progress correctly
        self.assertIn("600.00", history[0])  # 500 + 100
        self.assertIn("550.00", history[1])  # 600 - 50
        self.assertIn("575.00", history[2])  # 550 + 25

    def test_recovery_from_error(self):
        """Test that account state is preserved after an operation error."""
        account = BankAccount("Tester", 100.0)
        
        try:
            account.withdraw(200.0)  # This will fail
        except InsufficientFundsError:
            pass
        
        # Balance should be unchanged
        self.assertEqual(account.balance, 100.0)
        # No transaction should be recorded
        self.assertEqual(account.get_transaction_count(), 0)

    def test_circular_transfers(self):
        """Test circular transfers between multiple accounts."""
        a = BankAccount("A", 100.0)
        b = BankAccount("B", 100.0)
        c = BankAccount("C", 100.0)
        
        a.transfer(30.0, b)
        b.transfer(30.0, c)
        c.transfer(30.0, a)
        
        self.assertEqual(a.balance, 100.0)
        self.assertEqual(b.balance, 100.0)
        self.assertEqual(c.balance, 100.0)

    def test_floating_point_precision(self):
        """Test that floating point precision is maintained."""
        account = BankAccount("Precision", 0.1)
        account.deposit(0.2)
        account.deposit(0.3)
        self.assertAlmostEqual(account.balance, 0.6, places=10)

    def test_many_small_transactions(self):
        """Test account behavior with many small transactions."""
        account = BankAccount("Many", 0.0)
        
        for i in range(100):
            account.deposit(0.01)
        
        self.assertAlmostEqual(account.balance, 1.0, places=10)
        self.assertEqual(account.get_transaction_count(), 100)


class TestInsufficientFundsError(unittest.TestCase):
    """Test cases for the custom exception."""

    def test_exception_is_raised_on_withdrawal(self):
        """Test that InsufficientFundsError is raised on insufficient withdrawal."""
        account = BankAccount("Tester", 100.0)
        with self.assertRaises(InsufficientFundsError):
            account.withdraw(200.0)

    def test_exception_is_raised_on_transfer(self):
        """Test that InsufficientFundsError is raised on insufficient transfer."""
        a = BankAccount("A", 100.0)
        b = BankAccount("B", 0.0)
        with self.assertRaises(InsufficientFundsError):
            a.transfer(200.0, b)

    def test_exception_message_includes_details(self):
        """Test that exception message includes relevant details."""
        account = BankAccount("Tester", 50.0)
        with self.assertRaises(InsufficientFundsError) as context:
            account.withdraw(100.0)
        
        error_msg = str(context.exception)
        self.assertIn("100.00", error_msg)
        self.assertIn("50.00", error_msg)

    def test_exception_inheritance(self):
        """Test that InsufficientFundsError is an Exception."""
        self.assertTrue(issubclass(InsufficientFundsError, Exception))


if __name__ == "__main__":
    unittest.main()
 
