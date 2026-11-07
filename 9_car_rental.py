"""
LLD Problem: Car Rental System

Design a car rental system.

Customers should be able to request a car, reserve one if available,
pick it up, and return it.

The system should support multiple categories of cars with different
rental pricing.

A car should not be assigned to more than one active rental at a time.

The system should keep track of the rental lifecycle and calculate the
final rental cost when the car is returned.

Customers should also be able to cancel a reservation before pickup.

Assume the system runs in memory for now.

Keep the first version reasonably simple. Do not add databases, payment
gateways, insurance systems, GPS tracking, or multiple branches unless
they become necessary.

You may ask clarification questions before defining the scope and design.
"""

"""
CarState:
    - AVAILABLE
    - PICKEDUP
    - RESERVED
Car: car_id, make, model, year, daily_rate, is_available: CarState
User: user_id, name
Store: store_id, location, fleet
    - add_car()
    - get_available_cars()
    - remove_car()
Reservation: reservation_id, user: User, car: Car, reserved_date, pick_up_date, end_date
    - calculate_cost()
RentalSystem: users: list[User], stores: list[Store], reservations: list[Reservations], _next_reservation_id
    - add_user()
    - remove_user()
    - add_store()
    - remove_store()
    - search_cars(store_location == any store.location)
    - make_reservation()
    - pick_up_car()
    - cancel_reservation()
    - return_car() 
"""

from datetime import datetime
from enum import Enum

class Car:
    def __init__(self, car_id: str, make: str, model: str, year: str, rate: float) -> None:
        self.car_id = car_id
        self.make = make
        self.model = model
        self.year = year
        self.rate = rate

        self.availability = True

    def get_details(self) -> str:
        return f"Make: {self.make}, Model: {self.model}, Year: {self.year}, Daily Rate: {self.rate}"

class User:
    def __init__(self, user_id: int, name: str) -> None:
        self.user_id = user_id
        self.name = name

class Store:
    def __init__(self, store_id: int, location: str) -> None:
        self.store_id = store_id
        self.location = location
        self.cars = []

    def add_car(self, car: Car) -> None:
        if car in self.cars:
            raise ValueError("Car already present in fleet.")

        self.cars.append(car)

    def remove_car(self, car: Car) -> None:
        if car not in self.cars:
            raise ValueError("Car not in fleet.")

        self.cars.remove(car)

    def get_available_cars(self) -> list:
        return [c for c in self.cars if c.availability==True]

class ReservationState(Enum):
    RESERVED = 1
    PICKED_UP = 2
    CANCELLED = 3
    COMPLETED = 4
    ABANDONED = 5

class Reservation:
    def __init__(self, res_id: int, user: User, car: Car, start_date, end_date):
        self.res_id = res_id
        self.user = user
        self.car = car
        self.start_date = start_date
        self.end_date = end_date

        self.reservation_state = ReservationState.RESERVED # initialize to reserved as we only create a Reservation object when a car is reserved

    def calculate_cost(self) -> float:
        return (self.end_date - self.start_date).days * self.car.rate

class RentalSystem:
    def __init__(self) -> None:
        self.users = []
        self.stores = []
        self.reservations = [] # entire reservation history

        self._next_reservation_id = 1

    def add_user(self, user: User) -> None:
        if user in self.users:
            raise ValueError("User already present.")

        self.users.append(user)

    def remove_user(self, user: User) -> None:
        if user not in self.users:
            raise ValueError("User not present.")

        self.users.remove(user)

    def add_store(self, store: Store) -> None:
        if store in self.stores:
            raise ValueError("Store already added")

        self.stores.append(store)

    def remove_store(self, store: Store) -> None:
        if store not in self.stores:
            raise ValueError("Store not in list")

        self.stores.remove(store)

    def search_cars(self, store_location: str) -> list:
        for store in self.stores:
            if store.location.lower() == store_location.lower():
                return store.get_available_cars()

        return []

    def make_reservation(self, user: User, car: Car, start_date, end_date) -> (float, Reservation):
        if car.availability != True:
            raise ValueError("Car not available for selected dates")

        car.availability = False
        reservation = Reservation(
                self._next_reservation_id,
                user,
                car,
                start_date,
                end_date
            )
        self.reservations.append(reservation)
        self._next_reservation_id += 1
        
        cost = reservation.calculate_cost()

        return (cost, reservation)

    def cancel_reservation(self, reservation: Reservation) -> str:
        if reservation.reservation_state == ReservationState.PICKED_UP:
            raise ValueError("Cannot cancel reservation after picking the car up.")

        if reservation.reservation_state != ReservationState.RESERVED:
            raise ValueError("Car not reserved.")

        reservation.reservation_state = ReservationState.CANCELLED
        reservation.car.availability = True

        return f"Reservation {reservation.res_id} successfully cancelled."

    def pick_up_car(self, reservation: Reservation, current_date) -> str:
        if reservation.reservation_state != ReservationState.RESERVED:
            raise ValueError("Reservation either completed or cancelled")

        if current_date < reservation.start_date:
            raise ValueError("Can't pick up before start date")

        if current_date > reservation.end_date:
            reservation.reservation_state = ReservationState.ABANDONED
            reservation.car.availability = True

            raise ValueError("Reservation already ended")

        reservation.reservation_state = ReservationState.PICKED_UP
        return f"Car {reservation.car.car_id} picked up successfully"

    def return_car(self, reservation: Reservation) -> str:
        if reservation.reservation_state != ReservationState.PICKED_UP:
            raise ValueError("Car not picked up.")

        reservation.reservation_state = ReservationState.COMPLETED
        reservation.car.availability = True

        return f"Car {reservation.car.car_id} returned."


if __name__ == "__main__":
    system = RentalSystem()

    try:
        user1 = User(1, "Aakash")
        system.add_user(user1)

        store1 = Store(1, "RDU Airport")
        system.add_store(store1)

        car1 = Car("ABC101", "Toyota", "Camry", 2023, 100)
        car2 = Car("ABC102", "Toyota", "Corolla", 2024, 120)

        store1.add_car(car1)
        store1.add_car(car2)

        print("Searching for available cars at RDU Airport")
        available_cars = system.search_cars("rdu airport")
        for c in available_cars:
            print(f"{c.get_details()}")

        # if any cars are available
        if available_cars:
            start = datetime(2026, 11, 7) # YYYY, MM, DD; leading zeros not allowed
            end = datetime(2026, 11, 9)

            cost, reservation = system.make_reservation(
                    user1, available_cars[0], start, end
                )

            # if it was successful
            if reservation:
                print(f"Reservation successful for {user1.name}")
                print(f"Car: {reservation.car.make} {reservation.car.model}")
                print(f"Total Cost: ${cost:.2f}")

            # res = system.cancel_reservation(reservation)
            # print(res)

            res = system.pick_up_car(reservation, current_date=datetime(2026, 11, 8))
            print(res)

            res = system.return_car(reservation)
            print(res)


    except ValueError as e:
        print(e)