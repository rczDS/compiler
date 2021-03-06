# coding=utf-8
import os
import re


def lint(s):
    sstr = ''
    i = 0
    while i < len(s):
        if s[i] == '=':
            if s[i + 1] == '=':
                sstr += ' == '
                i = i + 2
                continue
            elif s[i + 1] != '=':
                sstr += ' = '
                i = i + 1
                continue
        elif s[i] == '!':
            if s[i + 1] == '=':
                sstr += ' != '
                i = i + 2
                continue
            elif s[i + 1] != '=':
                sstr += '!'
                i = i + 1
                continue
        elif s[i] == '>':
            if s[i + 1] == '=':
                sstr += ' >= '
                i = i + 2
                continue
            elif s[i + 1] != '=':
                sstr += ' > '
                i = i + 1
                continue
        elif s[i] == '<':
            if s[i + 1] == '=':
                sstr += ' <= '
                i = i + 2
                continue
            elif s[i + 1] != '=':
                sstr += ' < '
                i = i + 1
                continue
        elif s[i] == '+':
            if s[i + 1] == '=':
                sstr += ' += '
                i = i + 2
                continue
            elif s[i + 1] != '=':
                sstr += ' + '
                i = i + 1
                continue
        elif s[i] == '*':
            if s[i + 1] == '=':
                sstr += ' *= '
                i = i + 2
                continue
            elif s[i + 1] != '=':
                sstr += ' * '
                i = i + 1
                continue
        elif s[i] == '/':
            if s[i + 1] == '=':
                sstr += ' /= '
                i = i + 2
                continue
            elif s[i + 1] != '=':
                sstr += ' / '
                i = i + 1
                continue
        elif s[i] == '-':
            if s[i + 1] == '=':
                sstr += ' -= '
                i = i + 2
                continue
            elif s[i + 1] != '=':
                if not s[i + 1].isdigit():
                    sstr += ' - '
                    i = i + 1
                    continue
                else:
                    sstr += s[i]
                    i = i + 1
                    continue
        elif s[i] == "'":
            tmp = s.find("'", i + 1, len(s))
            sstr += s[i:tmp + 1]
            i = tmp + 1
            continue
        elif s[i] == ',':
            sstr += ', '
            i = i + 1
            continue
        elif s[i] == '"':
            next = s.find('"', i + 1, len(s))
            sstr += s[i:next + 1]
            i = next + 1
            continue
        else:
            sstr += s[i]
            i = i + 1
            continue
    return sstr


def formatIndent(item, rank=-1):
    INDENT_STRING = '    '
    if type(item) == str:
        item = lint(item)
        # ?????????????????????????????????????????????=None
        if '(' not in item and ' ' not in item and '=' not in item and item != '' and item != 'break' \
                and item != 'continue' and item != 'pass' and item != 'else:' and item != 'if' and item != 'return':
            item += ' = None'
        return INDENT_STRING * rank + item
    if type(item) == list:
        lines = []
        for i in item:
            lines.append(formatIndent(i, rank + 1))
        return '\n'.join(lines)


def precompile(filename):
    """ ??????????????? """
    """ ??????:(bool-????????????, string-?????????????????????????????????????????????????????????) """
    """ ??????:(bool, string) """
    # ???????????????
    folder = os.path.dirname(filename)
    # ????????????
    try:
        file = open(filename, 'r', encoding='utf-8')
        lines = file.read().split('\n')
        file.close()
    except FileNotFoundError:
        return False, '??????????????????"%s"' % filename
    # ?????????
    macro_define_list = []
    macro_include_list = []
    index = 0
    while index < len(lines):
        line = lines[index]
        line = line.strip(' ')
        line = line.strip('\t')
        line = line.strip('\r')
        line = line.strip('\n')
        # ???????????????
        if len(line) <= 0:
            lines.pop(index)
            continue
        if line[0] == '#':
            words = line[1:].strip(' ').split(' ', 2)
            try:
                # define ??????
                if words[0] == 'define':
                    macro_define_list.append((words[1], words[2]))
                # include ??????
                elif words[0] == 'include':
                    if words[1][0] == '"' and words[1][-1] == '"':
                        macro_include_list.append(os.path.join(folder, words[1][1:-1]))
                    elif words[1][0] == '<' and words[1][-1] == '>':
                        pass
                    else:
                        raise KeyError
                else:
                    raise KeyError
            except KeyError:
                return False, '????????????????????????"%s"???????????????"%s"' % (line, filename)
            lines.pop(index)
            continue
        index += 1
    # define ??????
    s = '\n'.join(lines)
    for m in macro_define_list:
        s = re.sub(m[0], m[1], s)
    # include ??????
    i = ''
    for m in macro_include_list:
        inc = precompile(m)
        if inc[0]:
            i = i + inc[1]
        else:
            return inc
    s = i + s + '\n'
    return True, s