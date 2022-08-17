from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QFileDialog, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys, os
import time

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi("ktl_ui.ui", self)
        self.show()

        # Define Widgets
        self.video_action = self.findChild(QAction,"actionVideo_tester")
        self.gloss_action = self.findChild(QAction,"actionGloss_tester")
        self.table_widget = self.findChild(QTableWidget, "tableWidget")
        #self.table_widget.setRowCount(3)
        #self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(('Filename','Ref','HYP','WER','Total time','SLT time'))

        #self.video_action.triggered.connect(lambda: self.clicked("video action"))
        #self.gloss_action.triggered.connect(lambda: self.clicked("gloss action"))
        self.video_action.triggered.connect(self.selectVideoFiles)
        self.gloss_action.triggered.connect(self.selectCSVFile)

    def clicked(self, text):
        print(text)

    def selectCSVFile(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Open File", "", "CSV Files (*.csv);;All Files(*)")
        if fname:
            self.table_widget.setRowCount(0)
            result = self.ai_csv_tester(fname)
            msg = QMessageBox()
            msg.setWindowTitle("Token")
            msg.setText(f"It has {result} tokens")
            x = msg.exec_()


    def selectVideoFiles(self):
        fnames, _ = QFileDialog.getOpenFileNames(self, "Open File", "", "MP4 Files (*.mp4);;All Files(*)")
        if fnames:
            self.table_widget.setRowCount(0)
            numFiles = len(fnames)
            msg = QMessageBox()
            msg.setWindowTitle("Selected Files")
            msg.setText(f"{numFiles} file(s) have been selected!")
            x = msg.exec_()

            for fname in fnames:
                # AI Video Tester
                # Input parameter has full path and filename
                # output is a list ['filename', ref, HYP, WER, inference time, slt time]
                result = self.ai_video_tester(fname)
                # The end of AI Video Tester

                rowCount = self.table_widget.rowCount()
                self.table_widget.insertRow(rowCount)
                self.table_widget.setItem(rowCount, 0, QTableWidgetItem(str(result[0])))
                self.table_widget.setItem(rowCount, 1, QTableWidgetItem(str(result[1])))
                self.table_widget.setItem(rowCount, 2, QTableWidgetItem(str(result[2])))
                self.table_widget.setItem(rowCount, 3, QTableWidgetItem(str(result[3])))
                self.table_widget.setItem(rowCount, 4, QTableWidgetItem(str(result[4])))
                self.table_widget.setItem(rowCount, 5, QTableWidgetItem(str(result[5])))

    # this is an example function.
    def ai_video_tester(self, filename):
        time.sleep(0.5)
        base_filename = os.path.basename(filename)
        return_list = [base_filename, "2.5", "2.3", "4.5", "7.2", "3.2"]
        return return_list

    def ai_csv_tester(self, filename):
        time.sleep(0.5)
        base_filename = os.path.basename(filename)
        return 758

app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
