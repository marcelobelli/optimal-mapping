# python 3.8.0
from pathlib import Path

from optimal_mapping import get_best_combination

project_dir = Path(__file__).absolute().parents[1]
csv_dir = project_dir / "csv_files"
cargos_csv = csv_dir / "cargo.csv"
trucks_csv = csv_dir / "trucks.csv"

get_best_combination(cargos_csv, trucks_csv)
