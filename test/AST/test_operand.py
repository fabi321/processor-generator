from processor_generator.AST.Operand import *
import unittest


class TestSignalOperand(unittest.TestCase):
    def test_constructor(self):
        net = Network()
        sig = Signal.SIGNAL_A
        op = SignalOperand(net, sig)
        self.assertEqual(op.signal, sig)
        self.assertIs(op.network(), net)

    def test_network_dropped(self):
        net = Network()
        op = SignalOperand(net, Signal.SIGNAL_A)
        del net
        with self.assertRaises(RuntimeError):
            op.value()

    def test_value(self):
        net = Network()
        sig = Signal.SIGNAL_A
        op = SignalOperand(net, sig)
        self.assertEqual(op.value(), 0)
        net.update_value(sig, 10)
        net.tick()
        self.assertEqual(op.value(), 10)
        net.update_value(Signal.SIGNAL_B, 10)
        net.tick()
        self.assertEqual(op.value(), 0)


class TestConstantOperand(unittest.TestCase):
    def test_constructo(self):
        op = ConstantOperand(10)
        self.assertEqual(op.constant, 10)

    def test_value(self):
        op = ConstantOperand(20)
        self.assertEqual(op.value(), 20)
