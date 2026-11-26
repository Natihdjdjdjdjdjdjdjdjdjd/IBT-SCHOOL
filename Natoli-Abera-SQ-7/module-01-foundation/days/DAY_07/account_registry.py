class Account:
    def __init__(self, account_number, balance=0):
        self.account_number = account_number
        self.balance = balance
        self.history = []  # Stack for transaction history

    def deposit(self, amount):
        self.balance += amount
        self.history.append(("deposit", amount))
        print(f"Deposited {amount}")

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.history.append(("withdraw", amount))
            print(f"Withdrew {amount}")
        else:
            raise ValueError("Insufficient funds")

    def undo_last(self):
        if not self.history:
            print("No transactions to undo.")
            return

        action, amount = self.history.pop()

        if action == "deposit":
            self.balance -= amount
            print(f"Undid deposit of {amount}")

        elif action == "withdraw":
            self.balance += amount
            print(f"Undid withdrawal of {amount}")

    def statement(self):
        return (
            f"Account {self.account_number} "
            f"Balance: {self.balance}"
        )


class SavingsAccount(Account):
    def __init__(self, account_number, balance=0, rate=0.01):
        super().__init__(account_number, balance)
        self.rate = rate

    def add_interest(self):
        interest = self.balance * self.rate
        self.deposit(interest)

    def statement(self):
        return (
            f"Savings Account {self.account_number} "
            f"Balance: {self.balance}"
        )


class CurrentAccount(Account):
    def __init__(self, account_number, balance=0, overdraft=0):
        super().__init__(account_number, balance)
        self.overdraft = overdraft

    def withdraw(self, amount):
        if self.balance + self.overdraft >= amount:
            self.balance -= amount
            self.history.append(("withdraw", amount))
            print(f"Withdrew {amount}")
        else:
            raise ValueError("Overdraft limit exceeded")

    def statement(self):
        return (
            f"Current Account {self.account_number} "
            f"Balance: {self.balance}, "
            f"Overdraft: {self.overdraft}"
        )


class AccountRegistry:
    def __init__(self):
        self.accounts = {}  # Dictionary

    def add(self, account):
        self.accounts[account.account_number] = account

    def find(self, account_number):
        return self.accounts.get(account_number)

    def list_all(self):
        for number in sorted(self.accounts):
            print(self.accounts[number].statement())


if __name__ == "__main__":
    registry = AccountRegistry()

    # Create accounts
    acc1 = SavingsAccount("1001", balance=1000, rate=0.05)
    acc2 = CurrentAccount("1002", balance=500, overdraft=200)

    # Add to registry
    registry.add(acc1)
    registry.add(acc2)

    # Transactions
    acc1.deposit(300)
    acc1.withdraw(100)

    acc2.withdraw(600)

    # Undo last transaction
    acc1.undo_last()

    # O(1) lookup
    account = registry.find("1001")
    print(account.statement())

    print("\nAll Accounts")
    registry.list_all()