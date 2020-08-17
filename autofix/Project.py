import git
from autofix.state.ProjectState import ProjectState
from autofix.util.FileUtil import removeComment
from autofix.util.version.PythonVersion import PythonVersion


class Project:
    def __init__(self, name: str, index):
        self._name = name
        self._index = index
        self._state = None
        self._gitRepo = None
        self._wheel = None
        self._defaultPythonVersion = None
        self._currentPythonVersion = None
        self._installedModule = list()
        self._propertyFile = list()
        self._replacementTargetFile = list()
        self._appendixTargetFile = list()
        self._generatedFile = list()
        self._excludeTask = list()
        self._extKeyValue = list()
        self._record = list()
        self._unreachableHost = list()
        self._commentRemoved = False
        self._compilationTrial = list()

    @property
    def name(self) -> str:
        return self._name

    @property
    def index(self) -> str:
        return self._index

    @property
    def state(self) -> ProjectState:
        return self._state

    @state.setter
    def state(self, state: ProjectState):
        self._state = state

    def operate(self):
        self._state.operation(self)

    @property
    def gitRepo(self) -> git.Repo:
        return self._gitRepo

    @gitRepo.setter
    def gitRepo(self, repo: git.Repo):
        self._gitRepo = repo

    @property
    def wheel(self) -> str:
        return self._wheel

    @wheel.setter
    def wheel(self, wheel: str):
        self._wheel = wheel

    @property
    def defaultPythonVersion(self) -> PythonVersion:
        return self._defaultPythonVersion

    @defaultPythonVersion.setter
    def defaultPythonVersion(self, version: PythonVersion):
        self._defaultPythonVersion = version

    @property
    def currentPythonVersion(self) -> PythonVersion:
        return self._currentPythonVersion

    @property
    def installedModule(self) -> list:
        return self._installedModule

    @currentPythonVersion.setter
    def currentPythonVersion(self, version: PythonVersion):
        self._currentPythonVersion = version

    @property
    def propertyFile(self) -> list:
        return self._propertyFile

    @property
    def replacementTargetFile(self) -> list:
        return self._replacementTargetFile

    @property
    def appendixTargetFile(self) -> list:
        return self._appendixTargetFile

    @property
    def generatedFile(self) -> list:
        return self._generatedFile

    @property
    def excludeTask(self) -> list:
        return self._excludeTask

    @property
    def extKeyValue(self) -> list:
        return self._extKeyValue

    @property
    def record(self) -> list:
        return self._record

    @property
    def unreachableHost(self) -> list:
        return self._unreachableHost

    @property
    def commentRemoved(self) -> bool:
        return self._commentRemoved

    @property
    def compilationTrial(self) -> list:
        return self._compilationTrial


if __name__ == '__main__':
    exit()
