import re
from autofix.util.OSUtil import MAX_INT
from autofix.util.version.BaseVersion import BaseVersion, compareVersionNumber
from autofix.util.version.VersionDistance import VersionDistance


class GeneralVersion(BaseVersion):
    """
    A concrete class implementing interface BaseVersion
    """
    _pattern = re.compile(r'([0-9]+(\.[0-9]+)*)')

    def __init__(self, version: str):
        longest = '0'
        for token in self._pattern.findall(version):
            longest = GeneralVersion._longer_token(longest, token[0])
        self._versionNum = longest
        self._version = version

    @staticmethod
    def _longer_token(tkn1: str, tkn2: str) -> str:
        seq1 = tkn1.split('.')
        seq2 = tkn2.split('.')
        if len(seq1) == len(seq2):
            for i in range(len(seq1)):
                if int(seq1[i]) > int(seq2[i]):
                    return tkn1
                elif int(seq1[i]) < int(seq2[i]):
                    return tkn2
        return tkn1 if len(seq1) >= len(seq2) else tkn2

    @property
    def versionNum(self):
        return self._versionNum

    def distance(self, other):
        seq1 = self.versionNum.split('.')
        seq2 = other.versionNum.split('.')
        for i in range(max(len(seq1), len(seq2))):
            a = 0 if i >= len(seq1) else int(seq1[i])
            b = 0 if i >= len(seq2) else int(seq2[i])
            if a > b:
                return VersionDistance(i, b - a, other)
            elif a < b:
                return VersionDistance(i, b - a, other)
        return VersionDistance(MAX_INT, 0, other)

    def __eq__(self, other):
        return compareVersionNumber(self.versionNum, other.versionNum) == 0

    def __lt__(self, other):
        cmp = compareVersionNumber(self.versionNum, other.versionNum)
        if cmp == 0:
            return str(self) < str(other)
        return cmp < 0

    def __gt__(self, other):
        cmp = compareVersionNumber(self.versionNum, other.versionNum)
        if cmp == 0:
            return str(self) > str(other)
        return cmp > 0

    def __ne__(self, other):
        return compareVersionNumber(self.versionNum, other.versionNum) != 0

    def __le__(self, other):
        cmp = compareVersionNumber(self.versionNum, other.versionNum)
        if cmp == 0:
            return str(self) <= str(other)
        return cmp < 0

    def __ge__(self, other):
        cmp = compareVersionNumber(self.versionNum, other.versionNum)
        if cmp == 0:
            return str(self) >= str(other)
        return cmp > 0


if __name__ == '__main__':
    exit()
