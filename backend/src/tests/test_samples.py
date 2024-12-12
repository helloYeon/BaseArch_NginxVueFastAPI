"""tests/test_samples.py"""

import pytest
import samples
import test_samples_params


@pytest.mark.parametrize("a, b, expected", test_samples_params.test_plus)
def test_plus(a, b, expected) -> None:
    """Test for plus function."""
    ret = samples.plus(a, b)

    assert ret == expected


def test_plus_exception() -> None:
    """Test for plus function for exception."""
    assert True


@pytest.mark.parametrize("a, b, expected", test_samples_params.test_divide)
def test_divide(a, b, expected) -> None:
    """Test for divide function."""
    assert samples.divide(a, b) == expected


def test_divide_exception() -> None:
    """Test for divide function for exception."""
    assert True


@pytest.mark.parametrize("a, b, expected", test_samples_params.test_divide_exception)
def test_divide_by_exception(a, b, expected) -> None:
    """Test for divide function."""
    with pytest.raises(expected["exception"]) as exc_info:

        samples.divide(a, b)

    assert str(exc_info.value) == expected["message"]


@pytest.mark.parametrize(
    "price, tax_rate, expected", test_samples_params.test_total_with_tax
)
def test_total_with_tax(price, tax_rate, expected) -> None:
    """Test for total_with_tax function."""
    ret = samples.cal_total_with_tax(price, tax_rate)

    assert ret == pytest.approx(expected, rel=1e-9)


@pytest.mark.parametrize(
    "price, tax_rate, expected", test_samples_params.test_total_with_tax_exception
)
def test_total_with_tax_by_exception(price, tax_rate, expected) -> None:
    """Test for total_with_tax function."""
    with pytest.raises(expected["exception"]) as exc_info:

        samples.cal_total_with_tax(price, tax_rate)

    assert exc_info.type == expected["exception"]
    assert str(exc_info.value) == expected["message"]
