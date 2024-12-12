"""tests/test_samples_params.py"""

test_plus = [
    # case 1 :  5 + 3 = 8
    (5, 3, 8),
    # case 2 : 2 + 4 = 6
    (2, 4, 6),
    # case 3 : -1 + 1 = 0
    (-1, 1, 0),
    # case 4 : 0 + 0 = 0
    (0, 0, 0),
]

test_divide = [
    # case 1 :  6 / 2 = 3
    (6, 2, 3),
    # case 2 :  5 / 5 = 1
    (5, 5, 1),
]

test_divide_exception = [
    # case 1 : 0で割る
    (
        1,
        0,
        {"exception": ValueError, "message": "Cannot divide by zero"},
    ),
]

test_total_with_tax = [
    # case 1 : 消費税10%
    (100, 10, 110),
    # case 2 : 消費税8%
    (200, 8, 216),
    # case 3 : 消費税15%
    (150, 15, 172.5),
]

test_total_with_tax_exception = [
    # case 1 : 価額がマイナス
    (
        -100,
        10,
        {"exception": ValueError, "message": "Price and tax rate must be non-negative"},
    ),
    # case 2 : 消費税がマイナス
    (
        100,
        -10,
        {"exception": ValueError, "message": "Price and tax rate must be non-negative"},
    ),
]
