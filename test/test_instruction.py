import unittest
from processor_generator.instruction.Instruction import *
from typing import List, Optional
from processor_generator.instruction.InstructionParameter import StoredInstructionParameter

PARAM1_NAME: str = 'param1'
PARAM1_SOURCE: str = '1-2,##,4-5'
PARAM2_NAME: str = 'param2'
PARAM2_SOURCE: str = '++,3-4,##'
PARAM1: StoredInstructionParameter = {'name': PARAM1_NAME, 'source': PARAM1_SOURCE}
PARAM2: StoredInstructionParameter = {'name': PARAM2_NAME, 'source': PARAM2_SOURCE}
PARAMETERS: List[InstructionParameter] = [
    InstructionParameter.from_obj(PARAM1),
    InstructionParameter.from_obj(PARAM2),
]
NAME: str = 'ADD'
DESCRIPTION: Optional[str] = 'desc'
ARCHITECTURE: str = '16bit'


class TestInstruction(unittest.TestCase):
    def test_constructor(self):
        ins = Instruction(NAME, DESCRIPTION, PARAMETERS, ARCHITECTURE)
        self.assertEqual(ins.name, NAME)
        self.assertEqual(ins.description, DESCRIPTION)
        self.assertEqual(ins.parameters, PARAMETERS)
        self.assertEqual(ins.architecture, ARCHITECTURE)

    def test_double_parameters(self):
        with self.assertRaises(ValueError):
            Instruction(NAME, DESCRIPTION, [*PARAMETERS, InstructionParameter(PARAM1_NAME, '#+#+')], ARCHITECTURE)

    def test_allowed_architectures(self):
        ins1 = Instruction(NAME, DESCRIPTION, PARAMETERS, ARCHITECTURE)
        for arch in ('8bit', '16bit', '32bit', '64bit'):
            ins1.architecture = arch
            ins2 = Instruction(NAME, DESCRIPTION, PARAMETERS, arch)
            self.assertEqual(ins1.architecture, arch)
            self.assertEqual(ins2.architecture, arch)
        with self.assertRaises(ValueError):
            ins1.architecture = 'no architecture'

    def test_from_obj(self):
        obj: StoredInstruction = {
            'name': NAME,
            'description': DESCRIPTION,
            'architecture': ARCHITECTURE,
            'parameters': [PARAM1, PARAM2]
        }
        ins = Instruction.from_obj(obj)
        self.assertEqual(ins.name, NAME)
        self.assertEqual(ins.parameters, PARAMETERS)
        self.assertEqual(ins.architecture, ARCHITECTURE)
        self.assertEqual(ins.description, DESCRIPTION)
        del obj['description']
        ins = Instruction.from_obj(obj)
        self.assertIsNone(ins.description)

    def test_eq(self):
        ins1 = Instruction(NAME, DESCRIPTION, PARAMETERS, ARCHITECTURE)
        obj: StoredInstruction = {
            'name': NAME,
            'description': DESCRIPTION,
            'architecture': ARCHITECTURE,
            'parameters': [PARAM1, PARAM2]
        }
        ins2 = Instruction.from_obj(obj)
        self.assertEqual(ins1, ins2)
        self.assertNotEqual(ins1, PARAMETERS[0])
        ins1.name = 'other'
        self.assertNotEqual(ins1, ins2)
        ins1.name = NAME
        ins2.architecture = '8bit'
        self.assertNotEqual(ins1, ins2)
        ins2.architecture = ARCHITECTURE
        ins1.description = None
        self.assertNotEqual(ins1, ins2)
        ins1.description = DESCRIPTION
        ins2.parameters.pop()
        self.assertNotEqual(ins1, ins2)
        ins2.parameters = PARAMETERS
        self.assertEqual(ins1, ins2)

    def test_parameters_for_instruction(self):
        ins = Instruction(NAME, DESCRIPTION, PARAMETERS, ARCHITECTURE)
        to_test: int = 0b0100_1101
        self.assertEqual(ins.parameters_for_instruction(to_test), {
            PARAM1_NAME: PARAMETERS[0].value(to_test),
            PARAM2_NAME: PARAMETERS[1].value(to_test),
        })
