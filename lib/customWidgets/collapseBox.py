import PySide2.QtCore as QtC, PySide2.QtWidgets as QtW


class QCollapseBox(QtW.QWidget):
    """
    自定义Qt5折叠菜单控件
    初始化参数：
            title:标题（显示在折叠按钮旁边）
            parent:父对象
    """
    def __init__(self, parent=None):
        super(QCollapseBox, self).__init__(parent)
        # toggle_Button为折叠开关
        self.toggleButtonLayout = QtW.QHBoxLayout()
        self.toggleButtonLayout.setObjectName(u"toggleButtonLayout")
        self.toggleButtonLayout.setContentsMargins(-1, -1, -1, 0)
        self.toggle_Button = QtW.QToolButton(checkable=True, checked=False)
        self.toggle_Button.setStyleSheet("QToolButton { border: none; }")
        self.toggle_Button.setToolButtonStyle(QtC.Qt.ToolButtonTextBesideIcon)
        self.toggle_Button.setArrowType(QtC.Qt.RightArrow)
        self.line = QtW.QFrame(self)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QtW.QFrame.HLine)
        self.line.setFrameShadow(QtW.QFrame.Sunken)
        self.toggleButtonLayout.addWidget(self.toggle_Button)
        self.toggleButtonLayout.addWidget(self.line)
        # 折叠动画定义
        self.toggle_Animation = QtC.QParallelAnimationGroup(self)
        # content_Area为实际折叠区域，存放内容
        self.content_Area = QtW.QScrollArea(maximumHeight=0, minimumHeight=0)
        self.content_Area.setSizePolicy(QtW.QSizePolicy.Expanding, QtW.QSizePolicy.Fixed)
        self.content_Area.setFrameShape(QtW.QFrame.NoFrame)
        # lay为控件整体布局
        lay = QtW.QVBoxLayout(self)
        lay.setSpacing(0)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addLayout(self.toggleButtonLayout)
        # lay.addWidget(self.toggle_Button)
        lay.addWidget(self.content_Area)

        self.toggle_Animation.addAnimation(QtC.QPropertyAnimation(self, b"minimumHeight"))
        self.toggle_Animation.addAnimation(QtC.QPropertyAnimation(self, b"maximumHeight"))
        self.toggle_Animation.addAnimation(QtC.QPropertyAnimation(self.content_Area, b"maximumHeight"))

        self.toggle_Button.pressed.connect(self.on_toggle_Button_pressed)

    @QtC.Slot()
    def on_toggle_Button_pressed(self):
        checked = self.toggle_Button.isChecked()
        self.toggle_Button.setArrowType(QtC.Qt.DownArrow if not checked \
                                            else QtC.Qt.RightArrow)
        self.toggle_Animation.setDirection(QtC.QAbstractAnimation.Forward if not checked \
                                               else QtC.QAbstractAnimation.Backward)
        self.toggle_Animation.start()

    def setContentLayout(self, layout):
        """
        设置内容区的布局
        创建折叠控件实例后调用此函数将布局赋予折叠区
        """
        # 获取折叠区的布局，并刷新
        lay = self.content_Area.layout()
        del lay
        self.content_Area.setLayout(layout)
        collapsed_Height = (self.sizeHint().height() - self.content_Area.maximumHeight())# 减去内容区的高度
        content_Height = layout.sizeHint().height()
        # 设定整个控件高度
        for i in range(self.toggle_Animation.animationCount() - 1):
            animation = self.toggle_Animation.animationAt(i)
            animation.setDuration(200)
            animation.setStartValue(collapsed_Height)
            animation.setEndValue(collapsed_Height + content_Height)
        # 设定折叠区的高度
        content_Animation = self.toggle_Animation.animationAt(self.toggle_Animation.animationCount() - 1)
        content_Animation.setDuration(200)
        content_Animation.setStartValue(0)
        content_Animation.setEndValue(content_Height)