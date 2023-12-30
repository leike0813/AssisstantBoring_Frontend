

class ArgumentError(Exception):
    def __init__(self, input):
        self.input = input

    def __str__(self):
        return '\nThe inputed argument ' + str(self.input) + ' is incorrect.'


class SizeError(Exception):
    """
    输入数组尺寸错误异常。
    """

    def __init__(self, input):
        self.input = input

    def __str__(self):
        return '\nThe size of inputed array (' + str(self.input) + ') does not match.'


class MatrixSizeError(Exception):
    """
    输入矩阵尺寸错误异常。
    """

    def __init__(self, input):
        self.input = input

    def __str__(self):
        return '\nThe size of inputed matrix ' + str(self.input) + ' is incorrect.\nIt must be a square matrix.'