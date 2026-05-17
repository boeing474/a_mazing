PYTHON = python3
PIP = pip3

.PHONY: install
install: venv
	$(PIP) install -r requirements.txt

.PHONY: run
run: install
	$(PYTHON) a_maze_ing.py config.txt

.PHONY: debug
debug: install
	$(PYTHON) -m pdb a_maze_ing.py config.txt

.PHONY: clean
clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -prune -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -prune -exec rm -rf {} +
	find . -type d -name "*.egg-info" -prune -exec rm -rf {} +
	rm -rf build dist

.PHONY: venv
venv:
	python3 -m venv venv

.PHONY: lint
lint:
	$(PYTHON) -m flake8 . /
	$(PYTHON) -m mypy . --warn-return-any --warn-unused-ignores 
		--ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

.PHONY: lint-strict
lint-strict:
	$(PYTHON) -m flake8 . /
	$(PYTHON) -m mypy . --strict