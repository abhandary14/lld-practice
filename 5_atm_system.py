"""
LLD Problem: ATM System

Design an ATM system.

A user should be able to insert a card, authenticate, view account
information, withdraw cash, and deposit money.

The ATM should keep track of the cash available inside the machine and
should not allow withdrawals that cannot be fulfilled.

A transaction should only be allowed after successful authentication.

The system should support canceling the current session before a
transaction is completed.

Assume the banking backend can be represented in memory for now.

Keep the first version reasonably simple. Do not add networking,
real card readers, hardware integrations, databases, or multiple banks
unless they become necessary.

You may ask clarification questions before defining the scope and design.
"""

# start_time: 3:15, end_time: 5:00
"""
User:
- name
- has-a Card

Card
- card number # set while define time
- expiry # set while define time
- PIN # set while define time (can be calculated as well as 5 years from today's date but not for now)

- has-a Account

Account
- acc number
- balance

- get_details()
- add_money()
- deduct_money()

ATM
- cash # has to be in multiples of 10
- min_withdrawal
- current_card
- current_account
- authenticated:T/F

- authenticate_user()
- insert_card()
- deposit_money() # has to be in multiples of 10
- withdraw_money() # minimum withdrawal amount has to match and can't exceed account balance, and not exceed atm cash
- remove_card()

# for now, let's assume that the atm only dispenses money in denominations of $10.
"""

from datetime import date

class Account:
    def __init__(self, user_name: str, number: str, balance: int):
        if balance < 0:
            raise ValueError("Balance can't be less than zero")
        
        self.user_name = user_name
        self.number = number
        self.balance = balance

    def get_details(self):
        res = f"Account holder name: {self.user_name}\nAccount number: {self.number}\nAvailable balance: {self.balance}"
        return res

    def add_money(self, amount):
        if amount <= 0:
            raise ValueError("Amount can't be negative or zero.")
        self.balance += amount

    def deduct_money(self, amount):
        if amount <= 0:
            raise ValueError("Amount can't be negative or zero.")
        if amount > self.balance:
            raise ValueError("Not enough balance in account.")
        
        self.balance -= amount

class Card:
    def __init__(self, number: str, expiry: date, pin: int, account: Account):
        self.number = number
        self.expiry = expiry
        self.pin = pin
        self.account = account

    def get_details(self):
        res = f"Card number: {self.number}\nExpiry: {self.expiry}\n"
        account_details = self.account.get_details()
        res += f"{account_details}\n"
        return res

class ATM:
    def __init__(self, cash, min_withdrawal: int):
        if cash <= 0:
            raise ValueError("Available cash must be greater than zero.")
        if cash % 10 != 0:
            raise ValueError("Available cash must be in multiples of 10.") 

        if min_withdrawal <= 0:
            raise ValueError("Minimum withdrawal threshold must be postitive and multiple of 10.")
        if min_withdrawal % 10 != 0:
            raise ValueError("Minimum withdrawal threshold must be multiple of 10.")
         
        self.cash = cash
        self.min_withdrawal = min_withdrawal
        self.current_card = None
        self.current_account = None
        self.authenticated = False

    def insert_card(self, card: Card):
        if self.current_card is None:
            self.current_card = card
        else:
            raise ValueError("Card already inserted.")
    
    def authenticate_user(self, pin: int):
        if self.current_card is not None:
            if self.current_card.pin == pin:
                self.authenticated = True
                self.current_account = self.current_card.account
            else:
                raise ValueError("Wrong pin!")
        else:
            raise ValueError("No card entered.")

    def withdraw_money(self, amount):
        if self.authenticated:
            if amount % 10 != 0:
                raise ValueError("Amount has to be multiple of 10.")
            
            if amount > self.cash:
                raise ValueError("Amount can't exceed available cash.")

            if amount < self.min_withdrawal:
                raise ValueError(f"Withdrawal amount can't be less than {self.min_withdrawal}.")
        
            if self.current_card.expiry < date.today():
                raise ValueError("Card Expired!")

            self.current_account.deduct_money(amount)
            self.cash -= amount
            
            print(f"{amount} {self.current_account.balance} {self.cash}")
        else:
            raise ValueError("User not authenticated.")

    def deposit_money(self, amount):
        if self.authenticated:
            if amount % 10 != 0:
                raise ValueError("Amount has to be multiple of 10.")

            if self.current_card.expiry < date.today():
                raise ValueError("Card Expired!")
    
            self.current_account.add_money(amount)
            self.cash += amount

            print(f"{amount} {self.current_account.balance} {self.cash}")
        else:
            raise ValueError("User not authenticated.")

    def remove_card(self):
        self.current_account = None
        self.current_card = None
        self.authenticated = False

    def get_user_details(self):
        if not self.authenticated:
            raise ValueError("User not authenticated.")
        
        if self.current_card is not None:
            return self.current_card.get_details()
        raise ValueError("No card inserted")


def main():
    try:
        atm = ATM(cash=5000, min_withdrawal=20)
        account = Account(user_name="Alice", number="100200", balance=400)
        card = Card(account=account, expiry=date(year=2026,month=11,day=14), number="1234-5678-9012-3456", pin=1000)


        atm.insert_card(card)
        atm.authenticate_user(1000)
        # atm.deposit_money(300)
        
        # print(atm.get_user_details())
        
        atm.withdraw_money(500)
        atm.remove_card()
        
        print(atm.get_user_details())
    except ValueError as e:
        print(e)
    finally:
        print(atm.cash)

if __name__ == "__main__":
    main()