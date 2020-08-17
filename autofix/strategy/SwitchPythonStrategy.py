import re
from autofix.Project import Project
from autofix.util.LoggingUtil import Logger
from autofix.util.OSUtil import setPythonVersion
from autofix.util.version.PythonVersion import PythonVersion, minPython, maxPython
from autofix.util.VirtualEnvironment import VirtualEnvironment


def switchPythonVersion(project: Project, param: tuple) -> bool:
    """Return a boolean

    Argument tuple: ([VERSION])
        [VERSION]: The target Python version

    :param project: target project
    :param param: argument to apply strategy
    :return: whether the appliance is successful
    """
    if len(param) < 1:
        Logger().targetLogger.error('Parameter tuple length less than 1.')
        return False
    virtualenv = VirtualEnvironment()
    env_name = "test_env_"+project.name
    virtualenv.deleteVirtualenv(env_name)
    env_ver = param[0]
    if '2' in env_ver:
        env_ver = '2.7'

    project.currentPythonVersion = min(max(PythonVersion(env_ver), minPython), maxPython)
    if not setPythonVersion(str(project.currentPythonVersion)):
        Logger().targetLogger.error('Failed to switch Python version.')
        return False
    virtualenv.createVirtualenv(env_ver, env_name)
    virtualenv.pipUpgrade(env_name)
    
    return True


if __name__ == '__main__':
    exit()
