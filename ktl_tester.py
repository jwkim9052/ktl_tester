from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QFileDialog, QTableWidget, QTableWidgetItem, QMessageBox, QStatusBar
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtTest import QTest
import sys, os, time, csv

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi("ktl_ui.ui", self)
        self.setWindowTitle("수어번역시간 측정기")
        self.show()

        # Define Widgets
        self.video_action = self.findChild(QAction,"actionVideo_tester")
        self.status_bar = self.findChild(QStatusBar,"statusbar")
        self.table_widget = self.findChild(QTableWidget, "tableWidget")
        self.table_widget.setHorizontalHeaderLabels(('파일명','Ref-값','HYP-예측값','WER','종합추론시간','수어번역시간'))
        self.table_widget.setColumnWidth(3,200)
        self.table_widget.setColumnWidth(4,200)
        self.table_widget.setColumnWidth(5,200)

        self.video_action.triggered.connect(self.selectVideoFiles)
        self.total_result = []
        self.total_WER = 0.0
        self.total_infer = 0.0
        self.total_slt = 0.0

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
            self.total_result = []
            self.total_WER = 0.0
            self.total_infer = 0.0
            self.total_slt = 0.0

            self.table_widget.setRowCount(0)
            numFiles = len(fnames)
            #msg = QMessageBox()
            #msg.setWindowTitle("Selected Files")
            #msg.setText(f"{numFiles} file(s) have been selected!")
            #x = msg.exec_()

            self.status_bar.showMessage(f"{numFiles} have been selected!")
            self.repaint()

            for fname in fnames:
                # AI Video Tester
                # Input parameter has full path and filename
                # output is a list ['filename', ref, HYP, WER, inference time, slt time]
                result = self.ai_video_tester(fname)
                # The end of AI Video Tester


                self.total_result.append(result)
                self.total_WER += float(result[3])
                self.total_infer += float(result[4])
                self.total_slt += float(result[5])

                rowCount = self.table_widget.rowCount()
                self.table_widget.insertRow(rowCount)
                self.table_widget.setItem(rowCount, 0, QTableWidgetItem(str(result[0])))
                self.table_widget.setItem(rowCount, 1, QTableWidgetItem(str(result[1])))
                self.table_widget.setItem(rowCount, 2, QTableWidgetItem(str(result[2])))
                self.table_widget.setItem(rowCount, 3, QTableWidgetItem(str(result[3])))
                self.table_widget.setItem(rowCount, 4, QTableWidgetItem(str(result[4])))
                self.table_widget.setItem(rowCount, 5, QTableWidgetItem(str(result[5])))

                self.status_bar.showMessage(f"{rowCount+1}/{numFiles} have been completed!")
                self.repaint()
            
            rowCount = self.table_widget.rowCount()
            tline = rowCount
            last_line = [ "Average", "", "", f"{self.total_WER/tline}", f"{self.total_infer/tline}", f"{self.total_slt/tline}" ]
            #print( tline )
            #print( self.total_WER )
            self.table_widget.insertRow(rowCount)
            self.table_widget.setItem(rowCount, 0, QTableWidgetItem(str(last_line[0])))
            self.table_widget.setItem(rowCount, 1, QTableWidgetItem(str(last_line[1])))
            self.table_widget.setItem(rowCount, 2, QTableWidgetItem(str(last_line[2])))
            self.table_widget.setItem(rowCount, 3, QTableWidgetItem(str(last_line[3])))
            self.table_widget.setItem(rowCount, 4, QTableWidgetItem(str(last_line[4])))
            self.table_widget.setItem(rowCount, 5, QTableWidgetItem(str(last_line[5])))

            # csv file
            if len(self.total_result) > 0:
                header = ['Filename','Ref','HYP','WER','Total time','SLT time']
                with open('result.csv', 'w', encoding='UTF8', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(header)
                    writer.writerows(self.total_result)
                    writer.writerow(last_line)

    # this is an example function.
    def ai_video_tester(self, filename):
        QTest.qWait(600)
        base_filename = os.path.basename(filename)
        return_list = [base_filename, "2.5", "2.3", "4.5", "7.2", "3.2"]
        return return_list

app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
