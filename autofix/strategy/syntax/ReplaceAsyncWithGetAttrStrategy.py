import os
from autofix.Project import Project


def replaceAsyncWithGetAttr(project: Project, param: tuple) -> bool:
    """Return a boolean
    :param project: target project
    :param param: (file_path, line_num)
    :return: whether the appliance is successful
    """
    if len(param) < 2:
        Logger().targetLogger.error('Parameter tuple length less than 2.')
        return False
    origin_file_path = param[0]
    file = open(origin_file_path, 'r', errors = 'ignore')
    target_line = param[1]
    file_path = param[0].rsplit('/', 1)[0] + '/'
    file_name = param[0].rsplit('/', 1)[1]
    fixed_file = open(file_path + "fix", 'w')
    line_num = 0
    for line in file:
        line_num = line_num + 1
        if line_num == int(target_line) or "async" in line:
            fixed_line = line.replace("asyncio.async", "getattr(asyncio, \'async\')")
            fixed_file.write(fixed_line)
        else:
            fixed_file.write(line)
    file.close()
    fixed_file.close()
    cmd = "rm "+origin_file_path
    os.system(cmd)
    os.rename(file_path + "fix", file_path + file_name)

    return True



if __name__ == '__main__':
    exit()
