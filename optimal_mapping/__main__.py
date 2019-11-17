from pathlib import Path

from .mapping import map_best_combinations

project_dir = Path(__file__).absolute().parents[1]
csv_dir = project_dir / "csv_files"
cargos_csv = csv_dir / "cargo.csv"
trucks_csv = csv_dir / "trucks.csv"

map_best_combinations(cargos_csv, trucks_csv)
