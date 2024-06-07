# Form implementation generated from reading ui file './qt_app/dialog_camera_source.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(827, 788)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(parent=Dialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.camera_source_list = QtWidgets.QListWidget(parent=Dialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.camera_source_list.setFont(font)
        self.camera_source_list.setObjectName("camera_source_list")
        self.verticalLayout.addWidget(self.camera_source_list)
        self.label_2 = QtWidgets.QLabel(parent=Dialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.preview_cam_img = QtWidgets.QLabel(parent=Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.preview_cam_img.sizePolicy().hasHeightForWidth())
        self.preview_cam_img.setSizePolicy(sizePolicy)
        self.preview_cam_img.setMinimumSize(QtCore.QSize(0, 480))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.preview_cam_img.setFont(font)
        self.preview_cam_img.setFrameShape(QtWidgets.QFrame.Shape.WinPanel)
        self.preview_cam_img.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.preview_cam_img.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.preview_cam_img.setObjectName("preview_cam_img")
        self.verticalLayout.addWidget(self.preview_cam_img)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=Dialog)
        self.buttonBox.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Camera source"))
        self.label.setText(_translate("Dialog", "Camera device port number:"))
        self.label_2.setText(_translate("Dialog", "Preview camera stream"))
        self.preview_cam_img.setText(_translate("Dialog", "Stream"))