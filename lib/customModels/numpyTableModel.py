from copy import deepcopy
import PySide2.QtWidgets as QtW, PySide2.QtGui as QtG, PySide2.QtCore as QtC
from ..customUtilities.customExceptions import *
from ..customUtilities.customFunctions import *
import numpy as np

__all__ = ['QNumpyArray2DModel', 'QNumpyMatrixModel', 'QNumpyArray1DModel', 'QNumpyArray1Model_Transpose']


class QAbstractNumpyModel(QtC.QAbstractTableModel):
    """
    用于PyQt5的Numpy数组模型抽象基类。
    不可变结构数据模型。
    实现基本的缓存/信号机制。
    """
    editConfirmed = QtC.Signal()  # 确认编辑的信号。
    editRefuted = QtC.Signal()  # 撤销编辑的信号。
    operationFailure = QtC.Signal(str) # 操作失败的信号。
    def __init__(self, parent=None):
        super(QAbstractNumpyModel, self).__init__(parent)
        self._editable = True  # 默认可编辑
        self._displayDecimal = None
        self.editConfirmed.connect(self.cacheArray)
        self.editRefuted.connect(self.cacheArray)

    @property
    def dtype(self):
        return self.npArray_Orig.dtype

    def isEditable(self):
        return self._editable

    def setEditable(self, editable):
        if type(editable) is not bool:
            raise TypeError("Only accept boolean variable as input.")
        self._editable = editable

    @property
    def displayDecimal(self):
        return self._displayDecimal

    def setDisplayDecimal(self, displayDecimal):
        if type(displayDecimal) is not int:
            raise TypeError("Only accept integer as input.")
        elif displayDecimal < 0 :
            raise ValueError("Decimal place must be non-negative.")
        self._displayDecimal = displayDecimal

    @QtC.Slot()
    def cacheArray(self):
        """
        生成nparray_orig的一个缓存副本nparray，用于界面编辑。
        nparray_orig为实际外部传入的数组对象。对nparray_orig的改变会直接反应在外部，而副本nparray则不会。
        """
        self.npArray = deepcopy(self.npArray_Orig)
        self.dataChanged.emit(self.index(0, 0),
                              self.index(self.npArray_Orig.shape[0] - 1, self.npArray_Orig.shape[1] - 1))

    def confirmEdit(self):
        """
        确认编辑时调用的槽函数。
        """
        self.editConfirmed.emit()

    def refuteEdit(self):
        """
        撤销编辑时调用的槽函数。
        """
        self.editRefuted.emit()


