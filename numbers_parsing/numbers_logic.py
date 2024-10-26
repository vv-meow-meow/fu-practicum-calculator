import logging

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


def parse_number_to_word(number: int) -> str:
    """
    Конвертирует число в строку, записанную словами
    :param number: число
    :return: строка с числом, записанным словами
    """
    logger.debug(f"Getting number {number}")
    if number == 0: return "ноль"

    def parse_units(unit_number: int,
                    is_thousands: bool = False) -> list[str]:
        if is_thousands:
            for word, value in UNITS_UNIQUE.items():
                if unit_number == value:
                    return [word]

        for word, value in UNITS.items():
            if unit_number == value:
                return [word]

    def parse_tens(teen_number: int,
                   is_thousands: bool = False) -> list[str]:
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
                result.extend(parse_units(units, is_thousands=is_thousands))
                return result
        else:
            raise ValueError(f"Число {number} больше 99")

    def parse_hundreds(hundreds_number: int,
                       is_thousands: bool = False) -> list[str]:
        result = []
        if hundreds_number < 10:
            for word, value in UNITS.items():
                if hundreds_number == value:
                    result.append(word)
                    return result
        elif hundreds_number < 100:
            result.extend(parse_tens(hundreds_number, is_thousands=is_thousands))
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
                result.extend(parse_tens(tens + units, is_thousands=is_thousands))
            else:
                if units != 0:
                    result.extend(parse_units(units, is_thousands=is_thousands))
            return result

    result = []
    if number < 0:
        result.append("минус")
        number = abs(number)

    groups: list[int] = []
    while number > 0:
        groups.append(number % 1000)
        number //= 1000

    enumerated_groups = tuple(enumerate(groups))

    for i in range(len(enumerated_groups) - 1, 0 - 1, -1):
        enum_group: tuple[int, int] = enumerated_groups[i]
        j = enum_group[0]
        group = enum_group[1]
        if group == 0: continue

        words = []

        is_thousands = False
        if j == 1: is_thousands = True

        if 100 <= group:
            words.extend(parse_hundreds(group, is_thousands=is_thousands))
        elif 10 <= group <= 99:
            words.extend(parse_tens(group, is_thousands=is_thousands))
        elif 0 < group < 10:
            words.extend(parse_units(group, is_thousands=is_thousands))

        if j == 0:
            result.extend(words)
        elif j == 1:
            result.extend(words)
            result.append(_determine_thousand_form(group))
        elif j == 2:
            result.extend(words)
            result.append(_determine_million_form(group))
        else:
            raise ValueError(f"Number {number} is too big (function support numbers up to million)")

    return " ".join(result)


if __name__ == '__main__':
    number = parse_word_to_number("сорок один и сто тридцать две тысячных")
    print(number)  # Ожидается: 41.31
