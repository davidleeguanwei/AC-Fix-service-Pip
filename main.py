import os
import re
import sys
import json
import subprocess
import requests
from autofix.util.LoggingUtil import dockerModeLogger, normalModeLogger, Logger
from autofix.util.Config import Config
from autofix.util.OSUtil import getEnvironmentVariable, cd
from autofix.PythonAutoFix import PythonAutoFix


def checkGithubRepoContents(project: str) -> str:
    api = 'https://api.github.com/repos/{}/contents'.format(project)
    res = requests.get(api, auth=('davidleeguanwei', '6f5a1fb75764d350faf9ec4992fd883f47a6da07'))
    if res.status_code != 200:
        return 'Github API failed to query repository {}'.format(project)
    contents = json.loads(res.text)
    for file in contents:
        if "setup.py" == file["name"]:
            return ''
    return 'Requires a project with setup.py as target'


def checkGitLabRepoContents(project: str) -> str:
    api = 'https://gitlab.com/api/v4/projects/{}/contents'.format(project.replace('/', '%2F'))
    res = requests.get(api, auth=('davidleeguanwei', '6f5a1fb75764d350faf9ec4992fd883f47a6da07'))
    if res.status_code != 200:
        return 'Gitlab API failed to query repository {}'.format(project)
    contents = json.loads(res.text)
    for file in contents:
        if "setup.py" == file["name"]:
            return ''
    return 'Requires a project with setup.py as target'


def dockerModeLogStageFailed(msg: str, stage: str, index: str):
    if len(msg) > 0:
        Logger().dockerLogger.error(msg)
    Logger().dockerLogger.stage('{}: Failed'.format(stage))
    Logger().dockerLogger.final('End Auto-Fix Service: Build#{}'.format(index))


if __name__ == '__main__':


    if len(sys.argv) < 2 or sys.argv[1] != 'docker':
        # Normal mode
        normalModeLogger()
        path = Config().get('PATH', 'PROJECT_LIST')
        if len(path) == 0 or not os.path.exists(path) or not os.path.isfile(path):
            exit(1)
        targetList = list()
        with open(path, "r") as f:
            for line in f:
                line = line.replace("\n", "")
                targetList.append(line.strip().split('\t'))
        scheme = PythonAutoFix()
        for target in targetList:
            scheme.setTarget(target[0], target[1])
            scheme.startFixing()
    else:
        # Docker mode

        # 0. Get docker environment variables
        idx = getEnvironmentVariable('BUILD_INDEX')
        url = getEnvironmentVariable('BUILD_TARGET')
        print(idx)
        print(url)
        if not idx.isdigit():
            exit(1)
        dockerModeLogger(idx)
        Logger().dockerLogger.start('Start Auto-Fix Service: Build#{}'.format(idx))

        # 1. Use API to check the repository
        Logger().dockerLogger.stage('Checking repository: ...')
        while url.endswith('.git'):
            url = url[:-4]
        m = re.fullmatch(r'https://(github|gitlab)\.com/(.+)', url)
        if m is not None:
            err = checkGithubRepoContents(m.group(2)) if m.group(1) == 'github' else checkGitLabRepoContents(m.group(2))
            if len(err) > 0:
                dockerModeLogStageFailed(err, 'Checking repository', idx)
                exit(1)
            name = url
        else:
            m = re.fullmatch(r'https://pypi.org/project/([-.\w]+)/?', url)
            if m is None:
                dockerModeLogStageFailed('Invalid URL: {}'.format(url), 'Checking repository', idx)
                exit(1)
            name = url
        Logger().dockerLogger.stage('Checking repository: OK')

        # 2. Fixing
        Logger().dockerLogger.stage('Fixing project: ...')
        scheme = PythonAutoFix()
        scheme.setTarget(idx, name)
        if scheme.startFixing():
            Logger().dockerLogger.stage('Fixing project: OK')
        else:
            dockerModeLogStageFailed('', 'Fixing project', idx)
            exit(1)

        # 3. Analyzing
        Logger().dockerLogger.stage('Analyzing project: ...')
        env_name = name.split('/')[-1]
        path = "./test_env_" + str(env_name)
        with cd(path):
            command = "sonar-scanner \
  -Dsonar.projectKey=AC-Fix-Build-@BUILD_INDEX@ \
  -Dsonar.projectName="+str(name)+" \
  -Dsonar.sources=. \
  -Dsonar.sourceEncoding=UTF-8 \
  -Dsonar.host.url=http://@SONAR_HOST@:@SONAR_PORT@ \
  -Dsonar.language=py"
            command = command.replace('@BUILD_INDEX@', Logger().targetLogger.name)\
                .replace('@SONAR_HOST@', Config().get('SONAR', 'SONAR_HOST'))\
                .replace('@SONAR_PORT@', Config().get('SONAR', 'SONAR_PORT'))
            status = os.system(command)
            if status != 0:
                dockerModeLogStageFailed('Failed to analyze code with Sonar Scanner',
                                         'Analyzing project', idx)
                exit(1)
        Logger().dockerLogger.stage('Analyzing project: OK')
        Logger().dockerLogger.final('End Auto-Fix Service: Build#{}'.format(idx))
        exit()
