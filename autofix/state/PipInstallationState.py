import re
import autofix.state.InterpretationState
from autofix.state.ProjectState import ProjectState
import autofix.state.ClassifyState
import autofix.state.FailureState
from autofix.Project import Project
from autofix.util.LoggingUtil import Logger
from autofix.util.Config import Config
from autofix.util.VirtualEnvironment import VirtualEnvironment


class PipInstallationState(ProjectState):
    """
    A concrete class implementing interface ProjectState
    In this state, following operations should be done:
        1. Install the project from PyPI repository through pip tool
    Next state should move to InterpretationState
    """
    def __init__(self):
        self._finish = False

    def operation(self, project: Project):
        Logger().targetLogger.debug('In state: PIP_INSTALLATION')

        # Operation 1
        virtualenv = VirtualEnvironment()
        env_ver = project.defaultPythonVersion if project.currentPythonVersion is None else project.currentPythonVersion
        env_name = "test_env_"+project.name
        error_log_path = Logger().logDir
        if project._wheel is not None:
            status = virtualenv.pipInstall(env_ver, env_name, project._wheel, error_log_path)
        elif project._gitRepo is not None:
            status = virtualenv.pipGitInstall(env_ver, env_name, project._gitRepo, error_log_path)
        else:
            status = virtualenv.pipInstall(env_ver, env_name, project.name, error_log_path)

        # Operation 1 logging
        if status == "SUCCESS":
            Logger().targetLogger.debug('Successful pip installation.')
        elif status == "EXCEED_TIME_LIMIT":
            Logger().targetLogger.error('Time limit exceeded.')
        else:
            Logger().targetLogger.error('Failed to pip install the project.')

        # Next state
        if status == "SUCCESS":
            project.state = autofix.state.InterpretationState.InterpretationState()
        elif status == "EXCEED_TIME_LIMIT":
            project.state = autofix.state.FailureState.FailureState()
        else:
            project.state = autofix.state.ClassifyState.ClassifyState()

if __name__ == '__main__':
    exit()
