from .Signal import Signal
from .Network import Network
from abc import ABC, abstractmethod
from weakref import ref, ReferenceType


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
        raise RuntimeError('Network belonging to signal has been destroyed')


class ConstantOperand(Operand):
    def __init__(self, constant: int):
        self.constant: int = constant

    def value(self) -> int:
        return self.constant
