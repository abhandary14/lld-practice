"""
LLD Problem: Pizza Ordering System

Design a pizza ordering system.

Customers should be able to view available pizzas, customize a pizza,
add one or more pizzas to an order, and place the order.

Different pizzas may have different sizes, toppings, and prices.

The system should calculate the total cost of the order based on the
selected pizzas and customizations.

An order should keep track of its current state and should support
cancellation when appropriate.

Assume payment can be handled as part of placing the order.

Assume the system runs in memory for now.

Keep the first version simple. Do not add delivery tracking, restaurant
chains, databases, or external payment integrations unless they become
necessary.

You may ask clarification questions before defining the scope and design.
"""

# start time -> 10:11 PM
# finish time -> 11:55 PM
"""
Pizza  system 
-> User can build their own pizza,
-> The pizza needs to be added to the order and cost calculated

class Crust(Enum): -> tuple of (price, name/number)
    thin, stuffed, hand-tossed

class Size(Enum):
    small, medium, large

class Toppings(Enum):
    pepperoni, pineapple, green pepper, banana pepper, feta cheese

class Sauce(Enum):
    marinara, garlic, alfredo


class Pizza:
    init: default medium marinara cheese(bool) hand-tossed

    # build_pizza() -> instead of this, we can implement multiple methods for customizability
    -> set_crust()
    -> modify_size()
    -> add_toppings()
    -> change_sauce()

    calculate_price()
    show_details()



# only take card payment for now, charging 2% on base price
class Payment:
    init: tip, amount, charge (hardcoded value)

    process_payment()
    cancel_payment()
    

class Order:
    init: order_id, items
    add_item(pizza)
    
    place_order()
    
    process_order()
    calculate_total()
    print_receipt()

    cancel_order()
"""

from enum import Enum
from typing import List, Set

class Size(Enum):
    SMALL = (8, "small")
    MEDIUM = (10, "medium")
    LARGE = (12, "large")

    def __init__(self, price, name):
        self.price = price
        self.display_name = name

class Crust(Enum):
    THIN = (0, "thin crust") # literally less dough they shouldn't charge more for a thin crust
    HAND_TOSSED = (0, "hand tossed") # price 0 as it is default
    STUFFED = (2.5, "stuffed")

    def __init__(self, price, name):
        self.price = price
        self.display_name = name

class Toppings(Enum):
    PEPPERONI = (1, "pepperoni")
    GREEN_PEPPER = (1, "green pepper")
    BANANA_PEPPER = (1, "banana pepper")
    PINEAPPLE = (1, "pineapple")
    ONION = (1, "onion")
    FETA = (1, "feta")
    MUSHROOM = (1, "mushroom")

    def __init__(self, price, name):
        self.price = price
        self.display_name = name

class Sauce(Enum):
    MARINARA = (0, "marinara") # default
    GARLIC = (1, "garlic")
    ALFREDO = (1, "alfredo")

    def __init__(self, price, name):
        self.price = price
        self.display_name = name

class Cut(Enum):
    SQUARE = (16, "square cut") # make only available on thin crust and large
    SIX = (6, "six")
    EIGHT = (8, "eight")

    def __init__(self, pieces, name):
        self.pieces = pieces
        self.display_name = name

# ---
class Pizza:
    def __init__(self, cheese: bool):
        self.size = Size.MEDIUM
        self.crust = Crust.HAND_TOSSED
        self.sauce = Sauce.MARINARA
        self.toppings: Set = set()
        self.cut = Cut.SIX
        self.cheese = cheese

    def set_size(self, size: Size):
        self.size = size

    def set_crust(self, crust: Crust):
        self.crust = crust

    def set_sauce(self, sauce: Sauce):
        self.sauce = sauce

    def add_topping(self, topping: Toppings):
        self.toppings.add(topping)

    def set_cut(self, cut: Cut):
        if cut == Cut.SQUARE and (self.crust != Crust.THIN or self.size != Size.LARGE):
            raise ValueError("Square cut only available on large thin-crust pizzas")

        self.cut = cut

    def calculate_price(self):
        price = self.size.price + self.crust.price + self.sauce.price
        for topping in self.toppings:
            price += topping.price

        return round(price, 2)
    
    def show_details(self):
        return f"{self.size}, {self.crust}, {self.sauce}, {self.toppings}, Cheese: {self.cheese}" # can build a better summary

