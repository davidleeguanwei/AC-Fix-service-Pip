import os
import re
from autofix.Project import Project


def putFromFutureAtFirstLine(project: Project, param: tuple) -> bool:
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
    target_line = int(param[1])
    from_future_statement = param[2]
    file_path = param[0].rsplit('/', 1)[0] + '/'
    file_name = param[0].rsplit('/', 1)[1]
    fixed_file = open(file_path + "fix", 'w')
    line_num = 0
    flag = False
    line_list = []
    print(origin_file_path)
    for line in file:
        line_num = line_num + 1
        if line_num == target_line:
            import_modules = line.split("; ")
            for module in import_modules:
                if "__future__" in module or "import" not in module:
                    module = module + "\n" if module != import_modules[-1] else module
                    fixed_file.write(module)
                    if module[-2] == "\\":
                        target_line = target_line + 1
                    else:
                        flag = True
                else:
                    module = module + "\n" if module[-2] != "\\" else module
                    line_list.append(module)
        elif flag == False:
            line_list.append(line)
        else:
            if len(line_list) > 0:
                line_size = len(line_list)
                for i in range(line_size):
                    fixed_file.write(line_list[0])
                    del line_list[0]
            fixed_file.write(line)
    file.close()
    fixed_file.close()
    cmd = "rm "+origin_file_path
    os.system(cmd)
    os.rename(file_path + "fix", file_path + file_name)

    return True



if __name__ == '__main__':
    exit()
