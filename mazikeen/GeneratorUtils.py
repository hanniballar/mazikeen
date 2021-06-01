from mazikeen.GeneratorException import GeneratorException

def getYamlInt(data, line, field):
    if data == None: return None
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