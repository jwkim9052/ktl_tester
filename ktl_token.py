from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QFileDialog, QTableWidget, QTableWidgetItem, QMessageBox, QStatusBar, QLabel
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtTest import QTest
import sys, os, time, csv

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi("ktl_token.ui", self)
        self.setWindowTitle("글로스 토큰")
        self.resize(800, 600)
        self.show()

        # Define Widgets
        self.open_csv_action = self.findChild(QAction,"actionOpen_csv")
        self.status_bar = self.findChild(QStatusBar,"statusbar")
        self.text_label = self.findChild(QLabel, "label")
        self.text_label.setText("CSV 파일을 선택하세요")
        self.open_csv_action.triggered.connect(self.selectCSVFile)


    def selectCSVFile(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Open File", "", "CSV Files (*.csv);;All Files(*)")
        if fname:
            self.text_label.setText("Working...")
            self.repaint()
            filename = os.path.basename(fname)
            result = self.ai_csv_tester(fname)
            self.text_label.setText(f" {filename} has {result} tokens \n\n (ktl_token_result에서 결과를 확인하세요)")
            #msg = QMessageBox()
            #msg.setWindowTitle("Token")
            #msg.setText(f"It has {result} tokens")
            #x = msg.exec_()

    def ai_csv_tester(self, filename):
        QTest.qWait(3500)
        base_filename = os.path.basename(filename)
        return 758

app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
