import re
from autofix.util.version.BaseVersion import BaseVersion
from autofix.util.Config import Config


class JavaVersion(BaseVersion):
    """
    A concrete class implementing interface BaseVersion
    """
    _pattern = re.compile(r'([0-9]+)')

    def __init__(self, version: str):
        m = self._pattern.fullmatch(version)
        if m is None:
            self._version = '0'
        else:
            self._version = m.group(1)

    @property
    def versionInt(self) -> int:
        return int(self._version)

    @classmethod
    def validate(cls, version: str):
        return JavaVersion._pattern.fullmatch(version) is not None

    def __eq__(self, other):
        return self.versionInt == other.versionInt

    def __lt__(self, other):
        return self.versionInt < other.versionInt

    def __gt__(self, other):
        return self.versionInt > other.versionInt

    def __ne__(self, other):
        return self.versionInt != other.versionInt

    def __le__(self, other):
        return self.versionInt <= other.versionInt

    def __ge__(self, other):
        return self.versionInt >= other.versionInt


defaultJava = JavaVersion(Config().get('JAVA', 'JAVA_DEFAULT'))
minJava = JavaVersion(Config().get('JAVA', 'JAVA_MIN'))
maxJava = JavaVersion(Config().get('JAVA', 'JAVA_MAX'))
zeroJava = JavaVersion('0')

if __name__ == '__main__':
    exit()
