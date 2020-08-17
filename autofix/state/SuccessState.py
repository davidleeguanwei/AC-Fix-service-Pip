import re
import os
import autofix.state.EndState
from autofix.Project import Project
from autofix.state.ProjectState import ProjectState
from autofix.util.LoggingUtil import Logger
from autofix.util.Config import Config
from autofix.util.OSUtil import cd, executeCommand


def compress_project(project: Project):
    path = os.path.join(Logger().logDir, '{}.tar.gz'.format(Logger().targetLogger.name))
    compress_path = os.getcwd()
    with cd(compress_path):
        executeCommand(['tar', 'zcvf', path, 'test_env_' + str(project.name)], [])
    return


class SuccessState(ProjectState):
    """
    A concrete class implementing interface ProjectState
    In this state, following operations should be done:
        1. Log 'Fixing successful' message
        2. Compress project
        3. Remove old error message if it exists
    Next state should move to EndState
    """
    def __init__(self):
        self._finish = False

    def operation(self, project: Project):
        Logger().targetLogger.debug('In state: SUCCESS')

        # Operation 1
        Logger().targetLogger.info('Python Auto Fixing Scheme succeed to fix project {}.'.format(project.name))

        # Operation 2
        compress_project(project)

        # Operation 3
        error_log_path = Logger().logDir
        error_log_path = error_log_path + "/error_" + project.name
        if os.path.isfile(error_log_path):
            os.system("rm " + error_log_path)
        # Next state
        project.state = autofix.state.EndState.EndState()


if __name__ == '__main__':
    exit()
