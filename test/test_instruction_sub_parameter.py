import unittest
from processor_generator.instruction.InstructionSubParameter import *


class TestInstructionSubParameter(unittest.TestCase):
    def test_abstract(self):
        with self.assertRaises(TypeError):
            InstructionSubParameter(0, 1)

    def test_value(self):
        param = StaticInstructionSubParameter(10, 1, 1)
        self.assertEqual(param.value(0), 0b0100_0000_0000)


class TestVariableInstructionSubParameter(unittest.TestCase):
    def test_constructor(self):
        param = VariableInstructionSubParameter(2, 0, 5)
        self.assertEqual(param.start, 0)
        self.assertEqual(param.end, 5)
        self.assertEqual(param.shift_by, 2)

    def test_mask(self):
        param = VariableInstructionSubParameter(0, 0, 5)
        self.assertEqual(param.mask(), 0b0011_1111)
        param = VariableInstructionSubParameter(10, 0, 5)
        self.assertEqual(param.mask(), 0b0011_1111)
        param = VariableInstructionSubParameter(0, 2, 10)
        self.assertEqual(param.mask(), 0b0111_1111_1100)
        param = VariableInstructionSubParameter(0, 20, 30)
        self.assertEqual(param.mask(), 0b0111_1111_1111_0000_0000_0000_0000_0000)
        param = VariableInstructionSubParameter(0, 0, 0)
        self.assertEqual(param.mask(), 0b0001)

    def test_value(self):
        param = VariableInstructionSubParameter(0, 0, 5)
        self.assertEqual(param._value(0b1001_1010), 0b0001_1010)
        param = VariableInstructionSubParameter(0, 3, 5)
        self.assertEqual(param._value(0b1001_1010), 0b0011)
        param = VariableInstructionSubParameter(0, 0, 0)
        self.assertEqual(param.value(1), 1)

    def test_eq(self):
        param1 = VariableInstructionSubParameter(0, 1, 2)
        param2 = VariableInstructionSubParameter(0, 1, 2)
        self.assertEqual(param1, param2)
        param1.shift_by = 1
        self.assertNotEqual(param1, param2)
        param1.shift_by = 0
        param2.end = 1
        self.assertNotEqual(param1, param2)
        param2.end = 2
        param1.start = 0
        self.assertNotEqual(param1, param2)
        param1.start = 1
        self.assertEqual(param1, param2)
        param2 = StaticInstructionSubParameter(0, 1, 1)
        self.assertNotEqual(param1, param2)

    def test_repr(self):
        param = VariableInstructionSubParameter(0, 1, 2)
        self.assertEqual(repr(param), 'VariableInstructionSubParameter(shift_by=0, start=1, end=2)')

    def test_len(self):
        param = VariableInstructionSubParameter(0, 0, 0)
        self.assertEqual(param.length, 1)
        param = VariableInstructionSubParameter(10, 4, 8)
        self.assertEqual(param.length, 5)


class TestStaticInstructionSubParameter(unittest.TestCase):
    def test_constructor(self):
        param = StaticInstructionSubParameter(0, 1, 1)
        self.assertEqual(param.shift_by, 0)
        self.assertEqual(param.number, 1)
        self.assertEqual(param.length, 1)

    def test_value(self):
        param = StaticInstructionSubParameter(0, 1, 1)
        self.assertEqual(param._value(0), 1)
        self.assertEqual(param._value(100), 1)
        param = StaticInstructionSubParameter(10, 1, 0)
        self.assertEqual(param._value(0), 0)

    def test_eq(self):
        param1 = StaticInstructionSubParameter(0, 1, 1)
        param2 = StaticInstructionSubParameter(0, 1, 1)
        self.assertEqual(param1, param2)
        param1.shift_by = 1
        self.assertNotEqual(param1, param2)
        param1.shift_by = 0
        param2.number = 0
        self.assertNotEqual(param1, param2)
        param2.number = 1
        param1.length = 2
        self.assertNotEqual(param1, param2)
        param1.length = 1
        self.assertEqual(param1, param2)
        param2 = VariableInstructionSubParameter(0, 1, 2)
        self.assertNotEqual(param1, param2)

    def test_repr(self):
        param = StaticInstructionSubParameter(0, 1, 2)
        self.assertEqual(repr(param), 'StaticInstructionSubParameter(shift_by=0, length=1, number=2)')


class TestSubParameterParser(unittest.TestCase):
    def test_static(self):
        with self.assertRaises(ValueError):
            sub_parameter_parser('#1', 0)
        with self.assertRaises(ValueError):
            sub_parameter_parser('+a', 0)
        self.assertEqual(sub_parameter_parser('+#', 0), StaticInstructionSubParameter(0, 2, 0b10))

    def test_variable(self):
        with self.assertRaises(ValueError):
            sub_parameter_parser('aksdjl', 0)
        with self.assertRaises(ValueError):
            sub_parameter_parser('a-b', 0)
        with self.assertRaises(ValueError):
            sub_parameter_parser('a-1', 0)
        with self.assertRaises(ValueError):
            sub_parameter_parser('1-a', 0)
        with self.assertRaises(ValueError):
            sub_parameter_parser('1-0', 0)
        self.assertEqual(sub_parameter_parser('0-1', 0), VariableInstructionSubParameter(0, 0, 1))
        self.assertEqual(sub_parameter_parser('0-0', 0), VariableInstructionSubParameter(0, 0, 0))

    def test_shift_by(self):
        self.assertEqual(sub_parameter_parser('#+#+', 1).shift_by, 1)
        self.assertEqual(sub_parameter_parser('2-3', 5).shift_by, 5)

