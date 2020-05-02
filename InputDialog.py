#!/usr/bin/python3
 
# Imports
 
import sys, time
from datetime import datetime, timedelta
 
from PyQt5 import QtWidgets,uic, QtCore
from PyQt5.QtWidgets import QWidget




# Classes
class InputDialog(QWidget):
	dest="time"
	cValue=0

	
	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		uic.loadUi('input.ui', self)
		self.plusButton=self.findChild(QtWidgets.QToolButton,"plusButton")
		self.minusButton=self.findChild(QtWidgets.QToolButton,"minusButton")
		self.okButton=self.findChild(QtWidgets.QToolButton,"okButton")

		self.plusButton.clicked.connect(self.increase_value)
		self.minusButton.clicked.connect(self.decrease_value)

	def showEvent(self, event):
		self.value=self.findChild(QtWidgets.QLabel, ("value"))
		self.unit=self.findChild(QtWidgets.QLabel, ("unit"))
		self.destination=self.findChild(QtWidgets.QLabel, ("source"))
		self.destination.setText(self.dest)
		if self.dest=="time":
			self.value.setText("0:00")
			self.unit.setText("h:min")
			self.destination.setText("Backzeit")			
		elif self.dest=="speed":
			self.value.setText("low")
			self.unit.setText("")
			self.destination.setText("Lüfter")			
		elif self.dest=="steam":
			self.value.setText("0")
			self.unit.setText("ml")
			self.destination.setText("Dampf")			
		elif self.dest=="temp":
			self.value.setText("180")
			self.unit.setText("°C")
			self.destination.setText("Temperatur")			
		else:
			self.value.setText("---")
			self.unit.setText("")
			self.destination.setText("---")

	
	def increase_value(self):
		if self.dest=="time":
			time=self.value.text()
			time1=datetime.strptime(time, '%H:%M')
			newTime= time1 + timedelta(minutes = 1)
			strTime=newTime.strftime("%H:%M")
			self.value.setText(strTime)
		elif self.dest=="speed":
			if self.value.text()=="low":
				self.value.setText("high")
			else:
				self.value.setText("low")
		elif self.dest=="steam":
			self.cValue = int(self.value.text()) + 10
			if self.cValue > 500:
				self.cValue=500
			self.value.setText(str(self.cValue))
		elif self.dest=="temp":
			self.cValue = int(self.value.text()) + 5
			if self.cValue > 250:
				self.cValue=250
			self.value.setText(str(self.cValue))
		else:
			pass

	def decrease_value(self):
		if self.dest=="time":
			time=self.value.text()
			time1=datetime.strptime(time, '%H:%M')
			newTime= time1 + timedelta(minutes = -1)
			strTime=newTime.strftime("%H:%M")
			self.value.setText(strTime)
		elif self.dest=="speed":
			if self.value.text()=="low":
				self.value.setText("high")
			else:
				self.value.setText("low")
		elif self.dest=="steam":
			self.cValue = int(self.value.text()) - 10
			if self.cValue < 0:
				self.cValue=0
			self.value.setText(str(self.cValue))
		elif self.dest=="temp":
			self.cValue = int(self.value.text()) - 5
			if self.cValue < 30:
				self.cValue=30
			self.value.setText(str(self.cValue))
		else:
			pass

	def quit_dialog(self):
		pass

# Main
def main(): 
	app = QtWidgets.QApplication(sys.argv)
	dialog = InputDialog()
	dialog.show()

	sys.exit(app.exec_())


# ______________________________________________________________________________________________________________
if __name__ == "__main__":
    main()

# EOF