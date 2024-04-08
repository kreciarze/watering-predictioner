.PHONY: Makefile

all: check test ### Run all checks and tests (lints, mypy, tests...)

all_ff: check_ff test ### Run all checks and tests, but fail on first that returns error (lints, mypy, tests...)

check/lint/black lint/black black-check:  ### Run black lint check (code formatting)
	-black . --diff --check --color

check_ff/lint/black lint_ff/black:
	black . --diff --check --color

check/lint/deps:
	-fawltydeps --detailed

check_ff/lint/deps:
	fawltydeps --detailed

check/lint/flake8 lint/flake8 flake8-check:  ### Run flake8 lint check (pep8 etc.)
	-flake8 .

check_ff/lint/flake8 lint_ff/flake8:
	flake8 .

check/lint/isort lint/isort isort-check:  ### Run isort lint check (import sorting)
	-isort . --diff --check --color

check_ff/lint/isort lint_ff/isort:
	isort . --diff --check --color

check/mypy check_ff/mypy lint/mypy lint_ff/mypy mypy:  ### Run mypy check (type checking)
	PYTHONPATH=./src mypy . --show-error-codes --show-traceback --implicit-reexport

check/lint lint: check/lint/black check/lint/deps check/lint/flake8 check/lint/isort  ### Run all lightweight lint checks (no mypy)

check_ff/lint lint_ff: check_ff/lint/black check_ff/lint/deps check_ff/lint/flake8 check_ff/lint/isort  ### Run all lightweight lint checks, but fail on first that returns error

check lint_full full_lint: check/lint check/mypy  ### Run all lint checks and mypy

check_ff lint_full_ff full_lint_ff: check_ff/lint check_ff/mypy  ### Run all lint checks and mypy, but fail on first that returns error

lint_fix lint/fix:  ### Automatically fix lint problems (only reported by black and isort)
	black .
	isort .

test:  ### Run all unittests
	PYTHONPATH=./src pytest tests --durations=10

### Help
help: ## Show this help
	@sed -Ene 's/^([^ 	]+)( [^ 	]+)*:.*##/\1:\t/p' $(MAKEFILE_LIST) | column -t -s $$'\t'
