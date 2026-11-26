
class Account:
    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            return amount
        else:
            raise ValueError("Insufficient funds")

    def statement(self):
        return f"Balance: {self.balance}"

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
            return amount
        else:
            raise ValueError("Overdraft limit exceeded")

    def statement(self):
        return f"Current Account - Balance: {self.balance}, Overdraft Allowed: {self.overdraft}"

if __name__ == "__main__":
    accounts = [
        SavingsAccount(balance=1000, rate=0.05),
        CurrentAccount(balance=200, overdraft=100),
        Account(balance=500),
    ]

    for account in accounts:
        print(account.statement())
