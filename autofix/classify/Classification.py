class Classification:
    def __init__(self, error: str, strategy: str, group: tuple, param: tuple):
        self._error = error
        self._strategy = strategy
        self._group = group
        self._param = param

    @property
    def error(self):
        return self._error

    @property
    def strategy(self):
        return self._strategy

    @property
    def group(self):
        return self._group

    @property
    def param(self):
        return self._param

    def __eq__(self, other):
        return self.error == other.error and \
               self.strategy == other.strategy and \
               self.group == other.group and \
               self.param == other.param

    def __str__(self):
        return "Classification Result\n" \
               "Type:\t{}\n" \
               "Key:\t{}\n" \
               "Group:\t{}\n" \
               "Param:\t{}".format(self.error, self.strategy, self.group, self.param)


if __name__ == '__main__':
    exit()
