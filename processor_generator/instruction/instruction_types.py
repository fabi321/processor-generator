from typing import TypedDict, List, Optional


class _StoredInstructionParameter(TypedDict):
    name: str
    source: str


class StoredInstructionParameter(_StoredInstructionParameter, total=False):
    description: Optional[str]


class _StoredInstruction(TypedDict):
    parameters: List[StoredInstructionParameter]
    name: str
    architecture: str


class StoredInstruction(_StoredInstruction, total=False):
    description: Optional[str]
