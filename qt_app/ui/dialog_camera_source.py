# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_camera_source.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.WindowModal)
        Dialog.resize(827, 788)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setLayoutDirection(Qt.LeftToRight)

        self.verticalLayout.addWidget(self.label)

        self.camera_source_list = QListWidget(Dialog)
        self.camera_source_list.setObjectName(u"camera_source_list")
        self.camera_source_list.setFont(font)
        self.camera_source_list.setStyleSheet(u"background-color: rgb(135, 135, 135);\n"
"color: rgb(239, 239, 239);")

        self.verticalLayout.addWidget(self.camera_source_list)

        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.verticalLayout.addWidget(self.label_2)

        self.preview_cam_img = QLabel(Dialog)
        self.preview_cam_img.setObjectName(u"preview_cam_img")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.preview_cam_img.sizePolicy().hasHeightForWidth())
        self.preview_cam_img.setSizePolicy(sizePolicy)
        self.preview_cam_img.setMinimumSize(QSize(0, 480))
        self.preview_cam_img.setFont(font)
        self.preview_cam_img.setFrameShape(QFrame.WinPanel)
        self.preview_cam_img.setFrameShadow(QFrame.Sunken)
        self.preview_cam_img.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.preview_cam_img)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setLayoutDirection(Qt.LeftToRight)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Camera source", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Camera device port number:", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Preview camera stream", None))
        self.preview_cam_img.setText(QCoreApplication.translate("Dialog", u"Stream", None))
    # retranslateUi

