import unittest
import yaml
import re
import Loopers
from GeneratorLooper import generateSerialBlock, generateParallelBlock
from GeneratorException import GeneratorException
from GeneratorUtils import SafeLineLoader

class GeneratorSerialTest(unittest.TestCase):
    def test_basic(self):
        with open('TestFiles/GeneratorLooper_test/test_basic/script.yaml') as f:
            data = yaml.load(f, Loader=SafeLineLoader)
            block = generateSerialBlock(data)
            self.assertEqual(block.entries, [{'color': 'red', 'shape': 'circle'}, {'color': 'yellow', 'shape': 'square'}, {'shape': 'triangle'}])
            self.assertEqual(block.failfast, False)
            self.assertEqual(block.steps[0].steps, [])
            self.assertEqual(block.steps[0].entries, [{'color': 'red', 'shape': 'circle'}, {'color': 'yellow', 'shape': 'circle'}, {'color': 'red', 'shape': 'square'}, {'color': 'yellow', 'shape': 'square'}, {'color': 'red', 'shape': 'triangle'}, {'color': 'yellow', 'shape': 'triangle'}])
            self.assertEqual(block.steps[0].steps, [])

    def test_multipleEntries(self):
        with open('TestFiles/GeneratorLooper_test/test_multipleEntries/script.yaml') as f:
            data = yaml.load(f, Loader=SafeLineLoader)
            block = generateSerialBlock(data)
            self.assertEqual(block.entries, [{'color': 'red', 'shape': 'circle'}, {'color': 'yellow', 'shape': 'square'}, {'shape': 'triangle'}, {'fruit': 'apple', 'vegetable': 'onion'}, {'fruit': 'apple', 'vegetable': 'carot'}, {'fruit': 'banana', 'vegetable': 'onion'}, {'fruit': 'banana', 'vegetable': 'carot'}])
            self.assertEqual(block.steps, [])
    def test_invalid_field(self):
        with open('TestFiles/GeneratorLooper_test/test_invalid_field/script.yaml') as f:
            data = yaml.load(f, Loader=SafeLineLoader)
            with self.assertRaisesRegex(GeneratorException, "Only one of the following keys are allowed: .*") as e:
                block = generateSerialBlock(data)
    def test_invalid_entries_field(self):
        with open('TestFiles/GeneratorLooper_test/test_invalid_entries_field/script.yaml') as f:
            data = yaml.load(f, Loader=SafeLineLoader)
            with self.assertRaisesRegex(GeneratorException, "Only one of the following keys are allowed: .*") as e:
                block = generateSerialBlock(data)
    def test_parallel(self):
        with open('TestFiles/GeneratorLooper_test/test_parallel/script.yaml') as f:
            data = yaml.load(f, Loader=SafeLineLoader)
            block = generateSerialBlock(data)
            self.assertTrue(isinstance(block.steps[0], Loopers.Parallel))
            self.assertEqual(block.failfast, False)
            self.assertEqual(block.steps[0].entries, [{'color': 'red', 'shape': 'circle'}, {'color': 'yellow', 'shape': 'circle'}, {'color': 'red', 'shape': 'square'}, {'color': 'yellow', 'shape': 'square'}, {'color': 'red', 'shape': 'triangle'}, {'color': 'yellow', 'shape': 'triangle'}])
            self.assertEqual(block.steps[0].max_workers, 5)
            self.assertTrue(isinstance(block.steps[0].steps[0], Loopers.Serial))
    def test_parallel_invalid_max_workers(self):
        with open('TestFiles/GeneratorLooper_test/test_parallel_invalid_max_workers/script.yaml') as f:
            data = yaml.load(f, Loader=SafeLineLoader)
            with self.assertRaisesRegex(GeneratorException, "field 'max_workers' expects an integer at line .*") as e:
                block = generateSerialBlock(data)

if __name__ == '__main__':
    unittest.main()
