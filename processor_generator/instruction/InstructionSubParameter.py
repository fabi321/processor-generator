from abc import ABC, abstractmethod

from typing import Any


class InstructionSubParameter(ABC):
    """
    A generic sub-parameter base class
    """

    def __init__(self, shift_by: int, length: int):
        self.shift_by: int = shift_by
        self.length: int = length

    @abstractmethod
    def _value(self, using: int) -> int:
        raise NotImplementedError

    def value(self, using: int) -> int:
        return self._value(using) << self.shift_by


class VariableInstructionSubParameter(InstructionSubParameter):
    """
    A sub-parameter that is based on the supplied number, and AND's it with a number
    that represents the inclusive input range
    """

    def __init__(self, shift_by: int, start: int, end: int):
        super().__init__(shift_by, end - start + 1)
        self.start: int = start
        self.end: int = end

    def mask(self) -> int:
        mask: int = 0
        for i in range(self.start, self.end + 1):
            mask |= 2 ** i
        return mask

    def _value(self, using: int) -> int:
        return (using & self.mask()) >> self.start

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, VariableInstructionSubParameter):
            return (
                self.start == other.start
                and self.end == other.end
                and self.shift_by == other.shift_by
            )
        return False

    def __repr__(self) -> str:
        return f"VariableInstructionSubParameter(shift_by={self.shift_by}, start={self.start}, end={self.end})"


class StaticInstructionSubParameter(InstructionSubParameter):
    """
    A sub-parameter that just returns a constant number
    """

    def __init__(self, shift_by: int, length: int, number: int):
        super().__init__(shift_by, length)
        self.number: int = number

    def _value(self, using: int) -> int:
        return self.number

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, StaticInstructionSubParameter):
            return (
                self.number == other.number
                and self.shift_by == other.shift_by
                and self.length == other.length
            )
        return False

    def __repr__(self) -> str:
        return f"StaticInstructionSubParameter(shift_by={self.shift_by}, length={self.length}, number={self.number})"


def sub_parameter_parser(parameter: str, shift_by: int) -> InstructionSubParameter:
    if "#" in parameter or "+" in parameter:
        if parameter.replace("#", "").replace("+", ""):
            raise ValueError(
                f"only allowed characters in static numbers are # for 0 and + for 1, got {parameter}"
            )
        num = parameter.replace("#", "0").replace("+", "1")
        return StaticInstructionSubParameter(shift_by, len(parameter), int(num, 2))
    try:
        start, end = parameter.split("-")
        if not start.isdigit():
            raise ValueError(
                f"The start of a parameter range needs to be an integer, got {start}"
            )
        if not end.isdigit():
            raise ValueError(
                f"The end of a parameter range needs to be an integer, got {end}"
            )
        start_n, end_n = int(start), int(end)
        if start_n > end_n:
            raise ValueError(
                f"The start of a parameter range may not be larger than the end, got {parameter}"
            )
        return VariableInstructionSubParameter(shift_by, start_n, end_n)
    except ValueError:
        raise ValueError(
            f'number ranges need to follow the format "int-int", got "{parameter}"'
        )
