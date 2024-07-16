from modules import math_numbers

def test_add():
    assert math_numbers.add(2, 3) == 5

def test_subtract():
    assert math_numbers.subtract(3, 2) == 1

def test_multiply():
    assert math_numbers.multiply(2, 3) == 6

def test_calculate_total():
    items = [10, 20, 30, 40]
    assert math_numbers.calculate_total(items) == 100