import unittest
import yaml
from mazikeen.GeneratorLooper import generateSerialBlock
from mazikeen.ScriptDataProcessor import SafeLineLoader
from mazikeen.MakedirsBlock import MakedirsBlock
from mazikeen.GeneratorException import GeneratorException

class GeneratorMakedirsBlock_test(unittest.TestCase):
    def test_basic(self):
        with open('TestFiles/MakedirsBlock_test/test_basic/script.yaml') as f:
            data = yaml.load(f, Loader=SafeLineLoader)
            block = generateSerialBlock(data)
            self.assertTrue(isinstance(block.steps[0], MakedirsBlock))
            self.assertEqual(block.steps[0].dir, 'Output/MkdirBlock_test/TestDir1')

if __name__ == '__main__':
    unittest.main()
