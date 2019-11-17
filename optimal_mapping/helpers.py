# python 3.8.0
import csv
from collections import namedtuple

from geopy.distance import distance

Cargo = namedtuple("Cargo", ["product", "city", "state", "latitude", "longitude"])
Truck = namedtuple("Truck", ["truck", "latitude", "longitude"])


def get_cargo(csv_file):
    with open(csv_file, "r") as file:
        reader = csv.DictReader(file)
        return [
            Cargo(
                row["product"], row["origin_city"], row["origin_state"], row["origin_lat"], row["origin_lng"]
            )
            for row in reader
        ]


def get_trucks(csv_file):
    with open(csv_file, "r") as file:
        reader = csv.DictReader(file)
        return [Truck(row["truck"], row["lat"], row["lng"]) for row in reader]


def get_distance_between(cargo, truck):
    return distance((cargo.latitude, cargo.longitude), (truck.latitude, truck.longitude)).km
