# python 3.8.0
from geopy import distance

from optimal_mapping.helpers import Cargo, Truck, get_cargo, get_distance_between, get_trucks


def test_get_cargos(cargo_csv, cargo):
    result = get_cargo(cargo_csv)
    assert result == cargo


def test_get_trucks(trucks_csv, trucks):
    result = get_trucks(trucks_csv)
    assert result == trucks


def test_get_distance_between():
    cargo = Cargo("Light bulbs", "Sikeston", "MO", "36.876719", "-89.5878579")
    truck = Truck("Viking Products Of Austin Incustin", "36.6634467", "-87.47739020000002")
    expected_result = distance.distance(
        (cargo.latitude, cargo.longitude), (truck.latitude, truck.longitude)
    ).km

    assert get_distance_between(cargo, truck) == expected_result
