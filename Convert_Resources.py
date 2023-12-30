import os
import os.path

dir = './'


def listQrcFile():
    list = []
    files = os.listdir(dir)
    for filename in files:
        if os.path.splitext(filename)[1] == '.qrc':
            list.append(filename)

    return list


def transPyFile(filename):
    return os.path.splitext(filename)[0] + '_rc.py'


def runMain():
    list = listQrcFile()
    for qrcfile in list:
        pyfile = transPyFile(qrcfile)
        cmd = 'pyside2-rcc -o {pyfile} {qrcfile}'.format(pyfile=pyfile, qrcfile=qrcfile)
        os.system(cmd)


if __name__ == "__main__":
    runMain()