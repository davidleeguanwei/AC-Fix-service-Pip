import os
import re
from autofix.Project import Project


def replaceCommaWithBracketsInRaise(project: Project, param: tuple) -> bool:
    """Return a boolean
    :param project: target project
    :param_list: (file_path, line_num)
    :return: whether the appliance is successful
    """

    if len(param) < 2:
        Logger().targetLogger[project.index].error('Parameter tuple length less than 2.')
        return False
    origin_file_path = param[0]
    file = open(origin_file_path, 'r', errors = 'ignore')
    target_line = param[1]
    print("HELLO: "+ target_line)
    file_path = param[0].rsplit('/', 1)[0] + '/'
    file_name = param[0].rsplit('/', 1)[1]
    fixed_file = open(file_path + "fix", 'w')
    line_num = 0
    flag = False
    line_not_end_keywords = ["\\", "(", ","]
    for line in file:
        line_num = line_num + 1
        if re.match(r'\s*raise (.+), (.+)', line) is not None:
            if line[-2] not in line_not_end_keywords:
                front = line.split(", ", 1)[0]
                back = line.split(", ", 1)[1]
                fixed_line = front + "(" + back[0:-1] + ")\n"
            else:
                flag = True
                fixed_line = line.split(", ", 1)[0] + "(" + line.split(", ", 1)[1]
            print(fixed_line)
            fixed_file.write(fixed_line)
        else:
            if flag == True:
                if len(line) > 1 and line[-2] not in line_not_end_keywords:
                    flag = False
                    line = line.replace("\n", ")\n")
            fixed_file.write(line)
    file.close()
    fixed_file.close()
    cmd = "rm "+origin_file_path
    os.system(cmd)
    os.rename(file_path + "fix", file_path + file_name)

    return True



if __name__ == '__main__':
    exit()
