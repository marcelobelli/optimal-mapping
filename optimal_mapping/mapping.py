# python 3.8.0
from copy import deepcopy

from geopy.distance import distance

from optimal_mapping.helpers import get_csv_content

def get_distance_between(cargo: dict, truck: dict) -> float:
    return distance((cargo["origin_lat"], cargo["origin_lng"]), (truck["lat"], truck["lng"])).km


def mapping(cargos_csv, trucks_csv):
    cargos_data = get_csv_content(cargos_csv)
    trucks_data = get_csv_content(trucks_csv)










# def mapping(cargos: list, trucks: list):



# Pra cada cargo faco o sorted dos trucks
# .get no result, voltou pego o cargo e confiro qual dos dois conpensa ir com qual caminhão
# Lembrando do caso.
# C1 -> 5 -> P1
# C1 -> 4 -> P2
# C2 -> 10 -> P1
# C3 -> 5 -> P2
# Compensa mais C1 -> P1, C3 -> P2, totalizando 10 km