import os
import PySide2.QtCore as QtC, PySide2.QtWidgets as QtW
import qtawesome as qta
import pandas as pd

from ..customModels.pandasTableModel import QDataFrameModel
from ..customModels.customDelegates import *

__all__ = ['QDataSheetWidget']


class QDataSheetWidget(QtW.QWidget):
    """
    监测数据编辑窗体。
    是对采用QDataFrameModel作为数据模型的QTableView的完善。
    没有对应的界面文件。一般用于其他窗体中的一个子窗体。
    """
    dataFrameChanged = QtC.Signal()

    def __init__(self, parent = None):
        """
        构造器。
        可选参数：
            1. parent            父对象。
        """
        super(QDataSheetWidget, self).__init__(parent)
        self.__iconSize = QtC.QSize(24, 24)
        self.__newcolumncount = 1
        self.__workFolder = None
        self.__delegates = {}
        self.delegates_Solid = {}
        self.setupUi()
        self.setOperatingAuthorization()

    def setupUi(self):
        """
        初始化窗体界面，创建必要的按钮。
        """
        self.gridLayout = QtW.QGridLayout(self)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        self.buttonFrame = QtW.QFrame(self)  # 按钮区域
        self.buttonFrame.setFrameShape(QtW.QFrame.NoFrame)
        spacerItemButton = QtW.QSpacerItem(40, 20, QtW.QSizePolicy.Expanding, QtW.QSizePolicy.Minimum)

        self.buttonFrameLayout = QtW.QGridLayout(self.buttonFrame)
        self.buttonFrameLayout.setContentsMargins(0, 0, 0, 0)

        self.loadDataButton = QtW.QToolButton(self.buttonFrame)  # 读取数据按钮
        self.loadDataButton.setObjectName('loadDataButton')
        self.loadDataButton.setIcon(qta.icon('mdi6.folder-open', color='deepskyblue'))
        self.loadDataButton.setText(self.tr('load'))
        self.loadDataButton.setToolTip(self.tr('load data'))

        self.clearDataButton = QtW.QToolButton(self.buttonFrame)  # 清空数据按钮
        self.clearDataButton.setObjectName('clearDataButton')
        self.clearDataButton.setIcon(qta.icon('mdi6.eraser', color='deepskyblue'))
        self.clearDataButton.setText(self.tr('clear'))
        self.clearDataButton.setToolTip(self.tr('clear data'))
        self.clearDataButton.setEnabled(False)

        self.editDataButton = QtW.QToolButton(self.buttonFrame)  # 编辑数据按钮
        self.editDataButton.setObjectName('editDataButton')
        self.editDataButton.setIcon(qta.icon('mdi6.file-document-edit', color='deepskyblue'))
        self.editDataButton.setText(self.tr('edit'))
        self.editDataButton.setToolTip(self.tr('edit data'))

        self.addColumnButton = QtW.QToolButton(self.buttonFrame)  # 新增列按钮
        self.addColumnButton.setObjectName('addColumnButton')
        self.addColumnButton.setIcon(qta.icon('mdi6.arrow-collapse-right', color='deepskyblue'))
        self.addColumnButton.setText(self.tr('+col'))
        self.addColumnButton.setToolTip(self.tr('add new column'))
        self.addColumnButton.setEnabled(False)

        self.addRowButton = QtW.QToolButton(self.buttonFrame)  # 新增行按钮
        self.addRowButton.setObjectName('addRowButton')
        self.addRowButton.setIcon(qta.icon('mdi6.arrow-collapse-down', color='deepskyblue'))
        self.addRowButton.setText(self.tr('+row'))
        self.addRowButton.setToolTip(self.tr('add new row'))
        self.addRowButton.setEnabled(False)

        self.removeColumnButton = QtW.QToolButton(self.buttonFrame)  # 删除列按钮
        self.removeColumnButton.setObjectName('removeColumnButton')
        self.removeColumnButton.setIcon(qta.icon('mdi6.arrow-expand-right', color='deepskyblue'))
        self.removeColumnButton.setText(self.tr('-col'))
        self.removeColumnButton.setToolTip(self.tr('remove a column'))
        self.removeColumnButton.setEnabled(False)

        self.removeRowButton = QtW.QToolButton(self.buttonFrame)  # 删除行按钮
        self.removeRowButton.setObjectName('removeRowButton')
        self.removeRowButton.setIcon(qta.icon('mdi6.arrow-expand-down', color='deepskyblue'))
        self.removeRowButton.setText(self.tr('-row'))
        self.removeRowButton.setToolTip(self.tr('remove selected rows'))
        self.removeRowButton.setEnabled(False)

        self.confirmButton = QtW.QToolButton(self.buttonFrame)  # 确认编辑按钮
        self.confirmButton.setObjectName('confirmButton')
        self.confirmButton.setIcon(qta.icon('mdi6.check-circle', color='green'))
        self.confirmButton.setText(self.tr('confirm'))
        self.confirmButton.setToolTip(self.tr('confirm edit'))
        self.confirmButton.setEnabled(False)

        self.refuteButton = QtW.QToolButton(self.buttonFrame)  # 撤销编辑按钮
        self.refuteButton.setObjectName('refuteButton')
        self.refuteButton.setIcon(qta.icon('mdi6.close-circle', color='red'))
        self.refuteButton.setText(self.tr('refute'))
        self.refuteButton.setToolTip(self.tr('refute edit'))
        self.refuteButton.setEnabled(False)

        self.buttons = [self.loadDataButton, self.editDataButton, self.clearDataButton,
                        self.addColumnButton, self.addRowButton,
                        self.removeColumnButton, self.removeRowButton,
                        self.confirmButton, self.refuteButton]

        for index, button in enumerate(self.buttons):
            button.setMinimumSize(self.__iconSize)
            button.setMaximumSize(self.__iconSize)
            button.setIconSize(self.__iconSize)
            button.setCheckable(True)
            self.buttonFrameLayout.addWidget(button, 0, index, 1, 1)
        self.buttonFrameLayout.addItem(spacerItemButton, 0, index +1, 1, 1)

        self.tableView = QtW.QTableView(self)  # tableView窗体
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSortingEnabled(False)
        self.tableView.horizontalHeader().setSectionResizeMode(QtW.QHeaderView.Stretch)
        self.tableView.horizontalHeader().setMinimumSectionSize(50)
        self.tableView.verticalHeader().setSectionResizeMode(QtW.QHeaderView.Fixed)
        self.tableView.verticalHeader().setDefaultSectionSize(20)
        self.tableView.verticalHeader().setSectionsMovable(False)

        self.gridLayout.addWidget(self.buttonFrame, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.tableView, 1, 0, 1, 1)

        QtC.QMetaObject.connectSlotsByName(self)

    def setOperatingAuthorization(
            self,
            allowLoad = True,
            allowEdit = True,
            allowColumnManipulation = True,
            allowRowManipulation = True
    ):
        self.__allowLoad = allowLoad
        self.__allowEdit = allowEdit
        self.__allowColumnManipulation = allowColumnManipulation
        self.__allowRowManipulation = allowRowManipulation
        self.loadDataButton.setEnabled(self.__allowLoad)
        self.editDataButton.setEnabled(self.editDataButton.isEnabled() and self.__allowEdit)
        self.clearDataButton.setEnabled(self.clearDataButton.isEnabled() and self.__allowEdit)
        self.addColumnButton.setEnabled(self.addColumnButton.isEnabled() and self.__allowColumnManipulation)
        self.addRowButton.setEnabled(self.addRowButton.isEnabled() and self.__allowRowManipulation)
        self.removeColumnButton.setEnabled(self.removeColumnButton.isEnabled() and self.__allowColumnManipulation)
        self.removeRowButton.setEnabled(self.removeRowButton.isEnabled() and self.__allowRowManipulation)
        self.confirmButton.setEnabled(self.confirmButton.isEnabled() and self.__allowEdit)
        self.refuteButton.setEnabled(self.refuteButton.isEnabled() and self.__allowEdit)

    def onDataChanged(self):
        if not self.editDataButton.isChecked():
            self.dataFrameChanged.emit()

    def onModelChanged(self):
        self.addColumnButton.setEnabled(self.tableView.model().isEditable() and self.__allowColumnManipulation)
        self.addRowButton.setEnabled(self.tableView.model().isEditable() and self.__allowRowManipulation)
        self.removeColumnButton.setEnabled(self.tableView.model().isEditable() and self.__allowColumnManipulation)
        self.removeRowButton.setEnabled(self.tableView.model().isEditable() and self.__allowRowManipulation)
        self.confirmButton.setEnabled(self.tableView.model().isEditable() and self.__allowEdit)
        self.refuteButton.setEnabled(self.tableView.model().isEditable() and self.__allowEdit)
        self.clearDataButton.setEnabled(self.tableView.model().isEditable() and self.__allowEdit)

    def setDelegates(self):
        if self.tableView.model():
            for i in range(self.tableView.model().dataFrame.shape[1]):
                if i in self.delegates_Solid.keys():
                    self.tableView.setItemDelegateForColumn(i, self.delegates_Solid[i])
                else:
                    if pd.api.types.is_integer_dtype(self.tableView.model().dataFrame.dtypes.iat[i]):
                        self.__delegates[i] = QSpinboxDelegate(singleStep=1, parent=self.tableView)
                        self.tableView.setItemDelegateForColumn(i, self.__delegates[i])
                    elif pd.api.types.is_float_dtype(self.tableView.model().dataFrame.dtypes.iat[i]):
                        self.__delegates[i] = QDoubleSpinboxDelegate(decimalPlace=2, singleStep=0.1, parent=self.tableView)
                        self.tableView.setItemDelegateForColumn(i, self.__delegates[i])

    def setModel(self, model):
        """
        为tableView控件设定数据模型。
        等价于table.setModel()
        """
        if isinstance(model, QDataFrameModel):
            self.tableView.setModel(model)
            self.tableView.model().dataChanged.connect(self.onDataChanged)
            if model.isEditable():
                self.editDataButton.setChecked(True)
                self.editDataButton.toggled.emit(True)
            # self.setDelegates()
            self.onModelChanged()
        else:
            raise TypeError("The input argument must be a QDataFrameModel object.")

    @QtC.Slot(bool)
    def on_loadDataButton_toggled(self, triggered):
        """
        为tableView控件的数据模型读取数据。
        """
        if triggered:
            model = self.tableView.model()
            if not model:
                temp_Model = QDataFrameModel()
                temp_Model.setEditable(False)
                self.setModel(temp_Model)
            filename, filetype =\
                QtW.QFileDialog.getOpenFileName(self, '打开数据文件',
                                                os.getcwd() if self.__workFolder == None else self.__workFolder,
                                    "Microsoft Excel Spreedsheets (*.xls, *.xlsx);;Comma Separated Values (*.csv)")
            if filetype == 'Comma Separated Values (*.csv)':
                self.tableView.model().readDataFrameFromFile(filename, 'CSV')
            elif filetype == 'Microsoft Excel Spreedsheets (*.xls, *.xlsx)':
                if os.path.splitext(filename)[1] == '.xls':
                    self.tableView.model().readDataFrameFromFile(filename, 'XLS')
                else:
                    self.tableView.model().readDataFrameFromFile(filename, 'XLSX')
            self.setDelegates()
            if not self.editDataButton.isChecked():
                self.tableView.model().confirmEdit()  # 改动直接反映至DataFrameModel中的原始DataFrame中，此句可根据实际需要调整
            self.dataFrameChanged.emit()
            self.sender().setChecked(False)

    @QtC.Slot(bool)
    def on_clearDataButton_toggled(self, triggered):
        if triggered:
            model = self.tableView.model()
            if model is not None:
                self.tableView.model().layoutAboutToBeChanged.emit()
                QDataFrameModel.clearDataFrameAndReshape(self.tableView.model().dataFrame, (0, 0))
                self.tableView.model().layoutChanged.emit()
                # self.tableView.model().confirmEdit()#改动直接反映至DataFrameModel中的原始DataFrame中，此句可根据实际需要调整
                # self.dataFrameChanged.emit()
            self.sender().setChecked(False)

    @QtC.Slot(bool)
    def on_editDataButton_toggled(self, triggered):
        model = self.tableView.model()
        if not model:
            temp_Model = QDataFrameModel()
            temp_Model.setEditable(False)
            self.setModel(temp_Model)
        if triggered:
            self.tableView.model().setEditable(True)
            self.editDataButton.setEnabled(False and self.__allowEdit)
            self.editDataButton.setIcon(qta.icon('mdi6.file-document-edit', color='darkblue'))
            self.setDelegates()
        else:
            self.tableView.model().setEditable(False)
            self.editDataButton.setEnabled(True and self.__allowEdit)
            self.editDataButton.setIcon(qta.icon('mdi6.file-document-edit', color='deepskyblue'))
            # self.tableView.model().confirmEdit()  # 改动直接反映至DataFrameModel中的原始DataFrame中，此句可根据实际需要调整
            # self.dataFrameChanged.emit()
        self.onModelChanged()


    @QtC.Slot()
    def uncheckButton(self):
        """
        Removes the checked stated of all buttons in this widget.
        This method is also a slot.
        """
        for button in self.buttons:
            if button.isChecked():
                button.setChecked(False)

    @QtC.Slot(bool)
    def on_addColumnButton_toggled(self, triggered):
        """
        Adds a column with the given parameters to the underlying model
        This method is also a slot.
        If no model is set, nothing happens.

        Args:
            triggered (bool): If the corresponding button was
                activated, the row will be appended to the end.
        """
        if triggered:
            model = self.tableView.model()
            if model is not None:
                selection = self.tableView.selectedIndexes()
                if len(selection) == 0:
                    position = -1
                else:
                    position = min([ind.column() for ind in selection])
                status = model.addDataFrameColumn('New Column' + str(self.__newcolumncount), position, float, 0.0)
                if status:
                    self.tableView.setItemDelegateForColumn(model.columnCount() - 1,
                                                            QDoubleSpinboxDelegate(singleStep = 0.1,
                                                                                   parent = self.tableView))
                    self.__newcolumncount += 1
                    self.onDataChanged()
            self.sender().setChecked(False)


    @QtC.Slot(bool)
    def on_addRowButton_toggled(self, triggered):
        """
        Adds a row to the model.
        This method is also a slot.
        If no model is set, nothing happens.

        Args:
            triggered (bool): If the corresponding button was
                activated, the row will be appended to the end.
        """
        if triggered:
            model = self.tableView.model()
            if model is not None:
                selection = self.tableView.selectedIndexes()
                if len(selection) == 0:
                    position = -1
                else:
                    position = min([ind.row() for ind in selection])
                status = model.addDataFrameRows(rowIndex = position)
                if status:
                    self.onDataChanged()
            self.sender().setChecked(False)

    @QtC.Slot(bool)
    def on_removeRowButton_toggled(self, triggered):
        """
        Removes one or multiple rows from the model.
        This method is also a slot.

        Args:
            triggered (bool): If the corresponding button was
                activated, the selected rows will be removed
                from the model.
        """
        if triggered:
            model = self.tableView.model()
            if model is not None:
                selection = self.tableView.selectedIndexes()
                rows = [index.row() for index in selection]
                status = model.removeDataFrameRows(set(rows))
                if status:
                    self.onDataChanged()
            self.sender().setChecked(False)

    @QtC.Slot(bool)
    def on_removeColumnButton_toggled(self, triggered):
        """
        Removes one or multiple columns from the model.
        This method is also a slot.

        Args:
            triggered (bool): If the corresponding button was
                activated, the selected columns will be removed
                from the model.
        """
        if triggered:
            model = self.tableView.model()
            if model is not None:
                selection = self.tableView.selectedIndexes()

                columnNames = [(index.column(),
                                model.dataFrame.columns[index.column()]) for index in selection]
                status = model.removeDataFrameColumns(set(columnNames))
                if status:
                    self.onDataChanged()
            self.sender().setChecked(False)

    @QtC.Slot(bool)
    def on_confirmButton_toggled(self, triggered):
        if triggered:
            self.editDataButton.setChecked(False)
            # self.editDataButton.toggled.emit(False)
            self.tableView.model().confirmEdit()
            self.dataFrameChanged.emit()
            self.confirmButton.setChecked(False)

    @QtC.Slot(bool)
    def on_refuteButton_toggled(self, triggered):
        if triggered:
            self.editDataButton.setChecked(False)
            # self.editDataButton.toggled.emit(False)
            self.tableView.model().refuteEdit()
            self.refuteButton.setChecked(False)
