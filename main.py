import re
import logging

from numbers import parse_number_word, parse_word_number

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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
            result_number = parse_word_number(equation[0]) + parse_word_number(equation[2])
        case "минус":
            result_number = parse_word_number(equation[0]) - parse_word_number(equation[2])
        case "умножить на":
            result_number = parse_word_number(equation[0]) * parse_word_number(equation[2])
        case "разделить на":
            result_number = parse_word_number(equation[0]) - parse_word_number(equation[2])

    result = parse_number_word(result_number)
    return result


def check_equation_string(equation: str) -> list | bool:
    """
    Check if the equation string is valid ("number operation number")
    :param equation: string of the equation
    :return: list of valid equation / False if equation string is invalid
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
    print("------------------------------------------------\n"
          "Здравствуйте! Небольшая сводка помощи перед началом использования.\n"
          "------------------------------------------------\n"
          "Q: Как писать выражение?\n"
          "A: [число операция число]\n"
          "------------------------------------------------\n"
          "Операции:\n"
          "- Сложение – плюс\n"
          "- Вычитание – минус\n"
          "- Умножение – умножить на\n"
          "- Деление – разделить на\n"
          "------------------------------------------------")
    equation = input("Введите математическое выражение: ").lower()

    equation = check_equation_string(equation)
    while not equation:
        equation = input("Введите корректную строку. [число оператор число]\n").lower()
        equation = check_equation_string(equation)

    result = parse_and_calculate(equation)
    print(result)


if __name__ == '__main__':
    main()
