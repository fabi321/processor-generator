from processor_generator.AST.Operation import *
import unittest


class TestOperation(unittest.TestCase):
    def test_constructor(self):
        op = Operation(NumericOperator.OR)
        self.assertEqual(op.operation, NumericOperator.OR)
