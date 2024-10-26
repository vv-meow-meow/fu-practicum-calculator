import logging
from typing import Literal

from numbers_parsing.numbers_dict import *

logger = logging.getLogger(__name__)


def _determine_thousand_form(num: int) -> str:
    if num < 0:
        raise ValueError("Negative numbers are not allowed")

    if 5 <= num % 100 <= 20:
        return "тысяч"
    elif num % 10 == 0:
        return "тысяч"
    elif num % 10 == 1:
        return "тысяча"
    elif num % 10 < 5:
        return "тысячи"
    else:
        return "тысяч"


def _determine_million_form(num: int) -> str:
    if num < 0:
        raise ValueError("Negative numbers are not allowed")

    if 5 <= num % 100 <= 20:
        return "миллионов"
    elif num % 10 == 0:
        return "миллионов"
    elif num % 10 == 1:
        return "миллион"
    elif num % 10 < 5:
        return "миллиона"
    else:
        return "миллионов"


def _determine_denominator_10_form(num: int) -> str:
    if num < 0:
        raise ValueError("Negative numbers are not allowed")

    if 5 <= num % 100 <= 20:
        return "десятых"
    elif num % 10 == 0:
        return "десятых"
    elif num % 10 == 1:
        return "десятая"
    elif num % 10 < 5:
        return "десятых"
    else:
        return "десятых"


def _determine_denominator_100_form(num: int) -> str:
    if num < 0:
        raise ValueError("Negative numbers are not allowed")

    if 5 <= num % 100 <= 20:
        return "сотых"
    elif num % 10 == 0:
        return "сотых"
    elif num % 10 == 1:
        return "сотая"
    elif num % 10 < 5:
        return "сотых"
    else:
        return "сотых"


def _determine_denominator_1000_form(num: int) -> str:
    if num < 0:
        raise ValueError("Negative numbers are not allowed")

    if 5 <= num % 100 <= 20:
        return "тысячных"
    elif num % 10 == 0:
        return "тысячных"
    elif num % 10 == 1:
        return "тысячная"
    elif num % 10 < 5:
        return "тысячных"
    else:
        return "тысячных"


def parse_word_to_number(word_num: str) -> float:
    """
    Конвертирует строку с числом, записанным словами в число
    :param word_num: число, записанное словами
    :return: Целое число
    """
    words: list[str] = word_num.lower().split()

    if "и" in words:
        index = words.index("и")
        integer_part_words = words[:index]
        fractional_part_words = words[index + 1:]
    else:
        if words[-1] in FRACTION_DENOMINATORS:
            integer_part_words = ["ноль"]
            fractional_part_words = words
        else:
            integer_part_words = words
            fractional_part_words = []

    result_number = 0
    current_number = 0
    fractional_part = 0.0
    negative = 1
    for word in integer_part_words:
        if word == "минус":
            negative = -1
        elif word in HUNDREDS:
            current_number += HUNDREDS[word]
        elif word in TEENS:
            current_number += TEENS[word]
        elif word in TENS:
            current_number += TENS[word]
        elif word in UNITS:
            current_number += UNITS[word]
        elif word in UNITS_UNIQUE:
            current_number += UNITS_UNIQUE[word]
        elif word in ORDERS:
            if current_number == 0:
                current_number = 1
            result_number += current_number * ORDERS[word]
            current_number = 0
        else:
            raise ValueError(f'Word "{word}" is not a valid number')

    if fractional_part_words:
        numerator_words = []
        denominator = None

        for i, word in enumerate(fractional_part_words):
            if word in FRACTION_DENOMINATORS:
                denominator = FRACTION_DENOMINATORS[word]
                numerator_words = fractional_part_words[:i]
                break

        if denominator and numerator_words:
            numerator_str = ' '.join(numerator_words)
            numerator = parse_word_to_number(numerator_str)
            fractional_part = numerator / denominator

    result_number = (result_number + current_number + fractional_part) * negative
    return result_number


def parse_fractional_part(fractional_number: float) -> list[str]:
    fractional_number = round(fractional_number, 3)
    numerator = int(fractional_number * 1000)
    if numerator == 0: return []

    if numerator % 100 == 0:
        denominator = 10
        numerator //= 100
    elif numerator % 10 == 0:
        denominator = 100
        numerator //= 10
    else:
        denominator = 1000

    words = []
    words.extend(parse_number_to_word(numerator, gender="feminine").split())

    if denominator == 10:
        words.append(_determine_denominator_10_form(numerator))
    elif denominator == 100:
        words.append(_determine_denominator_100_form(numerator))
    elif denominator == 1000:
        words.append(_determine_denominator_1000_form(numerator))

    return words


