# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Ui_LoginWindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from lib.customWidgets.collapseBox import QCollapseBox

import resources_rc

class Ui_LoginWindow(object):
    def setupUi(self, LoginWindow):
        if not LoginWindow.objectName():
            LoginWindow.setObjectName(u"LoginWindow")
        LoginWindow.setWindowModality(Qt.ApplicationModal)
        LoginWindow.resize(400, 357)
        self.verticalLayout = QVBoxLayout(LoginWindow)
        self.verticalLayout.setSpacing(12)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(-1, -1, -1, 0)
        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_7)

        self.label_3 = QLabel(LoginWindow)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(100, 100))
        self.label_3.setMaximumSize(QSize(100, 100))
        self.label_3.setPixmap(QPixmap(u":/resources/bitmap/BJTU.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_5.addWidget(self.label_3)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_8)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.label_4 = QLabel(LoginWindow)
        self.label_4.setObjectName(u"label_4")
        font = QFont()
        font.setFamily(u"\u534e\u6587\u96b6\u4e66")
        font.setPointSize(24)
        self.label_4.setFont(font)
        self.label_4.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_4)

        self.verticalSpacer_2 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_5)

        self.label = QLabel(LoginWindow)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(40, 0))

        self.horizontalLayout.addWidget(self.label)

        self.username_LineEdit = QLineEdit(LoginWindow)
        self.username_LineEdit.setObjectName(u"username_LineEdit")
        self.username_LineEdit.setMinimumSize(QSize(160, 0))

        self.horizontalLayout.addWidget(self.username_LineEdit)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_6)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.label_2 = QLabel(LoginWindow)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(40, 0))

        self.horizontalLayout_2.addWidget(self.label_2)

        self.password_LineEdit = QLineEdit(LoginWindow)
        self.password_LineEdit.setObjectName(u"password_LineEdit")
        self.password_LineEdit.setMinimumSize(QSize(160, 0))
        self.password_LineEdit.setEchoMode(QLineEdit.Password)

        self.horizontalLayout_2.addWidget(self.password_LineEdit)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.login_PushButton = QPushButton(LoginWindow)
        self.login_PushButton.setObjectName(u"login_PushButton")

        self.horizontalLayout_3.addWidget(self.login_PushButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.collapseWidget = QCollapseBox(LoginWindow)
        self.collapseWidget.setObjectName(u"collapseWidget")
        self.collapseWidget.setMinimumSize(QSize(0, 20))

        self.verticalLayout.addWidget(self.collapseWidget)

        self.contentAreaLayout = QVBoxLayout()
        self.contentAreaLayout.setObjectName(u"contentAreaLayout")
        self.contentAreaLayout.setContentsMargins(0, 0, 0, 0)
        self.contentWidget = QWidget(LoginWindow)
        self.contentWidget.setObjectName(u"contentWidget")
        self.horizontalLayout_4 = QHBoxLayout(self.contentWidget)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.domain_Label = QLabel(self.contentWidget)
        self.domain_Label.setObjectName(u"domain_Label")
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.domain_Label.sizePolicy().hasHeightForWidth())
        self.domain_Label.setSizePolicy(sizePolicy)

        self.horizontalLayout_4.addWidget(self.domain_Label)

        self.domain_LineEdit = QLineEdit(self.contentWidget)
        self.domain_LineEdit.setObjectName(u"domain_LineEdit")

        self.horizontalLayout_4.addWidget(self.domain_LineEdit)

        self.port_Label = QLabel(self.contentWidget)
        self.port_Label.setObjectName(u"port_Label")
        sizePolicy.setHeightForWidth(self.port_Label.sizePolicy().hasHeightForWidth())
        self.port_Label.setSizePolicy(sizePolicy)

        self.horizontalLayout_4.addWidget(self.port_Label)

        self.port_LineEdit = QLineEdit(self.contentWidget)
        self.port_LineEdit.setObjectName(u"port_LineEdit")

        self.horizontalLayout_4.addWidget(self.port_LineEdit)

        self.sslCheckBox = QCheckBox(self.contentWidget)
        self.sslCheckBox.setObjectName(u"sslCheckBox")
        self.sslCheckBox.setChecked(False)

        self.horizontalLayout_4.addWidget(self.sslCheckBox)

        self.horizontalLayout_4.setStretch(0, 1)
        self.horizontalLayout_4.setStretch(1, 15)
        self.horizontalLayout_4.setStretch(2, 1)
        self.horizontalLayout_4.setStretch(3, 5)

        self.contentAreaLayout.addWidget(self.contentWidget)


        self.verticalLayout.addLayout(self.contentAreaLayout)


        self.retranslateUi(LoginWindow)

        QMetaObject.connectSlotsByName(LoginWindow)
    # setupUi

    def retranslateUi(self, LoginWindow):
        LoginWindow.setWindowTitle(QCoreApplication.translate("LoginWindow", u"\u767b\u5f55", None))
        self.label_3.setText("")
        self.label_4.setText(QCoreApplication.translate("LoginWindow", u"TBM\u667a\u80fd\u8f85\u52a9\u6398\u8fdb\u7cfb\u7edf", None))
        self.label.setText(QCoreApplication.translate("LoginWindow", u"\u7528\u6237\u540d", None))
        self.label_2.setText(QCoreApplication.translate("LoginWindow", u"\u5bc6  \u7801", None))
        self.login_PushButton.setText(QCoreApplication.translate("LoginWindow", u"\u767b\u5f55", None))
        self.domain_Label.setText(QCoreApplication.translate("LoginWindow", u"\u57df", None))
        self.domain_LineEdit.setText(QCoreApplication.translate("LoginWindow", u"127.0.0.1", None))
        self.port_Label.setText(QCoreApplication.translate("LoginWindow", u"\u7aef\u53e3", None))
        self.port_LineEdit.setText(QCoreApplication.translate("LoginWindow", u"80", None))
        self.sslCheckBox.setText(QCoreApplication.translate("LoginWindow", u"SSL", None))
    # retranslateUi

