# python 3.8.0
import csv
from collections import namedtuple
from typing import List

from geopy.distance import distance

Cargo = namedtuple("Cargo", ["product", "latitude", "longitude"])
Truck = namedtuple("Truck", ["truck", "latitude", "longitude"])


def get_cargos(csv_file: str) -> List[Cargo]:
    with open(csv_file, "r") as file:
        reader = csv.DictReader(file)
        return [Cargo(row["product"], row["origin_lat"], row["origin_lng"]) for row in reader]


def get_trucks(csv_file: str) -> List[Truck]:
    with open(csv_file, "r") as file:
        reader = csv.DictReader(file)
        return [Truck(row["truck"], row["lat"], row["lng"]) for row in reader]


def get_distance_between(cargo, truck):
    return distance((cargo.latitude, cargo.longitude), (truck.latitude, truck.longitude)).km
