from abc import ABCMeta, abstractmethod


class BaseVersion(metaclass=ABCMeta):
    """
    An interface of version
    """
    _version = str()

    def __str__(self):
        return self._version

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __lt__(self, other):
        pass

    @abstractmethod
    def __gt__(self, other):
        pass

    @abstractmethod
    def __ne__(self, other):
        pass

    @abstractmethod
    def __le__(self, other):
        pass

    @abstractmethod
    def __ge__(self, other):
        pass


def compareVersionNumber(num1: str, num2: str):
    if num1 == num2:
        return 0
    seq1 = [int(num) for num in num1.split('.')]
    seq2 = [int(num) for num in num2.split('.')]
    for i in range(max(len(seq1), len(seq2))):
        a = 0 if i >= len(seq1) else int(seq1[i])
        b = 0 if i >= len(seq2) else int(seq2[i])
        if a > b:
            return 1
        elif b > a:
            return -1
    return 0


if __name__ == '__main__':
    exit()
