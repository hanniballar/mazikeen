import unittest
import yaml
from mazikeen.GeneratorLooper import generateSerialBlock
from mazikeen.GeneratorUtils import SafeLineLoader
from mazikeen.RmdirBlock import RmdirBlock
from mazikeen.GeneratorException import GeneratorException

class GeneratorRmdirBlock_test(unittest.TestCase):
    def test_basic(self):
        with open('TestFiles/GeneratorRmdirBlock_test/test_basic/script.yaml') as f:
            data = yaml.load(f, Loader=SafeLineLoader)
            block = generateSerialBlock(data)
            self.assertTrue(isinstance(block.steps[0], RmdirBlock))
            self.assertEqual(block.steps[0].dir, 'Output/GeneratorRmdirBlock_test/TestDir1')

if __name__ == '__main__':
    unittest.main()
