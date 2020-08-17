import os
import re
from autofix.Project import Project
from autofix.state.CreateVirtualenvState import CreateVirtualenvState
from autofix.state.FailureState import FailureState
from autofix.state.SuccessState import SuccessState
from autofix.util.LoggingUtil import newTargetLogger, Logger


class PythonAutoFix:
    """
    Main class of Python Auto Fixing Scheme
    """

    def __init__(self):
        self._MAX_ITER = 365
        self._target = None
    '''
    def setTarget(self, num: str, path: str):
        name = os.path.basename(path)
        if not os.path.exists(path) or not os.path.isdir(path):
            Logger().schemeLogger.error('Project not exists in path: {}'.format(path))
        else:
            newTargetLogger(num)
            self._target = Project(name, path)
    '''
    def setTarget(self, index, url: str):
        newTargetLogger(index)
        m = re.fullmatch(r'https://pypi.org/project/([-.\w]+)/?', url)
        project_name = url.split('/')[-1] if re.fullmatch(r'https://(github|gitlab)\.com/(.+)', url) else m.group(1)
        self._target = Project(project_name, index)
        if m is None:
            self._target._gitRepo = url

    def startFixing(self) -> bool:
        result = False
        Logger().schemeLogger.info('Execution for {} start.'.format(self._target.name))
        Logger().targetLogger.info('Project name: {}'.format(self._target.name))
        self._target.state = CreateVirtualenvState()
        iteration = 0
        while not self._target.state.finish and iteration < self._MAX_ITER:
            self._target.operate()
            iteration = iteration + 1
            if result == False:
                result = isinstance(self._target.state, SuccessState)
        if not self._target.state.finish and iteration >= self._MAX_ITER:
            Logger().targetLogger.error('Maximum iteration limit exceeded.')
            self._target.state = FailureState()
            self._target.operate()
        self._target.operate()
        Logger().schemeLogger.info('Execution for {} end.'.format(self._target.name))
        return result


if __name__ == '__main__':
    exit()
