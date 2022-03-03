#!/bin/sh
python3 -m black src
python3 -m black test
python3 -m mypy src
python3 -m flake8 src
python3 -m pytest --cov=src -v --ignore=test/integration --cov-report term-missing
