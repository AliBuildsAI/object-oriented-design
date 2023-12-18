from typing import List
import datetime


class Vehicle:
    def __init__(self, size: int):
        self._size = size

    @property
    def size(self) -> int:
        return self._size
    
class Car(Vehicle):
    def __init__(self):
        super().__init__(size=1)

class Limo(Vehicle):
    def __init__(self):
        super().__init__(size=2)

class Truck(Vehicle):
    def __init__(self):
        super().__init__(size=3)

class Driver:
    def __init__(self, vehicle: Vehicle, driver_id: int) -> None:
        self._vehicle = vehicle
        self._id = driver_id
        self._payment_due = 0

    @property
    def vehicle(self) -> Vehicle:
        return self._vehicle
    
    @property
    def driver_id(self) -> int:
        return self._id
    
    def charge(self, price: float) -> None:
        self._payment_due += price


class ParkingFloor:
    def __init__(self, capacity: int):
        self._capacity = capacity
        self._occupancy_map = {}
        self._is_occupied = [False] * capacity
    
    @property
    def capacity(self) -> int:
        return self._capacity
    
    @property
    def occupancy_map(self) -> List[bool]:
        return self._occupancy_map
    
    def park_vehicle(self, vehicle: Vehicle) -> bool:
        left, right = 0, vehicle.size
        while left < self._capacity:
            if right > self._capacity:
                return False
            if self._is_occupied[left]: 
                left += 1
                right += 1
                continue
            for j in range(left+1, right):
                if self._is_occupied[j]:
                    left = j + 1
                    right = j + 1 + vehicle.size
                    continue
            for j in range(left, right):
                self._is_occupied[j] = True
            self._occupancy_map[vehicle] = (left, right-1)
            return True
        return False

    def remove_vehicle(self, vehicle: Vehicle) -> None:
        left, right = self._occupancy_map[vehicle]
        for i in range(left, right+1):
            self._is_occupied = False
        del self._occupancy_map[vehicle]

    @property
    def vehicle_spot(self, vehicle: Vehicle):
        return self._occupancy_map.get(vehicle, False)

class ParkingGarage:
    def __init__(self, num_floors: int, capacity_per_floor: int) -> None:
        self._num_floors = num_floors
        self._parking_garage = [ParkingFloor(capacity_per_floor) for _ in range(num_floors)]
        self._vehicle_floor_map = {}
    def park_vehicle(self, vehicle: Vehicle) -> bool:
        for i in range(len(self._parking_garage)):
            if self._parking_garage[i].park_vehicle(vehicle):
                self._vehicle_floor_map[vehicle] = i
                return True
        return False

    def remove_vehicle(self, vehicle: Vehicle):
        floor_idx = self._vehicle_floor_map[vehicle]
        self._parking_garage[floor_idx].remove_vehicle(vehicle)
        del self._vehicle_floor_map[vehicle]

class ParkingPaymentSystem:
    def __init__(self, parking_garage: ParkingGarage, hourly_rate: int):
        self._parking_garage = parking_garage
        self._hourly_rate = hourly_rate
        self._time_parked = {} # map driver_id to time that they parked

    def park_vehicle(self, driver: Driver) -> bool:
        current_hour = datetime.datetime.now().hour
        if self._parking_garage.park_vehicle(driver.vehicle):
            self._time_parked[driver.driver_id] = current_hour
            return True
        
        else:
            return False

    def remove_vehicle(self, driver: Driver) -> bool:
        if driver.driver_id not in self._time_parked:
            return False
        current_hour = datetime.datetime.now().hour
        price = self._hourly_rate * (current_hour - self._time_parked[driver.driver_id])
        driver.charge(price)
        del self._time_parked[driver.driver_id]
        return True

if __name__ == '__main__':
    parking_garage = ParkingGarage(3, 2)
    parking_payment_system = ParkingPaymentSystem(parking_garage, 5)
    driver1 = Driver(Car(), 1)
    driver2 = Driver(Limo(), 2)
    driver3 = Driver(Truck(), 3)

    print(parking_payment_system.park_vehicle(driver1))      # true
    print(parking_payment_system.park_vehicle(driver2))      # true
    print(parking_payment_system.park_vehicle(driver3))      # false

    print(parking_payment_system.remove_vehicle(driver1))    # true
    print(parking_payment_system.remove_vehicle(driver2))    # true
    print(parking_payment_system.remove_vehicle(driver3))    # false