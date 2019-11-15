from optimal_mapping.helpers import get_cargos, get_distance_between, get_trucks


def get_matrix(cargos_csv, trucks_csv):
    cargos = get_cargos(cargos_csv)
    trucks = get_trucks(trucks_csv)

    matrix = []

    for truck in trucks:
        row = []
        for cargo in cargos:
            row.append(get_distance_between(cargo, truck))
        matrix.append(row)

    return matrix
