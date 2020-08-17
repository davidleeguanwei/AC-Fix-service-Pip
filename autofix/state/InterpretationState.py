import re
from autofix.Project import Project
from autofix.state.ProjectState import ProjectState
import autofix.state.ClassifyState
import autofix.state.SuccessState
from autofix.util.LoggingUtil import Logger
from autofix.util.Config import Config
from autofix.util.VirtualEnvironment import VirtualEnvironment


class InterpretationState(ProjectState):
    """
    A concrete class implementing interface ProjectState
    In this state, following operations should be done:
        1. Test interpretibility of the project
    Next state should move to SuccessState
    """
    def __init__(self):
        self._finish = False

    def operation(self, project: Project):
        Logger().targetLogger.debug('In state: INTERPRETATION')

        # Operation 1
        error_log_path = Logger().logDir
        virtualenv = VirtualEnvironment()
        project.defaultPythonVersion = Config().get('PYTHON', 'PYTHON_DEFAULT')
        env_ver = project.defaultPythonVersion
        env_name = "test_env_"+project.name
        status = virtualenv.compileall(env_ver, env_name, project.name, error_log_path)

        # Operation 1 logging
        if status == "SUCCESS":
            Logger().targetLogger.debug('Successful Interpretation.')
        else:
            Logger().targetLogger.error('Failed to interpret the project.')
        
        # Next state
        if status == "SUCCESS":
            project.state = autofix.state.SuccessState.SuccessState()
        else:
            project.state = autofix.state.ClassifyState.ClassifyState()


if __name__ == '__main__':
    exit()
