import yaml
from yaml.loader import SafeLoader

from mazikeen.GeneratorLooper import serialReadYaml

class SafeLineLoader(SafeLoader):
    def construct_mapping(self, node, deep=False):
        mapping = super(SafeLineLoader, self).construct_mapping(node, deep=deep)
        # Add 1 so line numbering starts at 1
        mapping['__line__'] = node.start_mark.line + 1
        return mapping

with open('script_test.yaml') as f:
    data = yaml.load(f, Loader=SafeLineLoader)
    print ("data = ", data)
    res = serialReadYaml(data)
    pass