import logging
from typing import Literal
from fractions import Fraction

from numbers_parsing.numbers_dict import *

logger = logging.getLogger(__name__)


def _determine_form(num: int, forms: tuple) -> str:
    """
    Определяет правильную форму слова в зависимости от числа.

    :param num: Число для определения формы
    :param forms: Кортеж из трех форм слова (1, 2-4, 5-0)
    :return: Правильная форма слова
    """
    if num < 0:
        raise ValueError("Negative numbers are not allowed")

    if 11 <= num % 100 <= 14:
        return forms[2]
    elif num % 10 == 1:
        return forms[0]
    elif 2 <= num % 10 <= 4:
        return forms[1]
    else:
        return forms[2]


def get_periodic_part(numerator: int, denominator: int) -> tuple[str, str]:
    """
    Определяет периодическую и непериодическую части дроби.

    :param numerator: Числитель дробной части
    :param denominator: Знаменатель дробной части
    :return: Кортеж, содержащий непериодическую и периодическую части
    """
    remainders = {}
    decimal_digits = ''
    remainder = numerator % denominator
    position = 0

    while remainder != 0 and position < 1000:
        if remainder in remainders:
            start = remainders[remainder]
            non_periodic = decimal_digits[:start]
            periodic = decimal_digits[start:]
            return non_periodic, periodic[:4]
        remainders[remainder] = position
        remainder *= 10
        digit = remainder // denominator
        decimal_digits += str(digit)
        remainder %= denominator
        position += 1

    return decimal_digits, ''


def _parse_fractional_part(fractional_number: float) -> list[str]:
    """
    Преобразует дробную часть числа в слова.

    :param fractional_number: Дробная часть числа
    :return: Список слов, представляющих дробную часть числа
    """
    fractional_number = round(fractional_number, 6)
    numerator = int(fractional_number * 1_000_000)
    if numerator == 0: return []

    denominators = (10, 100, 1_000, 10_000, 100_000, 1_000_000)
    for denom in denominators:
        if numerator % (1_000_000 // denom) == 0:
            denominator = denom
            numerator = numerator // (1_000_000 // denom)
            break
    else:
        denominator = 1_000_000

    words = []
    words.extend(parse_number_to_word(numerator, gender="feminine").split())
    denom_key = f"denominator_{denominator}"
    words.append(_determine_form(numerator, FORMS[denom_key]))

    return words


def parse_integer_part(integer_part: int,
                       gender: Literal["feminine", "masculine"] = None) -> list[str]:
    """
    Преобразует целую часть числа в слова.

    :param integer_part: Целая часть числа
    :param gender: Род числа (мужской или женский)
    :return: Список слов, представляющих число
    """

    def parse_units(unit_number: int,
                    gender: Literal["masculine", "feminine"] = "masculine") -> list[str]:
        return [UNITS_GENDER[unit_number][gender]]

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
            return parse_units(hundreds_number, gender=gender)
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
    groups = []
    while integer_part > 0:
        groups.append(integer_part % 1000)
        integer_part //= 1000

    default_gender = gender or "masculine"

    for i in range(len(groups) - 1, -1, -1):
        group = groups[i]
        if group == 0: continue

        group_words = []

        if i == 1:
            group_gender = "feminine"
        else:
            group_gender = default_gender

        group_words.extend(parse_hundreds(group, gender=group_gender))

        if i == 1:
            group_words.append(_determine_form(group, FORMS["thousand"]))
        elif i == 2:
            group_words.append(_determine_form(group, FORMS["million"]))

        result.extend(group_words)

    return result


def parse_number_to_word(number: float,
                         numerator: int = None,
                         denominator: int = None,
                         gender: Literal["masculine", "feminine"] = None) -> str:
    """
    Конвертирует число в строку, записанную словами.

    :param number: Число для преобразования
    :param numerator: Числитель дробной части, если есть
    :param denominator: Знаменатель дробной части, если есть
    :param gender: Род числа (мужской или женский)
    :return: Число, записанное словами
    """
    logger.debug(f"Getting number {number}")
    if number == 0: return "ноль"

    result = []
    if number < 0:
        result.append("минус")
        number = abs(number)

    if numerator: numerator = abs(numerator)

    integer_part = int(number)
    fractional_part = number - integer_part

    if integer_part == 0:
        result.append("ноль")
    else:
        integer_words = parse_integer_part(integer_part, gender)
        result.extend(integer_words)

    if fractional_part > 0 or (numerator and denominator):

        if numerator and denominator:
            non_periodic, periodic = get_periodic_part(numerator, denominator)

            if non_periodic:
                result.append("и")
                fractional_words = []
                digit_word = parse_integer_part(int(non_periodic), gender="feminine")
                fractional_words.extend(digit_word)
                denom_key = f"denominator_{10 ** len(non_periodic)}"
                if denom_key in FORMS:
                    fractional_words.append(_determine_form(int(non_periodic), FORMS[denom_key]))
                else:
                    fractional_words.append(f"делить на {parse_number_to_word(10 ** len(non_periodic))}")
                result.extend(fractional_words)

            if periodic:
                period_words = []
                for digit in periodic:
                    digit_word = parse_number_to_word(int(digit), gender="masculine")
                    period_words.append(digit_word)
                result.append("и")
                result.extend(period_words)
                result.append("в периоде")
        else:
            frac = Fraction(fractional_part).limit_denominator(1_000_000)
            numerator = frac.numerator
            denominator = frac.denominator

            non_periodic, periodic = get_periodic_part(numerator, denominator)

            if non_periodic:
                result.append("и")
                fractional_words = []
                digit_word = parse_number_to_word(int(non_periodic), gender="feminine")
                fractional_words.append(digit_word)
                denom_key = f"denominator_{10 ** len(non_periodic)}"
                if denom_key in FORMS:
                    fractional_words.append(_determine_form(int(non_periodic), FORMS[denom_key]))
                else:
                    fractional_words.append(f"делить на {parse_number_to_word(10 ** len(non_periodic))}")
                result.extend(fractional_words)

            if periodic:
                period_words = []
                for digit in periodic:
                    digit_word = parse_number_to_word(int(digit), gender="feminine")
                    period_words.append(digit_word)
                result.append("и ноль")
                result.extend(period_words)
                result.append("в периоде")

    return " ".join(result)


def parse_word_to_number(word_num: str) -> Fraction:
    """
    Конвертирует строку с числом, записанным словами, в число.

    :param word_num: Число, записанное словами
    :return: Число в виде объекта Fraction
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

    result_number = Fraction(0)
    current_number = 0
    fractional_part = Fraction(0)
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
        elif word in ORDERS:
            if current_number == 0:
                current_number = 1
            result_number += current_number * ORDERS[word]
            current_number = 0
        else:
            raise ValueError(f'Word "{word}" is not a valid number')

    result_number += current_number

    # Парсинг дробной части
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
            numerator = int(parse_word_to_number(numerator_str))
            fractional_part = Fraction(numerator, denominator)
        else:
            raise ValueError("Invalid fractional part")

    result_number += fractional_part
    result_number *= negative

    return result_number


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='[{asctime}] #{levelname:8} {filename}:{lineno} - {name} - {message}',
        style='{'
    )
    print(f"!!! numbers_logic is main !!!")
    text = parse_number_to_word(1002.22222222)
    print(text)
    number = parse_word_to_number("девятнадцать и восемьдесят две сотых")
    print(number.numerator, number.denominator)
