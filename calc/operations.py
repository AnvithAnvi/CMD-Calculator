def _ensure_two_numbers(args):
    if len(args) != 2:
        raise ValueError("expected two numbers, e.g. 'add 2 3'")
    try:
        a = float(args[0])
        b = float(args[1])
    except (TypeError, ValueError) as e:
        raise ValueError("arguments must be numbers") from e
    return a, b

def add(a, b): return a + b
def sub(a, b): return a - b
def mul(a, b): return a * b

def div(a, b):
    if b == 0:
        raise ZeroDivisionError("division by zero")
    return a / b
