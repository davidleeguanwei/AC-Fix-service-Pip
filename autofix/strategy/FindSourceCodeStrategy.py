import re
import os
from autofix.Project import Project
from autofix.util.LoggingUtil import Logger
from autofix.util.VirtualEnvironment import VirtualEnvironment
from autofix.util.Config import Config
from autofix.strategy.util.RetriveGitRepoFromPyPI import retriveGitRepoFromPyPI
from autofix.strategy.util.RetriveDownloadFileFromPyPI import retriveDownloadFileFromPyPI
from autofix.classify.Classifier import Classifier
from autofix.strategy.util.HandleModulePathFromDownloadFile import handleModulePathFromDownloadFile


class DependencyGraph():
    def __init__(self):
        self.graph = dict()
        self.V = []

    def addNode(self, v):
        if v not in self.V:
            self.V.append(v)
            self.graph[v] = []

    def addEdge(self, u, v):
        if v not in self.graph[u]:
            self.graph[u].append(v)

    def DFS_CheckCyclic(self, v, visited, recStack):
        # Mark current node as visited and adds to recusion stack
        visited[v] = True
        recStack[v] = True

        # Tour through all neighbors
        # If any neighbor is visited and in recStack then the graph is cyclic
        for neighbor in self.graph[v]:
            if visited[neighbor] == False:
                if self.DFS_CheckCyclic(neighbor, visited, recStack) == True:
                    return True
            elif recStack[neighbor] == True:
                return True

        # The node needs to be poped from stack after tour through all neighbors
        recStack[v] = False
        return False

    # Return True if graph is cyclic else False
    def isCyclic(self):
        visited = dict()
        recStack = dict()
        for node in self.V:
            visited[node] = False
            recStack[node] = False
        for node in self.V:
            if visited[node] == False:
                if self.DFS_CheckCyclic(node, visited, recStack) == True:
                    return True
        return False


def getDependencies(repo, error_log_path, graph):
    classification = Classifier().classify(error_log_path)
    dependent_repos = []
    dependent_file_links = []
    dependent_gitRepos = []
    dependent_gitRepo = None
    if classification.error == '1.3':
        for module_name in classification.group:
            if "==" in module_name:
                module_name = module_name.split("==")[0]
            elif ">=" in module_name:
                module_name = module_name.split(">=")[0]
            elif "<=" in module_name:
                module_name = module_name.split("<=")[0]
            module_name = module_name.rsplit(".", 1)[0]
            graph.addNode(module_name)
            graph.addEdge(repo, module_name)
            dependent_repos.append(module_name)
            dependent_file_link = retriveDownloadFileFromPyPI(module_name)
            dependent_file_links.append(dependent_file_link)
            urls = retriveGitRepoFromPyPI(module_name)
            if urls is not None:
                for url in urls:
                    if "http:" in url:
                        url = url.replace("http:", "https:")
                    m = re.fullmatch(r'https://(github|gitlab)\.com/(.+)/', url)
                    dependent_gitRepo = url if m is not None else None
                    if dependent_gitRepo is not None:
                        break
            dependent_gitRepos.append(dependent_gitRepo)
    return dependent_repos, dependent_file_links, dependent_gitRepos, graph


def tryInstallDependency(project: Project, repos, virtualenv, error_log_path, file_links, gitRepos, graph):
    # First check if dependency graph is cyclic
    print(graph.graph)
    if graph.isCyclic():
        Logger().targetLogger.error("Dependency has cycle.")
        return False

    env_name = "test_env_" + project.name
    #install files which are downloaded from PyPI
    env_ver = project.defaultPythonVersion if project.currentPythonVersion is None else project.currentPythonVersion
    env_ver = 'cp3'+str(env_ver).split('.')[-1]
    status = ''

    for i in range(len(repos)):
        if file_links[i] is not None:
            for link in file_links[i]:
                if re.search(env_ver, link) is not None and re.search(r'macosx', link) is not None:
                    os.system("wget " + link)
                    file_name = link.rsplit('/', 1)[-1]
                    cmd = ". "+env_name+"/bin/activate && "+"pip install "+ file_name
                    status, log = virtualenv.executeIn(cmd)
                    os.system("rm " + file_name)
                    break
        #install git repo of project's dependency
        if gitRepos[i] is None and status!= "SUCCESS":
            cmd = ". "+env_name+"/bin/activate && pip install "+repos[i]
            status, log = virtualenv.executeIn(cmd)
            if status != "SUCCESS":
                error_log_file = open(error_log_path, "w+", encoding="utf-8")
                error_content = "pip install failed Output: \n{}\n".format(log.decode("utf-8", errors="ignore"))
                error_log_file.write(error_content)
                error_log_file.close()
                dependent_repos, dependent_file_links, dependent_gitRepos, graph = getDependencies(repos[i], error_log_path, graph)
                if len(dependent_repos) == 0:
                    Logger().targetLogger.debug("Failed to pip install project's dependency.")
                    return False
                if tryInstallDependency(project, dependent_repos, virtualenv, error_log_path, dependent_file_links, dependent_gitRepos, graph):
                    return tryInstallDependency(project, repos, virtualenv, error_log_path, file_links, gitRepos, graph)
                else:
                    return False
        elif status!= "SUCCESS":
            cmd = ". "+env_name+"/bin/activate && "+"pip install git+"+ gitRepos[i]
            status, log = virtualenv.executeIn(cmd)
            if status != "SUCCESS":
                # log error messages if failed to pip+git install
                error_log_file = open(error_log_path, "w+", encoding="utf-8")
                error_content = "pip+git install failed Output: \n{}\n".format(log.decode("utf-8", errors="ignore"))
                error_log_file.write(error_content)
                error_log_file.close()
                dependent_repos, dependent_file_links, dependent_gitRepos, graph = getDependencies(repos[i], error_log_path, graph)
                if len(dependent_repos) == 0:
                    Logger().targetLogger.debug("Failed to pip+git install project's dependency.")
                    return False
                if tryInstallDependency(project, dependent_repos, virtualenv, error_log_path, dependent_file_links, dependent_gitRepos, graph):
                    return tryInstallDependency(project, repos, virtualenv, error_log_path, file_links, gitRepos, graph)
                else:
                    return False

    return True

