from abc import ABCMeta, abstractmethod


class ProjectState(metaclass=ABCMeta):
    """
    An interface of project state (the State Pattern)
    """
    _finish = bool()

    @property
    def finish(self):
        return self._finish

    @abstractmethod
    def operation(self, project):
        pass


if __name__ == '__main__':
    exit()
