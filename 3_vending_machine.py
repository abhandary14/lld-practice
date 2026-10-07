"""
LLD Problem: Vending Machine

Design a vending machine system.

The machine should allow a customer to select a product, pay for it,
and receive the product.

The machine contains a limited quantity of different products and
accepts money in predefined denominations. A purchase may require
returning change.

The machine should handle situations where a purchase cannot be
completed, such as insufficient payment, unavailable products, or
inability to provide the required change.

Assume the system runs in memory for now.

You may ask clarification questions before defining the scope and design.
"""

"""
What does a vending machine do -> stores items, accepts payment, dispenses items

What it needs to have:
- Item(name, price)

Inventory:
- Dict[item, quantity]


Payment(ABC)
- calculate_total(base_price) -> cash return base_price, card returns base_price + charge

- CashPayment(Payment) -> expects exact change
    - make_payment
    - cancel_transaction
- CardPayment(Payment)
    - make payment
    - cancel transaction

VendingMachine:
- has-a -> inventory
- user selects item -> check inventory -> show price
- ask user to tap/insert money
- user selects item -> check inventory -> deduct money -> dispense item (update inventory)
- cancel_transaction
- reset state after successful transaction
"""

from typing import Dict
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass(frozen=True)
class Item:
    item_id: str # for example, A001, B001 (not strictly enforced)
    item_name: str
    item_price: float

class Inventory:
    def __init__(self):
        self.items: Dict[str, tuple[Item, int]] = {}

    def add_item(self, item: Item, quantity: int):
        if quantity <= 0:
            raise ValueError("Quantity can't be negative or zero.")

        if item.item_id not in self.items:
            self.items[item.item_id] = (item, quantity)
        else:
            existing_item, existing_quantity = self.items[item.item_id]
            self.items[item.item_id] = (existing_item, existing_quantity + quantity)

    def get_item(self, item_id: str):
        if item_id not in self.items:
            raise ValueError("Item not in inventory")

        stored_item, quantity = self.items[item_id]

        if quantity <= 0:
            raise ValueError("Item out of stock")

        return stored_item
        

    def _remove_item(self, item: Item, quantity: int):
        item_id = item.item_id

        if item_id not in self.items:
            raise ValueError("Item not in inventory.")

        if quantity < 0:
            raise ValueError("Quantity can't be negative.")

        stored_item, current_quantity = self.items[item_id]

        if quantity > current_quantity:
            raise ValueError("Can't remove more items than in inventory.")

        self.items[item_id] = (stored_item, current_quantity - quantity)

    def dispense_item(self, item: Item):
        self._remove_item(item, 1)
        return f"Item {item.item_id} dispensed"

class Payment(ABC):
    @abstractmethod
    def calculate_total(self, base_price):
        pass

    @abstractmethod
    def process_payment(self):
        pass

    @abstractmethod
    def cancel_payment(self):
        pass

class CardPayment(Payment):
    def __init__(self):
        self.charge_percentage = 3
        self.total = None
        self.completed = False

    def calculate_total(self, base_price):
        self.total = base_price + (base_price * self.charge_percentage / 100)
        return self.total

    def process_payment(self):
        if self.total is None:
            raise ValueError("Payment total not calculated")

        self.completed = True
        return True

    def cancel_payment(self):
        if self.completed:
            raise ValueError("Payment already processed")

        self.total = None
        self.completed = False

        return f"Payment canceled"

class CashPayment(Payment):
    def __init__(self, inserted_amount):
        self.inserted_amount = inserted_amount
        self.total = None
        self.completed = False

    def calculate_total(self, base_price):
        self.total = base_price
        return self.total

    def process_payment(self):
        if self.total is None:
            raise ValueError("Payment total not calculated")

        if self.inserted_amount != self.total:
            raise ValueError("Please insert exact amount")

        self.completed = True
        return True

    def cancel_payment(self):
        if self.completed:
            raise ValueError("Payment already processed")

        amount_to_return = self.inserted_amount
        self.inserted_amount = 0
        self.total = None
        self.completed = False
        return f"Payment canceled. Please collect amount ${amount_to_return}"


class VendingMachine:
    def __init__(self):
        self.inventory = Inventory()
        self.selected_item = None
        self.payment = None

    def select_item(self, item_id: str):
        item = self.inventory.get_item(item_id)
        self.selected_item = item
        return f"Price ${item.item_price}"

    def start_payment(self, payment: Payment):
        if self.selected_item is None:
            raise ValueError("No item selected")

        if self.payment is not None:
            raise ValueError("Payment already started")

        self.payment = payment
        total = self.payment.calculate_total(self.selected_item.item_price)

        return total

    def complete_purchase(self):
        if self.selected_item is None:
            raise ValueError("No item selected")
        
        if self.payment is None:
            raise ValueError("Payment not initiated")

        self.payment.process_payment()
        result = self.inventory.dispense_item(self.selected_item)
        self._reset_transaction()
        return result

    def cancel_purchase(self):
        if self.payment is not None:
            cancellation_result = self.payment.cancel_payment()
        else:
            cancellation_result = None

        self._reset_transaction()

        return cancellation_result

    def _reset_transaction(self):
        self.selected_item = None
        self.payment = None

def main():
    vending_machine = VendingMachine()

    try:    
        item1 = Item(item_id="A001", item_name="Protein Bar", item_price=3.0)
        
        vending_machine.inventory.add_item(item=item1, quantity=20)

        # payment = CashPayment(3)
        payment = CardPayment()

        vending_machine.select_item("A001")
        vending_machine.start_payment(payment)
        print(vending_machine.complete_purchase())
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()