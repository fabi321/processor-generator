from __future__ import annotations

from typing import Optional, List, Any

from .InstructionSubParameter import InstructionSubParameter, sub_parameter_parser
from .instruction_types import StoredInstructionParameter


class InstructionParameter:
    def __init__(self, name: str, source: str, description: Optional[str] = None):
        self.name: str = name
        self.parameters: List[InstructionSubParameter] = []
        self.source: str = source
        self.description: Optional[str] = description

    @staticmethod
    def from_obj(obj: StoredInstructionParameter) -> InstructionParameter:
        return InstructionParameter(
            obj["name"],
            obj["source"],
            obj["description"] if "description" in obj else None,
        )

    @staticmethod
    def parse_parameters(parameters: str) -> List[InstructionSubParameter]:
        if not parameters:
            return []
        result: List[InstructionSubParameter] = []
        current_offset: int = 0
        for i in reversed(parameters.split(",")):
            sub_parameter: InstructionSubParameter = sub_parameter_parser(
                i, current_offset
            )
            result.append(sub_parameter)
            current_offset += sub_parameter.length
        result.reverse()
        return result

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        if name:
            self._name = name
        else:
            raise ValueError(f"Name mustn't be none or empty, got {name}")

    @property
    def source(self) -> str:
        return self._source

    @source.setter
    def source(self, source: str) -> None:
        if source:
            self._source = source
            self.parameters = self.parse_parameters(source)
        else:
            raise ValueError(f"Source mustn't be none or empty, got {source}")

    def __repr__(self) -> str:
        return f"InstructionParameter(name={self.name!r}, source={self.source!r}, description={self.description!r})"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, InstructionParameter):
            return (
                self.name == other.name
                and self.source == other.source
                and self.description == other.description
            )
        return False

    def value(self, using: int) -> int:
        return sum(sub_parameter.value(using) for sub_parameter in self.parameters)
