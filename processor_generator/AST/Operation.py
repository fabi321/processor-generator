from .ASTNode import ASTNode, Signals
from enum import Enum


class Operations(Enum):
    ADD = "+"
    SUBTRACT = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    MODULO = "%"
    EXPONENT = "^"
    LEFT_BIT_SHIFT = "<<"
    RIGHT_BIT_SHIFT = ">>"
    AND = "AND"
    OR = "OR"
    XOR = "XOR"


class Operation(ASTNode):
    def __init__(self, operation: Operations):
        super().__init__("Operation")
        self.operation: Operations = operation

    def output(self) -> Signals:
        raise NotImplementedError("")
