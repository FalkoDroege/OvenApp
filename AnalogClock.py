#!/usr/bin/python3
 
# Imports
 
import sys, time
from datetime import datetime
 
from PyQt5 import QtWidgets,QtGui, QtCore
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QLinearGradient
from PyQt5.QtWidgets import QWidget


# Classes
 
# AnalogClock
 
class AnalogClock(QWidget):
	secondPolygon = QtGui.QPolygon([QtCore.QPoint(2, -8), QtCore.QPoint(-2, -8), QtCore.QPoint(-1, 96), QtCore.QPoint(1, 96), ])
	minutePolygon = QtGui.QPolygon([QtCore.QPoint(3, -5), QtCore.QPoint(-3, -5), QtCore.QPoint(-2, 85), QtCore.QPoint(2, 85), ])
	hourPolygon = QtGui.QPolygon([QtCore.QPoint(4, -5), QtCore.QPoint(-4, -5), QtCore.QPoint(-3, 70), QtCore.QPoint(3, 70), ])
	secondPosition=0
	minutePosition=0
	hourPosition=0
	oldMiniutePosition=0

	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		# super(AnalogClock, self).__init__(parent)
		# self.setWindowTitle("Analog Clock")
		self.resize(300, 300)
		# self.setAutoFillBackground(True)

		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.updateClock)
		self.timer.start(1000)


	def paintEvent(self, event):
		width = self.width()
		height = self.height()
		# print("width: %s, height: %s" %(width, height))
		painter = QtGui.QPainter(self)
		painter.setRenderHint(QtGui.QPainter.Antialiasing)
		painter.setBackground(Qt.black)
		painter.translate(width / 2 , height /2)
		painter.scale(width / 250.0, height / 250.0)

# paint crown
		# gradient=QLinearGradient(0, -100, 0, 100)
		gradient=QtGui.QRadialGradient(0, 0, 110)
		gradient.setColorAt(1, Qt.lightGray)
		gradient.setColorAt(0.9, Qt.black)
		gradient.setColorAt(0.8, Qt.black)
		gradient.setColorAt(0, QColor(255,30,30))
		painter.setBrush(gradient)
		painter.setPen(QtGui.QPen(gradient, 10, Qt.SolidLine))

		painter.drawEllipse(-105,-105,210,210)
		painter.setPen(QtGui.QPen(Qt.white, 2, Qt.SolidLine))
		painter.drawEllipse(-110,-110,220,220)



# paint big ticks
		painter.setPen(QtGui.QPen(Qt.lightGray, 4, QtCore.Qt.SolidLine))
		painter.setFont(QtGui.QFont('Arial', 8))
		painter.rotate(-90)
		for i in range(12):
			painter.drawLine(90, 0, 98, 0)
			painter.rotate(30)

# draw numbers
		painter.save()
		painter.setFont(QtGui.QFont('Verdana', 10, weight=QtGui.QFont.Bold))
		painter.translate(75,-15)
		painter.rotate(90)
		painter.drawText(0, -10, 30, 10, QtCore.Qt.AlignCenter, "12")
		painter.translate(75,80)
		painter.drawText(0, -10, 30, 10, QtCore.Qt.AlignCenter, "3")
		painter.translate(-150,0)
		painter.drawText(0, -10, 30, 10, QtCore.Qt.AlignCenter, "9")
		painter.translate(75,75)
		painter.drawText(0, -10, 30, 10, QtCore.Qt.AlignCenter, "6")
		painter.restore()

# paint small ticks
		painter.setPen(QtCore.Qt.gray)
		painter.rotate(-90);
		for i in range(60):
			if (i % 5) != 0:
				painter.drawLine(95, 0, 100, 0)
			painter.rotate(6)

# paint seconds
		painter.save()
		painter.rotate(self.secondPosition)
		painter.setPen(QtCore.Qt.NoPen)
		painter.setBrush(QtCore.Qt.red)
		painter.drawConvexPolygon(AnalogClock.secondPolygon)
		painter.restore()
 
# paint minutes
		painter.save()
		painter.rotate(self.minutePosition)
		painter.setPen(QtCore.Qt.NoPen)
		painter.setBrush(QtCore.Qt.white)
		painter.drawConvexPolygon(AnalogClock.minutePolygon)
		painter.restore()

# paint hours
		painter.save()
		painter.rotate(self.hourPosition)
		painter.setPen(QtCore.Qt.NoPen)
		painter.setBrush(QtCore.Qt.white)
		painter.drawConvexPolygon(AnalogClock.hourPolygon)
		painter.restore()

# paint ccenter dot
		painter.save()
		coneGradient=QtGui.QConicalGradient(0, 0, -90.0)
		coneGradient.setColorAt(0,QtCore.Qt.black)
		coneGradient.setColorAt(0.5,QtCore.Qt.white)
		coneGradient.setColorAt(1,QtCore.Qt.black)
		painter.setOpacity(0.9)
		painter.setPen(QtCore.Qt.NoPen)
		painter.setBrush(coneGradient)
		painter.drawEllipse(-7,-7,15,15)
		painter.restore()

		painter.end()


	def update(self, hour, minute, second):
			self.secondPosition = second*6
			self.minutePosition = minute*6
			self.hourPosition = hour*30
			self.repaint()
 

	def updateClock(self):
		now = datetime.now()  
		self.update(now.hour,now.minute,now.second)
 

# Main
def main(): 
	app = QtWidgets.QApplication(sys.argv)
	clock = AnalogClock()
	p=clock.palette()
	p.setColor(clock.backgroundRole(), QtCore.Qt.black)
	clock.setPalette(p)
	clock.show()

	sys.exit(app.exec_())


# ______________________________________________________________________________________________________________
if __name__ == "__main__":
    main()

# EOF