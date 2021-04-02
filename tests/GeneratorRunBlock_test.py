import unittest
import yaml
from mazikeen.GeneratorLooper import generateSerialBlock
from mazikeen.GeneratorUtils import SafeLineLoader
from mazikeen.RunBlock import RunBlock
from mazikeen.GeneratorException import GeneratorException

class GeneratorRunBlock_test(unittest.TestCase):
    def test_basic(self):
        with open('TestFiles/GeneratorRunBlock_test/test_basic/script.yaml') as f:
            data = yaml.load(f, Loader=SafeLineLoader)
            block = generateSerialBlock(data)
            self.assertTrue(isinstance(block.steps[0], RunBlock))
            self.assertEqual(block.steps[0].exitcode, 0)
            self.assertEqual(block.steps[0].inputfile, 'input/inp.txt')
            self.assertEqual(block.steps[0].outputfile, 'output/out.txt')

    def test_basic_simple(self):
        with open('TestFiles/GeneratorRunBlock_test/test_basic_simple/script.yaml') as f:
            data = yaml.load(f, Loader=SafeLineLoader)
            block = generateSerialBlock(data)
            self.assertTrue(isinstance(block.steps[0], RunBlock))
            self.assertEqual(block.steps[0].exitcode, 0)
            self.assertEqual(block.steps[0].inputfile, None)
            self.assertEqual(block.steps[0].outputfile, None)

    def test_invalid_commad(self):
        with open('TestFiles/GeneratorRunBlock_test/test_invalid_commad/script.yaml') as f:
            data = yaml.load(f, Loader=SafeLineLoader)
            with self.assertRaisesRegex(GeneratorException, "'run' block not recognized") as e:
                block = generateSerialBlock(data)

    def test_invalid_exitcode(self):
        with open('TestFiles/GeneratorRunBlock_test/test_invalid_exitcode/script.yaml') as f:
            data = yaml.load(f, Loader=SafeLineLoader)
            with self.assertRaisesRegex(GeneratorException, "field 'exitCode' expects an integer at line .*") as e:
                block = generateSerialBlock(data)
if __name__ == '__main__':
    unittest.main()

