import re
import os
import autofix.state.EndState
from autofix.Project import Project
from autofix.state.ProjectState import ProjectState
from autofix.util.LoggingUtil import Logger
from autofix.util.Config import Config
from autofix.util.OSUtil import cd, executeCommand
from autofix.state.SuccessState import compress_project


class FailureState(ProjectState):
    """
    A concrete class implementing interface ProjectState
    In this state, following operations should be done:
        1. Log 'Fixing failed' message
        2. Compress the whole fixed project
    Next state should move to EndState
    """
    def __init__(self):
        self._finish = False

    def operation(self, project: Project):
        Logger().targetLogger.debug('In state: FAILURE')

        # Operation 1
        Logger().targetLogger.info('Python Auto Fixing Scheme failed to fix project {}.'.format(project.name))

        # Operation 2
        compress_project(project)

        # Next state
        project.state = autofix.state.EndState.EndState()


if __name__ == '__main__':
    exit()
