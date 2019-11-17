# python 3.8.0
from optimal_mapping.analyzer import RouteAnalyzer
from optimal_mapping.helpers import get_cargos, get_distance_between, get_trucks


def map_best_combinations(cargos_csv, trucks_csv):
    cargos = get_cargos(cargos_csv)
    trucks = get_trucks(trucks_csv)

    distance_matrix = [[get_distance_between(cargo, truck) for cargo in cargos] for truck in trucks]
    analyzer = RouteAnalyzer(distance_matrix)
    best_combinations = analyzer.get_combinations()

    for t, c in best_combinations:
        truck = trucks[t]
        cargo = cargos[c]
        print(f"* {truck.truck} is the truck chosen to get {cargo.product} from {cargo.city}, {cargo.state}")
