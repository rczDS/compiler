
def strlen_0(s):
    if isinstance(s, str):
        return len(s)
    else:
        _len = 0
        for i in s:
            if i is None:
                break
            _len += 1
        return _len

def gets_0(s):
    s_in = input()
    for i, c in enumerate(s_in):
        s[i] = c

def printf_0(format, *args):
    new_args = []
    for arg in args:
        if type(arg) == list:
            s = ''
            for c in arg:
                if c == None:
                    break
                s += c
            arg = s
        new_args.append(arg) 
    print(format % tuple(new_args), end='')

def system_0(s):
    if not isinstance(s, str):
        s = filter(lambda x: x != 0, s)
        s = ''.join(s)
    import os
    os.system(s)

def atoi_0(s):
    if isinstance(s, str):
        return int(s)
    else:
        sum = 0
        for i in s:
            if i is None:
                break
            sum *= 10
            sum += int(i)
        return sum

def atof_0(s):
    if isinstance(s, str):
        return int(s)
    else:
        mstr = ''
        for i in s:
            if i is None:
                break
            mstr += i
        return float(mstr)

def main_0():
    array_char_0 = [None] * 100
    array_int_0 = [None] * 100
    i_0 = 0
    while i_0 <= 99:
        array_int_0[i_0] = 0
        array_char_0[i_0] = None
        i_0  =  i_0 + 1
    gets_0(array_char_0)
    i_0 = 0
    j_0 = 0
    k_0 = 0
    if array_char_0[0] == '0':
        printf_0("no data")
        return 0
    i_0 = 0
    while i_0 <= 99:
        if array_char_0[i_0] == None:
            temp_0 = [None] * 100
            i_1 = 0
            while i_1 <= 99:
                temp_0[i_1] = None
                i_1  =  i_1 + 1
            l_0 = 0
            while j_0 != i_0:
                temp_0[l_0] = array_char_0[j_0]
                l_0 = l_0 + 1
                j_0 = j_0 + 1
            array_int_0[k_0] = atoi_0(temp_0)
            j_0 = j_0 + 1
            break
        else:
            if array_char_0[i_0] == ',':
                temp_1 = [None] * 100
                i_1 = 0
                while i_1 <= 99:
                    temp_1[i_1] = None
                    i_1  =  i_1 + 1
                l_1 = 0
                while j_0 != i_0:
                    temp_1[l_1] = array_char_0[j_0]
                    l_1 = l_1 + 1
                    j_0 = j_0 + 1
                j_0 = j_0 + 1
                array_int_0[k_0] = atoi_0(temp_1)
                k_0 = k_0 + 1
        i_0 = i_0 + 1
    i_1 = 0
    while i_1 <= k_0:
        j_1 = i_1
        while j_1 > 0:
            if array_int_0[j_1] < array_int_0[j_1-1]:
                tmp_0 = None
                tmp_0 = array_int_0[j_1]
                array_int_0[j_1] = array_int_0[j_1-1]
                array_int_0[j_1-1] = tmp_0
            j_1 = j_1-1
        i_1 = i_1 + 1
    i_1 = 0
    while i_1 <= k_0:
        printf_0("%d", array_int_0[i_1])
        if i_1 != k_0:
            printf_0(",")
        i_1  =  i_1 + 1

if __name__ == "__main__":
    main_0()
