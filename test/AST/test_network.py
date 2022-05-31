from processor_generator.AST.Network import *
import unittest


class TestNetwork(unittest.TestCase):
    def test_constructor(self):
        net = Network()
        self.assertEqual(net.depends_on, [])
