#!/usr/bin/python3
 
# Imports
 
import sys, time
import numpy as np
from datetime import datetime
 
from PyQt5 import QtWidgets,QtGui, QtCore
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QLinearGradient
from PyQt5.QtWidgets import QWidget, QPushButton


# Classes
 
# AnalogClock
 
class CircProgress(QPushButton):
	startIcon= QtGui.QPolygon([QtCore.QPoint(15, 0), QtCore.QPoint(-15, -18), QtCore.QPoint(-15, 18), QtCore.QPoint(15, 0), ])
	start=True
	# start=False
	unit="minute"
	value=0
	startAngle=0
	spanAngle=360
	initValue=60
	perc=0
	dot=QtCore.QRect(-15,-15,30,30)

	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		self.resize(300, 300)


	def paintEvent(self, event):

		width = self.width()
		height = self.height()
		painter = QtGui.QPainter(self)
		painter.setRenderHint(QtGui.QPainter.Antialiasing)
		painter.setBackground(Qt.black)
		painter.translate(width / 2 , height /2)
		painter.scale(width / 250.0, height / 250.0)

		# draw start icon if start=1
		if self.start==True:
			# self.setMouseTracking()
			painter.save()
			painter.setPen(QtCore.Qt.NoPen)
			painter.setPen(QtGui.QPen(Qt.white, 8, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
			painter.setBrush(QtCore.Qt.white)
			painter.drawConvexPolygon(CircProgress.startIcon)
			painter.restore()
		else:
			# draw text
			if self.unit=="celsius":
				self.unitSign="°C"
				self.startAngle=250
				self.spanAngle=-320
				self.info=self.value
			elif self.unit=="minute":
				self.unitSign=""
				self.startAngle=90
				self.spanAngle=-360
				self.info=self.secs_to_HMS(self.value*60)
			else: 	
				self.unitSign=""		
				self.startAngle=0
				self.spanAngle=-180
				self.info=self.value

			painter.setPen(QtGui.QPen(Qt.white, 4, Qt.SolidLine, Qt.RoundCap))
			rect=QtCore.QRect(-75,-25,150,50)
			painter.setFont(QtGui.QFont('Arial', 25))
			pvalue="%s %s" %(self.info, self.unitSign)
			painter.drawText(rect, QtCore.Qt.AlignCenter, pvalue)

		# draw arc
	    # painter.drawArc(-88, -88, 176, 176, 20 * 16, 140 * 16)
		painter.setPen(QtGui.QPen(QColor(80,0,0), 5, QtCore.Qt.SolidLine, Qt.RoundCap))
		rect=QtCore.QRect(-100,-100,200,200)
		painter.drawArc(rect, self.startAngle*16, self.spanAngle*16)

		# calculate angle
		self.perc=(self.value/self.initValue)
		self.percAngle=int(self.spanAngle*self.perc)
		# print("per: %s, percAngle: %s" %(self.perc, self.percAngle))

		# draw arc
		painter.setPen(QtCore.Qt.NoPen)
		gradient=QtGui.QRadialGradient(0, 0, 110)
		gradient.setColorAt(1, Qt.black)
		gradient.setColorAt(0.9, QColor(255,70,70))
		gradient.setColorAt(0.8, Qt.black)
		gradient.setColorAt(0, Qt.black)
		painter.setBrush(gradient)

		painter.setPen(QtGui.QPen(gradient, 20, QtCore.Qt.SolidLine, Qt.RoundCap))		
		painter.drawArc(rect, self.startAngle*16, self.percAngle*16)

		painter.save()
		#rotate to set startAngle of arc
		painter.rotate(-self.startAngle)
		#rotate to set value for dot
		painter.rotate(-self.percAngle)	

		#draw dot
		painter.translate(100, 0)
		painter.setOpacity(0.9)
		painter.setPen(QtCore.Qt.NoPen)
		gradient=QtGui.QRadialGradient(0, 0, 20)
		gradient.setColorAt(1, Qt.black)
		# gradient.setColorAt(0.9, Qt.black)
		# gradient.setColorAt(0.8, Qt.black)
		gradient.setColorAt(0, QColor(255,70,70))
		painter.setBrush(gradient)
		painter.drawEllipse(self.dot)
		painter.restore()

		# close painter
		painter.end()

	def update(self, parent=None):
			self.repaint()

	def secs_to_HMS(self, secs): 
		if secs < 3600:
			# return datetime.datetime.fromtimestamp(secs).strftime('%M:%S') 
			return time.strftime("%M:%S", time.gmtime(secs))
		else: 
			# return datetime.datetime.fromtimestamp(secs).strftime('%H:%M:%S') 
			return time.strftime("%H:%M:%S", time.gmtime(secs))


# Main
def main(): 
	app = QtWidgets.QApplication(sys.argv)
	progr = CircProgress()
	p=progr.palette()
	p.setColor(progr.backgroundRole(), QtCore.Qt.black)
	progr.setPalette(p)
	progr.show()

	sys.exit(app.exec_())


# ______________________________________________________________________________________________________________
if __name__ == "__main__":
    main()

# EOF