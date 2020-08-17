from autofix.util.version.BaseVersion import BaseVersion


class VersionDistance(BaseVersion):
    def __init__(self, index: int, differ: int, reference: BaseVersion):
        self._index = index
        self._differ = differ
        self._reference = reference
        self._version = str(reference)

    @property
    def index(self) -> int:
        return self._index

    @property
    def differ(self) -> int:
        return self._differ

    @property
    def reference(self) -> BaseVersion:
        return self._reference

    def __eq__(self, other):
        return str(self) == str(other)

    def __lt__(self, other):
        if self.index == other.index:
            if self.differ == other.differ:
                if self.reference == other.reference:
                    return str(self) < str(other)
                return self.reference > other.reference if self.differ < 0 else self.reference < other.reference
            elif abs(self.differ) == abs(other.differ):
                return self.differ > 0
            return abs(self.differ) < abs(other.differ)
        return self.index > other.index

    def __gt__(self, other):
        if self.index == other.index:
            if self.differ == other.differ:
                if self.reference == other.reference:
                    return str(self) > str(other)
                return self.reference > other.reference if self.differ > 0 else self.reference < other.reference
            elif abs(self.differ) == abs(other.differ):
                return self.differ < 0
            return abs(self.differ) > abs(other.differ)
        return self.index < other.index

    def __ne__(self, other):
        return not self.__eq__(other)

    def __le__(self, other):
        return not self.__gt__(other)

    def __ge__(self, other):
        return not self.__lt__(other)


if __name__ == '__main__':
    exit()
