import PySide2.QtCore as QtC
from ..customUtilities.customExceptions import *
from ..customUtilities.customFunctions import *
import numpy as np
import pandas as pd


class QDataFrameModel(QtC.QAbstractTableModel):
    """
    用于PyQt5的Pandas.DataFrame数据模型。
    """
    editConfirmed = QtC.Signal()  # 确认编辑的信号。
    editRefuted = QtC.Signal()  # 撤销编辑的信号。
    operationFailure = QtC.Signal(str)
    def __init__(self, dataFrame=None, parent=None):
        """
        构造器。
        可选参数：
            1. dataFrame: Pandas.DataFrame对象。
            2. parent: 父对象。一般留空即可。
        """
        super(QDataFrameModel, self).__init__(parent)
        if type(dataFrame) is type(
                None):  # 若指定了dataframe参数，则将dataframe赋予dataframe_orig参数；否则将一个空DataFrame赋予dataframe_orig参数
            self.setDataFrame(pd.DataFrame())
        else:
            self.setDataFrame(dataFrame)
        self.__displayDecimal = None # 默认保留小数点后2位
        self.__editable = True # 默认可编辑！
        # self.editConfirmed.connect(self.cacheDataFrame)
        self.editRefuted.connect(self.cacheDataFrame)

    def isEditable(self):
        return self.__editable

    def setEditable(self, editable):
        if type(editable) is not bool:
            raise TypeError("Only accept boolean variable as input.")
        self.__editable = editable

    @property
    def displayDecimal(self):
        return self.__displayDecimal

    def setDisplayDecimal(self, displayDecimal):
        if type(displayDecimal) is not int:
            raise TypeError("Only accept integer as input.")
        elif displayDecimal < 0:
            raise ValueError("Decimal place must be non-negative.")
        self.__displayDecimal = displayDecimal

    def cacheDataFrame(self):
        """
        生成dataframe_orig的一个缓存副本dataframe，用于界面编辑。
        dataframe_orig为实际外部传入的DataFrame对象。对dataframe_orig的改变会直接反应在外部，而副本dataframe则不会。
        注意：此方法可能会导致layout的改变，请在layoutAboutToBeChanged信号发出后调用，并在调用后发出layoutChanged信号。
        """
        # if self.dataFrame_Orig.shape[0] > 0 and self.dataFrame_Orig.shape[1] > 0:
        # 缓存shape
        QDataFrameModel.clearDataFrameAndReshape(self.dataFrame, self.dataFrame_Orig.shape)
        # 缓存数据
        for j in range(self.dataFrame_Orig.shape[1]):
            for i in range(self.dataFrame_Orig.shape[0]):
                self.dataFrame.iat[i, j] = self.dataFrame_Orig.iat[i, j]
        # 缓存列标题
        self.dataFrame.rename(columns={self.dataFrame.columns[k]:
                                           self.dataFrame_Orig.columns[k] for k in range(self.dataFrame_Orig.shape[1])},
                              inplace=True)
        # infer_Dtypes = self.dataFrame.infer_objects().dtypes # 推测dataFrame中每一列的dtype
        # 列数据类型转换
        for j in range(self.dataFrame_Orig.shape[1]):
            self.dataFrame[self.dataFrame.columns[j]] =\
                self.dataFrame[self.dataFrame.columns[j]].astype(self.dataFrame_Orig.dtypes.iat[j])
        if self.dataFrame_Orig.shape[0] > 0 and self.dataFrame_Orig.shape[1] > 0:
            self.dataChanged.emit(
                self.index(0, 0),
                self.index(self.dataFrame_Orig.shape[0] - 1, self.dataFrame_Orig.shape[1] - 1)
            )

    def setDataFrame(self, dataFrame):
        """
        设置数据模型对应的DataFrame对象。
        """
        if not isinstance(dataFrame, pd.DataFrame):
            raise TypeError("The input argument must be a pandas.DataFrame object.")

        self.layoutAboutToBeChanged.emit()
        self.dataFrame_Orig = dataFrame
        # self.columnTypes_Orig = [type(dataFrame.columns[i]) for i in range(dataFrame.shape[1])]
        self.dataFrame = pd.DataFrame(np.empty((dataFrame.shape[0], dataFrame.shape[1])), index=dataFrame.index)
        self.cacheDataFrame()
        self.layoutChanged.emit()

    def setDataFrameFromFile(self, filename, filetype, **kwargs):
        """
        从文件中读取数据，存入模型的DataFrame对象。
        这一操作会改变模型内外的连接关系，请注意。
        该方法会返回新的外部连接对象。
        可通过额外的关键字参数设置导入选项，这些参数会直接传入对应文件类型的读取API（CSV对应pandas.read_csv，XLS对应pandas.read_excel）
        """
        self.layoutAboutToBeChanged.emit()
        if filetype == 'CSV':
            self.dataFrame_Orig = pd.read_csv(filename, **kwargs)
        elif filetype == 'XLS':
            self.dataFrame_Orig = pd.read_excel(filename, engine='xlrd', **kwargs)
        elif filetype == 'XLSX':
            self.dataFrame_Orig = pd.read_excel(filename, engine='openpyxl', **kwargs)
        # self.columnTypes_Orig = [type(self.dataFrame_Orig.columns[i]) for i in range(self.dataFrame_Orig.shape[1])]
        self.dataFrame = pd.DataFrame(np.empty((self.dataFrame_Orig.shape[0], self.dataFrame_Orig.shape[1])))
        self.cacheDataFrame()
        self.layoutChanged.emit()
        return self.dataFrame_Orig

    def readDataFrameFromFile(self, filename, filetype, **kwargs):
        """
        从文件中读取数据，存入模型的缓存DataFrame对象。
        可通过额外的关键字参数设置导入选项，这些参数会直接传入对应文件类型的读取API（CSV对应pandas.read_csv，XLS对应pandas.read_excel）
        """
        self.layoutAboutToBeChanged.emit()
        if filetype == 'CSV':
            self.dataFrame = pd.read_csv(filename, **kwargs)
        elif filetype == 'XLS':
            self.dataFrame = pd.read_excel(filename, engine='xlrd', **kwargs)
        elif filetype == 'XLSX':
            self.dataFrame = pd.read_excel(filename, engine='openpyxl', **kwargs)
        # QDataFrameModel.clearDataFrameAndReshape(self.dataFrame_Orig,
        #                                          (self.dataFrame.shape[0], self.dataFrame.shape[1]))
        self.layoutChanged.emit()

    @staticmethod
    def clearDataFrameAndReshape(dataFrame, shape):
        """
        静态方法。
        清除dataFrame中所有数据，并将dataFrame改为指定的shape。
        不改变dataFrame对象的连接关系。
        """
        dataFrame.drop(range(dataFrame.shape[0]), inplace=True)
        dataFrame.drop(dataFrame.columns, axis=1, inplace=True)
        for i in range(shape[1]):
            dataFrame.insert(i, i, [])
        for j in range(shape[0]):
            dataFrame.loc[j] = [np.nan for i in range(shape[1])]
        dataFrame.reset_index(inplace=True, drop=True)

    def dtype(self, column):
        return self.dataFrame.dtypes.iat[column]

    @property
    def rank(self):
        return min(self.dataFrame_Orig.shape)

    def confirmEdit(self):
        """
        确认编辑时调用的槽函数。
        将缓存对象dataframe中的数据写入dataframe_orig，确认编辑。
        """
        if self.dataFrame.shape[0] > 0 and self.dataFrame.shape[1] > 0:
            # 写入shape
            QDataFrameModel.clearDataFrameAndReshape(self.dataFrame_Orig, self.dataFrame.shape)
            # 写数据
            for j in range(self.dataFrame.shape[1]):
                for i in range(self.dataFrame.shape[0]):
                    self.dataFrame_Orig.iat[i, j] = self.dataFrame.iat[i, j]
            # 写入列标题
            self.dataFrame_Orig.rename(columns={self.dataFrame_Orig.columns[k]:
                                                    self.dataFrame.columns[k] for k in range(self.dataFrame.shape[1])},
                                       inplace=True)
            # 列数据类型转换
            for j in range(self.dataFrame.shape[1]):
                self.dataFrame_Orig[self.dataFrame_Orig.columns[j]] =\
                    self.dataFrame_Orig[self.dataFrame_Orig.columns[j]].astype(self.dataFrame.dtypes.iat[j])
            # self.columnTypes_Orig = [type(self.dataFrame.columns[i]) for i in range(self.dataFrame.shape[1])]
            self.editConfirmed.emit()

    def refuteEdit(self):
        """
        撤销编辑时调用的槽函数。
        """
        self.layoutAboutToBeChanged.emit()
        self.editRefuted.emit()
        self.layoutChanged.emit()
        self.headerDataChanged.emit(QtC.Qt.Horizontal, 0, self.columnCount() - 1)


    def index(self, row, column, parent=QtC.QModelIndex()):
        """
        PyQt5数据模型必须重写的关键函数。
        返回模型索引对象(Index)。
        """
        return self.createIndex(row, column, self.dataFrame.iat[row, column])

    def rowCount(self, parent=QtC.QModelIndex()):
        """
        PyQt5数据模型必须重写的关键函数。
        返回模型的行数。
        """
        return self.dataFrame.shape[0]

    def columnCount(self, parent=QtC.QModelIndex()):
        """
        PyQt5数据模型必须重写的关键函数。
        返回模型的列数。
        """
        return self.dataFrame.shape[1]

    def data(self, index, role=QtC.Qt.DisplayRole):
        """
        PyQt5数据模型必须重写的关键函数。
        返回在指定的Role下的模型数据。
        其中DisplayRole为视图(View)中显示的数据；EditRole为传给编辑器的数据；TextAlignmentRole为数据显示时的对齐方式。
        """
        if not index.isValid() or \
                not 0 <= index.row() < self.dataFrame.shape[0] or \
                not 0 <= index.column() < self.dataFrame.shape[1]:
            return None

        if role == QtC.Qt.DisplayRole or role == QtC.Qt.EditRole:
            try:
                if not self.__displayDecimal:
                    return str(round(self.dataFrame.iat[index.row(), index.column()], 2)) # 默认保留小数点后2位
                else:
                    return str(round(self.dataFrame.iat[index.row(), index.column()], self.__displayDecimal))
            except TypeError:
                return str(self.dataFrame.iat[index.row(), index.column()])
        elif role == QtC.Qt.TextAlignmentRole:
            return QtC.Qt.AlignHCenter | QtC.Qt.AlignVCenter
        else:
            return None

    def flags(self, index):
        """
        PyQt5数据模型必须重写的关键函数。
        返回指定索引对应的flag。
        为使模型数据可在视图中编辑，需要额外返回ItemIsEditable这一flag。
        """
        flag = super(QDataFrameModel, self).flags(index)
        return flag | QtC.Qt.ItemIsEditable if self.__editable else flag

    def setData(self, index, value, role=QtC.Qt.EditRole):
        """
        PyQt5可编辑数据模型必须重写的关键函数。
        将编辑器传入的值写入缓存对象dataframe。
        """
        if pd.api.types.is_integer_dtype(self.dtype(index.column())):
            value_dtype, ok = str2int(value)
        elif pd.api.types.is_float_dtype(self.dtype(index.column())):
            value_dtype, ok = str2float(value)
        elif pd.api.types.is_bool_dtype(self.dtype(index.column())):
            value_dtype, ok = str2bool(value)
        elif pd.api.types.is_string_dtype(self.dtype(index.column())) == str:
            value_dtype, ok = value, True
        elif pd.api.types.is_object_dtype(self.dtype(index.column())) == object:
            value_dtype, ok = value, False
        else:
            value_dtype, ok = value, False
        if ok:
            self.dataFrame.iat[index.row(), index.column()] = value_dtype
            self.dataChanged.emit(index, index)
            return True
        self.operationFailure.emit('Type conversion failed.')
        return False

    def headerData(self, section, orientation, role=QtC.Qt.DisplayRole):
        """
        PyQt5数据模型必须重写的关键函数。
        返回表头信息。
        格式类似data()函数。
        """
        hdata = super(QDataFrameModel, self).headerData(section, orientation, role)
        if role == QtC.Qt.DisplayRole or role == QtC.Qt.EditRole:
            if orientation == QtC.Qt.Horizontal:
                return str(self.dataFrame.columns[section])
            elif orientation == QtC.Qt.Vertical:
                return str(self.dataFrame.index[section])
        elif role == QtC.Qt.TextAlignmentRole:
            return QtC.Qt.AlignHCenter | QtC.Qt.AlignVCenter
        else:
            return hdata

    def setHeaderData(self, section, orientation, value, role=QtC.Qt.EditRole):
        """
        PyQt5可编辑数据模型必须重写的关键函数。
        将编辑器传入的值写入dataframe的columns列表中。
        格式类似setData()函数。
        未完工。
        """
        if orientation == QtC.Qt.Horizontal:
            self.dataFrame.columns[section] = str(value)
            self.headerDataChanged.emit(orientation, section, section)
            return True
        self.operationFailure.emit('Can only set the horizontal header.')
        return False

    def addDataFrameRows(self, rowIndex = -1, count=1):
        """
        向dataframe中增加数行。
        可选参数：
            1. count: 增加的行数，默认为1。
        """
        if rowIndex == -1:
            position = self.rowCount()
        else:
            position = rowIndex
        if count < 1:
            self.operationFailure.emit('The number of rows to be added is less than 1.')
            return False

        if len(self.dataFrame.columns) == 0:
            self.operationFailure.emit('Cannot add rows to an dataframe with no columns.')
            return False

        self.beginInsertRows(QtC.QModelIndex(), position, position + count - 1)
        orig_Dtypes = self.dataFrame.dtypes
        defaultValues = []
        for dtype in orig_Dtypes:
            if pd.api.types.is_integer_dtype(dtype):
                val = 0
            elif pd.api.types.is_float_dtype(dtype):
                val = 0.0
            elif pd.api.types.is_bool_dtype(dtype):
                val = False
            elif pd.api.types.is_String_dtype(dtype):
                val = ''
            else:
                val = dtype.type()
            defaultValues.append(val)  # 根据每列不同的数据类型设置不同的初始值。
        if position != self.rowCount():
            for i in range(self.rowCount() - 1, position - 1, -1):
                self.dataFrame.loc[i + count] = self.dataFrame.loc[i]
        for i in range(count):
            self.dataFrame.loc[position + i] = defaultValues
        for j in range(self.dataFrame.shape[1]):
            self.dataFrame[self.dataFrame.columns[j]] = \
                self.dataFrame[self.dataFrame.columns[j]].astype(orig_Dtypes.iat[j])
        self.dataFrame.reset_index(inplace=True, drop=True)  # DataFrame中插入数据后必须执行的函数
        self.endInsertRows()
        return True

    def addDataFrameColumn(self, columnName, position = -1, dtype=float, defaultValue=None):
        """
        向dataframe中插入一列。
        必要参数：
            1. columnName: 列名称。
        可选参数：
            1. dtype: 该列的数据类型，默认为浮点型。
            2. defaultValue: 该列数据的初始值，默认为None。
        """
        elements = self.rowCount()
        if position == -1:
            columnPosition = self.columnCount()  # 默认插入在最右侧
        else:
            columnPosition = position
        newColumn = pd.Series([defaultValue] * elements, index=self.dataFrame.index, dtype=dtype)  # 生成一个Series，随后插入

        self.beginInsertColumns(QtC.QModelIndex(), columnPosition - 1, columnPosition - 1)
        try:
            self.dataFrame.insert(columnPosition, columnName, newColumn, allow_duplicates=False)
        except ValueError as e:
            self.operationFailure.emit('Column name does already exist.')
            return False
        self.endInsertColumns()
        return True

    def removeDataFrameRows(self, rows):
        """
        从dataframe中移除数行。
        必要参数：
            1. rows: 由需要移除的行索引号组成的列表
        """
        if rows:
            position = min(rows)
            count = len(rows)
            self.beginRemoveRows(QtC.QModelIndex(), position, position + count - 1)
            removedAny = False
            for idx, line in self.dataFrame.iterrows():
                if idx in rows:
                    removedAny = True
                    self.dataFrame.drop(idx, inplace=True)

            if not removedAny:
                self.operationFailure.emit('Failed to remove rows.')
                return False

            self.dataFrame.reset_index(inplace=True, drop=True)
            self.endRemoveRows()
            return True
        self.operationFailure.emit('The list of rows to be removed is empty.')
        return False

    def removeDataFrameColumns(self, columns):
        """
        从dataframe中移除数列。
        必要参数：
            1. columns: 由需要移除的列的(索引号, 列名称)元组组成的列表。
        """
        if columns:
            deleted = 0
            errored = False
            for (position, name) in columns:
                position = position - deleted
                if position < 0:
                    position = 0
                self.beginRemoveColumns(QtC.QModelIndex(), position, position)
                try:
                    self.dataFrame.drop(name, axis=1, inplace=True)
                except ValueError as e:
                    errored = True
                    continue
                self.endRemoveColumns()
                deleted += 1
            if self.columnCount() > 0:
                # self.dataChanged.emit(self.index(0, position - 1 if position == self.columnCount() else position),
                #                       self.index(self.rowCount() - 1,
                #                                  self.columnCount() - 1 if position + deleted > self.columnCount()\
                #                                      else position + deleted - 1))
                pass
            else:
                self.removeDataFrameRows(range(self.rowCount()))
                # self.dataChanged.emit(QtC.QModelIndex(), QtC.QModelIndex())

            if errored:
                self.operationFailure.emit('Unknown error has occurred when removing some column(s).')
                return False
            else:
                return True
        self.operationFailure.emit('The list of columns to be removed is empty.')
        return False