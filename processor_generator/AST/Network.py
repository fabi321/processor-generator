from weakref import ref, ReferenceType
from typing import List
from .ASTNode import ASTNode


class Network:
    def __init__(self):
        self.depends_on: List[ReferenceType[ASTNode]] = []
