import json


class BankAccount:

    UNKNOWN = {
        "Account Number": None,
        "Balance": None,
        "Transactions": []
    }

    def __init__(self, __account_number: str, __balance: int = 0) -> None:
        if self.check_account_number(__account_number, 'info.json'):
            self.__account_number = __account_number
            self.__balance = __balance
            self.transactions: list[int] = []

            self.add_in_json("info.json")
        else:
            raise Exception("Account Already exist.")

    def add_in_json(self, file_name):
        with open(file_name, 'r') as file:
            self.UNKNOWN["Account Number"] = self.__account_number
            self.UNKNOWN["Balance"] = self.__balance
            self.UNKNOWN["Transactions"] = self.transactions

            result = json.load(file)
            result.append(self.UNKNOWN)

        with open(file_name, 'w') as file:
            json.dump(result, file, indent=4)

    def deposit(self, amount: int) -> None:
        self.__balance += amount
        self.transactions.append(f"Deposit: +${amount}")
        self.save(self.__account_number, self.__balance, self.transactions)

    def withdraw(self, amount: int) -> None:
        if self.__balance >= amount:
            self.__balance -= amount
            self.transactions.append(f"Withdraw: -${amount}")
            self.save(self.__account_number, self.__balance, self.transactions)
        else:
            raise Exception("Not Enough Founds.")

    def transfer(self, account: object, amount: int) -> None:
        if self.__balance >= amount:

            self.__balance -= amount
            self.transactions.append(
                f"Transfer to ({account.__account_number}): -${amount}")

            account.__balance += amount
            account.transactions.append(f"Deposit: +${amount}")
            self.save(self.__account_number, self.__balance, self.transactions)

        else:
            raise Exception("Not Enough Founds.")

    def generate_statement(self) -> str:
        return '\n'.join(self.transactions)

    def get_balance(self) -> int:
        return self.__balance

    def clear_transactions(self) -> None:
        self.transactions.clear()

    @staticmethod
    def save(account_number, balance, transactions):
        with open('info.json', 'r') as file:
            result = json.load(file)
        for account in result:
            if account["Account Number"] == account_number:
                account["Balance"] = balance
                account["Transactions"] = transactions

        with open('info.json', 'w') as file:
            json.dump(result, file, indent=4)

    @staticmethod
    def check_account_number(account_number, file_name):
        with open(file_name, 'r') as file:
            result = json.load(file)
        account_numbers = []
        for account in result:
            account_numbers.append(account["Account Number"])

        return account_number not in account_numbers


account1 = BankAccount('1', 10000)
account2 = BankAccount('2', 20000)

account1.deposit(10000)
account1.withdraw(9999)
account2.transfer(account1, 20000)

# ___________________________________________________________________
# account1.deposit(10000)
# print(account1.get_balance())
# print(account1.generate_statement())
# account1.withdraw(99999)
# print(account1.get_balance())
# print(account1.generate_statement())

# account2.transfer(account1 , 20000)

# print(account2.get_balance())
# print(account2.generate_statement())
# print(account1.generate_statement())
# print(account1.get_balance())

# _____________________________________________________________________________________
