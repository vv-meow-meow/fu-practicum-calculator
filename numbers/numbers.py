_numbers_core = {
    1: "один",
    2: "два",
    3: "три",
    4: "четыре",
    5: "пять",
    6: "шесть",
    7: "семь",
    8: "восемь",
    9: "девять",
    10: "десять",
    11: "одиннадцать",
    12: "двенадцать",
    13: "тринадцать",
    14: "четырнадцать",
    15: "пятнадцать",
    16: "шестнадцать",
    17: "семнадцать",
    18: "восемнадцать",
    19: "девятнадцать",
    20: "двадцать",
    30: "тридцать",
    40: "сорок",
    50: "пятьдесят",
    60: "шестьдесят",
    70: "семьдесят",
    80: "восемьдесят",
    90: "девяносто",
    100: "сто",
    200: "двести",
    300: "триста",
    400: "четыреста",
    500: "пятьсот",
    600: "шестьсот",
    700: "семьсот",
    800: "восемьсот",
    900: "девятьсот",
}


def parse_word_number(word_num: str) -> int:
    word_num = word_num.split()
    result_number = 0
    for elem in word_num:
        for num, word in _numbers_core.items():
            if elem == word:
                result_number += num

    return result_number


def parse_number_word(number: int) -> str:
    str_num = str(number)
    num_digits = len(str_num)
    word_number = []
    for i in range(num_digits, 0, -1):
        if int(str_num[-i]) != 0:
            exp = i - 1
            round_num = int(str_num[-i]) * (10 ** exp)
            word_part_number = _numbers_core[round_num]
            word_number.append(word_part_number)

    # Пусть лучше останется, вдруг пригодится рефрактор алгоритма
    # dig_1 = number % 10  # 10 ^ 1
    # dig_2 = number % 100 // 10 * 10  # 10^2 // 10^(2-1) * 10^(2-1)
    # dig_3 = number % 1000 // 100 * 100  # 10^3 // 10^(3-1) * 10^(3-1)
    # result.append(_numbers_core[dig_3])
    # result.append(_numbers_core[dig_2])
    # result.append(_numbers_core[dig_1])
    result = " ".join(word_number)
    return result
