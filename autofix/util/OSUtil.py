import os
import subprocess
import sys
from contextlib import contextmanager
from autofix.util.Config import Config
from autofix.util.FileSystemUtil import expandPath


@contextmanager
def cd(newdir):
    """ Context Manager for changing directory safely """
    predir = os.getcwd()
    os.chdir(expandPath(newdir))
    try:
        yield
    finally:
        os.chdir(predir)


def executeCommandBySudo(cmd: list, inputs: list) -> (int, str, str):
    """Return a 3-tuple (int, string, string)

    :param cmd: the command need to be executed under sudo
    :param inputs: the input to the command
    :return: return code, stdout, and stderr of the command
    """
    pwd = Config().get('SUDO', 'PASSWORD')
    stream = '{}\n{}{}'.format(pwd, '\n'.join(inputs), '' if len(inputs) == 0 else '\n')
    sudo = ['sudo', '-S']
    sudo.extend(cmd)
    p = subprocess.Popen(sudo, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate(stream.encode())
    return p.poll(), out.decode('utf-8'), err.decode('utf-8')

def executeCommand(cmd: list, inputs: list) -> (int, str, str):
    """Return a 3-tuple (int, string, string)

    :param cmd: the command need to be executed
    :param inputs: the input to the command
    :return: return code, stdout, and stderr of the command
    """
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate('\n'.join(inputs).encode())
    return p.poll(), out.decode('utf-8'), err.decode('utf-8')


def setEnvironmentVariable(key: str, val: str) -> bool:
    """Return a boolean

    :param key: the environment variable to be set
    :param val: the value of the environment variable
    :return: whether the setting is successful
    """
    try:
        os.environ[key] = val
    except OSError:
        return False
    return True


def getEnvironmentVariable(key: str) -> str:
    """Return a string

    :param key: the environment variable
    :return: value of the environment variable
    """
    return os.environ[key] if key in os.environ else ''


def setGradleJavaVersion(version: str) -> bool:
    """Return a boolean

    :param version: Java version
    :return: whether the setting is successful
    """
    path = Config().get('JAVA_HOME', 'JAVA_{}_HOME'.format(version))
    if len(path) == 0:
        return False
    return setEnvironmentVariable('JAVA_HOME', path)


def setSystemJavaVersion(version: str) -> bool:
    """Return a boolean

    :param version: Java version
    :return: whether the setting is successful
    """
    path = Config().get('UPDATE-ALTERNATIVES', 'JAVA_{}_CONFIG'.format(version))
    if len(path) == 0:
        return False
    code, out, err = executeCommandBySudo(['update-alternatives', '--config', 'java'], [path])
    return True if code == 0 else False


def setPythonVersion(version: str) -> bool:
    """Return a boolean

    :param version: Python version
    :return: whether the setting is successful
    """
    path = Config().get('PYTHON_HOME', 'PYTHON_{}_HOME'.format(version))
    if len(path) == 0:
        return False
    return setEnvironmentVariable('PYTHON_HOME', path)


MAX_INT = sys.maxsize


if __name__ == '__main__':
    exit()
