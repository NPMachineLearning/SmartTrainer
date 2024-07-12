# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGroupBox,
    QHBoxLayout, QLabel, QLayout, QListWidget,
    QListWidgetItem, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QStatusBar, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.WindowModal)
        MainWindow.resize(1066, 866)
        font = QFont()
        font.setBold(False)
        font.setStrikeOut(False)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet(u"")
        self.action_open_video = QAction(MainWindow)
        self.action_open_video.setObjectName(u"action_open_video")
        font1 = QFont()
        font1.setPointSize(14)
        self.action_open_video.setFont(font1)
        self.action_camera_source = QAction(MainWindow)
        self.action_camera_source.setObjectName(u"action_camera_source")
        self.action_camera_source.setFont(font1)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setStyleSheet(u"")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.img_frame = QLabel(self.centralwidget)
        self.img_frame.setObjectName(u"img_frame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.img_frame.sizePolicy().hasHeightForWidth())
        self.img_frame.setSizePolicy(sizePolicy1)
        font2 = QFont()
        font2.setPointSize(14)
        font2.setBold(True)
        self.img_frame.setFont(font2)
        self.img_frame.setFrameShape(QFrame.Panel)
        self.img_frame.setFrameShadow(QFrame.Sunken)
        self.img_frame.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.img_frame)

        self.controller_layout = QHBoxLayout()
        self.controller_layout.setObjectName(u"controller_layout")
        self.controller_layout.setContentsMargins(0, -1, 0, -1)
        self.controller_left_layout = QFrame(self.centralwidget)
        self.controller_left_layout.setObjectName(u"controller_left_layout")
        self.controller_left_layout.setStyleSheet(u"background-color: rgb(170, 255, 127);")
        self.verticalLayout = QVBoxLayout(self.controller_left_layout)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.controller_left_layout)
        self.label.setObjectName(u"label")
        self.label.setFont(font2)
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.exercise_list = QListWidget(self.controller_left_layout)
        self.exercise_list.setObjectName(u"exercise_list")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.exercise_list.sizePolicy().hasHeightForWidth())
        self.exercise_list.setSizePolicy(sizePolicy2)
        self.exercise_list.setFont(font2)
        self.exercise_list.setStyleSheet(u"background-color: rgb(135, 135, 135);\n"
"color: rgb(239, 239, 239);")
        self.exercise_list.setFrameShape(QFrame.Panel)

        self.verticalLayout.addWidget(self.exercise_list)

        self.current_exercise_label = QLabel(self.controller_left_layout)
        self.current_exercise_label.setObjectName(u"current_exercise_label")
        font3 = QFont()
        font3.setPointSize(12)
        font3.setBold(True)
        self.current_exercise_label.setFont(font3)
        self.current_exercise_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.current_exercise_label)


        self.controller_layout.addWidget(self.controller_left_layout)

        self.controller_mid_layout = QFrame(self.centralwidget)
        self.controller_mid_layout.setObjectName(u"controller_mid_layout")
        self.controller_mid_layout.setStyleSheet(u"background-color: rgb(255, 170, 127);")
        self.verticalLayout_3 = QVBoxLayout(self.controller_mid_layout)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.label_3 = QLabel(self.controller_mid_layout)
        self.label_3.setObjectName(u"label_3")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy3)
        self.label_3.setFont(font2)
        self.label_3.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_3)

        self.groupBox = QGroupBox(self.controller_mid_layout)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setFont(font3)
        self.groupBox.setStyleSheet(u"")
        self.groupBox.setFlat(False)
        self.groupBox.setCheckable(False)
        self.verticalLayout_4 = QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.draw_skeleton_checkbox = QCheckBox(self.groupBox)
        self.draw_skeleton_checkbox.setObjectName(u"draw_skeleton_checkbox")
        palette = QPalette()
        brush = QBrush(QColor(255, 170, 127, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush)
        palette.setBrush(QPalette.Active, QPalette.Base, brush)
        palette.setBrush(QPalette.Active, QPalette.Window, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush)
        self.draw_skeleton_checkbox.setPalette(palette)
        font4 = QFont()
        font4.setPointSize(12)
        font4.setBold(True)
        font4.setKerning(True)
        self.draw_skeleton_checkbox.setFont(font4)
        self.draw_skeleton_checkbox.setAutoFillBackground(False)
        self.draw_skeleton_checkbox.setStyleSheet(u"")
        self.draw_skeleton_checkbox.setIconSize(QSize(20, 20))
        self.draw_skeleton_checkbox.setChecked(False)

        self.verticalLayout_4.addWidget(self.draw_skeleton_checkbox)


        self.verticalLayout_3.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.controller_mid_layout)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setFont(font3)
        self.verticalLayout_6 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, -1, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(7)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.start_button = QPushButton(self.groupBox_2)
        self.start_button.setObjectName(u"start_button")
        sizePolicy3.setHeightForWidth(self.start_button.sizePolicy().hasHeightForWidth())
        self.start_button.setSizePolicy(sizePolicy3)
        self.start_button.setFont(font2)
        self.start_button.setStyleSheet(u"background-color: rgb(85, 170, 255);")
        self.start_button.setFlat(False)

        self.horizontalLayout.addWidget(self.start_button)

        self.pause_button = QPushButton(self.groupBox_2)
        self.pause_button.setObjectName(u"pause_button")
        sizePolicy3.setHeightForWidth(self.pause_button.sizePolicy().hasHeightForWidth())
        self.pause_button.setSizePolicy(sizePolicy3)
        self.pause_button.setFont(font2)
        self.pause_button.setStyleSheet(u"background-color: rgb(85, 170, 255);")

        self.horizontalLayout.addWidget(self.pause_button)


        self.verticalLayout_6.addLayout(self.horizontalLayout)


        self.verticalLayout_3.addWidget(self.groupBox_2)


        self.controller_layout.addWidget(self.controller_mid_layout)

        self.controller_right_layout = QFrame(self.centralwidget)
        self.controller_right_layout.setObjectName(u"controller_right_layout")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.controller_right_layout.sizePolicy().hasHeightForWidth())
        self.controller_right_layout.setSizePolicy(sizePolicy4)
        self.controller_right_layout.setStyleSheet(u"background-color: rgb(85, 255, 255);")
        self.controller_right_layout.setFrameShape(QFrame.StyledPanel)
        self.controller_right_layout.setFrameShadow(QFrame.Sunken)
        self.verticalLayout_5 = QVBoxLayout(self.controller_right_layout)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_2 = QLabel(self.controller_right_layout)
        self.label_2.setObjectName(u"label_2")
        sizePolicy3.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy3)
        self.label_2.setFont(font2)
        self.label_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.label_2)

        self.rep_count_label = QLabel(self.controller_right_layout)
        self.rep_count_label.setObjectName(u"rep_count_label")
        sizePolicy4.setHeightForWidth(self.rep_count_label.sizePolicy().hasHeightForWidth())
        self.rep_count_label.setSizePolicy(sizePolicy4)
        font5 = QFont()
        font5.setPointSize(36)
        font5.setBold(True)
        self.rep_count_label.setFont(font5)
        self.rep_count_label.setFrameShape(QFrame.NoFrame)
        self.rep_count_label.setFrameShadow(QFrame.Plain)
        self.rep_count_label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.rep_count_label)


        self.controller_layout.addWidget(self.controller_right_layout)


        self.verticalLayout_2.addLayout(self.controller_layout)

        self.plotLayout = QVBoxLayout()
        self.plotLayout.setSpacing(7)
        self.plotLayout.setObjectName(u"plotLayout")
        self.plotLayout.setContentsMargins(-1, -1, -1, 1)

        self.verticalLayout_2.addLayout(self.plotLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1066, 37))
        font6 = QFont()
        font6.setPointSize(14)
        font6.setBold(True)
        font6.setItalic(False)
        font6.setUnderline(False)
        self.menubar.setFont(font6)
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        font7 = QFont()
        font7.setFamilies([u"Segoe UI"])
        font7.setPointSize(9)
        font7.setBold(False)
        self.menuFile.setFont(font7)
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.action_open_video)
        self.menuFile.addAction(self.action_camera_source)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Exercise Repetition Counter", None))
        self.action_open_video.setText(QCoreApplication.translate("MainWindow", u"Video clip", None))
        self.action_camera_source.setText(QCoreApplication.translate("MainWindow", u"Camera", None))
        self.img_frame.setText(QCoreApplication.translate("MainWindow", u"No video source", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Select exercise", None))
        self.current_exercise_label.setText("")
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Control panel", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Setting", None))
        self.draw_skeleton_checkbox.setText(QCoreApplication.translate("MainWindow", u"Draw skeleton", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Video", None))
        self.start_button.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.pause_button.setText(QCoreApplication.translate("MainWindow", u"Pause", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Repetition", None))
        self.rep_count_label.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"&Video Source", None))
    # retranslateUi

