import PySide2.QtCore as QtC, PySide2.QtWidgets as QtW
from lib.globalParameters import globalParameters as gParam
import datetime
import requests as rq
import json

__all__ = ['DaemonWidget']


class DaemonWidget(QtW.QWidget):


    def __init__(self, mainWindow = None, parent = None):
        super(DaemonWidget, self).__init__(parent)
        self.mainWindow = mainWindow
        self.daemonWorker = DaemonWorker(self)
        self.daemonWorker.sendText2DaemonWidget.connect(self.addText)
        self.daemonWorker.sendText.connect(self.mainWindow.statusBarShowMessage)
        self.daemonWorker.sendBoringParameter.connect(self.mainWindow.monitor_SubWidget.plotBoringParameter)
        self.daemonWorker.sendMuckInformation.connect(self.mainWindow.monitor_SubWidget.plotMuckInformation)
        self.daemonWorker.sendVibrationInformation.connect(self.mainWindow.monitor_SubWidget.plotVibrationInformation)
        self.daemonWorker.sendRockInformation.connect(self.mainWindow.monitor_SubWidget.plotRockInformation)
        self.checkAliveTimer = QtC.QTimer()
        self.getBoringParameterTimer = QtC.QTimer()
        self.getMuckInformationTimer = QtC.QTimer()
        self.getVibrationInformationTimer = QtC.QTimer()
        self.getRockInformationTimer = QtC.QTimer()
        self.setupUi()

    def setupUi(self):
        self.setObjectName(u"DaemonWidget")
        self.resize(800, 400)
        self.verticalLayout = QtW.QVBoxLayout(self)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.textBrowser = QtW.QTextBrowser(self)
        self.textBrowser.setObjectName(u"textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)

        self.setWindowTitle(QtC.QCoreApplication.translate("DaemonWidget", u"\u540e\u53f0\u76d1\u63a7\u5668", None))

        QtC.QMetaObject.connectSlotsByName(self)

    @QtC.Slot(str)
    def addText(self, text):
        self.textBrowser.setText(self.textBrowser.toPlainText() + '\n' + text)
        self.textBrowser.verticalScrollBar().setValue(self.textBrowser.verticalScrollBar().maximum())

    @QtC.Slot(int)
    def startCheckAlive(self, timeInterval):
        self.checkAliveTimer.timeout.connect(self.daemonWorker.checkAlive)
        self.checkAliveTimer.start(timeInterval)

    @QtC.Slot()
    def stopCheckAlive(self):
        self.checkAliveTimer.stop()
        self.checkAliveTimer.timeout.disconnect(self.daemonWorker.checkAlive)

    @QtC.Slot(int)
    def startGetBoringParameter(self, timeInterval):
        self.getBoringParameterTimer.timeout.connect(self.daemonWorker.getBoringRecord)
        self.getBoringParameterTimer.start(timeInterval)

    @QtC.Slot()
    def stopGetBoringParameter(self):
        self.getBoringParameterTimer.stop()
        self.getBoringParameterTimer.timeout.disconnect(self.daemonWorker.getBoringRecord)

    @QtC.Slot(int)
    def startGetMuckInformation(self, timeInterval):
        self.getMuckInformationTimer.timeout.connect(self.daemonWorker.getMuckInformation)
        self.getMuckInformationTimer.start(timeInterval)

    @QtC.Slot()
    def stopGetMuckInformation(self):
        self.getMuckInformationTimer.stop()
        self.getMuckInformationTimer.timeout.disconnect(self.daemonWorker.getMuckInformation)

    @QtC.Slot(int)
    def startGetVibrationInformation(self, timeInterval):
        self.getVibrationInformationTimer.timeout.connect(self.daemonWorker.getVibrationInformation)
        self.getVibrationInformationTimer.start(timeInterval)

    @QtC.Slot()
    def stopGetVibrationInformation(self):
        self.getVibrationInformationTimer.stop()
        self.getVibrationInformationTimer.timeout.disconnect(self.daemonWorker.getVibrationInformation)

    @QtC.Slot(int)
    def startGetRockInformation(self, timeInterval):
        self.getRockInformationTimer.timeout.connect(self.daemonWorker.getRockInformation)
        self.getRockInformationTimer.start(timeInterval)

    @QtC.Slot()
    def stopGetRockInformation(self):
        self.getRockInformationTimer.stop()
        self.getRockInformationTimer.timeout.disconnect(self.daemonWorker.getRockInformation)


class DaemonWorker(QtC.QObject):
    sendText = QtC.Signal(str, int, int)
    sendText2DaemonWidget = QtC.Signal(str)
    sendBoringParameter = QtC.Signal(dict)
    sendMuckInformation = QtC.Signal(dict)
    sendVibrationInformation = QtC.Signal(dict)
    sendRockInformation = QtC.Signal(dict)
    def __init__(self, daemonWidget = None, parent = None):
        super(DaemonWorker, self).__init__(parent)
        self.daemonWidget = daemonWidget
        self.connectTarget = self.daemonWidget.mainWindow.serverDomain + ':' + self.daemonWidget.mainWindow.serverPort
        self.checkAliveUrl = self.daemonWidget.mainWindow.urlHead + 'api/mon/alive'
        self.boringParameterUrl = self.daemonWidget.mainWindow.urlHead + 'api/mon/get_boring_parameter'
        self.muckInformationUrl = self.daemonWidget.mainWindow.urlHead + 'api/mon/get_muck_information'
        self.vibrationInformationUrl = self.daemonWidget.mainWindow.urlHead + 'api/mon/get_vibration_information'
        self.rockInformationUrl = self.daemonWidget.mainWindow.urlHead + 'api/mon/get_rock_information'
        self.session = rq.Session()
        self.boringParameter_Previous = {
            "record_time": datetime.datetime.now().replace(microsecond=0).isoformat(),
            "propulsion_rate": 0.0,
            "total_thrust": 0.0,
            "RPM": 0.0,
            "torque": 0.0,
            "penetration": 0.0
        }
        self.rockInformation_Previous = {
            "record_time": datetime.datetime.now().replace(microsecond=0).isoformat(),
            "rock_grade": 0,
            "UCS": 0.0,
            "Kv": 0.0
        }

    def checkAlive(self):
        # self.sendText2DaemonWidget.emit('Check connection status at ' + datetime.datetime.now().strftime('%Y-%m-%d::%H:%M:%S'))
        try:
            res = self.session.get(self.checkAliveUrl)
            if res.status_code == 200:
                self.sendText.emit('成功连接至服务器：' + self.connectTarget + '。',
                                   gParam['sb_Tout'], 1)
                # self.sendText2DaemonWidget.emit('Connection is still alive.')
            else:
                self.sendText.emit('尝试连接至' + self.connectTarget + '时发生错误：' + str(res.status_code) + '。', 5000, 1)
                # self.sendText2DaemonWidget.emit('Unknown error occurred when establishing connection.')
        except rq.exceptions.ConnectionError:
            self.sendText.emit('无法连接至服务器：' + self.connectTarget + '。',
                               gParam['sb_Tout'], 1)
            # self.sendText2DaemonWidget.emit('Connection failed.')

    def getBoringRecord(self):
        getTime = datetime.datetime.now().replace(microsecond=0)# - datetime.timedelta(seconds=2)
        # self.sendText2DaemonWidget.emit('Asking for in-time boring parameters.\nCurrent time: '\
        #                                 + getTime.strftime('%Y-%m-%d::%H:%M:%S'))
        try:
            res = self.session.post(self.boringParameterUrl, data = {'time': getTime.isoformat()}) # 发向后端的time为isoformat
            if res.status_code == 200:
                res_Json = res.json()
                if  res_Json['ret'] == 0:
                    parameter = res_Json['boring_Parameter'] # 后端传回的record_time为isoformat
                    # _buf = 'Successfully get boring paramter.\n'
                    # _buf += 'Record time: '\
                    #         + datetime.datetime.fromisoformat(parameter['record_time']).strftime('%Y-%m-%d::%H:%M:%S') + '\n'
                    # _buf += 'Propulsion rate: ' + str(parameter['propulsion_rate']) + '\n'
                    # _buf += 'Total thrust: ' + str(parameter['total_thrust']) + '\n'
                    # _buf += 'Cutterhead RPM: ' + str(parameter['RPM']) + '\n'
                    # _buf += 'Cutterhead torque: ' + str(parameter['torque']) + '\n'
                    # _buf += 'Cutterblade penetration: ' + str(parameter['penetration'])
                    # self.sendText2DaemonWidget.emit(_buf)
                    self.sendBoringParameter.emit(parameter)
                    self.boringParameter_Previous = parameter
                else:
                    self.boringParameter_Previous['record_time'] = getTime.isoformat()
                    self.sendText2DaemonWidget.emit('Failed to get in-time boring parameters.')
                    self.sendBoringParameter.emit(self.boringParameter_Previous)
            else:
                self.sendText2DaemonWidget.emit('Unknown error occurred when establishing connection.')
        except rq.exceptions.ConnectionError:
            self.sendText2DaemonWidget.emit('Connection failed.')
        except Exception as e:
            raise e

    def getMuckInformation(self):
        getTime = datetime.datetime.now().replace(microsecond=0)# - datetime.timedelta(seconds=2)
        # self.sendText2DaemonWidget.emit('Asking for in-time boring parameters.\nCurrent time: '\
        #                                 + getTime.strftime('%Y-%m-%d::%H:%M:%S'))
        try:
            res = self.session.post(self.muckInformationUrl, data = {'time': getTime.isoformat()}) # 发向后端的time为isoformat
            if res.status_code == 200:
                res_Json = res.json()
                if  res_Json['ret'] == 0:
                    parameter = res_Json['muck_Information'] # 后端传回的record_time为isoformat
                    # _buf = 'Successfully get boring paramter.\n'
                    # _buf += 'Record time: '\
                    #         + datetime.datetime.fromisoformat(parameter['record_time']).strftime('%Y-%m-%d::%H:%M:%S') + '\n'
                    # _buf += 'Propulsion rate: ' + str(parameter['propulsion_rate']) + '\n'
                    # _buf += 'Total thrust: ' + str(parameter['total_thrust']) + '\n'
                    # _buf += 'Cutterhead RPM: ' + str(parameter['RPM']) + '\n'
                    # _buf += 'Cutterhead torque: ' + str(parameter['torque']) + '\n'
                    # _buf += 'Cutterblade penetration: ' + str(parameter['penetration'])
                    # self.sendText2DaemonWidget.emit(_buf)
                    self.sendMuckInformation.emit(parameter)
                else:
                    self.sendText2DaemonWidget.emit('Failed to get in-time muck information.')
            else:
                self.sendText2DaemonWidget.emit('Unknown error occurred when establishing connection.')
        except rq.exceptions.ConnectionError:
            self.sendText2DaemonWidget.emit('Connection failed.')
        except Exception as e:
            raise e

    def getVibrationInformation(self):
        getTime = datetime.datetime.now().replace(microsecond=0)# - datetime.timedelta(seconds=2)
        # self.sendText2DaemonWidget.emit('Asking for in-time boring parameters.\nCurrent time: '\
        #                                 + getTime.strftime('%Y-%m-%d::%H:%M:%S'))
        try:
            res = self.session.post(self.vibrationInformationUrl, data = {'time': getTime.isoformat()}) # 发向后端的time为isoformat
            if res.status_code == 200:
                res_Json = res.json()
                if  res_Json['ret'] == 0:
                    parameter = res_Json['vibration_Information'] # 后端传回的record_time为isoformat
                    # _buf = 'Successfully get boring paramter.\n'
                    # _buf += 'Record time: '\
                    #         + datetime.datetime.fromisoformat(parameter['record_time']).strftime('%Y-%m-%d::%H:%M:%S') + '\n'
                    # _buf += 'Propulsion rate: ' + str(parameter['propulsion_rate']) + '\n'
                    # _buf += 'Total thrust: ' + str(parameter['total_thrust']) + '\n'
                    # _buf += 'Cutterhead RPM: ' + str(parameter['RPM']) + '\n'
                    # _buf += 'Cutterhead torque: ' + str(parameter['torque']) + '\n'
                    # _buf += 'Cutterblade penetration: ' + str(parameter['penetration'])
                    # self.sendText2DaemonWidget.emit(_buf)
                    self.sendVibrationInformation.emit(parameter)
                else:
                    self.sendText2DaemonWidget.emit('Failed to get in-time vibration information.')
            else:
                self.sendText2DaemonWidget.emit('Unknown error occurred when establishing connection.')
        except rq.exceptions.ConnectionError:
            self.sendText2DaemonWidget.emit('Connection failed.')
        except Exception as e:
            raise e

    def getRockInformation(self):
        getTime = datetime.datetime.now().replace(microsecond=0)# - datetime.timedelta(seconds=2)
        # self.sendText2DaemonWidget.emit('Asking for in-time boring parameters.\nCurrent time: '\
        #                                 + getTime.strftime('%Y-%m-%d::%H:%M:%S'))
        try:
            res = self.session.post(self.rockInformationUrl, data = {'time': getTime.isoformat()}) # 发向后端的time为isoformat
            if res.status_code == 200:
                res_Json = res.json()
                if  res_Json['ret'] == 0:
                    parameter = res_Json['rock_Information'] # 后端传回的record_time为isoformat
                    # _buf = 'Successfully get boring paramter.\n'
                    # _buf += 'Record time: '\
                    #         + datetime.datetime.fromisoformat(parameter['record_time']).strftime('%Y-%m-%d::%H:%M:%S') + '\n'
                    # _buf += 'Propulsion rate: ' + str(parameter['propulsion_rate']) + '\n'
                    # _buf += 'Total thrust: ' + str(parameter['total_thrust']) + '\n'
                    # _buf += 'Cutterhead RPM: ' + str(parameter['RPM']) + '\n'
                    # _buf += 'Cutterhead torque: ' + str(parameter['torque']) + '\n'
                    # _buf += 'Cutterblade penetration: ' + str(parameter['penetration'])
                    # self.sendText2DaemonWidget.emit(_buf)
                    self.sendRockInformation.emit(parameter)
                    self.rockInformation_Previous = parameter
                else:
                    self.rockInformation_Previous['record_time'] = getTime.isoformat()
                    self.sendText2DaemonWidget.emit('Failed to get in-time rock information.')
                    self.sendRockInformation.emit(self.rockInformation_Previous)
            else:
                self.sendText2DaemonWidget.emit('Unknown error occurred when establishing connection.')
        except rq.exceptions.ConnectionError:
            self.sendText2DaemonWidget.emit('Connection failed.')
        except Exception as e:
            raise e



