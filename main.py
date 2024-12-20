import re
import logging

from numbers_parsing import parse_number_to_word, parse_word_to_number

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.CRITICAL,
    format='[{asctime}] #{levelname:8} {filename}:{lineno} - {name} - {message}',
    style='{'
)


def parse_and_calculate(equation: list = ("ноль", "плюс", "ноль")) -> str:
    """
    Parse the equation and calculate the result
    :param equation: a list with [number, operation, number]
    :return: result of calculation
    """
    logger.debug(equation)
    left_number = parse_word_to_number(equation[0])
    right_number = parse_word_to_number(equation[2])
    numerator, denominator = None, None

    match equation[1]:
        case "плюс":
            result_number = left_number + right_number
        case "минус":
            result_number = left_number - right_number
        case "умножить на":
            result_number = left_number * right_number
        case "разделить на":
            if right_number == 0:
                return "Ошибка: деление на ноль"
            result_number = left_number / right_number
            numerator = result_number.numerator
            denominator = result_number.denominator
        case "остаток от деления на":
            if right_number == 0:
                return "Ошибка: деление на ноль"
            result_number = left_number % right_number
        case "процент":
            if right_number == 0:
                return "Ошибка: деление на ноль"
            result_number = left_number % right_number
        case _:
            return "Ошибка: Неизвестная операция"

    if numerator and denominator:
        result = parse_number_to_word(number=float(result_number), numerator=numerator, denominator=denominator)
    else:
        result = parse_number_to_word(number=float(result_number))

    return result


def check_equation_string(equation: str) -> list | bool:
    """
    Check if the equation string is valid ("number operation number")
    :param equation: string of the equation
    :return: list of valid equation / False if equation string is invalid
    """
    equation = re.split(r'(плюс|минус|умножить на|разделить на|процент|остаток от деления на)', equation)
    equation = [element.strip() for element in equation]
    if len(equation) == 3:
        flag = True
        for element in equation:
            if not element:
                flag = False
        if flag:
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
          "+ Сложение – плюс\n"
          "- Вычитание – минус\n"
          "* Умножение – умножить на\n"
          "/ Деление – разделить на\n"
          "% Остаток от деления – процент / остаток от деления на\n"
          "------------------------------------------------")
    equation = input("Введите математическое выражение: ").lower()

    equation = check_equation_string(equation)
    while not equation:
        equation = input("Введите корректную строку. [число оператор число]\n").lower()
        equation = check_equation_string(equation)

    result = parse_and_calculate(equation)
    print(result)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.exception(e)
        print("Произошла непредвиденная ошибка. Перезапустите программу.")
