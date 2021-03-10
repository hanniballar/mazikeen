import unittest
import yaml
from GeneratorUtils import SafeLineLoader
from GeneratorException import GeneratorException
from GeneratorLooper import generateSerialBlock
from DiffBlock import DiffBlock
from Utils import diffStrategy

class GeneratorDiffBlock_test(unittest.TestCase):
    def test_basic(self):
        with open('TestFiles/GeneratorDiffBlock_test/test_basic/script.yaml') as f:
            data = yaml.load(f, Loader=SafeLineLoader)
            block = generateSerialBlock(data)
            self.assertTrue(isinstance(block.steps[0], DiffBlock))
            self.assertEqual(block.steps[0].binarycompare, True)
            self.assertEqual(block.steps[0].ignorelines, ['Time:'])
            self.assertEqual(block.steps[0].leftpath, 'output/leftpath')
            self.assertEqual(block.steps[0].rightpath, 'output/rightpath')
            self.assertEqual(block.steps[0].strategy, diffStrategy.IgnoreLeftOrphans)

    def test_simple_fail(self):
        with open('TestFiles/GeneratorDiffBlock_test/test_simple_fail/script.yaml') as f:
            data = yaml.load(f, Loader=SafeLineLoader)
            with self.assertRaisesRegex(GeneratorException, "'diff' block not recognized") as e:
                block = generateSerialBlock(data)

    def test_invalid_binarycompare(self):
        with open('TestFiles/GeneratorDiffBlock_test/test_invalid_binarycompare/script.yaml') as f:
            data = yaml.load(f, Loader=SafeLineLoader)
            with self.assertRaisesRegex(GeneratorException, "field 'binarycompare' expects a bool at line .*") as e:
                block = generateSerialBlock(data)

    def test_invalid_strategy(self):
        with open('TestFiles/GeneratorDiffBlock_test/test_invalid_strategy/script.yaml') as f:
            data = yaml.load(f, Loader=SafeLineLoader)
            with self.assertRaisesRegex(GeneratorException, "Invalid value 'IgnoreLeftOrphanss' for field 'strategy' at line .*") as e:
                block = generateSerialBlock(data)

    def test_invalid_ignorelines(self):
        with open('TestFiles/GeneratorDiffBlock_test/test_invalid_ignorelines/script.yaml') as f:
            data = yaml.load(f, Loader=SafeLineLoader)
            with self.assertRaisesRegex(GeneratorException, "field 'ignorelines' expects a list at line .*") as e:
                block = generateSerialBlock(data)
if __name__ == '__main__':
    unittest.main()
