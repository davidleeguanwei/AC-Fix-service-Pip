import os
from autofix.Project import Project
from autofix.util.LoggingUtil import Logger


def addParentheses(project: Project, param: tuple) -> bool:
    """Return a boolean
    :param project: target project
    :param_list: (file_path, line_num, inform_need_to_include)
    :return: whether the appliance is successful
    """

    if len(param) < 2:
        Logger().targetLogger[project.index].error('Parameter tuple length less than 2.')
        return False
    origin_file_path = param[0]
    if not os.path.exists(origin_file_path) or not os.path.isfile(origin_file_path):
        Logger().targetLogger[project.index].error('Cannot fix SyntaxError due to file path not found.')
        return False
    file = open(origin_file_path, 'r', encoding='utf-8', errors='ignore')
    target_line = int(param[1])
    information = param[2]
    file_path = param[0].rsplit('/', 1)[0] + '/'
    file_name = param[0].rsplit('/', 1)[1]
    fixed_file = open(file_path + "fix", 'w')
    line_num = 0
    line_not_end_keywords = ["\\", "(", ","]
    flag = False
    for line in file:
        line_num = line_num + 1
        if line_num == target_line:
            if line.lstrip() != line:
                fixed_line = ((len(line)-len(line.lstrip()))*" ") + line.lstrip().split(" ", 1)[0]+"("+information+(")\n" if information[-1] not in line_not_end_keywords else "\n")
                if information[-1] in line_not_end_keywords:
                    flag = True
            else:
                fixed_line = line.split(" ", 1)[0]+"("+information+(")\n" if information[-1] not in line_not_end_keywords else "\n")
                if information[-1] in line_not_end_keywords:
                    flag = True
            print("+++++++++")
            print(fixed_line)
            fixed_file.write(fixed_line)
        elif flag == True:
            if len(line) > 1 and line[-2] in line_not_end_keywords:
                fixed_file.write(line)
            else:
                flag = False
                fixed_file.write(line.replace("\n", ")\n"))
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
