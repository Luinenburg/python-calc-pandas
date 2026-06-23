import calculation
from calculator_memento import data_handler

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
    username = input("Enter your username: ")
    user_data = data_handler(username)
    user_data.load_config_from_csv()
    user_data.load_history_from_csv()

    while True:
        user_input = input("Enter a calculation (or 'exit' to quit, or 'help' for commands): ")
        if user_input.lower() == 'exit':
            break
        elif user_input.lower() == 'history':
            history_df = user_data.get_history_dataframe()
            print(history_df)
            continue
        elif user_input.lower().startswith('history_size'):
            try:
                _, size_str = user_input.split()
                new_size = int(size_str)
                user_data.config.history_size = new_size
                print(f"History size updated to {new_size}.")
            except ValueError:
                print("Invalid history size command. Use 'history_size <number>'.")
            continue
        elif user_input.lower().startswith('clear'):
            user_data.history.clear()
            print("History cleared.")
            continue
        elif user_input.lower().startswith('help'):
            print("Available commands:")
            print("  exit - Quit the calculator")
            print("  history - Display calculation history")
            print("  history_size <number> - Set the maximum number of calculations to store")
            print("  clear - Clear the calculation history")
            print("  help - Display this help message")
            continue
        try:
            head = parse(user_input)
            if head is None:
                print("No calculation provided.")
                continue
            calculator = calculation.Calculator(head)
            result = calculator.calculate()
            print(f"Result: {result}")
            user_data.add_history_entry(user_input, result)
        except Exception as exception:
            print(f"Error: {exception}")

    user_data.save_history_to_csv()
    user_data.save_config_to_csv()

if __name__ == "__main__":
    test_repl()