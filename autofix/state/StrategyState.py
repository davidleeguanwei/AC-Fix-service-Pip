import re
import autofix.state.PipInstallationState
import autofix.state.InterpretationState
import autofix.state.FailureState
import autofix.state.SuccessState
from autofix.Project import Project
from autofix.state.ProjectState import ProjectState
from autofix.strategy.StrategySwitch import StrategySwitch
from autofix.util.LoggingUtil import Logger
from autofix.util.Config import Config


class StrategyState(ProjectState):
    """
    A concrete class implementing interface ProjectState
    In this state, following operation should be done:
        1. Apply proper strategy according to classification
    Next state should move to StrategyState
    """
    def __init__(self):
        self._finish = False

    def operation(self, project: Project):
        Logger().targetLogger.debug('In state: STRATEGY')

        # Operation 1
        cur = project.record[-1]
        if len(project.record) > 1 and cur == project.record[-2]:
            Logger().targetLogger.error('Same classification as last one, strategy applied had no effect.')
            project.state = autofix.state.FailureState.FailureState()
            return
        strategy = StrategySwitch().getStrategy(cur.strategy)
        if strategy is None:
            if cur.error == '9':
                Logger().targetLogger.error('Not recognized error log, cannot be fixed.')
            else:
                Logger().targetLogger.error('No proper strategy can be applied, cannot be fixed.')
            project.state = autofix.state.FailureState.FailureState()
            return
        if not strategy(project, cur.param):
            Logger().targetLogger.error('Failed to apply strategy.')
            project.state = autofix.state.FailureState.FailureState()
            return

        # Next state
        error_log_path = Logger().logDir
        error_log_path = error_log_path + "/error_"+project.name
        error_file = open(error_log_path, 'r')
        error_content = error_file.read()
        error_file.close()
        if re.search(r'compile all failed Output:', error_content) is not None:
            project.state = autofix.state.InterpretationState.InterpretationState()
        else:
            project.state = autofix.state.PipInstallationState.PipInstallationState()


if __name__ == '__main__':
    exit()
