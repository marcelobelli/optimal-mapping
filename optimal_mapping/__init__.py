# python 3.8.0
from optimal_mapping.analyzer import RouteAnalyzer


def get_best_combination(cargo_csv, trucks_csv):
    route_combinations = RouteAnalyzer.make_routes_combination(cargo_csv, trucks_csv)

    for truck, load in route_combinations.items():
        print(f"* {truck.truck} is the truck chosen to get {load.product} from {load.city}, {load.state}")
