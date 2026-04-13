# Comprehensive Test Suite for BankAccount

## Overview
A complete test suite with **60 tests** covering all aspects of the `BankAccount` class. All tests pass successfully.

## Test Coverage Breakdown

### 1. **TestBankAccountInitialization** (9 tests)
Tests the constructor and parameter validation:
- Valid account creation with owner and balance
- Default (zero) initial balance
- Whitespace stripping in owner names
- Large balance handling
- Rejection of empty/whitespace-only owner names
- Rejection of negative initial balances
- Type conversion of integer balances to float

### 2. **TestDeposit** (8 tests)
Tests the `deposit()` method:
- Valid positive deposits
- Small and large deposit amounts
- Multiple sequential deposits
- Deposits to zero-balance accounts
- Rejection of zero and negative amounts
- Transaction history recording

### 3. **TestWithdraw** (11 tests)
Tests the `withdraw()` method:
- Valid withdrawals
- Withdrawing entire balance
- Small and large withdrawal amounts
- Multiple sequential withdrawals
- Rejection of zero and negative amounts
- Insufficient funds detection (exact and slightly over)
- Withdrawing from zero-balance accounts
- Transaction history recording

### 4. **TestTransfer** (10 tests)
Tests the `transfer()` method:
- Valid transfers between accounts
- Transferring entire balance
- Small and large transfer amounts
- Multiple sequential transfers
- Self-transfer rejection
- Rejection of zero and negative amounts
- Insufficient funds detection
- Transaction history recording in both accounts

### 5. **TestTransactionHistory** (6 tests)
Tests transaction tracking and history:
- Empty history for new accounts
- Transaction count incrementation
- History order (oldest first)
- History immutability (returns copy, not reference)
- Balance inclusion in history records
- Transfer count tracking

### 6. **TestProperties** (4 tests)
Tests read-only properties:
- Owner property is read-only and returns correct value
- Balance property is read-only and reflects all operations

### 7. **TestRepr** (3 tests)
Tests string representation:
- Proper format with owner and balance
- Handling of zero balance
- Handling of large balances

### 8. **TestComplexScenarios** (6 tests)
Tests real-world usage patterns:
- Joint account simulation with multiple transfers
- Complete transaction logs with proper balance progression
- Error recovery (state preservation after failed operations)
- Circular transfers between multiple accounts
- Floating-point precision handling
- Many small transactions (100 deposits)

### 9. **TestInsufficientFundsError** (4 tests)
Tests the custom exception:
- Raised on insufficient withdrawal
- Raised on insufficient transfer
- Includes relevant error details
- Proper exception inheritance

## Edge Cases Covered

1. **Boundary conditions**: Zero balance, exact balance transfers
2. **Floating-point precision**: Small amounts (0.01), many decimals
3. **Large numbers**: Large balances and transactions
4. **String handling**: Whitespace stripping, special characters
5. **State integrity**: Failed operations don't modify state
6. **History accuracy**: All transactions properly recorded with balances

## Test Results
```
Ran 60 tests in 0.001s
OK
```

All tests pass with no failures or errors.

## Running the Tests

```bash
python3 test-last-copy.py -v
```

For quiet mode:
```bash
python3 test-last-copy.py
```

## Key Testing Features

- **Comprehensive coverage**: All public methods tested
- **Error handling**: All exception cases validated
- **State verification**: Balance and history checked after each operation
- **Isolation**: Each test uses `setUp()` with fresh accounts
- **Clear documentation**: Each test has a docstring explaining its purpose
- **Edge case focus**: Special attention to boundary conditions
- **Real-world scenarios**: Tests simulate actual banking operations
