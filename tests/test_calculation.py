import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))

from calculation import Calculator, Operation, OperationLink


def test_calculate_respects_pemdas_for_addition_and_multiplication():
    head = OperationLink(2.0, Operation.ADD)
    head.AssignNext(OperationLink(3.0, Operation.MULTIPLY))
    head.next.AssignNext(OperationLink(4.0, Operation.END))

    calculator = Calculator(head)

    assert calculator.calculate() == 14.0


def test_string_representation_stops_at_end_marker():
    head = OperationLink(2.0, Operation.ADD)
    head.AssignNext(OperationLink(3.0, Operation.END))

    assert str(head) == "2.0 + 3.0 ="
