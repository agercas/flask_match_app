.PHONY: test lint format all

# Command to run pytest
test:
	pytest

# Command to run flake8
lint:
	flake8 .

# Command to run black check
format-check:
	black --check .

# Command to run isort check
isort-check:
	isort --check-only .

# Command to automatically format code using black
format:
	black .

# Command to automatically sort imports using isort
isort:
	isort .

# Command to run all checks
check: lint format-check isort-check
