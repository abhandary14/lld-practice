"""
Design a parking lot system.
"""

"""
Questions:
1. What does the parking lot system do? -> allows for parking of vehicles and any other functional requirements
 - assuming only one vehicle can enter and exit at one time.

2. What does the parking lot state represent at any given moment -> number of parked vehicles, number of vacant spots

3. It should allow for how many types of vehicles? let's assume 2 -> big, and small. big include trucks, and small include car and motorcycle.


Functional Requirements:
Parking Lot:
store parking spots, will be fixed as most real-world parking lots have fixed size
allow for vehicle to enter (reserve a spot)
allow for vehicle to park (actually park, ask for how many hours, and calculate charge)
allow for vehicle to exit (make the spot available)

Parking Spot:
store id
store type
store state
allow for it to be reserved/parked/vacated
allow for revealing which type it is (big/small)

Vehicle: parent for vehicles
store information like type and identifier (license plate)

Car, Motorcycle, Truck: vehicle child class
initialize with type and identifier using super

"""
from enum import Enum

class VehicleType(Enum):
    MOTORCYCLE = 1
    CAR = 2
    TRUCK = 3

class SpotType(Enum):
    SMALL = 1
    BIG = 2

class SpotState(Enum):
    AVAILABLE = 0
    RESERVED = 1
    PARKED = 2

# ---

# doesn't need to be abc
class Vehicle:
    def __init__(self, license_plate, vehicle_type):
        self.license_plate = license_plate
        self.vehicle_type = vehicle_type

class Motorcycle(Vehicle):
    def __init__(self, license_plate):
        super().__init__(license_plate, VehicleType.MOTORCYCLE)

class Car(Vehicle):
    def __init__(self, license_plate):
        super().__init__(license_plate, VehicleType.CAR)

class Truck(Vehicle):
    def __init__(self, license_plate):
        super().__init__(license_plate, VehicleType.TRUCK)

# ---

class ParkingSpot:
    def __init__(self, spot_id, spot_type):
        self.spot_id = spot_id
        self.spot_type = spot_type
        self.spot_state = SpotState.AVAILABLE
        self.vehicle = None

    def can_accept(self, vehicle: Vehicle):
        if self.spot_state != SpotState.AVAILABLE:
            return False

        if self.spot_type == SpotType.SMALL:
            return vehicle.vehicle_type in {
                VehicleType.CAR,
                VehicleType.MOTORCYCLE
            }

        if self.spot_type == SpotType.BIG:
            return vehicle.vehicle_type == VehicleType.TRUCK

        return False

    def reserve_spot(self, vehicle: Vehicle):
        if not self.can_accept(vehicle):
            raise Exception("Spot can't accept this vehicle")

        self.spot_state = SpotState.RESERVED
        self.vehicle = vehicle 

    def park_vehicle(self):
        if self.spot_state == SpotState.RESERVED:
            self.spot_state = SpotState.PARKED
        else:
            raise Exception("Invalid parking requested")

    def vacate_spot(self):
        if self.spot_state == SpotState.RESERVED or self.spot_state == SpotState.PARKED:
            self.spot_state = SpotState.AVAILABLE
            self.vehicle = None
        else:
            raise Exception("Spot not reserved or parked")

# ---

class ParkingLot:
    def __init__(self, small_capacity, big_capacity):
        if small_capacity < 0 or big_capacity < 0:
            raise Exception("Parking lot must have at least 0 slots.")
        
        self.parking_spots = []
        self.rate = 5.0 # $5.0 per hour

        i = 0
        while i < small_capacity:
            self.parking_spots.append(ParkingSpot(i, SpotType.SMALL))
            i += 1

        while i < big_capacity + small_capacity:
            self.parking_spots.append(ParkingSpot(i, SpotType.BIG))
            i += 1

    def enter(self, vehicle: Vehicle):
        for spot in self.parking_spots:
            if spot.vehicle is not None and vehicle.license_plate == spot.vehicle.license_plate:
                raise Exception("Vehicle already exists in parking lot")

        for spot in self.parking_spots:
            if spot.can_accept(vehicle):
                spot.reserve_spot(vehicle)
                return spot

        raise Exception("No compatible parking spot available")

    def park(self, vehicle: Vehicle, hours: int):
        if hours <= 0:
            raise Exception("Parking duration must be positive.")

        for spot in self.parking_spots:
            if (spot.vehicle is not None) and (spot.spot_state == SpotState.RESERVED) and (spot.vehicle.license_plate == vehicle.license_plate):
                spot.park_vehicle()
                charge = hours * self.rate
                return f"Vehicle parked, please pay ${charge}"
            
        raise Exception("Vehicle can't be parked")

    def leave(self, vehicle: Vehicle):
        for spot in self.parking_spots:
            if spot.vehicle is not None and spot.vehicle.license_plate == vehicle.license_plate and spot.spot_state in {SpotState.RESERVED, SpotState.PARKED}:
                spot.vacate_spot()
                return f"Parking Spot {spot.spot_id} vacated."

        raise Exception("Vehicle not in parking spot")
