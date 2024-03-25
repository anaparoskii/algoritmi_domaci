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


class OperationPositionError(Exception):
    pass


def infix_to_postfix(expression):
    operations = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2,
        '^': 3
    }

    tokens = tokenize(expression)
    stack = Stack()
    postfix = []

    unary = ""
    open_parentheses = 0
    parentheses_opened = False
    closed_parentheses = 0
    operation_detected = False

    if tokens[-1] in operations:
        raise OperationPositionError("Binary operation in the end of expression!")
    elif tokens[0] in operations and tokens[0] != "-":
        raise OperationPositionError("Binary operation in the beginning of expression!")

    if tokens[0] == "-":
        stack.push("_")
        unary = "-"
        operation_detected = True
        tokens = tokens[1:]

    for token in tokens:
        if token != "-":
            parentheses_opened = False

        if token in operations and operation_detected:
            raise MultipleOperationsError("Multiple operations detected!")
        else:
            operation_detected = False

        if token == "(":
            open_parentheses += 1
            parentheses_opened = True
            if not stack.is_empty() and stack.top() == "_":
                unary = ""
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
                stack.push("_")  # unary minus
                operation_detected = True
                unary = "-"
            else:
                stack.push(token)
                operation_detected = True
        else:
            if unary == "-" and stack.top() == "_":
                stack.pop()
                postfix.append(unary + token)
                unary = ""
            else:
                postfix.append(token)

    while not stack.is_empty():
        if stack.top() == "_":
            postfix.append("-")
            stack.pop()
        else:
            postfix.append(stack.pop())

    if open_parentheses != closed_parentheses:
        raise InvalidParenthesesError("Invalid parentheses!")

    return postfix


def calculate_postfix(token_list):
    """Funkcija izračunava vrednost izraza zapisanog u postfiksnoj notaciji

    Args:
        token_list (list): Lista tokena koja reprezentuje izraz koji se izračunava. Izraz može da sadrži cifre, zagrade,
         znakove računskih operacija.
        U slučaju da postoji problem sa brojem parametara, potrebno je baciti odgovarajući izuzetak.

    Returns:
        result: Broj koji reprezentuje konačnu vrednost izraza

    Primer:
        Ulaz [6.11, 74, 2, '*', '-'] se pretvara u izlaz -141.89
    """
    pass


def calculate_infix(expression):
    """Funkcija izračunava vrednost izraza zapisanog u infiksnoj notaciji

    Args:
        expression (string): Izraz koji se parsira. Izraz može da sadrži cifre, zagrade, znakove računskih operacija.
        U slučaju da postoji problem sa formatom ili sadržajem izraza, potrebno je baciti odgovarajući izuzetak.

        U slučaju da postoji problem sa brojem parametara, potrebno je baciti odgovarajući izuzetak.
        

    Returns:
        result: Broj koji reprezentuje konačnu vrednost izraza

    Primer:
        Ulaz '6.11 – 74 * 2' se pretvara u izlaz -141.89
    """
    pass


if __name__ == "__main__":
    print(infix_to_postfix("-20*.9/(3-7)"))
