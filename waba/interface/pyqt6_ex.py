import sys
from PyQt6 import QtCore, QtWidgets, uic

import qdarktheme

# from interface.qt_modified.modernMain import Ui_MainWindow
#
# class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
#     def __init__(self, *args, **kwargs):
#         super(MainWindow, self).__init__(*args, **kwargs)
#         self.setupUi(self)
QtCore.QDir.addSearchPath('google', '../resources/google')

app = QtWidgets.QApplication(sys.argv)
# app.setStyle("Fusion")
qdarktheme.setup_theme("auto")
# qdarktheme.setup_theme("light")

# window = uic.loadUi("qt_design/main.ui")
window = uic.loadUi("qt_design/modernMain.ui")
# window = MainWindow()
# window.statusBar().showMessage("This is status bar")
window.statusBar().hide()
# window.statusBar().setStyleSheet("background-color : gray")
window.show()
app.exec()
