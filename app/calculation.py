from __future__ import annotations

import copy
import sys

class Operation:
    POWER = "^"
    ROOT = "%"
    MULTIPLY = "*"
    DIVIDE = "/"
    ADD = "+"
    SUBTRACT = "-"
    END = "="

class OperationLink:
    def __init__(self, number: float, operation: Operation):
        self.number = number
        self.operation = operation
        self.next = None
    def AssignOperation(self, operation: Operation):
        self.operation = operation
    def AssignNext(self, next_link: OperationLink):
        self.next = next_link
    def __str__(self):
        link = self
        val = ""
        while link is not None:
            if link.operation == Operation.END:
                val += f"{link.number} ="
                break
            val += f"{link.number} {link.operation} "
            link = link.next
        return val

class Calculator:
    def __init__(self, head):
        self.head = copy.copy(head)
        self.result = None

    def calculate(self):
        backup_head = copy.copy(self.head)
        if not self.head:
            raise ValueError("No calculation to perform.")

        current_link = self.head
        while current_link is not None and current_link.operation != Operation.END:
            if current_link.operation == Operation.POWER:
                current_link.number **= current_link.next.number
                current_link.operation = current_link.next.operation
                current_link.AssignNext(current_link.next.next)
            elif current_link.operation == Operation.ROOT:
                if current_link.next.number == 0:
                    raise ZeroDivisionError("Division by zero.")
                current_link.number **= 1 / current_link.next.number
                current_link.operation = current_link.next.operation
                current_link.AssignNext(current_link.next.next)
            else:
                current_link = current_link.next
        current_link = self.head
        
        while current_link is not None and current_link.operation != Operation.END:
            if current_link.operation == Operation.MULTIPLY:
                current_link.number *= current_link.next.number
                current_link.operation = current_link.next.operation
                current_link.AssignNext(current_link.next.next)
            elif current_link.operation == Operation.DIVIDE:
                if current_link.next.number == 0:
                    raise ZeroDivisionError("Division by zero.")
                current_link.number /= current_link.next.number
                current_link.operation = current_link.next.operation
                current_link.AssignNext(current_link.next.next)
            else:
                current_link = current_link.next
        current_link = self.head
        
        while current_link is not None and current_link.operation != Operation.END:
            if current_link.operation == Operation.ADD:
                current_link.number += current_link.next.number
                current_link.operation = current_link.next.operation
                current_link.AssignNext(current_link.next.next)
            elif current_link.operation == Operation.SUBTRACT:
                current_link.number -= current_link.next.number
                current_link.operation = current_link.next.operation
                current_link.AssignNext(current_link.next.next)
            else:
                current_link = current_link.next
        
        self.result = self.head.number
        self.head = backup_head
        return self.result