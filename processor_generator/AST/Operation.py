from enum import Enum
from typing import Optional

from .ASTNode import ASTNode, Signals
from .Operand import Operand, ConstantOperand


class NumericOperator(Enum):
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
    def __init__(
        self,
        operation: NumericOperator,
        left: Optional[Operand] = None,
        right: Optional[Operand] = None,
    ):
        super().__init__("Operation")
        self.operation: NumericOperator = operation
        self.left: Operand = left if left else ConstantOperand(0)
        self.right: Operand = right if right else ConstantOperand(0)

    def output(self) -> Signals:
        raise NotImplementedError("")
