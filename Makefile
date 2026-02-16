.PHONY: venv install lint format test run docker-build docker-run k8s-apply download-model benchmark clean

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
UVICORN := $(VENV)/bin/uvicorn
PYTEST := $(VENV)/bin/pytest
RUFF := $(VENV)/bin/ruff

venv:
	if [ ! -d "$(VENV)" ]; then python3 -m venv $(VENV); fi

install: venv
	$(PIP) install -e ".[dev]"

lint:
	$(RUFF) check .
	$(RUFF) format --check .

format:
	$(RUFF) format .
	$(RUFF) check --fix .

test:
	$(PYTEST) --cov=app --cov-report=term --cov-report=xml --cov-fail-under=70

run: install
	$(UVICORN) app.main:app --reload --host 0.0.0.0 --port 8000

docker-build:
	docker build -t apiproject:latest .

docker-run:
	docker run -p 8000:8000 apiproject:latest

download-model: install
	$(PYTHON) scripts/download_model.py

k8s-apply:
	kubectl apply -f k8s/

benchmark:
	@echo "Run: ghz --insecure --connections=10 --duration=30s --rps=50 http://localhost:8000/health"
	@echo "See docs/benchmark.md for full commands."

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -f .coverage
	rm -rf htmlcov
	rm -f profile.stats
	rm -f *.prof
