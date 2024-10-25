import pytest
from numbers_dict import *


@pytest.mark.parametrize("input_value, expected_output", [
    ("ноль", 0),
    ("один", 1),
    ("десять", 10),
    ("одиннадцать", 11),
    ("двадцать три", 23),
    ("сто", 100),
    ("сто пять", 105),
    ("сто пятьдесят", 150),
    ("пять тысяч", 5000),
    ("тысяча двести пятьдесят два", 1252),
    ("миллион", 1_000_000),
    ("пять миллионов", 5_000_000),
    # Negative
    ("минус один", -1),
    ("минус сорок два", -42),
    ("минус тысяча сто один", -1101),
    ("минус ноль", 0)

]
                         )
def test_parse_word_to_number(input_value, expected_output) -> None:
    result = parse_word_to_number(input_value)

    # Assert
    assert result == expected_output


@pytest.mark.parametrize("input_value, expected_output", [
    (0, 'ноль'),
    (1, 'один'),
    (9, 'девять'),
    (10, 'десять'),
    (15, 'пятнадцать'),
    (20, 'двадцать'),
    (25, 'двадцать пять'),
    (30, 'тридцать'),
    (42, 'сорок два'),
    (50, 'пятьдесят'),
    (99, 'девяносто девять'),
    (100, 'сто'),
    (101, 'сто один'),
    (110, 'сто десять'),
    (115, 'сто пятнадцать'),
    (120, 'сто двадцать'),
    (199, 'сто девяносто девять'),
    (200, 'двести'),
    (342, 'триста сорок два'),
    (999, 'девятьсот девяносто девять'),
    # Negative tests: TODO
    (-10, 'минус десять'),
])
def test_parse_number_to_word(input_value, expected_output) -> None:
    result = parse_number_to_word(input_value)

    # Assert
    assert result == expected_output
