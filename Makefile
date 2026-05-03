PYTHON = python3
PIP = pip3

.PHONY: install
install:
	$(PIP) install -r requirements.txt

.PHONY: run
run:
	$(PYTHON) # arquivo princp. do prj

.PHONY: debug
debug:
	$(PYTHON) -m pdb # arquivo princp. do prj

.PHONY: clean
clean:
	rm -rf __pycache__/
	rm .mypy_cache/

.PHONY: lint
lint:
	$(PYTHON) -m flake8 . /
	$(PYTHON) -m mypy . --warn-return-any --warn-unused-ignores 
		--ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

.PHONY: lint-strict
lint-strict:
	$(PYTHON) -m flake8 . /
	$(PYTHON) -m mypy . --strict