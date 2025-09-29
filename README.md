# CLI Calculator

A simple **command-line calculator** written in Python.  
Implements a REPL (Read–Eval–Print Loop) with input validation, error handling, and **100% test coverage** enforced by GitHub Actions.

---

## Features
- REPL interface (`python -m calc`)
- Supports addition, subtraction, multiplication, division
- Input validation (wrong args → helpful error)
- Division by zero handled gracefully
- Follows DRY principle: all operations defined in `calc/operations.py`
- Unit + parameterized tests with pytest

---

## Setup

```bash
# create and activate venv
python -m venv .venv
source .venv/bin/activate

# install dependencies
pip install -r requirements.txt

# install package in editable mode
pip install -e .
```

---

## Usage

### Run CLI (REPL)
```bash
python -m calc
```
Example:
```
> add 2 3
5
> div 4 0
Error: division by zero
```

### Run GUI (optional)
```bash
python main.py
```
Opens a simple calculator window with buttons for digits and operators.

---

## Testing

Run all tests:
```bash
pytest
```

Check coverage:
```bash
pytest --cov=calc --cov-report=term-missing
```

Coverage is enforced at **100%** in CI.

---

## Continuous Integration

- GitHub Actions workflow runs tests on each push/PR.  
- The build fails if coverage < 100%.  

---

## Repo Layout
```
calc/           # core package
  cli.py        # REPL implementation
  operations.py # arithmetic functions
tests/          # pytest suite
.github/workflows/ci.yml # CI pipeline
main.py         # optional GUI app
```
