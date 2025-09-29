import pytest

from calc.operations import _ensure_two_numbers, add, div, mul, sub


@pytest.mark.parametrize("a,b,exp", [
    (0, 0, 0),
    (2, 3, 5),
    (-1, 4, 3),
    (2.5, 0.5, 3.0),
])
def test_add(a, b, exp):
    assert add(a, b) == pytest.approx(exp)

@pytest.mark.parametrize("a,b,exp", [
    (0, 0, 0),
    (5, 3, 2),
    (-1, 4, -5),
    (2.5, 0.5, 2.0),
])
def test_sub(a, b, exp):
    assert sub(a, b) == pytest.approx(exp)

@pytest.mark.parametrize("a,b,exp", [
    (0, 0, 0),
    (2, 3, 6),
    (-1, 4, -4),
    (2.5, 0.5, 1.25),
])
def test_mul(a, b, exp):
    assert mul(a, b) == pytest.approx(exp)

@pytest.mark.parametrize("a,b,exp", [
    (6, 3, 2),
    (-4, 2, -2),
    (2.5, 0.5, 5.0),
])
def test_div(a, b, exp):
    assert div(a, b) == pytest.approx(exp)

def test_div_by_zero():
    with pytest.raises(ZeroDivisionError):
        div(1, 0)

def test_ensure_two_numbers_valid():
    a, b = _ensure_two_numbers(["2", "3"])
    assert a == 2.0 and b == 3.0

@pytest.mark.parametrize("args", [
    [], ["1"], ["1", "2", "3"]
])
def test_ensure_two_numbers_wrong_arity(args):
    with pytest.raises(ValueError):
        _ensure_two_numbers(args)

@pytest.mark.parametrize("args", [
    ["a", "2"], ["1", "b"]
])
def test_ensure_two_numbers_non_numeric(args):
    with pytest.raises(ValueError):
        _ensure_two_numbers(args)
