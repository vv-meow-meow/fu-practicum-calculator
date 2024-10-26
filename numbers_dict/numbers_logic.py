UNITS: dict[str, int] = {'ноль': 0,
                         'один': 1,
                         'два': 2,
                         'три': 3,
                         'четыре': 4,
                         'пять': 5,
                         'шесть': 6,
                         'семь': 7,
                         'восемь': 8,
                         'девять': 9}

TEENS: dict[str, int] = {'десять': 10,
                         'одиннадцать': 11,
                         'двенадцать': 12,
                         'тринадцать': 13,
                         'четырнадцать': 14,
                         'пятнадцать': 15,
                         'шестнадцать': 16,
                         'семнадцать': 17,
                         'восемнадцать': 18,
                         'девятнадцать': 19}

TENS: dict[str, int] = {'двадцать': 20,
                        'тридцать': 30,
                        'сорок': 40,
                        'пятьдесят': 50,
                        'шестьдесят': 60,
                        'семьдесят': 70,
                        'восемьдесят': 80,
                        'девяносто': 90}

HUNDREDS: dict[str, int] = {
    "сто": 100,
    "двести": 200,
    "триста": 300,
    "четыреста": 400,
    "пятьсот": 500,
    "шестьсот": 600,
    "семьсот": 700,
    "восемьсот": 800,
    "девятьсот": 900
}

ORDERS: dict[str, int] = {
    "тысяча": 1000,
    "тысячи": 1000,
    "тысяч": 1000,
    "миллион": 1_000_000,
    "миллиона": 1_000_000,
    "миллионов": 1_000_000,
}


def _determine_thousand_form(num: int) -> str:
    if num < 0:
        raise ValueError("Negative numbers are not allowed")

    if num % 10 == 1:
        return "тысяча"
    elif num % 10 < 5:
        return "тысячи"
    else:
        return "тысяч"


def _determine_million_form(num: int) -> str:
    if num < 0:
        raise ValueError("Negative numbers are not allowed")

    if num % 10 == 1:
        return "миллион"
    if num % 10 < 5:
        return "миллиона"
    else:
        return "миллионов"


def parse_word_to_number(word_num: str) -> int:
    """
    Конвертирует строку с числом, записанным словами в число типа int
    :param word_num: число, записанное словами
    :return: Целое число
    """
    words: list[str] = word_num.lower().split()
    result_number = 0
    current_number = 0
    negative = 1
    for word in words:
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
    result_number *= negative
    return result_number


def parse_number_to_word(number: int) -> str:
    """
    Конвертирует число в строку, записанную словами
    :param number: число
    :return: строка с числом, записанным словами
    """

    if number == 0: return "ноль"

    def parse_units(unit_number: int) -> list[str]:
        for word, value in UNITS.items():
            if unit_number == value:
                return [word]

    def parse_tens(teen_number: int) -> list[str]:
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
                for word, value in UNITS.items():
                    if units == value:
                        result.append(word)
                        break
                return result
        else:
            raise ValueError(f"Число {number} больше 99")

    def parse_hundreds(hundreds_number: int) -> list[str]:
        result = []
        if hundreds_number < 10:
            for word, value in UNITS.items():
                if hundreds_number == value:
                    result.append(word)
                    return result
        elif hundreds_number < 100:
            result.extend(parse_tens(hundreds_number))
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
                result.extend(parse_tens(tens + units))
            else:
                if units != 0:
                    for word, value in UNITS.items():
                        if units == value:
                            result.append(word)
                            break
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

        words = []

        hundreds = (group // 100) * 100
        tens_units = group % 100

        if hundreds > 0:
            words.extend(parse_hundreds(group))
        elif 0 < tens_units < 10:
            words.extend(parse_units(tens_units))

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
    print("sup! numbers is __main__")
    r1 = parse_word_to_number(
        "сто пятьдесят два")  # девятьсот двенадцать миллионов шестьсот двадцать пять тысяч сто сорок четыре
    r2 = parse_number_to_word(105_104_421)
    print(r1)
    print(r2)
