from PyQt5 import QtWidgets, QtGui
import shared

class computerHole(QtWidgets.QWidget):
	def __init__(self, parent):
		QtWidgets.QWidget.__init__(self,parent)
		#store important hole information
		self.peg = False
		self.ship = False
		self.hit = False
		self.sunk = False
		self.parent = parent
		#used to draw proportional circle for holes
		self.circle = (shared.APP_HEIGHT*2)/(self.width()/2)
		
	#draw hole depending on status of hole
	def paintEvent(self, event):
		if self.peg == True and self.ship == True and self.sunk == False:
			qp = QtGui.QPainter()
			qp.begin(self)
			brush = QtGui.QBrush(QtGui.QImage('images/explosion.jpg'))
			qp.setBrush(brush)
			qp.drawEllipse((self.width()-self.circle)/2,(self.height()-self.circle)/2,self.circle,self.circle)
			qp.end()
		elif self.peg == True and self.hit == True and self.sunk == True:
			None
		elif self.peg == True and self.ship == False:
			None
		else:
			qp = QtGui.QPainter()
			qp.begin(self)
			brush = QtGui.QBrush(QtGui.QColor(0,0,0,255))
			qp.setBrush(brush)
			qp.drawEllipse((self.width()-self.circle)/2,(self.height()-self.circle)/2,self.circle,self.circle)
			qp.end()

	#reads in players hole choice
	#makes necessary checks and updates
	#then switches to computer turn
	def mousePressEvent(self, event):
		if self.peg == False and self.parent.turn == False:
			self.parent.turn = True
			if self.ship == True:
				self.peg = True
				self.hit = True
				self.update()
				self.parent.check()
			else:
				self.peg = True
				self.update()
			self.parent.move()
			self.parent.turn = False

	#Used by parent function to keep track of ship widgets
	def isShip(self):
		self.ship = True
		self.update()

	#color ship red when it sinks
	def sunken(self):
		self.sunk = True
		b = QtGui.QBrush(QtGui.QImage('images/explosion.jpg'))
		p = self.palette()
		p.setBrush(self.backgroundRole(), b)
		self.setPalette(p)
		self.setAutoFillBackground(True)