class QAbstractNumpy2DModel(QAbstractNumpyModel):
    """
    用于PyQt5的Numpy二维数组模型抽象基类。
    不可变结构数据模型。
    实现数组设置、索引、读写功能。
    """
    def __init__(self, npArray=None, parent=None):
        super(QAbstractNumpy2DModel, self).__init__(parent)
        if type(npArray) is type(None):  # 若指定了nparray参数，则将nparray赋予nparray_orig参数；否则将一个空数组赋予nparray_orig参数
            self.setNumpyArray(np.empty((0, 0)))
        else:
            self.setNumpyArray(npArray)

    def setNumpyArray(self, npArray):
        """
        设置数据模型对应的二维Numpy数组。
        """
        if not isinstance(npArray, np.core.ndarray):
            raise TypeError("The input argument must be a numpy.ndarray object.")

        self.layoutAboutToBeChanged.emit()
        self.npArray_Orig = npArray
        self.npArray = np.empty((npArray.shape[0], npArray.shape[1]), dtype=npArray.dtype)
        self.cacheArray()
        self.layoutChanged.emit()

    def confirmEdit(self):
        """
        确认编辑时调用的槽函数。
        将缓存数组npArray中的数据写入npArray_Orig，确认编辑。此时外部引用对象会随之改变。
        """
        if self.npArray_Orig.shape[0] > 0 and self.npArray_Orig.shape[1] > 0:
            for i in range(self.npArray_Orig.shape[0]):
                for j in range(self.npArray_Orig.shape[1]):
                    self.npArray_Orig[i, j] = self.npArray[i, j]
            super(QAbstractNumpy2DModel, self).confirmEdit()
        else:
            raise RuntimeError()

    def index(self, row, column, parent=QtC.QModelIndex()):
        """
        PyQt5数据模型必须重写的关键函数。
        返回模型索引对象(Index)。
        """
        return self.createIndex(row, column, self.npArray[row, column])

    def rowCount(self, parent=QtC.QModelIndex()):
        """
        PyQt5数据模型必须重写的关键函数。
        返回模型的行数。
        """
        return self.npArray.shape[0]

    def columnCount(self, parent=QtC.QModelIndex()):
        """
        PyQt5数据模型必须重写的关键函数。
        返回模型的列数。
        """
        return self.npArray.shape[1]

    def data(self, index, role=QtC.Qt.DisplayRole):
        """
        PyQt5数据模型必须重写的关键函数。
        返回在指定的Role下的模型数据。
        其中DisplayRole为视图(View)中显示的数据；EditRole为传给编辑器的数据；TextAlignmentRole为数据显示时的对齐方式。
        """
        # 若index超出数组范围，则返回super的值
        if not index.isValid() or \
                not 0 <= index.row() < self.npArray.shape[0] or \
                not 0 <= index.column() < self.npArray.shape[1]:
            return None
        # 对于DisplayRole和EditRole，返回数组中的值
        if role == QtC.Qt.DisplayRole or role == QtC.Qt.EditRole:
            if self._displayDecimal == None: # 若未设定_displayDecimal值，则原样返回。
                return str(self.npArray[index.row(), index.column()])
            else:# 若设定了_displayDecimal值，则返回小数点后固定位数。
                return str(round(self.npArray[index.row(), index.column()], self._displayDecimal))
        elif role == QtC.Qt.TextAlignmentRole: # 对于TextAlignmentRole，返回水平/垂直居中。
            return QtC.Qt.AlignHCenter | QtC.Qt.AlignVCenter
        else: # 对于其它Role，返回super的值
            return None

    def flags(self, index):
        """
        PyQt5数据模型必须重写的关键函数。
        返回指定索引对应的flag。
        为使模型数据可在视图中编辑，需要额外返回ItemIsEditable这一flag。
        """
        flag = super(QAbstractNumpy2DModel, self).flags(index)
        # 若_editable为True，则返回打开了ItemIsEditable的flag
        return flag | QtC.Qt.ItemIsEditable if self._editable else flag

    def setData(self, index, value, role=QtC.Qt.EditRole):
        """
        PyQt5可编辑数据模型必须重写的关键函数。
        将编辑器传入的值写入缓存数组nparray。
        """
        if self.dtype() == int:  # 由于编辑器传入值均为str类型，需进行相应的数据类型转换及校验。
            value_dtype, ok = str2int(value)
        elif self.dtype() == float:
            value_dtype, ok = str2float(value)
        elif self.dtype() == str:
            value_dtype, ok = value, True
        elif self.dtype() == object:
            value_dtype, ok = value, True
        else:
            value_dtype, ok = value, False
        if ok:
            self.npArray[index.row(), index.column()] = value_dtype
            self.dataChanged.emit(index, index)
            return True
        self.operationFailure.emit('Type conversion failed.')
        return False


