PY=python
PIP=pip

.PHONY: install demo lint test

install:
	$(PIP) install -r requirements.txt -r dev-requirements.txt

demo:
	$(PY) scripts/demo.py

lint:
	ruff check .
	black --check .

test:
	pytest -q
