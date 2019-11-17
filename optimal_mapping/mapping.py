# python 3.8.0
from optimal_mapping.analyzer import RouteAnalyzer
from optimal_mapping.helpers import get_cargo, get_distance_between, get_trucks


def map_best_combinations(cargo_csv, trucks_csv):
    cargo = get_cargo(cargo_csv)
    trucks = get_trucks(trucks_csv)

    distance_matrix = [[get_distance_between(load, truck) for load in cargo] for truck in trucks]
    analyzer = RouteAnalyzer(distance_matrix)
    best_combinations = analyzer.get_combinations()

    for t, c in best_combinations:
        truck = trucks[t]
        load = cargo[c]
        print(f"* {truck.truck} is the truck chosen to get {load.product} from {load.city}, {load.state}")
