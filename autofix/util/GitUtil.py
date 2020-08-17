import os
import git
import autofix.Project
from autofix.util.FileSystemUtil import removePath


def initialize(project: autofix.Project.Project) -> bool:
    """Return a boolean

    Initialization steps:
    1. Confirm that directory points to a git project
    2. Reset the project to reset all modifications
    3. Remove '.gitignore' in case that some modifications be ignored
    4. Remove files untracked by 'git status'
    5. Reset the project to recover '.gitignore'

    :param project: project to initialize
    :return: whether the initialization is successful
    """
    path = project.path
    # Step 1
    try:
        if project.gitRepo is None:
            project.gitRepo = git.Repo(path)
        repo = project.gitRepo
    except git.exc.InvalidGitRepositoryError:
        return False
    # Step 2
    if not gitReset(repo):
        return False
    # Step 3
    if not removePath(os.path.join(path, '.gitignore')):
        return False
    # Step 4
    files = [s[1:] for s in repo.git.status().split('\n') if len(s) > 0 and s[0] == '\t']
    for f in files:
        if not removePath(os.path.join(path, f)):
            return False
    # Step 5
    if not gitReset(repo):
        return False
    return True


def gitReset(repo: git.Repo) -> bool:
    """Return a boolean

    :param repo: the git repo to reset
    :return: whether the reset is successful
    """
    try:
        repo.git.reset(hard=True)
    except git.exc.GitCommandError:
        return False
    return True


def gitUnshallow(repo: git.Repo) -> bool:
    """Return a boolean

    :param repo: the git repo to unshallow
    :return: whether the unshallow is successful
    """
    try:
        repo.git.fetch(unshallow=True)
    except git.exc.GitCommandError:
        return False
    return True


if __name__ == '__main__':
    exit()
