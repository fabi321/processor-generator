from abc import ABC, abstractmethod
from typing import Any
from weakref import ref, ReferenceType

from .Network import Network
from .Signal import Signal


class Operand(ABC):
    @abstractmethod
    def value(self) -> int:
        raise NotImplementedError


class SignalOperand(Operand):
    def __init__(self, network: Network, signal: Signal):
        self.network: ReferenceType[Network] = ref(network)
        self.signal: Signal = signal

    def value(self) -> int:
        if network := self.network():
            return network.get_signal_value(self.signal)
        raise RuntimeError("Network belonging to signal has been destroyed")

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, SignalOperand):
            return self.network == other.network and self.signal == other.signal
        return False

    def __repr__(self) -> str:
        return f"SignalOperand(network={self.network!r}, signal={self.signal!r})"


class ConstantOperand(Operand):
    def __init__(self, constant: int):
        self.constant: int = constant

    def value(self) -> int:
        return self.constant
