# Калькулятор

- Выполнил: Владимир, ТРПО24-3
- Количество баллов – 10
- Базовая часть – 5 баллов
- Дополнительная часть – до 5 баллов
- Дедлайн: 21.11.2024

**Выполненные задания:**

- Базовая часть (5 баллов)

## Демонстрация калькулятора

https://youtu.be/eLKMTPkO7gY

## Задание

**Структура проекта**

- app.py – реализация программы
- README.md – отчет к работе
- requirements.txt – список библиотек и версий

### Базовая часть (выполняется всеми самостоятельно!)

Написать калькулятор для строковых выражений вида '<число> <операция> <число>', где <число> - не отрицательное целое
число меньшее 100, записанное словами, например "тридцать четыре", <арифметическая операция> - одна из операций "
плюс", "минус", "умножить". Результат выполнения операции вернуть в виде текстового представления числа. Пример calc("
двадцать пять плюс тринадцать") -> "тридцать восемь"

Оформить калькулятор в виде функции, которая принимает на вход строку и возвращает строку.

### Дополнительные задания:

#### 1. Баллы 2

Реализовать поддержку операции деления и остатка от деления и работу с дробными числами (десятичными дробями). Пример:
calc ("сорок один и тридцать одна сотая разделить на семнадцать") -> "два и сорок три сотых". Обрабатывать дробную часть
до тысячных включительно, если при делении получаются числа с меньшей дробной частью выполнять округление до тысячных.

#### 2. Баллы 3

Расширение задания 1. Реализовать поддержку десятичной дробной части до миллионных долей включительно. Реализовать
корректный вывод информации о периодической десятичной дроби (период дроби вплоть до 4-х десятичных знаков). Пример:
calc("девятнадцать и восемьдесят две сотых разделить на девяносто девять") -> "ноль и двадцать сотых и ноль два в
периоде ".

#### 3. Баллы 3

Реализовать текстовый калькулятор для выражения из произвольного количества операций с учетом приоритета операций.
Пример: calc("пять плюс два умножить на три минус один") -> "десять". (Для реализации рекомендуется использовать
алгоритмы основанные на польской инверсной записи см.
например, https://ru.wikipedia.org/wiki/Обратная_польская_запись)

#### 4. Баллы 3

Расширение задания 3. Добавить поддержку приоритета операций с помощью скобок. Пример: calc("скобка открывается пять
плюс два скобка закрывается умножить на три минус один") -> "двадцать".

#### 5. Баллы 1

Добавить возможность использования отрицательных чисел. Пример: calc("пять минус минус один") -> "шесть".

#### 6. Баллы 3

Добавить возможность оперировать с дробями (правильными и смешанными). Реализовать поддержку сложения, вычитания и
умножения, дробей. Результат операций не должен представлять неправильную дробь, такие результаты нужно превращать в
смешанные дроби. Пример: calc("один и четыре пятых плюс шесть седьмых ") -> "два и двадцать три тридцать пятых".

#### 7. Баллы 1

Расширение задания 6. Добавить автоматическое сокращение дроби в ответе. Пример: calc("одна шестая умножить на две
третьих") -> "одна девятая".

#### 8. Баллы 2

Расширение задания 1. Добавить операции возведения в степень и тригонометрические операции синус, косинус, тангенс и
константу пи. Допускается как минимум одна из этих функций в выражении с обычными операциями. Пример: calc("два в
степени четыре") -> "шестнадцать". Пример: calc("синус от пи разделить на четыре") -> "ноли и семьсот семь тысячных".

#### 9. Баллы 1

Добавить комбинаторные операции перестановки, размещения и сочетания. Пример: calc("размещений из трех по два") -> "
шесть".

#### 10. Баллы 2

Диагностировать ошибки: неправильную запись числа; неправильную последовательность чисел и операций; (задание 1) деление
на ноль; (задание 3) неправильную последовательность чисел и операций; (задание 4) некорректный баланс и вложенность
скобок; (задание 6) некорректную запись числа

## Дополнительная информация

- Используемый формат документации – [Phoenix](https://docs.wxpython.org/DocstringsGuidelines.html)

## TODO

- [ ] Сделать 1 дополнительное задание
- [ ] Сделать 2 дополнительное задание
- [x] Сделать базовую часть
- [x] Сделать документацию
- [x] Написать используемый тип документации
