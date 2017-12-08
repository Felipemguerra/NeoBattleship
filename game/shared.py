from PyQt5 import QtWidgets

#[x1,y1,x2,y2,length]
SHIPS = [[[4,0,4,3,4],[0,1,2,1,3],[0,3,1,3,2]], [[1,2,4,2,4],[0,4,0,6,3],[4,7,5,7,2]],[[2,0,5,0,4],[6,4,6,6,3],[0,7,0,8,2]], [[8,0,8,3,4],[5,6,7,6,3],[3,2,4,2,2]], [[7,1,7,4,4],[2,2,2,4,3],[4,8,5,8,2]]]

APP_HEIGHT = 0
APP_WIDTH = 0

def set(app):
	global APP_HEIGHT
	global APP_WIDTH
	size =  app.desktop().screenGeometry()
	APP_HEIGHT = size.width()/3
	APP_WIDTH = size.width()/3

class winMessage(QtWidgets.QMessageBox):
	def __init__(self):
		QtWidgets.QMessageBox.__init__(self)
		self.setWindowTitle("Congrats")
		self.setText("Would you like to play again?")
		self.addButton(self.Yes)
		self.addButton(self.No)

class loseMessage(QtWidgets.QMessageBox):
	def __init__(self):
		QtWidgets.QMessageBox.__init__(self)
		self.setWindowTitle("You Lose")
		self.setText("Would you like to play again?")
		self.addButton(self.Yes)
		self.addButton(self.No)
