import re
import autofix.state.PipInstallationState
from autofix.state.ProjectState import ProjectState
from autofix.Project import Project
from autofix.util.LoggingUtil import Logger
from autofix.util.Config import Config
from autofix.util.VirtualEnvironment import VirtualEnvironment


class CreateVirtualenvState(ProjectState):
    """
    A concrete class implementing interface ProjectState
    In this state, following operations should be done:
        1. Initialize the virtual environment for the project installation
    Next state should move to PipInstallationState
    """
    def __init__(self):
        self._finish = False

    def operation(self, project: Project):
        Logger().targetLogger.debug('In state: CREATE_VIRTUALENV')

        # Operation 1
        project.defaultPythonVersion = Config().get('PYTHON', 'PYTHON_DEFAULT')
        env_ver = project.defaultPythonVersion if project.currentPythonVersion is None else project.currentPythonVersion
        env_name = "test_env_"+project.name
        virtualenv = VirtualEnvironment()
        virtualenv.createVirtualenv(env_ver, env_name)
        virtualenv.pipUpgrade(env_name)

        # Operation 1 logging
        Logger().targetLogger.debug('Virtual environment initialized.')

        # Next state
        project.state = autofix.state.PipInstallationState.PipInstallationState()

if __name__ == '__main__':
    exit()
