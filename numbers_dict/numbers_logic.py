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


def parse_word_to_number(word_num: str) -> int:
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
    if number < 10:
        for word, value in UNITS.items():
            if number == value:
                return word
    elif number < 20:
        for word, value in TEENS.items():
            if number == value:
                return word
    elif number < 100:
        tens = (number // 10) * 10
        units = number % 10
        if units == 0:
            for word, value in TEENS.items():
                if number == value:
                    return word
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
            return " ".join(result)
    elif number < 1000:
        hundreds = (number // 100) * 100
        tens = ((number % 100) // 10) * 10


if __name__ == '__main__':
    print("sup! numbers is __main__")
    r1 = parse_word_to_number("девятьсот двенадцать миллионов шестьсот двадцать пять тысяч сто сорок четыре")
    r2 = parse_number_to_word(25)
    print(r1)
    print(r2)
