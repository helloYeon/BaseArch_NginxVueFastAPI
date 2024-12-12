"""tests/samples.py"""


def plus(a, b) -> int:
    """Add two numbers."""
    return a + b


def divide(a, b) -> float:
    """Divide two numbers."""
    if b == 0:

        raise ValueError("Cannot divide by zero")

    return a / b


def cal_total_with_tax(price: float, tax_rate: float) -> float | int:
    """Calculate the total price including tax."""
    if price < 0 or tax_rate < 0:

        raise ValueError("Price and tax rate must be non-negative")

    total_price = price * (1 + tax_rate / 100)

    return total_price
