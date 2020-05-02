#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Marin Purgar - marin.purgar@gmail.com
# This code is freeware, do whatever you want with it!
 
# Imports
 
import sys
 
from PyQt5 import QtWidgets, uic, QtGui, QtGui, QtCore
from PyQt5.QtCore import QThread, pyqtSignal, QTimer, QTime, QSize
from PyQt5.QtGui import QColor, QPixmap
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox


# Classes
 
# AnalogMultimeter
 
class AnalogMultimeter(QtWidgets.QMainWindow):
  needlePosition = 0
  needlePolygon = QtGui.QPolygon([QtCore.QPoint(2, -8), QtCore.QPoint(-2, -8), QtCore.QPoint(-1, 96), QtCore.QPoint(1, 96), ])
 
  def __init__(self, parent=None):
    super(AnalogMultimeter, self).__init__(parent)
    self.setWindowTitle("Analog Multimeter")
    self.resize(220, 140)
 
  def paintEvent(self, event):
    width = self.width()
    height = self.height()
    painter = QtGui.QPainter(self)
    painter.setRenderHint(QtGui.QPainter.Antialiasing)
    painter.translate(width / 2, height * 0.85)
    painter.scale(width / 220.0, height / 140.0)
# paint arc
    painter.setPen(QtGui.QPen(QtCore.Qt.gray, 1, QtCore.Qt.SolidLine))
    painter.drawArc(-88, -88, 176, 176, 20 * 16, 140 * 16)
# paint big ticks
    painter.setPen(QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine))
    painter.setFont(QtGui.QFont('Arial', 8))
    painter.rotate(200);
    for i in range(11):
      painter.drawLine(88, 0, 96, 0)
      if (i % 2) == 0:
        painter.save()
        painter.translate(98, -15)
        painter.rotate(90);
        painter.drawText(0, -10, 30, 10, QtCore.Qt.AlignCenter, str(i / 2))
        painter.restore()
      painter.rotate(14)
# paint small ticks
    painter.setPen(QtCore.Qt.gray)
    painter.rotate(206)
    for i in range(50):
      if (i % 5) != 0:
        painter.drawLine(88, 0, 92, 0)
      painter.rotate(2.8)
# paint needle
    painter.rotate(130 + self.needlePosition)
    painter.setPen(QtCore.Qt.NoPen)
    painter.setBrush(QtCore.Qt.red)
    painter.drawConvexPolygon(AnalogMultimeter.needlePolygon)
    painter.end()
 
  def updatePosition(self, position):
    if position != self.needlePosition:
      self.needlePosition = position
      self.repaint()
 

# Main methods
 
def updateMeter():
    meter.updatePosition(100)
 
# Main
 
app = QtWidgets.QApplication(sys.argv)
 
meter = AnalogMultimeter()
meter.show()
 
timer = QtCore.QTimer()
timer.timeout.connect(updateMeter)
timer.start(10)
 
sys.exit(app.exec_())
 
# EOF