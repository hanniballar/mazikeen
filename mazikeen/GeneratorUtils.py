from yaml.loader import SafeLoader

from mazikeen.GeneratorException import GeneratorException


class SafeLineLoader(SafeLoader):
    def construct_mapping(self, node, deep=False):
        mapping = super(SafeLineLoader, self).construct_mapping(node, deep=deep)
        # Add 1 so line numbering starts at 1
        mapping['__line__'] = node.start_mark.line + 1
        return mapping
        

def getYamlInt(data, line, field):
    if (not isinstance(data, int)):
        if (isinstance(data, dict)):
            raise GeneratorException(f"field '{field}' expects an integer at line {data['__line__']}")
        raise GeneratorException(f"field '{field}' expects an integer at line {line}")

    return data

def getYamlIntOrNone(data, line, field):
    if isinstance(data, str):
        if data.lower() == "none": return None
    if (not isinstance(data, int)):
        if (isinstance(data, dict)):
            raise GeneratorException(f"field '{field}' expects an integer at line {data['__line__']}")
        raise GeneratorException(f"field '{field}' expects an integer at line {line}")

    return data

def getYamlBool(data, line, field):
    if (not isinstance(data, bool)):
        if (isinstance(data, dict)):
            raise GeneratorException(f"field '{field}' expects a bool at line {data['__line__']}")
        raise GeneratorException(f"field '{field}' expects a bool at line {line}")
    return data

def getYamlString(data, line, field):
    if (not isinstance(data, str)):
        if (isinstance(data, dict)):
            raise GeneratorException(f"field '{field}' expects an integer at line {data['__line__']}")
        raise GeneratorException(f"field '{field}' expects a string at line {line}")
    return data

def getYamlList(data, line, field):
    if (not isinstance(data, list)):
        if (isinstance(data, dict)):
            raise GeneratorException(f"field '{field}' expects a list at line {data['__line__']}")
        raise GeneratorException(f"field '{field}' expects a list at line {line}")
    return data