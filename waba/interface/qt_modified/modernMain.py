# Form implementation generated from reading ui file './interface/qt_design/modernMain.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from importlib.resources import path
from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(455, 379)
        MainWindow.setMinimumSize(QtCore.QSize(455, 0))
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.toolButton = QtWidgets.QToolButton(parent=self.centralwidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./interface/qt_design\\../../resources/google/settings_FILL0_wght200_GRAD0_opsz48.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.toolButton.setIcon(icon)
        self.toolButton.setIconSize(QtCore.QSize(32, 32))
        self.toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout_2.addWidget(self.toolButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.toolButton_5 = QtWidgets.QToolButton(parent=self.centralwidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("./interface/qt_design\\../../resources/google/display_settings_FILL0_wght200_GRAD0_opsz48.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.toolButton_5.setIcon(icon1)
        self.toolButton_5.setIconSize(QtCore.QSize(32, 32))
        self.toolButton_5.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.toolButton_5.setObjectName("toolButton_5")
        self.horizontalLayout_2.addWidget(self.toolButton_5)
        self.toolButton_9 = QtWidgets.QToolButton(parent=self.centralwidget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("./interface/qt_design\\../../resources/google/delete_FILL0_wght200_GRAD0_opsz48.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.toolButton_9.setIcon(icon2)
        self.toolButton_9.setIconSize(QtCore.QSize(32, 32))
        self.toolButton_9.setPopupMode(QtWidgets.QToolButton.ToolButtonPopupMode.MenuButtonPopup)
        self.toolButton_9.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.toolButton_9.setObjectName("toolButton_9")
        self.horizontalLayout_2.addWidget(self.toolButton_9)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.scrollArea = QtWidgets.QScrollArea(parent=self.centralwidget)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.Shape.Box)
        self.scrollArea.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 422, 520))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.groupBox_3 = QtWidgets.QGroupBox(parent=self.scrollAreaWidgetContents_2)
        self.groupBox_3.setCheckable(True)
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_3.setContentsMargins(6, 6, 6, 6)
        self.horizontalLayout_3.setSpacing(2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.frame_4 = QtWidgets.QFrame(parent=self.groupBox_3)
        self.frame_4.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.frame_4)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("./interface/qt_design\\../../resources/google/chronic_FILL0_wght200_GRAD0_opsz48.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButton_2.setIcon(icon3)
        self.pushButton_2.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_3.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(parent=self.frame_4)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_3.addWidget(self.pushButton)
        self.horizontalLayout_3.addWidget(self.frame_4)
        self.frame_5 = QtWidgets.QFrame(parent=self.groupBox_3)
        self.frame_5.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_5.setObjectName("frame_5")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_5)
        self.verticalLayout_4.setSpacing(2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.toolButton_3 = QtWidgets.QToolButton(parent=self.frame_5)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("./interface/qt_design\\../../resources/google/open_in_new_FILL0_wght200_GRAD0_opsz48.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.toolButton_3.setIcon(icon4)
        self.toolButton_3.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.toolButton_3.setAutoRaise(True)
        self.toolButton_3.setObjectName("toolButton_3")
        self.verticalLayout_4.addWidget(self.toolButton_3, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.progressBar = QtWidgets.QProgressBar(parent=self.frame_5)
        self.progressBar.setProperty("value", 15)
        self.progressBar.setTextVisible(False)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_4.addWidget(self.progressBar)
        self.horizontalLayout_3.addWidget(self.frame_5)
        self.frame_6 = QtWidgets.QFrame(parent=self.groupBox_3)
        self.frame_6.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_6.setObjectName("frame_6")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_6)
        self.verticalLayout_5.setSpacing(2)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.pushButton_4 = QtWidgets.QPushButton(parent=self.frame_6)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("./interface/qt_design\\../../resources/google/photo_camera_FILL0_wght200_GRAD0_opsz48.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButton_4.setIcon(icon5)
        self.pushButton_4.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_4.setCheckable(False)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout_5.addWidget(self.pushButton_4)
        self.pushButton_3 = QtWidgets.QPushButton(parent=self.frame_6)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("./interface/qt_design\\../../resources/google/monitor_FILL0_wght200_GRAD0_opsz48.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButton_3.setIcon(icon6)
        self.pushButton_3.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_5.addWidget(self.pushButton_3)
        self.horizontalLayout_3.addWidget(self.frame_6)
        self.verticalLayout_9.addWidget(self.groupBox_3)
        self.groupBox_7 = QtWidgets.QGroupBox(parent=self.scrollAreaWidgetContents_2)
        self.groupBox_7.setCheckable(True)
        self.groupBox_7.setObjectName("groupBox_7")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBox_7)
        self.horizontalLayout_4.setContentsMargins(6, 6, 6, 6)
        self.horizontalLayout_4.setSpacing(2)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.frame_8 = QtWidgets.QFrame(parent=self.groupBox_7)
        self.frame_8.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_8.setObjectName("frame_8")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frame_8)
        self.verticalLayout_6.setSpacing(2)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.pushButton_5 = QtWidgets.QPushButton(parent=self.frame_8)
        self.pushButton_5.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("./interface/qt_design\\../../resources/google/sensors_FILL0_wght200_GRAD0_opsz48.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButton_5.setIcon(icon7)
        self.pushButton_5.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_5.setObjectName("pushButton_5")
        self.verticalLayout_6.addWidget(self.pushButton_5)
        self.pushButton_6 = QtWidgets.QPushButton(parent=self.frame_8)
        self.pushButton_6.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("./interface/qt_design\\../../resources/google/fast_forward_FILL0_wght200_GRAD0_opsz48.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButton_6.setIcon(icon8)
        self.pushButton_6.setIconSize(QtCore.QSize(16, 16))
        self.pushButton_6.setObjectName("pushButton_6")
        self.verticalLayout_6.addWidget(self.pushButton_6)
        self.horizontalLayout_4.addWidget(self.frame_8)
        self.frame_9 = QtWidgets.QFrame(parent=self.groupBox_7)
        self.frame_9.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_9.setObjectName("frame_9")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.frame_9)
        self.verticalLayout_7.setSpacing(2)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.toolButton_4 = QtWidgets.QToolButton(parent=self.frame_9)
        self.toolButton_4.setIcon(icon4)
        self.toolButton_4.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.toolButton_4.setAutoRaise(True)
        self.toolButton_4.setObjectName("toolButton_4")
        self.verticalLayout_7.addWidget(self.toolButton_4, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.progressBar_2 = QtWidgets.QProgressBar(parent=self.frame_9)
        self.progressBar_2.setProperty("value", 75)
        self.progressBar_2.setTextVisible(False)
        self.progressBar_2.setInvertedAppearance(False)
        self.progressBar_2.setObjectName("progressBar_2")
        self.verticalLayout_7.addWidget(self.progressBar_2)
        self.toolButton_8 = QtWidgets.QToolButton(parent=self.frame_9)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("./interface/qt_design\\../../resources/google/data_info_alert_FILL0_wght200_GRAD0_opsz48.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.toolButton_8.setIcon(icon9)
        self.toolButton_8.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.toolButton_8.setAutoRaise(True)
        self.toolButton_8.setObjectName("toolButton_8")
        self.verticalLayout_7.addWidget(self.toolButton_8, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.horizontalLayout_4.addWidget(self.frame_9)
        self.frame_10 = QtWidgets.QFrame(parent=self.groupBox_7)
        self.frame_10.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_10.setObjectName("frame_10")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.frame_10)
        self.verticalLayout_8.setSpacing(2)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.pushButton_7 = QtWidgets.QPushButton(parent=self.frame_10)
        self.pushButton_7.setText("")
        self.pushButton_7.setIcon(icon5)
        self.pushButton_7.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_7.setObjectName("pushButton_7")
        self.verticalLayout_8.addWidget(self.pushButton_7)
        self.pushButton_8 = QtWidgets.QPushButton(parent=self.frame_10)
        self.pushButton_8.setText("")
        self.pushButton_8.setIcon(icon6)
        self.pushButton_8.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_8.setObjectName("pushButton_8")
        self.verticalLayout_8.addWidget(self.pushButton_8)
        self.horizontalLayout_4.addWidget(self.frame_10)
        self.verticalLayout_9.addWidget(self.groupBox_7)
        self.groupBox_8 = QtWidgets.QGroupBox(parent=self.scrollAreaWidgetContents_2)
        self.groupBox_8.setCheckable(True)
        self.groupBox_8.setChecked(False)
        self.groupBox_8.setObjectName("groupBox_8")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.groupBox_8)
        self.horizontalLayout_6.setContentsMargins(6, 6, 6, 6)
        self.horizontalLayout_6.setSpacing(2)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.frame_11 = QtWidgets.QFrame(parent=self.groupBox_8)
        self.frame_11.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frame_11.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_11.setObjectName("frame_11")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.frame_11)
        self.verticalLayout_10.setSpacing(2)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.pushButton_10 = QtWidgets.QPushButton(parent=self.frame_11)
        self.pushButton_10.setIcon(icon3)
        self.pushButton_10.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_10.setObjectName("pushButton_10")
        self.verticalLayout_10.addWidget(self.pushButton_10)
        self.pushButton_11 = QtWidgets.QPushButton(parent=self.frame_11)
        self.pushButton_11.setObjectName("pushButton_11")
        self.verticalLayout_10.addWidget(self.pushButton_11)
        self.horizontalLayout_6.addWidget(self.frame_11)
        self.frame_12 = QtWidgets.QFrame(parent=self.groupBox_8)
        self.frame_12.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frame_12.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_12.setObjectName("frame_12")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.frame_12)
        self.verticalLayout_11.setSpacing(2)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.toolButton_6 = QtWidgets.QToolButton(parent=self.frame_12)
        self.toolButton_6.setIcon(icon4)
        self.toolButton_6.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.toolButton_6.setAutoRaise(True)
        self.toolButton_6.setObjectName("toolButton_6")
        self.verticalLayout_11.addWidget(self.toolButton_6, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.progressBar_3 = QtWidgets.QProgressBar(parent=self.frame_12)
        self.progressBar_3.setProperty("value", 0)
        self.progressBar_3.setTextVisible(False)
        self.progressBar_3.setInvertedAppearance(False)
        self.progressBar_3.setObjectName("progressBar_3")
        self.verticalLayout_11.addWidget(self.progressBar_3)
        self.horizontalLayout_6.addWidget(self.frame_12)
        self.frame_13 = QtWidgets.QFrame(parent=self.groupBox_8)
        self.frame_13.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frame_13.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_13.setObjectName("frame_13")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.frame_13)
        self.verticalLayout_12.setSpacing(2)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.pushButton_12 = QtWidgets.QPushButton(parent=self.frame_13)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("./interface/qt_design\\../../resources/google/sensors_off_FILL0_wght200_GRAD0_opsz48.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButton_12.setIcon(icon10)
        self.pushButton_12.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_12.setObjectName("pushButton_12")
        self.verticalLayout_12.addWidget(self.pushButton_12)
        self.pushButton_13 = QtWidgets.QPushButton(parent=self.frame_13)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("./interface/qt_design\\../../resources/google/desktop_access_disabled_FILL0_wght200_GRAD0_opsz48.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButton_13.setIcon(icon11)
        self.pushButton_13.setIconSize(QtCore.QSize(32, 32))
        self.pushButton_13.setObjectName("pushButton_13")
        self.verticalLayout_12.addWidget(self.pushButton_13)
        self.horizontalLayout_6.addWidget(self.frame_13)
        self.verticalLayout_9.addWidget(self.groupBox_8)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(16, 24, 16, 24)
        self.gridLayout.setObjectName("gridLayout")
        self.toolButton_10 = QtWidgets.QToolButton(parent=self.scrollAreaWidgetContents_2)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap("./interface/qt_design\\../../resources/google/new_window_FILL0_wght200_GRAD0_opsz48.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.toolButton_10.setIcon(icon12)
        self.toolButton_10.setIconSize(QtCore.QSize(24, 24))
        self.toolButton_10.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.toolButton_10.setObjectName("toolButton_10")
        self.gridLayout.addWidget(self.toolButton_10, 0, 0, 1, 1)
        self.verticalLayout_9.addLayout(self.gridLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_9.addItem(spacerItem1)
        self.label = QtWidgets.QLabel(parent=self.scrollAreaWidgetContents_2)
        self.label.setEnabled(False)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_9.addWidget(self.label)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout_2.addWidget(self.scrollArea)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.pushButton_9 = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_9.setObjectName("pushButton_9")
        self.horizontalLayout_5.addWidget(self.pushButton_9)
        self.toolButton_2 = QtWidgets.QToolButton(parent=self.centralwidget)
        self.toolButton_2.setObjectName("toolButton_2")
        self.horizontalLayout_5.addWidget(self.toolButton_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 455, 21))
        self.menubar.setDefaultUp(False)
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.toolButton.setText(_translate("MainWindow", "Settings"))
        self.toolButton_5.setText(_translate("MainWindow", "Calibration"))
        self.toolButton_9.setText(_translate("MainWindow", "Delete..."))
        self.groupBox_3.setTitle(_translate("MainWindow", "Instruction 1"))
        self.pushButton_2.setText(_translate("MainWindow", "Trigger"))
        self.pushButton.setText(_translate("MainWindow", "On"))
        self.toolButton_3.setText(_translate("MainWindow", "Wating 20 sec..."))
        self.pushButton_4.setText(_translate("MainWindow", "Sensor"))
        self.pushButton_3.setText(_translate("MainWindow", "Displays"))
        self.groupBox_7.setTitle(_translate("MainWindow", "Instruction 2"))
        self.toolButton_4.setText(_translate("MainWindow", "Capture..."))
        self.toolButton_8.setText(_translate("MainWindow", "Linked to display\'s combination"))
        self.groupBox_8.setTitle(_translate("MainWindow", "Instruction 3"))
        self.pushButton_10.setText(_translate("MainWindow", "Trigger"))
        self.pushButton_11.setText(_translate("MainWindow", "On"))
        self.toolButton_6.setText(_translate("MainWindow", "Not active"))
        self.pushButton_12.setText(_translate("MainWindow", "Sensor"))
        self.pushButton_13.setText(_translate("MainWindow", "Displays"))
        self.toolButton_10.setText(_translate("MainWindow", "Add new instruction"))
        self.label.setText(_translate("MainWindow", "- Strange Dog Workshop -"))
        self.pushButton_9.setText(_translate("MainWindow", "PushButton"))
        self.toolButton_2.setText(_translate("MainWindow", "..."))

