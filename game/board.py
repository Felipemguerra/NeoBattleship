import player, computer
from PyQt5 import QtWidgets, QtGui

class gameboard(QtWidgets.QWidget):
	def __init__(self, parent, diff):
		QtWidgets.QWidget.__init__(self)
		#set background color
		b = QtGui.QBrush(QtGui.QImage('images/metal.jpg'))
		p = self.palette()
		p.setBrush(self.backgroundRole(), b)
		self.setPalette(p)
		self.setAutoFillBackground(True)
		self.setup(diff)
		#store parent needed for restart mid-game
		self.parent = parent

	def setup(self, diff):
		self.player = player.player(self)
		self.enemy = computer.computer(self, diff)
		self.grid = QtWidgets.QGridLayout()
		self.setLayout(self.grid)
		self.grid.addWidget(self.enemy, 0,0,1,1)
		self.grid.addWidget(self.player, 0,1,1,1) 
