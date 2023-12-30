import sys, os
import PySide2.QtWidgets as QtW
from lib.publicModules import GlobalContainer as GC

from widgets.loginWindow import LoginWindow

if __name__ == '__main__':
    # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AssisstantBoring.settings')
    app = QtW.QApplication(sys.argv)
    GC.loginWindow = LoginWindow()
    GC.loginWindow.show()
    sys.exit(app.exec_())