def findSourceCode(project: Project, param: tuple) -> bool:
    """Return a boolean
    :param project: target project
    :param param: (module_name)
    :return: whether the appliance is successful
    """
    if len(param) < 1:
        Logger().targetLogger.error('Parameter tuple length less than 1.')
        return False

    submodule = None
    if len(param) >= 4:
        submodule = param[3]

    virtualenv = VirtualEnvironment()
    repos = []

    if len(param) >= 3:
        repo = project.name if param[2] == "project.name" else param[2]
    else:
        repo = project.name if param[0] == "project.name" else param[0]
    if "==" in repo:
        repo = repo.split("==")[0]
    elif ">=" in repo:
        repo = repo.split(">=")[0]
    elif "<=" in repo:
        repo = repo.split("<=")[0]
    repo = repo.rsplit(".", 1)[0]
    repos.append(repo)
    env_name = "test_env_" + project.name
    error_log_path = Logger().logDir
    error_log_path = error_log_path + "/error_"+project.name

    file_links = []
    urls = retriveGitRepoFromPyPI(repo)
    file_link = retriveDownloadFileFromPyPI(param[0])
    gitRepos = []
    file_links.append(file_link)
    gitRepo = None

    if urls is not None:
        for url in urls:
            if "http:" in url:
                url = url.replace("http:", "https:")
            m = re.fullmatch(r'https://(github|gitlab)\.com/(.+)/', url)
            gitRepo = url if m is not None else None
            if gitRepo is not None:
                break
    gitRepos.append(gitRepo)

    origin_file_path = param[0]
    if (not os.path.exists(origin_file_path) or not os.path.isfile(origin_file_path)) and not os.path.isdir(project.name):
        env_ver = project.currentPythonVersion
        env_name = "test_env_" + project.name
        virtualenv = VirtualEnvironment()
        virtualenv.pipDownload(env_ver, env_name, project.name)
        status = True if os.path.isdir(project.name) else False
        return status

    # Differentiate repo of dependency or the real project
    if repo != project.name:
        if os.path.isdir(project.name):
            status = handleModulePathFromDownloadFile(project, origin_file_path, repo, submodule)
            if status == True:
                return True
        if repo in project.installedModule:
            return False
        graph = DependencyGraph()
        graph.addNode(repo)
        graph.addNode(project.name)
        graph.addEdge(project.name, repo)
        if tryInstallDependency(project, repos, virtualenv, error_log_path, file_links, gitRepos, graph) is False:
            return False
        return True
    else:
        #configure git repo of the project
        env_ver = project.defaultPythonVersion if project.currentPythonVersion is None else project.currentPythonVersion
        env_ver = 'cp3'+str(env_ver).split('.')[-1]

        if file_link is not None:
            for link in file_link:
                if re.search(env_ver, link) is not None and re.search(r'macosx', link) is not None:
                    os.system("wget " + link)
                    file_name = link.rsplit('/', 1)[-1]
                    project._wheel = file_name
            if project._wheel is not None:
                return True
        if gitRepo is None and project._wheel is None:
            Logger().targetLogger.error("Cannot find source code of the project.")
            return False
        if project._gitRepo is not None and project._gitRepo == gitRepo:
            Logger().targetLogger.debug("The git repository of the project has been configured.")
            return False
        project._gitRepo = gitRepo
        Logger().targetLogger.debug("Configure git repository of the project.")
        return True


if __name__ == '__main__':
    exit()
