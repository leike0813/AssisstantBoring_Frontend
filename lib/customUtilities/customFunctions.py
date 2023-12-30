

def str2int(str):
    """
    字符串转化为整型，附带校验。
    """
    try:
        ret = int(str)
        ok = True
    except ValueError:
        ret = str
        ok = False
    return ret, ok

def str2float(str):
    """
    字符串转化为浮点型，附带校验。
    """
    try:
        ret = float(str)
        ok = True
    except ValueError:
        ret = str
        ok = False
    return ret, ok

def str2bool(str):
    """
    字符串转化为布尔型，附带校验。
    传入字符串必须为'True'， 结果才是True；传入字符串必须为'False'， 结果才是False。这与bool()函数转化的结果不同，请注意。
    另外传入值若为整数1/0，也会返回True/False。
    其它传入值会原样返回。
    """
    if str == 'True' or str == 1:
        ret = True
        ok = True
    elif str == 'False' or str == 0:
        ret = False
        ok = True
    else:
        ret = str
        ok = False
    return ret, ok