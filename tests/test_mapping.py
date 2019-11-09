from optimal_mapping.mapping import get_distance_between


def test_get_distance_between():
    cargo_data = {
        "product": "Light bulbs",
        "origin_lat": "36.876719",
        "origin_lng": "-89.5878579",
    }
    truck_data = {
        "truck": "Hartford Plastics Incartford",
        "lat": "34.79981",
        "lng": "-87.677251",
    }

    assert get_distance_between(cargo_data, truck_data) == 287.9114022038136
