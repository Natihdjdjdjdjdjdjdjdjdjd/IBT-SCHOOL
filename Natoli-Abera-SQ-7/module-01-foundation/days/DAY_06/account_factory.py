class AlertService:
    """Handles sending alerts (SRP)."""

    def send(self, message):
        print(f"ALERT: {message}")


class SMSAlert:
    """Observer that receives account notifications."""

    def update(self, message):
        print(f"SMS: {message}")


class Account:
    def __init__(self, balance=0):
        self.balance = balance
        self._subscribers = []

    # Observer methods
    def subscribe(self, observer):
        self._subscribers.append(observer)

    def _notify(self, message):
        for observer in self._subscribers:
            observer.update(message)

    def deposit(self, amount):
        self.balance += amount
        self._notify(f"Deposited {amount}. New balance: {self.balance}")

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self._notify(f"Withdrew {amount}. New balance: {self.balance}")
        else:
            raise ValueError("Insufficient funds")

    def statement(self):
        return f"Account - Balance: {self.balance}"


class SavingsAccount(Account):
    def __init__(self, balance=0, rate=0.01):
        super().__init__(balance)
        self.rate = rate

    def add_interest(self):
        interest = self.balance * self.rate
        self.deposit(interest)

    def statement(self):
        return f"Savings Account - Balance: {self.balance}"


class CurrentAccount(Account):
    def __init__(self, balance=0, overdraft=0):
        super().__init__(balance)
        self.overdraft = overdraft

    def withdraw(self, amount):
        if self.balance + self.overdraft >= amount:
            self.balance -= amount
            self._notify(f"Withdrew {amount}. New balance: {self.balance}")
        else:
            raise ValueError("Overdraft limit exceeded")

    def statement(self):
        return (
            f"Current Account - Balance: {self.balance}, "
            f"Overdraft: {self.overdraft}"
        )


class AccountFactory:
    """Factory for creating accounts."""

    @staticmethod
    def create(kind, **kwargs):
        if kind.lower() == "savings":
            return SavingsAccount(**kwargs)
        elif kind.lower() == "current":
            return CurrentAccount(**kwargs)
        else:
            return Account(**kwargs)


if __name__ == "__main__":
    # Create observer
    sms = SMSAlert()

    # Create accounts using the factory
    savings = AccountFactory.create(
        "savings",
        balance=1000,
        rate=0.05
    )

    current = AccountFactory.create(
        "current",
        balance=200,
        overdraft=100
    )

    # Attach observer
    savings.subscribe(sms)
    current.subscribe(sms)

    # Transactions
    savings.deposit(500)
    savings.add_interest()

    current.withdraw(250)

    # Statements
    print("\nAccount Statements")
    print(savings.statement())
    print(current.statement())