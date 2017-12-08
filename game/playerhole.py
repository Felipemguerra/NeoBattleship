from PyQt5 import QtWidgets, QtGui
import shared

class playerHole(QtWidgets.QWidget):
	def __init__(self, parent):
		QtWidgets.QWidget.__init__(self,parent)
		#store important hole information
		self.parent = parent
		self.peg = False
		self.ship = False
		self.hit = False
		self.sunk = False
		#used to draw proportional circle for holes
		self.circle = (shared.APP_HEIGHT*2)/(self.width()/2)

	#draw hole depending on status of hole
	def paintEvent(self, event):
		if self.peg == True and self.hit == True and self.sunk == False:
			qp = QtGui.QPainter()
			qp.begin(self)
			brush = QtGui.QBrush(QtGui.QImage('images/explosion.jpg'))
			qp.setBrush(brush)
			qp.drawEllipse((self.width()-self.circle)/2,(self.height()-self.circle)/2,self.circle,self.circle)
			qp.end()
		elif self.peg == True and self.hit == True and self.sunk == True:
			None
		elif self.peg == True and self.hit == False:
			None
		else:
			qp = QtGui.QPainter()
			qp.begin(self)
			brush = QtGui.QBrush(QtGui.QColor(0,0,0,255))
			qp.setBrush(brush)
			qp.drawEllipse((self.width()-self.circle)/2,(self.height()-self.circle)/2,self.circle,self.circle)
			qp.end()

	#called by computer when it makes a move
	#makes necessary checks and updates
	#then switches to player turn
	def addPeg(self):
		if self.ship == True:
			self.peg = True
			self.hit = True
			self.update()
			self.parent.check()
			self.parent.parent.enemy.turn = False
		else:
			self.peg = True
			self.update()
			self.parent.parent.enemy.turn = False		
	
	#Used by parent function to keep track of ship widgets
	#makes player ships visible
	def isShip(self):
		self.ship = True
		b = QtGui.QBrush(QtGui.QImage('images/ship.jpg'))
		p = self.palette()
		p.setBrush(self.backgroundRole(), b)
		self.setPalette(p)
		self.setAutoFillBackground(True)
		self.update()

	#color ship red when it sinks
	def sunken(self):
		self.sunk = True
		b = QtGui.QBrush(QtGui.QImage('images/explosion.jpg'))
		p = self.palette()
		p.setBrush(self.backgroundRole(), b)
		self.setPalette(p)
