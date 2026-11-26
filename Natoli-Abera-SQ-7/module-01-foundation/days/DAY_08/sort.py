class Account:
    def __init__(self, account_number, balance=0):
        self.account_number = account_number
        self.balance = balance
        self.history = []  # Stack of transactions

    def deposit(self, amount):
        self.balance += amount
        self.history.append(("deposit", amount))

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.history.append(("withdraw", amount))
        else:
            raise ValueError("Insufficient funds")

    def undo_last(self):
        if not self.history:
            print("No transactions to undo.")
            return

        action, amount = self.history.pop()

        if action == "deposit":
            self.balance -= amount
        elif action == "withdraw":
            self.balance += amount

    def statement(self):
        return f"Account {self.account_number}: Balance = {self.balance}"


class SavingsAccount(Account):
    def __init__(self, account_number, balance=0, rate=0.01):
        super().__init__(account_number, balance)
        self.rate = rate

    def add_interest(self):
        interest = self.balance * self.rate
        self.deposit(interest)


class CurrentAccount(Account):
    def __init__(self, account_number, balance=0, overdraft=0):
        super().__init__(account_number, balance)
        self.overdraft = overdraft

    def withdraw(self, amount):
        if self.balance + self.overdraft >= amount:
            self.balance -= amount
            self.history.append(("withdraw", amount))
        else:
            raise ValueError("Overdraft limit exceeded")


class AccountRegistry:
    def __init__(self):
        self.accounts = {}

    # O(1)
    def add(self, account):
        self.accounts[account.account_number] = account

    # O(1)
    def find(self, account_number):
        return self.accounts.get(account_number)

    def list_all(self):
        for number in sorted(self.accounts):
            print(self.accounts[number].statement())

    # ---------- Day 8 ----------

    # 1. Leaderboard
    def top_by_balance(self, n):
        return sorted(
            self.accounts.values(),
            key=lambda acc: acc.balance,
            reverse=True
        )[:n]

    # 2. Binary Search
    def binary_search(self, numbers, target):
        left = 0
        right = len(numbers) - 1

        while left <= right:
            mid = (left + right) // 2

            if numbers[mid] == target:
                return mid
            elif numbers[mid] < target:
                left = mid + 1
            else:
                right = mid - 1

        return -1

    def find_by_number(self, account_number):
        numbers = sorted(self.accounts.keys())
        index = self.binary_search(numbers, account_number)

        if index == -1:
            return None

        return self.accounts[numbers[index]]

    # 3. Recursive total transactions
    def total_transactions(self, history):
        if not history:
            return 0
        return history[-1][1] + self.total_transactions(history[:-1])


# ---------------- Main ----------------

if __name__ == "__main__":
    registry = AccountRegistry()

    a1 = SavingsAccount("1001", 1500, 0.05)
    a2 = CurrentAccount("1002", 800, 300)
    a3 = Account("1003", 2500)

    registry.add(a1)
    registry.add(a2)
    registry.add(a3)

    a1.deposit(500)
    a1.withdraw(200)

    a2.deposit(300)
    a2.withdraw(400)

    a3.deposit(1000)

    print("=== Leaderboard ===")
    for acc in registry.top_by_balance(2):
        print(acc.statement())

    print("\n=== Binary Search ===")
    result = registry.find_by_number("1002")
    if result:
        print(result.statement())

    print("\n=== Total Transactions ===")
    print(registry.total_transactions(a1.history))