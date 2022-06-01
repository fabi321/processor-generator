from weakref import ref, ReferenceType
from typing import List
from .ASTNode import ASTNode


class Network:
    def __init__(self) -> None:
        self.depends_on: List[ReferenceType[ASTNode]] = []

    def depend_on(self, node: ASTNode) -> None:
        self.depends_on.append(ref(node))
