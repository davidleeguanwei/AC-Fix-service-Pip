import re
from autofix.util.version.GeneralVersion import GeneralVersion
from autofix.util.Config import Config


class PythonVersion(GeneralVersion):
    _pattern = re.compile(r'([0-9]+(\.[0-9]+)*)')

    def __init__(self, version: str):
        longest = '0'
        for token in self._pattern.findall(version):
            longest = GeneralVersion._longer_token(longest, token[0])
        self._versionNum = longest
        self._version = version
        

defaultPython = PythonVersion(Config().get('PYTHON', 'PYTHON_DEFAULT'))
minPython = PythonVersion(Config().get('PYTHON', 'PYTHON_MIN'))
maxPython = PythonVersion(Config().get('PYTHON', 'PYTHON_MAX'))
zeroPython = PythonVersion('0')

if __name__ == '__main__':
    exit()
