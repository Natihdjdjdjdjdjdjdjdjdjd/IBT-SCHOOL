class Account:

    def __init__(self, owner, account_number, balance=0):
        self.owner = owner
        self.account_number = account_number
        self.__balance = balance

    @property
    def balance(self):
        return self.__balance

    def deposit(self, amount):
        if amount <= 0:
            print("Deposit amount must be positive.")
        else:
            self.__balance += amount
            print(f"Deposited {amount} ETB.")

    def withdraw(self, amount):
        if amount <= 0:
            print("Withdrawal amount must be positive.")
        elif amount > self.__balance:
            print("Insufficient balance.")
        else:
            self.__balance -= amount
            print(f"Withdrew {amount} ETB.")


account1 = Account("Natoli", "1001")
account2 = Account("Abel", "1002")

account1.deposit(2000)
account2.deposit(1000)

account1.withdraw(500)
account2.withdraw(1500)

print(account1.owner, "Balance:", account1.balance, "ETB")
print(account2.owner, "Balance:", account2.balance, "ETB")