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
	rm -rf __pycache__/
	rm .mypy_cache/

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