class QNumpyArray2DModel(QAbstractNumpy2DModel):
    """
    用于PyQt5的Numpy二维array数据模型。
    不可变结构数据模型。
    继承QAbstractNumpy2DModel
    """
    def __init__(self, npArray=None, header_Num = False, parent=None):
        """
        构造器。
        可选参数：
            1. npArray: 二维Numpy数组。不要采用Matrix数据类型。
            2. parent: 父对象。一般留空即可。
        """
        super(QNumpyArray2DModel, self).__init__(npArray, parent)
        self._hasHeader_H = False  # 默认不含水平header信息
        self._hasHeader_V = False  # 默认不含竖向header信息
        self._vHeader_Num = header_Num  # 默认不将行号作为默认垂直header

    @property
    def rank(self):
        """
        返回m×n数组的阶数（非数学定义）。
        当m≠n时，阶数定义为m和n中较小者。
        """
        return min(self.npArray_Orig.shape)

    def headerData(self, section, orientation, role=QtC.Qt.DisplayRole):
        """
        PyQt5数据模型必须重写的关键函数。
        返回表头信息。
        格式类似data()函数。
        """
        hdata = super(QNumpyArray2DModel, self).headerData(section, orientation, role)
        if orientation == QtC.Qt.Horizontal and self._hasHeader_H:
            if role == QtC.Qt.DisplayRole or role == QtC.Qt.EditRole:
                return str(self.headerArray_H[section])
            elif role == QtC.Qt.TextAlignmentRole:
                return QtC.Qt.AlignHCenter | QtC.Qt.AlignVCenter
            else:
                return hdata
        elif orientation == QtC.Qt.Vertical and self._hasHeader_V:# _hasHeader_V比_VHeader_Num具有更高优先级
            if role == QtC.Qt.DisplayRole or role == QtC.Qt.EditRole:
                return str(self.headerArray_V[section])
            elif role == QtC.Qt.TextAlignmentRole:
                return QtC.Qt.AlignHCenter | QtC.Qt.AlignVCenter
            else:
                return hdata
        elif orientation == QtC.Qt.Vertical and self._vHeader_Num: #若_VHeader_Num为True，则直接返回行号作为VerticalHeader
            if role == QtC.Qt.DisplayRole or role == QtC.Qt.EditRole:
                return str(section)
            elif role == QtC.Qt.TextAlignmentRole:
                return QtC.Qt.AlignHCenter | QtC.Qt.AlignVCenter
            else:
                return hdata
        return hdata

    def setHeader_Batch(self, headerArray, orientation):
        """
        批量设置表头信息。
        参数：
            1. headerArray            一维Numpy数组，长度与数组相应维度的阶数一致。
            2. orientation            维度，1代表水平，2代表垂直。可用QtCore.Qt.Horizontal和QtCore.Qt.Vertical等价。
        """
        if type(headerArray) is np.ndarray:
            if orientation == QtC.Qt.Horizontal:
                if headerArray.shape[0] == self.npArray.shape[1]:
                    self.headerArray_H = headerArray
                    self._hasHeader_H = True
                    self.headerDataChanged.emit(QtC.Qt.Horizontal, 0, self.npArray.shape[1] - 1)
                else:
                    raise SizeError(headerArray.shape[0])
            elif orientation == QtC.Qt.Vertical:
                if headerArray.shape[0] == self.npArray.shape[0]:
                    self.headerArray_V = headerArray
                    self._hasHeader_V = True
                    self.headerDataChanged.emit(QtC.Qt.Vertical, 0, self.npArray.shape[0] - 1)
                else:
                    raise SizeError(headerArray.shape[0])
            else:
                raise ArgumentError(orientation)
        else:
            raise TypeError('The input argument must be a numpy.ndarray object.')

    def setRowNumber2VerticalHeader(self):
        self._vHeader_Num = True
        self.headerDataChanged.emit(QtC.Qt.Vertical, 0, self.npArray.shape[0] - 1)


class QNumpyMatrixModel(QAbstractNumpy2DModel):
    """
    用于PyQt5的Numpy二维等阶array数据模型。
    继承QAbstractNumpyArray2Model。
    不可变结构数据模型。
    """
    def __init__(self, npArray=None, header_Num = False, parent=None):
        super(QNumpyMatrixModel, self).__init__(npArray, parent)
        self._hasHeader = False
        self._header_Num = header_Num  # 默认不将行/列号作为默认header

    def setNumpyArray(self, npArray):
        """
        设置数据模型对应的二维Numpy数组。
        附带方阵校验。
        """
        if npArray.shape[0] != npArray.shape[1]: # 方阵校验
            raise MatrixSizeError(npArray.shape)
        else:
            super(QNumpyMatrixModel, self).setNumpyArray(npArray)

    @property
    def rank(self):
        """返回方阵的阶数"""
        return self.npArray_Orig.shape[0]

    def headerData(self, section, orientation, role=QtC.Qt.DisplayRole):
        """
        PyQt5数据模型必须重写的关键函数。
        返回表头信息。
        格式类似data()函数。
        """
        hdata = super(QNumpyMatrixModel, self).headerData(section, orientation, role)
        if orientation == QtC.Qt.Horizontal or orientation == QtC.Qt.Vertical:
            if role == QtC.Qt.DisplayRole or role == QtC.Qt.EditRole:
                if self._hasHeader:
                    return str(self.headerArray[section])
                elif self._header_Num:
                    return str(section)
            elif role == QtC.Qt.TextAlignmentRole:
                return QtC.Qt.AlignHCenter | QtC.Qt.AlignVCenter
            else:
                return hdata
        else:
            return hdata

    def setHeader_Batch(self, headerArray):
        """
        批量设置表头信息。
        参数：
            1. headerArray: 一维Numpy数组，长度与矩阵阶数一致。
        """
        if type(headerArray) is np.ndarray:
            if headerArray.shape[0] == self.rank:
                self.headerArray = headerArray
                self._hasHeader = True
                self.headerDataChanged.emit(QtC.Qt.Horizontal, 0, self.rank - 1)
                self.headerDataChanged.emit(QtC.Qt.Vertical, 0, self.rank - 1)
            else:
                raise SizeError(headerArray.shape[0])
        else:
            raise TypeError('The input argument must be a numpy.ndarray object.')

    def setNumber2Header(self):
        self._header_Num = True
        self.headerDataChanged.emit(QtC.Qt.Horizontal, 0, self.rank - 1)
        self.headerDataChanged.emit(QtC.Qt.Vertical, 0, self.rank - 1)


