import pytest
from app.calculations import add, subtract, multiply, divide


@pytest.mark.parametrize(
    "num1,num2,expected",
    [
        (5, 3, 8),
        (2, 3, 5),
    ],
)
def test_add(num1, num2, expected):
    print(f"testing add")
    sum = add(num1, num2)
    assert sum == expected


def test_subtract():
    print(f"testing subtract")
    diff = subtract(5, 3)
    assert diff == 2


def test_multiply():
    print(f"testing multiply")
    product = multiply(5, 3)
    assert product == 15


def test_divide():
    print(f"testing divide")
    assert divide(6, 3) == 2
