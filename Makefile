.PHONY: all simulate metrics clean test

export PYTHONPATH := src:$(PYTHONPATH)

all: simulate metrics

simulate:
	@echo "Running simulations..."
	python src/simulation.py

metrics:
	@echo "Generating metrics and figures..."
	python src/metrics.py

test:
	@echo "Running unit tests..."
	pytest tests/tests.py -v

clean:
	@echo "Cleaning simulated data cache..."
	rm -rf data/simulated/*.csv
	rm -rf data/simulated/*.pdf
	rm -rf tests/__pycache__
	rm -rf src/__pycache__