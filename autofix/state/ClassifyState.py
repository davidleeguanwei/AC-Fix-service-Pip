import re
import os
import autofix.state.StrategyState
from autofix.Project import Project
from autofix.state.ProjectState import ProjectState
from autofix.classify.Classifier import Classifier
from autofix.util.Config import Config
from autofix.util.LoggingUtil import Logger
from autofix.util.FileSystemUtil import copyFile


class ClassifyState(ProjectState):
    """
    A concrete class implementing interface ProjectState
    In this state, following operation should be done:
        1. Read building log and classify it
        2. Restore error log file
    Next state should move to StrategyState
    """
    def __init__(self):
        self._finish = False

    def operation(self, project: Project):
        Logger().targetLogger.debug('In state: CLASSIFY')

        # Operation 1
        error_log_path = Logger().logDir
        log = os.path.join(error_log_path, "error_" + project.name)
        classification = Classifier().classify(log)
        project.record.append(classification)

        # Operation 1 logging
        Logger().targetLogger.info('Iteration {}'.format(len(project.record)))
        for line in str(project.record[-1]).split('\n'):
            Logger().targetLogger.info(line)


        # Operation 2
        path = os.path.join(Config().get('PATH', 'LOG_DIR_PATH'),
                            '{}-{}-{}.err'.format(Logger().targetLogger.name,
                                                  len(project.record), project.record[-1].error))
        copyFile(log, path)

        # Next state
        project.state = autofix.state.StrategyState.StrategyState()


if __name__ == '__main__':
    exit()
