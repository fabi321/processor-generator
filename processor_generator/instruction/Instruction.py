from __future__ import annotations
from typing import Optional, List, Dict, Any
from .instruction_types import StoredInstruction
from .InstructionParameter import InstructionParameter


class Instruction:
    def __init__(
        self,
        name: str,
        description: Optional[str],
        parameters: List[InstructionParameter],
        architecture: str,
    ):
        self.name: str = name
        self.description: Optional[str] = description
        self.parameters: List[InstructionParameter] = parameters
        self.architecture: str = architecture

    @property
    def architecture(self) -> str:
        return self._architecture

    @architecture.setter
    def architecture(self, arch: str) -> None:
        if arch in ("8bit", "16bit", "32bit", "64bit"):
            self._architecture = arch
        else:
            raise ValueError(f'Invalid instruction architecture "{arch}"')

    @property
    def parameters(self) -> List[InstructionParameter]:
        return self._parameters

    @parameters.setter
    def parameters(self, params: List[InstructionParameter]) -> None:
        found = []
        for param in params:
            if param.name in found:
                raise ValueError("Same parameter cannot occur twice")
            found.append(param.name)
        self._parameters = params

    @staticmethod
    def from_obj(obj: StoredInstruction) -> Instruction:
        return Instruction(
            obj["name"],
            obj["description"] if "description" in obj else None,
            [InstructionParameter.from_obj(i) for i in obj["parameters"]],
            obj["architecture"],
        )

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Instruction):
            return (
                self.name == other.name
                and self.architecture == other.architecture
                and self.description == other.description
                and self.parameters == other.parameters
            )
        return False

    def __repr__(self) -> str:
        return (
            f"Instruction("
            f"name={self.name!r}, "
            f"description={self.description!r}, "
            f"parameters={self.parameters!r}, "
            f"architecture={self.architecture!r})"
        )

    def parameters_for_instruction(self, instruction: int) -> Dict[str, int]:
        return {
            parameter.name: parameter.value(instruction)
            for parameter in self.parameters
        }
