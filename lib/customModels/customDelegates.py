import PySide2.QtCore as QtC, PySide2.QtWidgets as QtW

__all__ = ['QDoubleSpinboxDelegate', 'QSpinboxDelegate', 'QComboboxDelegate']


class QDoubleSpinboxDelegate(QtW.QStyledItemDelegate):
    """
    用于PyQt5的浮点数输入框代理。
    """
    def __init__(self, decimalPlace = 2, singleStep = 0.01, range = [-65535, 65535], parent=None):
        """
        构造器
        默认数据范围为(-65535.0 ~ 65535.0)。
        默认步长为0.01。
        默认小数位数为2。
        """
        super(QDoubleSpinboxDelegate, self).__init__(parent)
        self.__decimalPlace = decimalPlace
        self.__singleStep = singleStep
        self.__range = range

    @property
    def decimalPlace(self):
        return self.__decimalPlace

    def setDecimalPlace(self, decimalPlace):
        if type(decimalPlace) is not int:
            raise TypeError("Only accept integer as input.")
        elif decimalPlace < 0 :
            raise ValueError("Decimal place must be non-negative.")
        self.__decimalPlace = decimalPlace

    @property
    def sigleStep(self):
        return self.__singleStep

    def setSingleStep(self, stepLength):
        if not (type(stepLength) is float or type(stepLength) is int):
            raise TypeError("Only accept float or integer as input.")
        elif stepLength <= 0 :
            raise ValueError("Step length must be positive.")
        self.__singleStep = stepLength

    @property
    def range(self):
        return self.__range

    def setMinimum(self, value):
        if not (type(value) is float or type(value) is int):
            raise TypeError("Only accept float or integer as input.")
        elif value > self.__range[1]:
            raise ValueError("The minimum must be smaller than the maximum.")
        self.__range[0] = value

    def setMaximum(self, value):
        if not (type(value) is float or type(value) is int):
            raise TypeError("Only accept float or integer as input.")
        elif value < self.__range[0]:
            raise ValueError("The maximum must be greater than the minimum.")
        self.__range[1] = value

    def setRange(self, range):
        if len(range) != 2:
            raise TypeError("Only accept iterable with 2 elements as input.")
        elif not ((type(range[0]) is float or type(range[0]) is int)\
            and (type(range[1]) is float or type(range[1]) is int)):
            raise TypeError("Only accept iterable with float or integer elements as input.")
        elif range[0] > range[1]:
            raise ValueError("The minimum of the range must be smaller than its maximum.")
        self.__range = list(range)

    def createEditor(self, parent, option, index):
        """
        PyQt5的代理必须重写的关键函数。
        创建编辑器。
        """
        editor = QtW.QDoubleSpinBox(parent)
        editor.setFrame(False)
        editor.setMinimum(self.range[0])
        editor.setMaximum(self.range[1])
        editor.setSingleStep(self.__singleStep)
        editor.setDecimals(self.__decimalPlace)
        return editor

    def setEditorData(self, editor, index):
        """
        PyQt5的代理必须重写的关键函数。
        从模型中读取数据传给编辑器。
        """
        editor.setValue(float(index.data(QtC.Qt.EditRole)))

    def setModelData(self, editor, model, index):
        """
        PyQt5的代理必须重写的关键函数。
        将编辑器的数值写入模型。
        """
        model.setData(index, editor.value())


class QSpinboxDelegate(QtW.QStyledItemDelegate):
    """
    用于PyQt5的整数输入框代理。
    """
    def __init__(self, singleStep = 1, range = [-65535, 65535], parent=None):
        """
        构造器
        默认数据范围为(-65535.0 ~ 65535.0)。
        默认步长为1。
        """
        super(QSpinboxDelegate, self).__init__(parent)
        self.__singleStep = singleStep
        self.__range = range

    @property
    def sigleStep(self):
        return self.__singleStep

    def setSingleStep(self, stepLength):
        if type(stepLength) is not int:
            raise TypeError("Only accept integer as input.")
        elif stepLength <= 0:
            raise ValueError("Step length must be positive.")
        self.__singleStep = stepLength

    @property
    def range(self):
        return self.__range

    def setMinimum(self, value):
        if type(value) is not int:
            raise TypeError("Only accept integer as input.")
        elif value > self.__range[1]:
            raise ValueError("The minimum must be smaller than the maximum.")
        self.__range[0] = value

    def setMaximum(self, value):
        if type(value) is not int:
            raise TypeError("Only accept integer as input.")
        elif value < self.__range[0]:
            raise ValueError("The maximum must be greater than the minimum.")
        self.__range[1] = value

    def setRange(self, range):
        if len(range) != 2:
            raise TypeError("Only accept iterable with 2 elements as input.")
        elif (type(range[0]) is not int) or (type(range[1]) is not int):
            raise TypeError("Only accept iterable with integer elements as input.")
        elif range[0] > range[1]:
            raise ValueError("The minimum of the range must be smaller than its maximum.")
        self.__range = list(range)

    def createEditor(self, parent, option, index):
        """
        PyQt5的代理必须重写的关键函数。
        创建编辑器。
        """
        editor = QtW.QSpinBox(parent)
        editor.setFrame(False)
        editor.setMinimum(self.__range[0])
        editor.setMaximum(self.__range[1])
        editor.setSingleStep(self.__singleStep)
        return editor

    def setEditorData(self, editor, index):
        """
        PyQt5的代理必须重写的关键函数。
        从模型中读取数据传给编辑器。
        """
        editor.setValue(int(float(index.data(QtC.Qt.EditRole))))

    def setModelData(self, editor, model, index):
        """
        PyQt5的代理必须重写的关键函数。
        将编辑器的数值写入模型。
        """
        model.setData(index, editor.value())


class QComboboxDelegate(QtW.QStyledItemDelegate):
    """
    用于PyQt5的下拉菜单输入框代理，对应的数据类型必须为整数。
    """
    def __init__(self, itemList, parent=None):
        """
        构造器
        默认含有两项。
        """
        super(QComboboxDelegate, self).__init__(parent)
        self.__itemList = itemList

    @property
    def itemList(self):
        return self.__itemList

    @property
    def count(self):
        return len(self.__itemList)

    def createEditor(self, parent, option, index):
        """
        PyQt5的代理必须重写的关键函数。
        创建编辑器。
        """
        editor = QtW.QComboBox(parent)
        editor.setFrame(False)
        editor.addItems(self.__itemList)
        return editor

    def setEditorData(self, editor, index):
        """
        PyQt5的代理必须重写的关键函数。
        从模型中读取数据传给编辑器。
        """
        editor.setCurrentIndex(int(float(index.data(QtC.Qt.EditRole))))

    def setModelData(self, editor, model, index):
        """
        PyQt5的代理必须重写的关键函数。
        将编辑器的数值写入模型。
        """
        model.setData(index, editor.currentIndex())