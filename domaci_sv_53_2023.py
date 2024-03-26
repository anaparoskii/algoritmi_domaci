from tokenizer import tokenize


class EmptyStackError(Exception):
    pass


class Stack(object):
    def __init__(self):
        self._data = []

    def __len__(self):
        return len(self._data)

    def is_empty(self):
        return len(self._data) == 0

    def push(self, element):
        self._data.append(element)

    def pop(self):
        if self.is_empty():
            raise EmptyStackError("Stack is empty!")
        return self._data.pop()

    def top(self):
        if self.is_empty():
            raise EmptyStackError("Stack is empty!")
        return self._data[-1]


class InvalidParenthesesError(Exception):
    pass


class MultipleOperationsError(Exception):
    pass


class MultipleNumbersError(Exception):
    pass


class OperationPositionError(Exception):
    pass


class ParameterNumberError(Exception):
    pass


class ExpressionLengthError(Exception):
    pass


class InvalidResultError(Exception):
    pass


def infix_to_postfix(expression):
    operations = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2,
        '_': 3,  # unary minus
        '^': 4
    }
    stack = Stack()

    tokens = tokenize(expression)
    postfix = []

    # if there is no token in the expression
    if len(tokens) == 0:
        raise ExpressionLengthError("Empty expression!")
    # if there is only one operation in the expression
    if len(tokens) == 1 and tokens[0] not in "0123456789":
        raise ExpressionLengthError("Expression contains only one operation!")

    # if there is a binary operation in the beginning or in the end of the expression
    if tokens[0] in operations and tokens[0] != "-":
        raise OperationPositionError("Binary operation in the beginning of expression!")
    elif tokens[-1] in operations:
        raise OperationPositionError("Binary operation in the end of expression!")

    open_parentheses = 0
    closed_parentheses = 0
    parentheses_opened = False
    operation_detected = False
    number_detected = False
    unary = False

    if tokens[0] == "-":
        stack.push("_")
        unary = True
        operation_detected = True
        tokens = tokens[1:]

    for token in tokens:
        # if "-" isn't the first character after "(" then it's not unary
        if token != "-":
            parentheses_opened = False

        # if there are two operations in a row
        if token in operations and operation_detected:
            raise MultipleOperationsError("Multiple operations detected!")
        else:
            operation_detected = False

        # if there are two numbers in a row
        if token in "0123456789" and number_detected:
            raise MultipleNumbersError("Multiple numbers detected!")
        else:
            number_detected = False

        if token == "(":
            open_parentheses += 1
            parentheses_opened = True
            if not stack.is_empty() and stack.top() == "_":
                stack.push(token)
            else:
                stack.push(token)
        elif token == ")":
            closed_parentheses += 1
            while stack.top() != "(":
                postfix.append(stack.pop())
            stack.pop()
        elif token in operations:
            while (not stack.is_empty() and
                    stack.top() in operations and
                   operations[stack.top()] >= operations[token]):
                postfix.append(stack.pop())
            if token == "-" and parentheses_opened:
                stack.push("_")
                operation_detected = True
                unary = True
            else:
                stack.push(token)
                operation_detected = True
        else:
            postfix.append(token)
            number_detected = True

    while not stack.is_empty():
        if stack.top() == "_" and not unary:
            postfix.append("-")
            stack.pop()
        else:
            postfix.append(stack.pop())

    # if the number of open and closed parentheses is not equal
    if open_parentheses != closed_parentheses:
        raise InvalidParenthesesError("Invalid parentheses!")

    return postfix


def calculate_postfix(token_list):
    operations = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2,
        '_': 3,  # unary minus
        '^': 4
    }
    stack = Stack()
    
    for token in token_list:
        if token in operations and token != "_":
            operation = token
            if len(stack) < 2:
                raise ParameterNumberError("Invalid number of parameters!")
            else:
                second = stack.pop()
                first = stack.pop()
                if operation == "+":
                    stack.push(first + second)
                elif operation == "-":
                    stack.push(first - second)
                elif operation == "*":
                    stack.push(first * second)
                elif operation == "/":
                    if second == 0:
                        raise InvalidResultError("Division by zero!")
                    stack.push(first / second)
                elif operation == "^":
                    if first < 0 and second < 1:
                        raise InvalidResultError("Can't take root from negative number!")
                    stack.push(first ** second)
        elif token == "_":
            if len(stack) < 1:
                raise ParameterNumberError("Invalid number of parameters!")
            else:
                stack.push(0 - stack.pop())
        else:
            token = float(token)
            stack.push(token)

    return stack.pop()


def calculate_infix(expression):
    return calculate_postfix(infix_to_postfix(expression))


if __name__ == "__main__":
    value = input("Enter expression: ")
    postfix_value = infix_to_postfix(value)
    print("Postfix expression: {}".format(postfix_value))
    print("Result: %.2f" % calculate_infix(value))
