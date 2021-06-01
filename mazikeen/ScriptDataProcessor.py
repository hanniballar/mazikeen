import copy
import yaml
from yaml.loader import SafeLoader

from mazikeen.ConsolePrinter import Printer

class SafeLineLoader(SafeLoader):
    def construct_mapping(self, node, deep=False):
        mapping = super(SafeLineLoader, self).construct_mapping(node, deep=deep)
        # Add 1 so line numbering starts at 1
        mapping['__line__'] = node.start_mark.line + 1
        return mapping

class Version():
    def __init__(self, versionStr): 
        (self.major, self.minor, self.patch) = ("", "", "")
        if versionStr == None or versionStr == "": 
            return

        versionTupl = versionStr.split('.')
        if len(versionTupl) > 3: 
            raise Exception("Invalid version. Version is too long")
        try:
            if len(versionTupl) >= 1: 
                self.major = int(versionTupl[0])
            if len(versionTupl) >= 2: 
                self.minor = int(versionTupl[1])
            if len(versionTupl) == 3: 
                self.patch = int(versionTupl[2])
        except ValueError as e:
            raise ValueError("Invalid version. Version may only contain numbers")

    def __hash__(self):
        return self.major * 10000 + self.minor * 100 + self.patch

    def __eq__(self, other):
        return (self.major == self.major and
                self.minor == self.minor and
                self.patch == self.patch)

    def __lt__(self, other):
        if self.major == "" and other.major != "": return True;
        if self.major < other.major: return True;
        if self.minor == "" and other.minor != "": return True;
        if self.minor < other.minor: return True;
        if self.patch == "" and other.patch != "": return True;
        if self.patch < other.patch: return True;

    def __str__(self):
        return f"{str(self.major)}.{str(self.minor)}.{str(self.patch)}"


def __upgradeScript1_0_0(data):
    def fixDiffBlock(data):
        if not isinstance(data, dict): 
            return data
        leftpath = ""
        rightpath = ""
        leftpathkey = None
        rightpathkey = None
        for key in data:
            if key.lower() == "leftpath":
                leftpath = data[key]
                leftpathkey = key
            elif key.lower() == "rightpath":
                rightpath = data[key]
                rightpathkey = key
        if leftpathkey: data.pop(leftpathkey, None)
        if rightpathkey: data.pop(rightpathkey, None)
        if (leftpath == "" and rightpath == ""):
            return data
        data["paths"] = "\"" + leftpath + "\" \"" + rightpath + "\""
        return data
    
    def fixRunBlock(data):
        if isinstance(data, str):
            return {'__line__': -1, 'cmd' : data, 'exitcode': 0}
        if not isinstance(data, dict): 
            return data
        for key in data:
            exitcode = None
            if key.lower() == "exitCode":
                exitcode = data[key]
        if exitcode == None:
            data["exitcode"] = 0
        return data

    def fixLooperData(data):
        for key in data:
            if key.lower() == "steps":
                fixStepsData(data[key])

    def fixStepsData(data):
        if data == None: return
        if not isinstance(data, list): 
            raise Exception("Scriptfile can not be upgraded")

        for step in data:
            for key in step:
                if key.lower() == "steps":
                    fixStepsData(step[key])
                if key.lower() == "run":
                    step[key] = fixRunBlock(step[key])
                if key.lower() == "diff":
                    step[key] = fixDiffBlock(step[key])

    data["version"]="1.1.0"
    fixLooperData(data)
    return (data, Version("1.1.0"))

def __upgradeScript1_1_0(data):
    def fixLooperData(data):
        for key in data:
            if key.lower() == "steps":
                fixStepsData(data[key])

    def fixStepsData(data):
        if data == None: return
        if not isinstance(data, list): 
            raise Exception("Scriptfile can not be upgraded")

        for step in data:
            for key in step:
                if key.lower() == "steps":
                    fixStepsData(step[key])
                if key.lower() == "diff":
                    step[key] = fixDiffBlock(step[key])
                if key.lower() == "run":
                    step[key] = fixRunBlock(step[key])

    def fixRunBlock(data):
        if not isinstance(data, dict): 
            return data
        for key in data:
            if key.lower() == "exitcode":
                if data[key] == 'None':
                    data.pop(key, None)
                break
        return data

    def fixDiffBlock(data):
        if not isinstance(data, dict): 
            return data
        for key in data:
            if key.lower() == "ignoreline":
                data['ignore'] = data[key]
                data.pop(key, None)
                break
        return data

    data["version"]="1.2.0"
    fixLooperData(data)
    return (data, Version("1.2.0"))

__upgradeDic = {Version("1.0.0"): __upgradeScript1_0_0,
                Version("1.1.0"): __upgradeScript1_1_0,}
__workingVersion = Version("1.2.0")

def __upgradeScriptData(data_, printer):
    if data_ == None: return (False, data_)
    data = data_.copy()

    upgraded = False
    currentVersion = Version(data.get("version", str(__workingVersion)))
    if (currentVersion < __workingVersion): 
        printer.verbose(f"Warning: script file needs to be upgraded to version: {str(__workingVersion)}. Use --upgradeScriptFile to save upgraded script file")
        upgraded = True
    while(currentVersion < __workingVersion):
        (data, currentVersion) = __upgradeDic[currentVersion](data)
    return (upgraded, data)

def __removeLineInfo(data):
    if isinstance(data, dict):
        data.pop("__line__", None)
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict) or isinstance(item, list):
                __removeLineInfo(item)
    if isinstance(data, dict):
        for key in data:
            if isinstance(data[key], dict) or isinstance(data[key], list): 
                __removeLineInfo(data[key])

def processScriptData(file, saveUpgradedScript = False, printer = Printer()):
    with open(file) as f:
        data = yaml.load(f, Loader=SafeLineLoader)
    if data == None: return data
    (upgradedScript, data) = __upgradeScriptData(data, printer)
    if saveUpgradedScript and upgradedScript:
        dumpData = copy.deepcopy(data)
        __removeLineInfo(dumpData)
        with open(file, "w") as f:
            yaml.dump(dumpData, f)
    data.pop("version", None)
    return data
