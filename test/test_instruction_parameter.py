import unittest
from processor_generator.instruction.InstructionParameter import InstructionParameter
from processor_generator.instruction.instruction_types import StoredInstructionParameter
from processor_generator.instruction.InstructionSubParameter import sub_parameter_parser


NAME: str = 'ADD'
SOURCE: str = '1-2'
DESCRIPTION: str = 'abc'


def get_param() -> InstructionParameter:
    return InstructionParameter(
        NAME,
        SOURCE,
        DESCRIPTION
    )


class InstructionParameterTest(unittest.TestCase):
    def test_constructor(self):
        param = InstructionParameter(NAME, SOURCE, DESCRIPTION)
        self.assertEqual(param.name, NAME)
        self.assertEqual(param.source, SOURCE)
        self.assertEqual(param.description, DESCRIPTION)
        self.assertEqual(param.parameters, InstructionParameter.parse_parameters(SOURCE))

    def test_from_obj(self):
        obj: StoredInstructionParameter = {
            'source': SOURCE,
            'description': DESCRIPTION,
            'name': NAME,
        }
        param: InstructionParameter = InstructionParameter.from_obj(obj)
        self.assertEqual(param.name, NAME)
        self.assertEqual(param.source, SOURCE)
        self.assertEqual(param.description, DESCRIPTION)
        del obj['description']
        param: InstructionParameter = InstructionParameter.from_obj(obj)
        self.assertIsNone(param.description)
        obj['description'] = None
        param: InstructionParameter = InstructionParameter.from_obj(obj)
        self.assertIsNone(param.description)

    def test_set_name(self):
        param: InstructionParameter = get_param()
        with self.assertRaises(ValueError):
            param.name = None
        param.name = 'def'
        self.assertEqual(param.name, 'def')

    def test_set_source(self):
        param: InstructionParameter = get_param()
        with self.assertRaises(ValueError):
            param.source = None
        param.source = '4-5'
        self.assertEqual(param.source, '4-5')
        self.assertEqual(param.parameters, [
            sub_parameter_parser('4-5', 0)
        ])

    def test_set_description(self):
        param: InstructionParameter = get_param()
        param.description = ''
        self.assertEqual(param.description, '')
        param.description = None
        self.assertIsNone(param.description)

    def test_parse_parameters(self):
        self.assertEqual(InstructionParameter.parse_parameters(''), [])
        self.assertEqual(InstructionParameter.parse_parameters('1-2'), [
            sub_parameter_parser('1-2', 0),
        ])
        self.assertEqual(InstructionParameter.parse_parameters('+#'), [
            sub_parameter_parser('+#', 0),
        ])
        self.assertEqual(InstructionParameter.parse_parameters('1-2,+#'), [
            sub_parameter_parser('1-2', 2),
            sub_parameter_parser('+#', 0),
        ])
        self.assertEqual(InstructionParameter.parse_parameters('#,1-2'), [
            sub_parameter_parser('#', 2),
            sub_parameter_parser('1-2', 0),
        ])

    def test_repr(self):
        param = get_param()
        self.assertEqual(repr(param), f'InstructionParameter(name={NAME!r}, source={SOURCE!r}, description={DESCRIPTION!r})')

    def test_eq(self):
        param1 = InstructionParameter(NAME, SOURCE, DESCRIPTION)
        param2 = InstructionParameter.from_obj({
            'name': NAME,
            'source': SOURCE,
            'description': DESCRIPTION
        })
        self.assertEqual(param1, param2)
        sub_param = sub_parameter_parser('1-2', 0)
        self.assertNotEqual(param1, sub_param)
        param1.name = 'other'
        self.assertNotEqual(param1, param2)
        param1.name = NAME
        param2.source = '##++'
        self.assertNotEqual(param1, param2)
        param2.source = SOURCE
        param1.description = None
        self.assertNotEqual(param1, param2)
        param1.description = DESCRIPTION
        self.assertEqual(param1, param2)

    def test_value(self):
        param = InstructionParameter(NAME, '++')
        self.assertEqual(param.value(0), 0b11)
        param = InstructionParameter(NAME, '0-1')
        self.assertEqual(param.value(0b10), 0b10)
        param = InstructionParameter(NAME, '0-3,##')
        self.assertEqual(param.value(0b1011_0100), 0b0001_0000)
        param = InstructionParameter(NAME, '##,0-3,++')
        self.assertEqual(param.value(0b1011_0100), 0b0001_0011)
        param = InstructionParameter(NAME, '+,1-4,#,0-0')
        self.assertEqual(param.value(0b1011_0100), 0b0110_1000)
