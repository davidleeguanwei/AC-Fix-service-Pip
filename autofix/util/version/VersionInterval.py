import re
from abc import ABCMeta, abstractmethod
from autofix.util.OSUtil import MAX_INT
from autofix.util.version.GeneralVersion import GeneralVersion


class VersionInterval:
    def __init__(self, lower: GeneralVersion, lclosed: bool, upper: GeneralVersion, rclosed: bool):
        if lower > upper:
            raise ValueError('Invalid interval: lower bound is higher than upper bound.')
        self._lower = lower
        self._lclosed = lclosed
        self._upper = upper
        self._rclosed = rclosed

    @property
    def lower(self) -> GeneralVersion:
        return self._lower

    @property
    def lclosed(self) -> bool:
        return self._lclosed

    @property
    def upper(self) -> GeneralVersion:
        return self._upper

    @property
    def rclosed(self) -> bool:
        return self._rclosed

    def contain(self, item: GeneralVersion):
        if self.lclosed and item < self.lower:
            return -1
        if not self.lclosed and item <= self.lower:
            return -1
        if self.rclosed and item > self.upper:
            return 1
        if not self.rclosed and item >= self.upper:
            return 1
        return 0

    def __str__(self):
        return '{}{}, {}{}'.format('[' if self.lclosed else '(', self.lower, self.upper, ']' if self.rclosed else ')')


class VersionIntervalHandler(metaclass=ABCMeta):
    def __init__(self, chain=None):
        if chain is not None and isinstance(chain, VersionIntervalHandler):
            self._next = chain
        else:
            self._next = None

    def hasNext(self):
        return self._next is not None

    @abstractmethod
    def handle(self, version: str) -> VersionInterval or None:
        pass


class PlusHandler(VersionIntervalHandler):
    def handle(self, version: str) -> VersionInterval or None:
        if version == '+':
            return VersionInterval(GeneralVersion('0'), False, GeneralVersion(str(MAX_INT)), False)
        if self.hasNext():
            return self._next.handle(version)
        return None


class VersionPlusHandler(VersionIntervalHandler):
    _pattern = re.compile(r'([0-9]+(\.[0-9]+)*)\.?\+')

    def handle(self, version: str) -> VersionInterval or None:
        m = self._pattern.fullmatch(version)
        if m is not None:
            return VersionInterval(GeneralVersion(m.group(1)), True,
                                   GeneralVersion('{}.{}'.format(m.group(1), MAX_INT)), False)
        if self.hasNext():
            return self._next.handle(version)
        return None


class IntervalHandler(VersionIntervalHandler):
    _pattern = re.compile(r'([\[(])[ \t]*([0-9]+(\.[0-9]+)*)[ \t]*,[ \t]*([0-9]+(\.[0-9]+)*)[ \t]*([\])])')

    def handle(self, version: str) -> VersionInterval or None:
        m = self._pattern.match(version)
        if m is not None:
            return VersionInterval(GeneralVersion(m.group(2)), True if m.group(1) == '[' else False,
                                   GeneralVersion(m.group(4)), True if m.group(6) == ']' else False)
        if self.hasNext():
            return self._next.handle(version)
        return None


if __name__ == '__main__':
    exit()
