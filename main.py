import re
import logging

from num2words import num2words

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def generate_numbers(min: int, max: int) -> dict[str, int]:
    numbers: dict = {}
    for i in range(min, max + 1):
        word = num2words(i, lang='ru')
        numbers[word] = i
    return numbers


numbers = generate_numbers(1, 100)


def parse_and_calculate(equation: list = ("ноль", "плюс", "ноль")):
    logger.debug(equation)

    result_number = 0

    match equation[1]:
        case "плюс":
            result_number = numbers[equation[0]] + numbers[equation[2]]
        case "минус":
            result_number = numbers[equation[0]] - numbers[equation[2]]
        case "умножить на":
            result_number = numbers[equation[0]] * numbers[equation[2]]
        case "разделить на":
            result_number = numbers[equation[0]] / numbers[equation[2]]

    result = num2words(result_number, lang='ru')
    return result


def check_equation_string(equation: str) -> list | bool:
    equation = re.split(r'(плюс|минус|умножить на|разделить на)', equation)
    equation = [element.strip() for element in equation]
    if len(equation) == 3:
        return equation
    return False


def main():
    equation = input("Здравствуйте, введите математическое выражение. [число оператор число]\n").lower()

    equation = check_equation_string(equation)
    while not equation:
        equation = input("Введите корректную строку. [число оператор число]\n").lower()
        equation = check_equation_string(equation)

    result = parse_and_calculate(equation)
    print(result)


if __name__ == '__main__':
    main()
