deps:
	pip install -r requirements.txt

test:
	pytest -v

run:
	python -m optimal_mapping
