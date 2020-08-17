import os
import re
from autofix.Project import Project
from autofix.util.LoggingUtil import Logger
from autofix.util.Config import Config
from autofix.util.VirtualEnvironment import VirtualEnvironment
from autofix.util.FileSystemUtil import fileWithName


def handleAttributeError(project: Project, param: tuple) -> bool:
    """Return a boolean
    :param project: target project
    :param_list: (file_path, inform_need_to_include)
    :return: whether the appliance is successful
    """

    if len(param) < 2:
        Logger().targetLogger.error('Parameter tuple length less than 2.')
        return False
    origin_file_path = param[0]
    if (not os.path.exists(origin_file_path) or not os.path.isfile(origin_file_path)) and not os.path.isdir(project.name):
        env_ver = project.currentPythonVersion
        env_name = "test_env_" + project.name
        virtualenv = VirtualEnvironment()
        virtualenv.pipDownload(env_ver, env_name, project.name)
        Logger().targetLogger.debug('Redownloading project due to file path not found..')
        return True
    information = param[1]
    if ":" in information:
        Logger().targetLogger.error('Unproper strategy for this statement.')
        return False
    file_name = param[0].rsplit('/', 1)[1]
    file_path_list = list()
    if os.path.isdir(project.name):
        file_path_list = fileWithName(project.name, file_name)
        for i in range(len(file_path_list)):
            file_path_list[i] = file_path_list[i].rsplit('/', 1)[0] + '/'
    else:
        file_path = param[0].rsplit('/', 1)[0] + '/'
        file_path_list.append(file_path)

    for file_path in file_path_list:
        file = open(file_path + file_name, 'r', encoding='utf-8', errors='ignore')
        fixed_file = open(file_path + "fix", 'w')
        line_num = 0
        for line in file:
            line_num = line_num + 1
            if information in line:
                indented_space_num = len(line)-len(line.lstrip())
                fixed_file.write((indented_space_num*" ")+"try:\n")
                fixed_file.write((4*" ")+line)
                fixed_file.write((indented_space_num*" ")+"except AttributeError as e:\n")
                fixed_file.write(((indented_space_num+4)*" ")+"print(e)\n")
                m = re.match(r'(.+) = (.+)', line)
                if m is not None:
                    variable_name = m.group(1)
                    fixed_file.write(((indented_space_num+4)*" ")+variable_name+" = None\n")
            else:
                fixed_file.write(line)
        file.close()
        fixed_file.close()
        cmd = "rm "+file_path + file_name
        os.system(cmd)
        os.rename(file_path + "fix", file_path + file_name)

    return True



if __name__ == '__main__':
    exit()
