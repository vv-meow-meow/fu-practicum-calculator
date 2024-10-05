import re
import logging

from num2words import num2words

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def generate_numbers(min_num: int, max_num: int) -> dict[str, int]:
    """
    Generate a dictionary with numbers between min and max
    :param min_num: minimal number
    :param max_num: maximal number
    :return: a dictionary with numbers between min and max
    """
    numbers: dict = {}
    for i in range(min_num, max_num + 1):
        word = num2words(i, lang='ru')
        numbers[word] = i
    return numbers


numbers = generate_numbers(1, 100)


def parse_and_calculate(equation: list = ("ноль", "плюс", "ноль")) -> str:
    """
    Parse the equation and calculate the result
    :param equation: a list with [number, operation, number]
    :return: result of calculation
    """
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
    """
    Check if the equation string is valid ("number operation number")
    :param equation: string of the equation
    :return: list of valid equations / False if equation string is invalid
    """
    equation = re.split(r'(плюс|минус|умножить на|разделить на)', equation)
    equation = [element.strip() for element in equation]
    if len(equation) == 3:
        return equation
    return False


def main() -> None:
    """
    Main function of the program. Requests the user to input the equation and prints the result of the equation.
    :return: nothing
    """
    equation = input("Здравствуйте, введите математическое выражение. [число оператор число]\n").lower()

    equation = check_equation_string(equation)
    while not equation:
        equation = input("Введите корректную строку. [число оператор число]\n").lower()
        equation = check_equation_string(equation)

    result = parse_and_calculate(equation)
    print(result)


if __name__ == '__main__':
    main()