class QAbstractNumpy1DModel(QAbstractNumpyModel):
    """
    用于PyQt5的Numpy一维数组模型抽象基类。
    不可变结构数据模型。
    实现数组设置、索引、读写功能。
    继承QAbstractNumpyModel。
    """
    def __init__(self, npArray=None, direction = None, header_Num = False, parent=None):
        super(QAbstractNumpy1DModel, self).__init__(parent)
        if type(npArray) is type(None):  # 若指定了nparray参数，则将nparray赋予nparray_orig参数；否则将一个空数组赋予nparray_orig参数
            self.setNumpyArray(np.empty(0))
        else:
            self.setNumpyArray(npArray)
        self._hasHeader = False  # 默认不含header信息
        self._hasCategory = False # 默认不含数据头信息
        self._header_Num = header_Num
        self._direction = direction # 不定方向
        self._otherDirection = QtC.Qt.Horizontal if direction == QtC.Qt.Vertical else QtC.Qt.Vertical

    @property
    def rank(self):
        return self.npArray_Orig.shape[0]

    def setNumpyArray(self, npArray):
        """
        设置数据模型对应的一维Numpy数组。
        """
        if not isinstance(npArray, np.core.ndarray):
            raise TypeError("The input argument must be a numpy.ndarray object.")

        self.layoutAboutToBeChanged.emit()
        self.npArray_Orig = npArray
        self.npArray = np.empty(npArray.shape[0], dtype=npArray.dtype)
        self.cacheArray()
        self.layoutChanged.emit()

    def confirmEdit(self):
        """
        确认编辑时调用的槽函数。
        将缓存数组nparray中的数据写入nparray_orig，确认编辑。
        """
        if self.npArray_Orig.shape[0] > 0:
            for i in range(self.npArray_Orig.shape[0]):
                self.npArray_Orig[i] = self.npArray[i]
            super(QAbstractNumpy1DModel, self).confirmEdit()
        else:
            raise RuntimeError()

    def setData_Batch(self, dataArray):
        """
        批量为数组赋值。
        """
        if type(dataArray) is np.ndarray:
            if dataArray.shape[0] == self.rank:
                self.npArray[:] = dataArray
                if self._direction == QtC.Qt.Vertical:
                    self.dataChanged.emit(self.index(0, 0), self.index(self.rank - 1, 0))
                elif self._direction == QtC.Qt.Horizontal:
                    self.dataChanged.emit(self.index(0, 0), self.index(0, self.rank - 1))
            else:
                raise SizeError(dataArray.shape[0])
        else:
            raise TypeError('The input argument must be a numpy.ndarray object.')

    def setHeader_Batch(self, headerArray):
        """
        批量设置表头信息。
        参数：
            1. headerArray: 一维Numpy数组，长度与数组阶数一致。
        """
        if type(headerArray) is np.ndarray:
            if headerArray.shape[0] == self.rank:
                self.headerArray = headerArray
                self._hasHeader = True
                self.headerDataChanged.emit(self._direction, 0, self.rank - 1)
            else:
                raise SizeError(headerArray.shape[0])
        else:
            raise TypeError('The input argument must be a numpy.ndarray object.')

    def setCategory(self, category):
        if type(category) is not str:
            raise TypeError("Only accept string as input.")
        self.category = category
        self._hasCategory = True
        self.headerDataChanged.emit(self._otherDirection, 0, 0)

    def rowCount(self, parent=QtC.QModelIndex()):
        """
        PyQt5数据模型必须重写的关键函数。
        返回模型的行数。
        """
        return self.rank if self._direction == QtC.Qt.Vertical else 1

    def columnCount(self, parent=QtC.QModelIndex()):
        """
        PyQt5数据模型必须重写的关键函数。
        返回模型的列数。
        """
        return 1 if self._direction == QtC.Qt.Vertical else self.rank

    def index(self, row, column, parent=QtC.QModelIndex()):
        """
        PyQt5数据模型必须重写的关键函数。
        返回模型索引对象(Index)。
        """
        return self.createIndex(row, column, (self.npArray[row]\
                                                  if self._direction == QtC.Qt.Vertical\
                                                  else self.npArray[column]))

    def data(self, index, role=QtC.Qt.DisplayRole):
        """
        PyQt5数据模型必须重写的关键函数。
        返回在指定的Role下的模型数据。
        其中DisplayRole为视图(View)中显示的数据；EditRole为传给编辑器的数据；TextAlignmentRole为数据显示时的对齐方式。
        """
        if not index.isValid() or \
                not 0 <= (index.row() if self._direction == QtC.Qt.Vertical else index.column()) <= self.rank:
            return None

        if role == QtC.Qt.DisplayRole or role == QtC.Qt.EditRole:
            if self._displayDecimal == None:
                return str((self.npArray[index.row()]\
                                if self._direction == QtC.Qt.Vertical\
                                else self.npArray[index.column()]))
            else:
                return str(round((self.npArray[index.row()]\
                                      if self._direction == QtC.Qt.Vertical\
                                      else self.npArray[index.column()]), self._displayDecimal))
        elif role == QtC.Qt.TextAlignmentRole:
            return QtC.Qt.AlignHCenter | QtC.Qt.AlignVCenter
        else:
            return None

    def headerData(self, section, orientation, role=QtC.Qt.DisplayRole):
        """
        PyQt5数据模型必须重写的关键函数。
        返回表头信息。
        格式类似data()函数。
        """
        hdata = super(QNumpyArray1DModel, self).headerData(section, orientation, role)
        if orientation == self._otherDirection:
            if role == QtC.Qt.DisplayRole or role == QtC.Qt.EditRole:
                if self._hasCategory:
                    return self.category
            elif role == QtC.Qt.TextAlignmentRole:
                return QtC.Qt.AlignHCenter | QtC.Qt.AlignVCenter
            else:
                return hdata
        elif orientation == self._direction:
            if role == QtC.Qt.DisplayRole or role == QtC.Qt.EditRole:
                if self._hasHeader:
                    return str(self.headerArray[section])
                elif self._header_Num:
                    return str(section)
            elif role == QtC.Qt.TextAlignmentRole:
                return QtC.Qt.AlignHCenter | QtC.Qt.AlignVCenter
            else:
                return hdata
        else:
            return hdata

    def setData(self, index, value, role=QtC.Qt.EditRole):
        """
        PyQt5可编辑数据模型必须重写的关键函数。
        将编辑器传入的值写入缓存数组nparray。
        """
        if self.dtype() == int:  # 由于编辑器传入值均为str类型，需进行相应的数据类型转换及校验。
            value_dtype, ok = str2int(value)
        elif self.dtype() == float:
            value_dtype, ok = str2float(value)
        elif self.dtype() == str:
            value_dtype, ok = value, True
        elif self.dtype() == object:
            value_dtype, ok = value, True
        else:
            value_dtype, ok = value, False
        if ok:
            if self._direction == QtC.Qt.Vertical:
                self.npArray[index.row()] = value_dtype
            else:
                self.npArray[index.column()] = value_dtype
            self.dataChanged.emit(index, index)
            return True
        self.operationFailure.emit('Type conversion failed.')
        return False


class QNumpyArray1DModel(QAbstractNumpy1DModel):
    """
    用于PyQt5的Numpy一维array数组模型(竖向)。
    继承QAbstractNumpy1DModel
    """

    def __init__(self, npArray=None, header_Num = False, parent=None):
        """
        构造器。
        可选参数：
            1. npArray: 一维Numpy数组。
            2. parent: 父对象。一般留空即可。
        """
        # 指定方向为竖向
        super(QNumpyArray1DModel, self).__init__(npArray, QtC.Qt.Vertical, header_Num, parent)


class QNumpyArray1Model_Transpose(QAbstractNumpy1DModel):
    """
    用于PyQt5的Numpy一维array数组模型(横向)。
    继承QAbstractNumpy1DModel
    """
    def __init__(self, npArray=None, header_Num = False, parent=None):
        """
        构造器。
        可选参数：
            1. npArray: 一维Numpy数组。
            2. parent: 父对象。一般留空即可。
        """
        # 指定方向为竖向
        super(QNumpyArray1Model_Transpose, self).__init__(npArray, QtC.Qt.Horizontal, header_Num, parent)
