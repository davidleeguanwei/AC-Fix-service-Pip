import os
import shutil


def expandPath(path: str) -> str:
    """Return a string

    :param path: string to be expanded
    :return: the path expanded
    """
    return os.path.abspath(os.path.realpath(os.path.expanduser(path)))


def fileWithExtension(base: str, extension: str) -> list:
    """Return a list

    :param base: directory to search
    :param extension: target file extension
    :return: list of filenames with target file extension
    """
    lst = list()
    ext = '.{}'.format(extension)
    if not os.path.exists(base) or not os.path.isdir(base):
        return lst
    for root, dirs, files in os.walk(base):
        for file in files:
            if file.endswith(ext):
                lst.append(os.path.join(root, file))
    return lst


def fileWithName(base: str, name: str) -> list:
    """Return a list

    :param base: directory to search
    :param name: target file name
    :return: list of filenames with target file extension
    """
    lst = list()
    if not os.path.exists(base) or not os.path.isdir(base):
        return lst
    for root, dirs, files in os.walk(base):
        for file in files:
            if file == name:
                lst.append(os.path.join(root, file))
    return lst


def createDir(path: str) -> bool:
    """Return a boolean

    :param path: the directory path to create
    :return: whether the creation is successful
    """
    if len(path) == 0:
        return False
    if os.path.exists(path) and os.path.isdir(path):
        return True
    if os.path.exists(path) and not os.path.isdir(path):
        return False
    if not createDir(os.path.dirname(path)):
        return False
    try:
        os.mkdir(path)
    except OSError:
        return False
    return True


def createFile(path: str) -> bool:
    """Return a boolean
    
    :param path: the file path to create
    :return: whether the creation is successful
    """
    if len(path) == 0:
        return False
    if os.path.exists(path) and os.path.isfile(path):
        return True
    if os.path.exists(path) and not os.path.isfile(path):
        return False
    if not createDir(os.path.dirname(path)):
        return False
    try:
        with open(path, 'a'):
            os.utime(path, None)
    except OSError:
        return False
    return True


def removePath(path: str) -> bool:
    """Return a boolean

    :param path: the path to remove
    :return: whether the removal is successful
    """
    if not os.path.exists(path):
        return True
    try:
        if os.path.isfile(path):
            os.unlink(path)
        else:
            shutil.rmtree(path)
    except (OSError, shutil.Error):
        return False
    return True


def renameFile(src: str, dst: str) -> bool:
    """Return a boolean

    :param src: old file name
    :param dst: new file name
    :return: whether the rename is successful
    """
    if not os.path.exists(src) or os.path.exists(dst):
        return False
    try:
        os.rename(src, dst)
    except OSError:
        return False
    return True


def copyFile(src: str, dst: str) -> bool:
    """Return a boolean

    :param src: source file name
    :param dst: destination file name
    :return: whether the copy is successful
    """
    if not os.path.exists(src) or not os.path.isfile(src):
        return False
    if os.path.exists(dst) and not removePath(dst):
        return False
    try:
        shutil.copy(src, dst)
    except shutil.Error:
        return False
    return True


if __name__ == '__main__':
    exit()
