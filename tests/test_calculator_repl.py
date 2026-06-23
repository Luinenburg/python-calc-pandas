import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "app"))

from calculation import Operation
from calculator_repl import parse
from calculation import Calculator

def test_parse_returns_none_for_empty_input():
    assert parse("") is None


def test_parse_builds_a_simple_linked_list_and_solves():
    string = "2 + 3 ="
    head = parse(string)

    assert head is not None
    assert head.number == 2.0
    assert head.operation == Operation.ADD

    assert head.next is not None
    assert head.next.number == 3.0
    assert head.next.operation == Operation.END

    calculator = Calculator(head)
    assert calculator.calculate() == 5.0
    assert calculator.head != head

def test_parse_raises_for_operator_without_a_preceding_number():
    with pytest.raises(ValueError, match="cannot be assigned"):
        parse("+ 3 =")

def test_parse_builds_a_complex_linked_list_and_solves():
    string = "2 + 3 * 6 ^ 2 - 6 / 4 % 2 ="
    head = parse(string)

    assert head is not None
    assert head.number == 2.0
    assert head.operation == Operation.ADD

    assert head.next is not None
    assert head.next.number == 3.0
    assert head.next.operation == Operation.MULTIPLY

    assert head.next.next is not None
    assert head.next.next.number == 6.0
    assert head.next.next.operation == Operation.POWER

    assert head.next.next.next is not None
    assert head.next.next.next.number == 2.0
    assert head.next.next.next.operation == Operation.SUBTRACT

    assert head.next.next.next.next is not None
    assert head.next.next.next.next.number == 6.0
    assert head.next.next.next.next.operation == Operation.DIVIDE

    assert head.next.next.next.next.next is not None
    assert head.next.next.next.next.next.number == 4
    assert head.next.next.next.next.next.operation == Operation.ROOT

    assert head.next.next.next.next.next.next is not None
    assert head.next.next.next.next.next.next.number == 2
    assert head.next.next.next.next.next.next.operation == Operation.END

    calculator = Calculator(head)
    assert calculator.calculate() == 107
    assert calculator.head != head