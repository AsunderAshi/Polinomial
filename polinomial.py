import re
import rpn
import random
import argparse


def replace(string, symbol_to_replace, new_symbol):
    minus_symbol_to_replace = '-' + symbol_to_replace
    for (i, c) in enumerate(string):
        if string[i] == symbol_to_replace:
            string[i] = new_symbol
        elif string[i] == minus_symbol_to_replace:
            if new_symbol.find('-') != -1:
                string[i] = new_symbol[1:]
            else:
                string[i] = '-' + new_symbol
    return string


def sort_variables(numbers):
    for (i, c) in enumerate(numbers):
        if re.findall(r'-[a-zA-Z]', numbers[i]):
            numbers[i] = numbers[i][1:]
    numbers = list(set(numbers))
    return [number for number in numbers if re.findall(r'[a-zA-Z]', number)]


def check_left_variables(polinom):
    for symbol in polinom:
        if re.findall(r'[a-zA-Z]', symbol):
            return True


def compare(polinomial1, polinomial2, epsilon):
    variables_one = rpn.get_numbers(polinomial1)
    variables_two = rpn.get_numbers(polinomial2)
    number_one = sort_variables(variables_one)
    substitution = max(len(variables_one), len(variables_two)) + 1
    previous_numbers = []
    negative_border = round(-(substitution * len(number_one) / 2))
    positive_border = round(substitution * len(number_one) / 2)
    for i in range(substitution):
        interpreted_polinomial1 = rpn.interpret(polinomial1)
        interpreted_polinomial2 = rpn.interpret(polinomial2)
        for num in number_one:
            number = random.randint(negative_border, positive_border)
            while number in previous_numbers:
                number = random.randint(negative_border, positive_border)
            previous_numbers.append(number)
            replace(interpreted_polinomial1,num, str(number))
            replace(interpreted_polinomial2, num, str(number))
        if check_left_variables(interpreted_polinomial1) or check_left_variables(interpreted_polinomial2):
            return False
        first_result = rpn.compute(interpreted_polinomial1)
        second_result = rpn.compute(interpreted_polinomial2)
        if abs(first_result - second_result) >= float(epsilon):
            return False
        i += 1
    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="This program compares polynomials, variables are inputed as x1,x2..,xn",
        epilog='(c) Anton Shishkin 2016.')
    parser.add_argument('polinomial_one')
    parser.add_argument('polinomial_two')
    parser.add_argument('epsilon', nargs='?', default='0.1')
    info = parser.parse_args()
    if compare(info.polinomial_one, info.polinomial_two, info.epsilon):
        print("Polinomials are equal")
    else:
        print("Polinomials are different")