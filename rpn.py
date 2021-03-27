import re


def get_operators(polinomial):
    operators = re.split(r'(?<=[(])-\d+\.\d+|^-\d+\.\d+|\d+\.\d+|'
                         r'(?<=[(])-\w\d*|^-\w\d*|\w\d*', polinomial)
    operators = [x for x in operators if x]
    op = ''.join(operators)
    return re.findall(r'[\+/\*\^\(\)-]', op)


def get_numbers(polinomial):
    return re.findall(r'(?<=[(])-\d+\.\d+|^-\d+\.\d+|\d+\.\d+|'
                      r'(?<=[(])-\w\d*|^-\w\d*|\w\d*', polinomial)


def unary_minus_handler(polinomial):
    if polinomial[0:2] == '-(':
        polinomial = '(-1)*' + polinomial[1:]
    return polinomial.replace('(-(', '((-1)*(')


def add_multiplication(polinomial):
    new_polinomial = polinomial[0]
    num = list(set(re.findall(r'\w', polinomial)))
    variables = [x for x in num if x not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                                             '(', ')', '-', '+', '/', '*', '^']]
    for i in range(1, len(polinomial)):
        if (polinomial[i-1] in num and
                (polinomial[i] in variables or polinomial[i] == '(')) \
                or (polinomial[i-1] == ')' and polinomial[i] == '(') \
                or (polinomial[i] in num
                    and polinomial[i-1] == ')'):
            new_polinomial += '*'
        new_polinomial += polinomial[i]
    return new_polinomial


def polinomial_to_list(polinomial):
    numbers = get_numbers(polinomial)
    operators = get_operators(polinomial)
    new_polinomial = []
    i = 0
    j = 0
    while len(polinomial) > 0:
        if not polinomial.find(numbers[i]):
            new_polinomial.append(numbers[i])
            polinomial = polinomial[len(numbers[i]):]
            if i < (len(numbers) - 1):
                i += 1
        else:
            new_polinomial.append(operators[j])
            polinomial = polinomial[1:]
            j += 1
    return new_polinomial


def operators_handler(operator, output_line, stack):
    if operator == ')':
        try:
            stack.index('(')
        except ValueError:
            raise ValueError("Unclosed bracket")
        while stack[len(stack) - 1] != "(":
            output_line.append(stack[len(stack) - 1])
            stack.pop(len(stack) - 1)
        stack.pop(len(stack) - 1)
    elif operator == '+' or operator == '-':
        while stack[len(stack) - 2] != "(" and len(stack) > 1:
            output_line.append(stack[len(stack) - 2])
            stack.pop(len(stack) - 2)
    elif operator == '*' or operator == '/':
        while not stack[len(stack) - 2] in ['+', '-', '(', ')'] \
                and len(stack) > 1:
            output_line.append(stack[len(stack) - 2])
            stack.pop(len(stack) - 2)


def extract_left_operators(output_line, stack, operator1, operator2):
    for j in range(len(stack)):
        if stack[j] == operator1 or stack[j] == operator2:
            output_line.append(stack[j])


def interpret(polinomial):
    polinomial = polinomial.replace(' ', '')
    polinomial = unary_minus_handler(polinomial)
    polinomial = add_multiplication(polinomial)
    operators = get_operators(polinomial)
    polinomial = polinomial_to_list(polinomial)
    stack = []
    output_line = []
    for i in range(len(polinomial)):
        if not polinomial[i] in operators:
            output_line.append(polinomial[i])
        else:
            if polinomial[i] != ')':
                stack.append(polinomial[i])
            operators_handler(polinomial[i], output_line, stack)
        i += 1
    for i in range(len(stack)):
        if stack[i] == '^':
            output_line.append(stack[i])
    extract_left_operators(output_line, stack, '*', '/')
    extract_left_operators(output_line, stack, '+', '-')
    if '(' in stack:
        raise ValueError('Unclosed bracket')
    return output_line


def compute(sentence):
    def operation():
        sentence[i - 2] = result
        sentence.pop(i)
        sentence.pop(i - 1)
    while len(sentence) > 1:
        i = 0
        while i < len(sentence):
            if sentence[i] in ['+', '-', '*', '/', '^']:
                try:
                    if sentence[i] == '+':
                        result = float(sentence[i-2]) + float(sentence[i-1])
                        operation()
                    elif sentence[i] == '-':
                        result = float(sentence[i-2]) - float(sentence[i-1])
                        operation()
                    elif sentence[i] == '*':
                        result = float(sentence[i - 2]) * float(sentence[i - 1])
                        operation()
                    elif sentence[i] == '/':
                        if sentence[i-1] == '0':
                            raise ZeroDivisionError("Attempted to divide by zero")
                        result = float(sentence[i - 2]) / float(sentence[i - 1])
                        operation()
                    elif sentence[i] == '^':
                        result = float(sentence[i-2]) ** float(sentence[i-1])
                        operation()
                    i = 0
                except ValueError:
                    raise ValueError("Too many operators")
            i += 1
    string_format_of_sentence = str(sentence[0])
    if string_format_of_sentence.find('e') != -1:
        sentence[0] = float(string_format_of_sentence[0:string_format_of_sentence.index('e')])
    return float(sentence[0])
