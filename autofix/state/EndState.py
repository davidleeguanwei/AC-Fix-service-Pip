import re
import os
from autofix.Project import Project
from autofix.state.ProjectState import ProjectState
from autofix.util.VirtualEnvironment import VirtualEnvironment
from autofix.util.Config import Config
from autofix.util.LoggingUtil import Logger


class EndState(ProjectState):
    """
    A concrete class implementing interface ProjectState
    This is a state identifying the end of the fixing process, nothing should be done in this state
    """
    def __init__(self):
        self._finish = True

    def operation(self, project: Project):
        '''
        virtualenv = VirtualEnvironment()
        env_name = "test_env_"+project.name
        error_log_path = Config().get('PATH', 'LOG_DIR_PATH')
        error_log_path = error_log_path + "/error_" + project.name
        if os.path.isfile(error_log_path):
            virtualenv.deleteVirtualenv(env_name)
        '''
        if os.path.isdir(project.name):
           os.system("rm -rf "+project.name)
        return


if __name__ == '__main__':
    exit()
