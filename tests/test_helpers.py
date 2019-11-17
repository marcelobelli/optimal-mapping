from geopy import distance

from optimal_mapping.helpers import Cargo, Truck, get_cargo, get_distance_between, get_trucks


def test_get_cargos(cargo_csv):
    cargo = get_cargo(cargo_csv)
    expected_cargo = [
        Cargo("Light bulbs", "Sikeston", "MO", "36.876719", "-89.5878579"),
        Cargo("Apples", "Columbus", "OH", "39.9611755", "-82.99879419999999"),
    ]

    assert cargo == expected_cargo


def test_get_trucks(trucks_csv):
    trucks = get_trucks(trucks_csv)
    expected_trucks = [
        Truck("Viking Products Of Austin Incustin", "36.6634467", "-87.47739020000002"),
        Truck("Kjellberg'S Carpet Oneuffalo", "40.3933956", "-82.4857181"),
    ]

    assert trucks == expected_trucks


def test_get_distance_between():
    cargo = Cargo("Light bulbs", "Sikeston", "MO", "36.876719", "-89.5878579")
    truck = Truck("Viking Products Of Austin Incustin", "36.6634467", "-87.47739020000002")
    expected_result = distance.distance((cargo.latitude, cargo.longitude), (truck.latitude, truck.longitude)).km

    assert get_distance_between(cargo, truck) == expected_result
