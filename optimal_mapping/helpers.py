# python 3.8.0
import csv


def get_csv_content(csv_file):
    with open(csv_file, "r") as file:
        reader = csv.DictReader(file)
        return [row for row in reader]
