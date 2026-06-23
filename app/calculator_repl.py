import calculation


def parse(calculation_string: str):
    """
    Parses a calculation string into a linked list of OperationLink objects.
    """
    tokens = calculation_string.split()
    if not tokens:
        return None

    head = None
    current_link = None

    for token in tokens:
        if token == calculation.Operation.END:
            if current_link is not None:
                current_link.AssignOperation(calculation.Operation.END)
            break

        if token in [calculation.Operation.POWER, calculation.Operation.ROOT, calculation.Operation.MULTIPLY, calculation.Operation.DIVIDE, calculation.Operation.ADD, calculation.Operation.SUBTRACT]:
            if current_link is None:
                raise ValueError(f"Operation '{token}' cannot be assigned without a preceding number.")
            current_link.AssignOperation(token)
            continue

        try:
            number = float(token)
        except ValueError as exception:
            raise ValueError(f"Invalid token: {token}") from exception

        new_link = calculation.OperationLink(number, None)
        if head is None:
            head = new_link
        elif current_link is not None:
            current_link.AssignNext(new_link)
        current_link = new_link

    if head is not None and current_link is not None and current_link.operation is None:
        current_link.AssignOperation(calculation.Operation.END)

    return head

def test_repl():
    while True:
        user_input = input("Enter a calculation (or 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break
        try:
            head = parse(user_input)
            if head is None:
                print("No calculation provided.")
                continue
            calculator = calculation.Calculator(head)
            result = calculator.calculate()
            print(f"Result: {result}")
        except Exception as exception:
            print(f"Error: {exception}")

if __name__ == "__main__":
    test_repl()