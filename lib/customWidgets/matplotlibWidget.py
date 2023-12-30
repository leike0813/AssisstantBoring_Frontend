import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import PySide2.QtWidgets as QtW, PySide2.QtCore as QtC
from ..customUtilities.customExceptions import ArgumentError

__all__ = ['QMatplotlibWidget']


class MyMplCanvas(FigureCanvas):
    """
    用于PyQt5的Matplotlib画布。
    FigureCanvas的最终的父类其实是QWidget。
    """

    def __init__(self, parent=None, width=5, height=4, dpi=100):

        # 配置中文显示
        plt.rcParams['font.family'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        # plt.ion()  # 打开交互式绘图

        self.fig = Figure(figsize=(width, height), dpi=dpi)  # 新建一个figure
        # self.axes = self.fig.add_subplot(111)  # 建立一个子图，如果要建立复合图，可以在这里修改

        # self.axes.hold(False)  # 每次绘图的时候不保留上一次绘图的结果

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        '''定义FigureCanvas的尺寸策略，这部分的意思是设置FigureCanvas，使之尽可能的向外填充空间。'''
        FigureCanvas.setSizePolicy(self,
                                   QtW.QSizePolicy.Expanding,
                                   QtW.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

class QMatplotlibWidget(QtW.QWidget):
    """
    用于PyQt5的Matplotlib窗体。
    """
    def __init__(self, parent=None, ntb_on = False):
        super(QMatplotlibWidget, self).__init__(parent)
        self.initUi(ntb_on)

    def initUi(self, ntb_on):
        self.layout = QtW.QVBoxLayout(self)
        self.matplotlibCanvas = MyMplCanvas(self, width=5, height=4, dpi=100)
        self.axesList = []
        self.fig = self.matplotlibCanvas.fig
        self.add_subplot = self.matplotlibCanvas.fig.add_subplot
        self.draw = self.matplotlibCanvas.draw
        self.navigationToolbar = NavigationToolbar(self.matplotlibCanvas, self)  # 添加完整的 toolbar
        self.layout.addWidget(self.matplotlibCanvas)
        self.layout.setContentsMargins(0, 0, 0, 0)
        if ntb_on:
            self.layout.addWidget(self.navigationToolbar)

    def clear(self):
        self.matplotlibCanvas.fig.clf()
        self.axesList.clear()

    def plotLine(self, axesindex, *args, **kwargs):
        obj = self.axesList[axesindex].plot(*args, **kwargs)
        return obj

    def plotBar(self, axesindex, *args, **kwargs):
        obj = self.axesList[axesindex].bar(*args, **kwargs)
        return obj

    def plotScatter(self, axesindex, *args, **kwargs):
        obj = self.axesList[axesindex].scatter(*args, **kwargs)
        return obj

    def plotStack(self, axesindex, *args, **kwargs):
        obj = self.axesList[axesindex].stackplot(*args, **kwargs)
        return obj

    def plotBarH(self, axesindex, *args, **kwargs):
        obj = self.axesList[axesindex].barh(*args, **kwargs)
        return obj

    def plotFillBetweenX(self, axesindex, *args, **kwargs):
        obj = self.axesList[axesindex].fill_betweenx(*args, **kwargs)
        return obj

    def plotSpan(self, axesindex, orientation, *args, **kwargs):
        if orientation == 'horizontal' or orientation == 'h' or orientation == QtC.Qt.Horizontal:
            obj = self.axesList[axesindex].axhspan(*args, **kwargs)
        elif orientation == 'vertical' or orientation == 'v' or orientation == QtC.Qt.Vertical:
            obj = self.axesList[axesindex].axvspan(*args, **kwargs)
        else:
            raise ArgumentError(orientation)
        return obj

    def plotSurface(self, axesindex, *args, **kwargs):
        obj = self.axesList[axesindex].plot_surface(*args, **kwargs)
        return obj