# only card payment
class Payment:
    def __init__(self, amount, tip=0):
        self.card_charge_percentage = 2 # fix hard-coded percentage 
        self.tax_percentage = 3
        self.tip = tip
        self.amount = amount
        self.completed = False

        self.subtotal = 0
        self.tax = 0
        self.card_fee = 0

    def calculate_total(self):
        self.tax = self.amount * self.tax_percentage / 100
        self.subtotal = self.amount + self.tax + self.tip
        self.card_fee = self.subtotal * self.card_charge_percentage / 100

        total = self.subtotal + self.card_fee
        return total
    
    def process_payment(self):
        if self.completed:
            raise ValueError("Payment already processed.")
        
        total = self.calculate_total()
        self.completed = True
        return f"Payment of ${round(total, 2)} processed."

    def cancel_payment(self):
        if self.completed:
            raise ValueError("Payment already processed.")

        self.completed = False
        return f"Payment canceled."

    def get_payment_details(self):
        total = self.calculate_total()
        return f"{self.amount} + {self.tax} + {self.tip} -> {self.subtotal} + {self.card_fee} -> {total}"


import uuid
class Order:
    def __init__(self):
        self.order_id = uuid.uuid4()
        self.items: List[Pizza] = []
        self.payment = None
        self.placed = False

    def add_pizza(self, pizza: Pizza):
        if self.placed:
            raise ValueError("Can't modify order after being placed")
        
        self.items.append(pizza)

    def calculate_total(self):
        total = sum(pizza.calculate_price() for pizza in self.items)
        return total

    def place_order(self, payment: Payment):
        if not self.items:
            raise ValueError("Can't place an empty order.")

        if self.placed:
            raise ValueError("Order already placed.")

        # ChatGPT suggestion [
        amount = self.calculate_total()
        if payment.amount != amount:
            raise ValueError("Payment amount does not match order total")
        # ]

        self.payment = payment
        payment_result = self.payment.process_payment()

        self.placed = True
        return f"Order placed. {payment_result}"

    def cancel_order(self):
        if self.placed:
            raise ValueError("Order already placed.")

        if self.payment is not None:
            self.payment.cancel_payment()
            self.payment = None
        self.items = []

        return "Order canceled."

    def get_order_summary(self):
        summary = f"Order ID: {self.order_id}\n"
                
        for pizza in self.items:
            summary += f"{pizza.show_details()}\n"

        return summary

    def get_receipt(self):
        if not self.placed:
            raise ValueError("Order has not been placed.")

        if self.payment is None:
            raise ValueError("Payment method not set.")

        payment_details = self.payment.get_payment_details()
        summary = self.get_order_summary()
        receipt = summary + f"\n{payment_details}"

        return receipt

# ---

def main():
    try:
        order = Order()
        pizza = Pizza(cheese=True)
        pizza.set_crust(Crust.THIN)
        pizza.set_size(Size.LARGE)
        pizza.add_topping(Toppings.PEPPERONI)
        pizza.set_cut(Cut.SQUARE)

        order.add_pizza(pizza)
        order.add_pizza(pizza)

        print("Order details:", order.get_order_summary())
        
        amount = order.calculate_total()

        payment = Payment(amount=amount, tip=5)

        order.place_order(payment=payment)

        print(order.get_receipt())
    except ValueError as e:
        print(e)

# ChatGPT -> one thing to keep in mind here is that a pizza can be customized after an order is placed. or even, an order can be modified after it is placed, which should not happen.

# Me -> in an interview setting, it may (probably) be safe to assume that we won't need to implement that, but it is a good extensibiltiy measure for production environments. In an interview setting, payment could also be skipped.

if __name__ == "__main__":
    main()