def parse_number_to_word(number: float,
                         gender: Literal["masculine", "feminine"] = None) -> str:
    """
    Конвертирует число в строку, записанную словами
    :param number: число
    :param gender: род числа (мужской или женский)
    :return: строка с числом, записанным словами
    """
    logger.debug(f"Getting number {number}")
    if number == 0: return "ноль"

    def parse_units(unit_number: int,
                    gender: Literal["masculine", "feminine"] = "masculine") -> list[str]:

        units_gender = {
            1: {"masculine": "один", "feminine": "одна"},
            2: {"masculine": "два", "feminine": "две"},
            3: {"masculine": "три", "feminine": "три"},
            4: {"masculine": "четыре", "feminine": "четыре"},
            5: {"masculine": "пять", "feminine": "пять"},
            6: {"masculine": "шесть", "feminine": "шесть"},
            7: {"masculine": "семь", "feminine": "семь"},
            8: {"masculine": "восемь", "feminine": "восемь"},
            9: {"masculine": "девять", "feminine": "девять"}
        }

        return [units_gender[unit_number][gender]]

    def parse_tens(teen_number: int,
                   gender: Literal["masculine", "feminine"] = "masculine") -> list[str]:
        if teen_number < 20:
            for word, value in TEENS.items():
                if teen_number == value:
                    return [word]
        elif teen_number < 100:
            tens = (teen_number // 10) * 10
            units = teen_number % 10
            if units == 0:
                for word, value in TENS.items():
                    if teen_number == value:
                        return [word]
            else:
                result = []
                for word, value in TENS.items():
                    if tens == value:
                        result.append(word)
                        break
                result.extend(parse_units(units, gender=gender))
                return result
        else:
            raise ValueError(f"Число {number} больше 99")

    def parse_hundreds(hundreds_number: int,
                       gender: Literal["masculine", "feminine"] = "masculine") -> list[str]:
        result = []
        if hundreds_number < 10:
            for word, value in UNITS.items():
                if hundreds_number == value:
                    result.append(word)
                    return result
        elif hundreds_number < 100:
            result.extend(parse_tens(hundreds_number, gender=gender))
            return result
        elif hundreds_number < 1000:
            hundreds = (hundreds_number // 100) * 100
            tens = ((hundreds_number % 100) // 10) * 10
            units = hundreds_number % 10
            for word, value in HUNDREDS.items():
                if hundreds == value:
                    result.append(word)
                    break

            if tens != 0:
                result.extend(parse_tens(tens + units, gender=gender))
            else:
                if units != 0:
                    result.extend(parse_units(units, gender=gender))
            return result

    result = []
    if number < 0:
        result.append("минус")
        number = abs(number)

    integer_part = int(number)
    fractional_part = number - integer_part

    if integer_part == 0: result.append("ноль")

    groups: list[int] = []
    while integer_part > 0:
        groups.append(integer_part % 1000)
        integer_part //= 1000

    enumerated_groups = tuple(enumerate(groups))

    empty_flag = False
    if gender is None:
        gender: Literal["masculine", "feminine"] = "masculine"
        empty_flag = True

    for i in range(len(enumerated_groups) - 1, 0 - 1, -1):
        enum_group: tuple[int, int] = enumerated_groups[i]
        j = enum_group[0]
        group = enum_group[1]
        if group == 0: continue

        words = []

        if j == 1: gender = "feminine"

        if 100 <= group:
            words.extend(parse_hundreds(group, gender=gender))
        elif 10 <= group <= 99:
            words.extend(parse_tens(group, gender=gender))
        elif 0 < group < 10:
            words.extend(parse_units(group, gender=gender))

        if j == 0:
            result.extend(words)
        elif j == 1:
            result.extend(words)
            result.append(_determine_thousand_form(group))
            if empty_flag: gender = "masculine"
        elif j == 2:
            result.extend(words)
            result.append(_determine_million_form(group))
        else:
            raise ValueError(f"Number {number} is too big (function support numbers up to million)")

    if fractional_part > 0:
        result.append("и")
        result.extend(parse_fractional_part(fractional_part))

    return " ".join(result)


if __name__ == '__main__':
    print(f"!!! numbers_logic is main !!!")
    text = parse_number_to_word(1002)
    print(text)
    number = parse_word_to_number("пятьдесят два")
    print(number)