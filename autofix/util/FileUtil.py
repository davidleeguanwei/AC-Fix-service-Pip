import os


def readFileContent(path: str) -> str:
    """Return a string

    :param path: file path to read
    :return: file content
    """
    if not os.path.exists(path) or not os.path.isfile(path):
        return ''
    with open(path, 'r', encoding='utf-8', errors='ignore') as file:
        try:
            content = file.read()
        except UnicodeDecodeError:
            return ''
        return content


def readFileContentByLine(path: str) -> list:
    """Return a list

    :param path: file path to read
    :return: file content in lines
    """
    if not os.path.exists(path) or not os.path.isfile(path):
        return list()
    with open(path, 'r', encoding='utf-8', errors='ignore') as file:
        try:
            content = file.readlines()
        except UnicodeDecodeError:
            return list()
        return content


def appendToTop(path: str, msg: str) -> bool:
    """Return a boolean

    :param path: file path to append message
    :param msg: message to append to file top
    :return: whether the append is successful
    """
    if os.path.exists(path) and not os.path.isfile(path):
        return False
    content = readFileContent(path)
    with open(path, 'w') as f:
        if f.write(msg + '\n\n' + content) != (len(msg) + len(content) + 2):
            return False
    return True


def appendToBottom(path: str, msg: str) -> bool:
    """Return a boolean

    :param path: file path to append message
    :param msg: message to append to file bottom
    :return: whether the append is successful
    """
    if os.path.exists(path) and not os.path.isfile(path):
        return False
    with open(path, 'a') as f:
        if f.write('\n\n' + msg + '\n') != (len(msg) + 3):
            return False
    return True


def removeComment(path: str):
    """Return a string

    Finite states:

    state 00000: initial state
    state 00001: read a slash out of string or comment
    state 00010: in single quotation string
    state 00011: read backslash in single quotation string
    state 00100: in double quotation string
    state 00101: read backslash in double quotation string
    state 01000: in one line comment
    state 10000: in multi-line comment
    state 10001: read * in multi-line comment

    :param: path: file path to target file
    :return: content of target file without annotation
    """
    content = readFileContent(path)
    removed = list()

    state = 0b00000
    multiple_comment = 0b10000
    one_line_comment = 0b01000
    double_quote_str = 0b00100
    single_quote_str = 0b00010
    star_back_slash = 0b00001

    for char in content:
        if state == 0b00000:
            if char == '/':
                state = state ^ star_back_slash
            elif char == '\'':
                state = state ^ single_quote_str
            elif char == '"':
                state = state ^ double_quote_str
        elif state == 0b00001:
            if char == '/':
                state = state ^ star_back_slash ^ one_line_comment
                removed.pop()
                continue
            elif char == '*':
                state = state ^ star_back_slash ^ multiple_comment
                removed.pop()
                continue
            else:
                state = state ^ star_back_slash
        elif state == 0b00010:
            if char == '\\':
                state = state ^ star_back_slash
            elif char == '\'':
                state = state ^ single_quote_str
        elif state == 0b00100:
            if char == '\\':
                state = state ^ star_back_slash
            elif char == '"':
                state = state ^ double_quote_str
        elif state == 0b01000:
            if char == '\n':
                state = state ^ one_line_comment
            else:
                continue
        elif state == 0b10000:
            if char == '*':
                state = state ^ star_back_slash
            continue
        elif state == 0b10001:
            if char == '/':
                state = state ^ star_back_slash ^ multiple_comment
                removed.append(' ')
            elif char != '*':
                state = state ^ star_back_slash
            continue
        elif state == 0b00011 or state == 0b00101:
            state = state ^ star_back_slash
        removed.append(char)

    with open(path, 'w') as f:
        f.write(''.join(removed))

    return True


if __name__ == '__main__':
    exit()
