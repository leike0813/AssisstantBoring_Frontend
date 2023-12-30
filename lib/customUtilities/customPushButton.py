import PySide2.QtCore as QtC, PySide2.QtWidgets as QtW


class CustomPushButton(QtW.QPushButton):
    """
    自定义按钮控件。
    可指定其从属的主窗体及一个相关对象。
    """
    pressed_Mod = QtC.Signal(QtC.QObject, object)  # 按钮按下信号，将主窗体及相关对象作为参数发送。

    def __init__(self, mainWindow, _object, *args, **kwargs):
        """
        构造器。
        必要参数：
            1.mainWindow: 按钮从属的主窗体，必须是PyQt5.QtWidgets.QWidget对象。
            2._object: 与按钮相关的任意对象。
        可选参数：
            1.*args, **kwargs       原始的QPushButton的构造参数。
        """
        super(CustomPushButton, self).__init__(*args, **kwargs)
        self.mainwindow = mainWindow
        self.object = _object

        self.pressed.connect(self.onButtonPressed)

    def onButtonPressed(self):
        """
        按钮按下时调用的槽函数。
        发送pressed_Mod信号。
        """
        self.pressed_Mod.emit(self.mainwindow, self.object)