import re
from autofix.util.Config import Config
from autofix.util.version.BaseVersion import BaseVersion, compareVersionNumber


class GradleVersion(BaseVersion):
    """
    A concrete class implementing interface BaseVersion
    Gradle version format: [VERSION]-[M/RC]-[M/RC NUMBER]-[YYYYMMDDHHMMSS][-/+][ZONE]
    Ex: 4.10.2-milestone-3a-20181012073855+0800
        Group 1: 4.10.2
        Group 3: -milestone-3a
        Group 4: milestone
        Group 5: 3a
        Group 6: -20181012073855+0800
        Group 7: 20181012073855+0800
    """
    _pattern = re.compile(r'([0-9]+([.][0-9]+)*)(-(milestone|rc)-([0-9a-z]+))?(-([0-9]{14}[-+][0-9]{4}))?')

    def __init__(self, version: str):
        m = self._pattern.fullmatch(version)
        if m is None:
            self._version = '0'
            self._versionNum = '0'
            self._releaseType = ''
            self._releaseNum = ''
        else:
            self._versionNum = m.group(1)
            while len(self._versionNum.split('.')) > 2 and int(self._versionNum.split('.')[-1]) == 0:
                self._versionNum = '.'.join(self._versionNum.split('.')[:-1])
            self._version = self._versionNum + ('' if m.group(3) is None else m.group(3))
            self._releaseType = '' if m.group(4) is None else m.group(4)
            self._releaseNum = '' if m.group(5) is None else m.group(5)

    @property
    def versionNum(self):
        return self._versionNum

    @property
    def releaseType(self):
        return self._releaseType

    @property
    def releaseNum(self):
        return self._releaseNum

    @classmethod
    def validate(cls, version: str):
        return GradleVersion._pattern.fullmatch(version) is not None

    @staticmethod
    def _compareRelease(type1: str, num1: str, type2: str, num2: str):
        if type1 is '' and type2 is '':
            return 0
        elif type1 is '':
            return 1
        elif type2 is '':
            return -1
        elif type1 == type2:
            return 1 if num1 > num2 else (-1 if num1 < num2 else 0)
        else:
            d = {'rc': 2, 'milestone': 1}
            return 1 if d[type1] > d[type2] else (-1 if d[type2] > d[type1] else 0)

    def __eq__(self, other):
        return self.versionNum == other.versionNum and \
               self.releaseType == other.releaseType and \
               self.releaseNum == other.releaseNum

    def __lt__(self, other):
        cmp = compareVersionNumber(self.versionNum, other.versionNum)
        if cmp < 0:
            return True
        elif cmp > 0:
            return False
        cmp = GradleVersion._compareRelease(self.releaseType, self.releaseNum, other.releaseType, other.releaseNum)
        return cmp < 0

    def __gt__(self, other):
        cmp = compareVersionNumber(self.versionNum, other.versionNum)
        if cmp > 0:
            return True
        elif cmp < 0:
            return False
        cmp = GradleVersion._compareRelease(self.releaseType, self.releaseNum, other.releaseType, other.releaseNum)
        return cmp > 0

    def __ne__(self, other):
        return not self.__eq__(other)

    def __le__(self, other):
        return not self.__gt__(other)

    def __ge__(self, other):
        return not self.__lt__(other)


defaultGradle = GradleVersion(Config().get('GRADLE', 'GRADLE_DEFAULT'))
zeroGradle = GradleVersion('0')


if __name__ == '__main__':
    exit()
