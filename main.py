# !/usr/bin/python3

import sys, time
from time import gmtime, strftime
from datetime import datetime, timedelta
from queue import Queue 
from PyQt5 import QtWidgets, uic, QtGui, QtGui, QtCore
from PyQt5.QtCore import QThread, pyqtSignal, QTimer, QTime, QSize, Qt
from PyQt5.QtGui import QColor, QPixmap
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
# from analog_clock import AnalogClock
# AnalogClock=AnalogClock


# __________________________________________________________________________________________________________main
def main():
    app = QtWidgets.QApplication(sys.argv)
    Man=ManualGui()
    Window=Ui()
    Window.show()
    sys.exit(app.exec_())
# ________________________________________________________________________________________________________
# class ManualGui
class ManualGui(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        self.source=""
        self.manualQueue=Queue()
        super(ManualGui, self).__init__(parent)
        uic.loadUi('ManuellWindow.ui', self)
        self.time=self.findChild(QtWidgets.QWidget,"time")
        self.temp=self.findChild(QtWidgets.QWidget,"temp")
        self.timeButton=self.findChild(QtWidgets.QToolButton,"timeButton")
        # self.setCursor(Qt.BlankCursor)

        self.target="time"
        self.timeButton.clicked.connect(self.open_time_dialog)
        self.speedButton.clicked.connect(self.open_speed_dialog)
        self.steamButton.clicked.connect(self.open_steam_dialog)
        self.tempButton.clicked.connect(self.open_temp_dialog)
        self.doorButton.clicked.connect(self.open_door)

        self.temp.start=False
        self.temp.unit="celsius"
        self.temp.value=30
        self.temp.initValue=250

        self.time.start=True
        self.time.unit="minute"
        self.time.value=0
        self.time.initValue=60
        self.time.clicked.connect(self.run_job)
        self.dialog=Dialog(self)
        self.dialog.accepted.connect(self.get_result)
        self.dialog.rejected.connect(self.set_reject)




        
    def run_job(self):
        if self.time.start:
            print("Time is %s" %self.lb_tg_durcance.text())
            if self.lb_tg_durcance.text()=="00:00":
                print("Nothing setted!")
            else:
                self.time.start=False
                self.timer = QtCore.QTimer()
                self.timer.timeout.connect(self.update_timer)
                self.timer.start(1000)                
        else: 
            self.time.start=True
        
    def update_timer(self):
        inTime=self.time.value
        isTime=(inTime)-1/60
        print("Time is: %s" %isTime)
        if isTime <= 1/60:
            self.timer.stop()
            self.time.start=True
        self.time.value=isTime
        self.time.repaint()


    def stop_baking(self):
        pass


    def set_reject(self):
        self.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect())

    def get_result(self):
        self.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect())
        res=self.dialog.dialog.value.text()
        if self.source=="time":
            self.lb_tg_durcance.setText("%s" %res)
            t=res.split(':')
            total_minutes= int(t[0])*60+int(t[1])
            if total_minutes > 0:
                self.time.initValue=total_minutes
                self.time.value=total_minutes
        if self.source=="speed":
            self.lb_tg_speed.setText("%s" %res)
        if self.source=="steam":
            self.lb_tg_steam.setText("%s" %res)
        if self.source=="temp":
            self.lb_tg_temp.setText("%s" %res)
            self.temp.initValue=int(res)

    def open_time_dialog(self):
        self.setGraphicsEffect(QtWidgets.QGraphicsBlurEffect())
        self.source="time"
        self.dialog.init=True
        self.dialog.show_dialog(self.source)

    def open_speed_dialog(self):
        self.setGraphicsEffect(QtWidgets.QGraphicsBlurEffect())
        self.source="speed"
        self.dialog.init=True
        self.dialog.show_dialog(self.source)

    def open_steam_dialog(self):
        self.setGraphicsEffect(QtWidgets.QGraphicsBlurEffect())
        self.source="steam"
        self.dialog.init=True
        self.dialog.show_dialog(self.source)

    def open_temp_dialog(self):
        self.setGraphicsEffect(QtWidgets.QGraphicsBlurEffect())
        self.source="temp"
        self.dialog.init=True
        self.dialog.show_dialog(self.source)

    def open_door(self):
        pass

# ________________________________________________________________________________________________________
# class Dialog
class Dialog(QtWidgets.QDialog):
    def __init__(self, parent = None):
        super(Dialog, self).__init__(parent)
        uic.loadUi('dialogs.ui', self)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)    
        self.setGeometry(50,40,700,400)
        self.dialog=self.findChild(QtWidgets.QWidget,"dialog")
        self.dialog.dest="speed"

    def show_dialog(self, source):
        self.dialog.dest=source
        self.dialog.update()
        self.show()



# ________________________________________________________________________________________________________
# class Settings
class Settings(QtWidgets.QDialog):
    def __init__(self, parent = None):
        super(Settings, self).__init__(parent)
        uic.loadUi('settings.ui', self)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)    
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect())    
        self.setGeometry(50,40,700,400)



# ________________________________________________________________________________________________________
# class Ui
class Ui(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Ui, self).__init__(parent)
        uic.loadUi('MainWindow.ui', self)
        self.onoffButton=self.findChild(QtWidgets.QToolButton, "onoffButton")
        self.manButton=self.findChild(QtWidgets.QToolButton, "manButton")
        self.onoffButton.clicked.connect(self.exit_prog)
        self.manButton.clicked.connect(self.call_man)
        self.settingsButton.clicked.connect(self.call_settings)
        self.settings=Settings(self)
        self.settings.accepted.connect(self.reset_blur)
        self.settings.rejected.connect(self.reset_blur)

        # self.setCursor(Qt.BlankCursor)
        self.showFullScreen()

    def call_man(self):
        # self.hide()
        self.manual=ManualGui(self)
        self.manual.showFullScreen()

    def open_door(self):
        pass

    def reset_blur(self):
        self.setGraphicsEffect(QtWidgets.QGraphicsDropShadowEffect())    

    def call_settings(self):
        self.setGraphicsEffect(QtWidgets.QGraphicsBlurEffect())
        self.settings.show()



    def exit_prog(self):
        exit()

# ______________________________________________________________________________________________________________
if __name__ == "__main__":
    main()
