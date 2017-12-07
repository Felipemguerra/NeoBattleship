"""
NeoBattleship main.py

"""
import sys, random
from PyQt5 import QtWidgets, QtCore, QtGui

NBS_HEIGHT = 800/2
NBS_WIDTH = 800/2
#[x1,y1,x2,y2,length]
SHIPS = [[[4,0,4,3,4],[0,1,2,1,3],[0,3,1,3,2]], [[1,2,4,2,4],[0,4,0,6,3],[4,7,5,7,2]], [[2,0,5,0,4],[6,4,6,6,3],[0,7,0,8,2]], [[8,0,8,3,4],[5,6,7,6,3],[3,2,4,2,2]], [[7,1,7,4,4],[2,2,2,4,3],[4,8,5,8,2]]]

class gameWindow(QtWidgets.QMainWindow):
	def __init__(self):
		QtWidgets.QWidget.__init__(self)
		self.setWindowTitle("NeoBattleship")
		
		exit_action = QtWidgets.QAction("Exit", self)
		exit_action.triggered.connect(QtWidgets.qApp.quit)
		restart_action = QtWidgets.QAction("Restart", self)
		restart_action.triggered.connect(self.setup)
		menu_bar = self.menuBar()
		menu_bar.setNativeMenuBar(False)
		file_menu = menu_bar.addMenu("Options")
		file_menu.addAction(exit_action) 
		file_menu.addAction(restart_action) 
		self.setup()

	def setup(self):		
		self.game_grid = gameGrid(self)
		self.setCentralWidget(self.game_grid)        
		self.show()
        
	def closeEvent(self, event):
		reply = quitMessage().exec_()
		if (reply == QtWidgets.QMessageBox.Yes):
			event.accept()
		else:
			event.ignore()
            
class gameGrid(QtWidgets.QWidget):
	def __init__(self, parent):
		QtWidgets.QWidget.__init__(self)
		p = self.palette()
		p.setColor(self.backgroundRole(), QtGui.QColor(150,150,150,255))
		self.setPalette(p)
		self.setAutoFillBackground(True)
		self.parent = parent
		self.setup()

	def setup(self):
		self.board = Player(self)
		self.enemyBoard = Computer(self)
		self.grid = QtWidgets.QGridLayout()
		self.setLayout(self.grid)
		self.grid.addWidget(self.enemyBoard, 0,0,1,1)
		self.grid.addWidget(self.board, 1,0,1,1)         

class Player(QtWidgets.QWidget):
	def __init__(self, parent):
		QtWidgets.QWidget.__init__(self, parent)
		self.setFixedSize(NBS_WIDTH, NBS_HEIGHT)
		b = QtGui.QBrush(QtGui.QImage('water.bmp'))
		p = self.palette()
		p.setBrush(self.backgroundRole(), b)
		self.setPalette(p)
		self.setAutoFillBackground(True)
		self.grid = QtWidgets.QGridLayout()
		self.setLayout(self.grid)
		self.grid.setSpacing(0)
		self.parent = parent
		self.ships = random.choice(SHIPS)
		self.holes = []	
		self.status = []	
		self.positions = []
		self.place_holes()		
		self.placeShips()
		self.setPositions()

	def paintEvent(self, event):
		qp = QtGui.QPainter()
		qp.begin(self)
		pen = qp.pen()
		pen.setColor(QtGui.QColor(255,255,255,255))
		qp.setPen(pen)
		j = 10
		dev = 10
		for i in range(j):
			qp.drawLine(QtCore.QLineF((NBS_WIDTH/j)*i+dev, 10, (NBS_WIDTH/j)*i+dev, NBS_HEIGHT-12))
			qp.drawLine(QtCore.QLineF(10, (NBS_WIDTH/j)*i+dev, NBS_HEIGHT-12, (NBS_WIDTH/j)*i+dev))
			dev +=2
			
		qp.end()

	def place_holes(self):
		for col in range(9):
			temp = []
			for row in range(9):
				hole = playerHole(self, row, col)
				self.grid.addWidget(hole, row, col)
				temp.append(hole)
			self.holes.append(temp[:])

	def placeShips(self):
		for ship in self.ships:
			temp = []
			if ship[0] == ship[2]:			
				for i in range(ship[4]):	
					self.holes[ship[0]][ship[1]+i].isShip()
					temp.append(self.holes[ship[0]][ship[1]+i])
			else:
				for i in range(ship[4]):	
					self.holes[ship[0]+i][ship[1]].isShip()
					temp.append(self.holes[ship[0]+i][ship[1]])
			temp2 = [temp[:],False]
			self.status.append(temp2)

	def setPositions(self):
		clist = []
		for ship in self.ships:
			if ship[0] == ship[2]:			
				for i in range(ship[4]):	
					clist.append([ship[0],i])
			else:
				for i in range(ship[4]):
					clist.append([i,ship[1]])
		self.positions = clist[:]

	def check(self):
		for i in self.status:
			if i[1] == False:
				temp = True			
				for e in i[0]:
					if e.hit == False:
						temp = False
				i[1] = temp
				if i[1] == True:
					for j in i[0]:
						j.sunken()

		end = True
		for i in self.status:
			if i[1] == False:
				end = False
		if end == True:
			reply = loseMessage().exec_()
			if reply == QtWidgets.QMessageBox.Yes:
				self.parent.parent.setup()
			elif reply == QtWidgets.QMessageBox.No:
				quit()

class Computer(QtWidgets.QWidget):
	def __init__(self, parent):
		QtWidgets.QWidget.__init__(self, parent)
		self.setFixedSize(NBS_WIDTH, NBS_HEIGHT)
		b = QtGui.QBrush(QtGui.QImage('water.bmp'))
		p = self.palette()
		p.setBrush(self.backgroundRole(), b)
		self.setPalette(p)
		self.setAutoFillBackground(True)
		self.grid = QtWidgets.QGridLayout()
		self.setLayout(self.grid)
		self.grid.setSpacing(0)
		self.choices = []
		self.createChoices()
		self.holes = []		
		self.place_holes()
		self.ships = random.choice(SHIPS)
		self.status = []
		self.positions = []
		self.placeShips()
		self.parent = parent
		self.turn = False

	def paintEvent(self, event):
		qp = QtGui.QPainter()
		qp.begin(self)
		pen = qp.pen()
		pen.setColor(QtGui.QColor(255,255,255,255))
		qp.setPen(pen)
		j = 10
		dev = 10
		for i in range(j):
			qp.drawLine(QtCore.QLineF((NBS_WIDTH/j)*i+dev, 10, (NBS_WIDTH/j)*i+dev, NBS_HEIGHT-12))
			qp.drawLine(QtCore.QLineF(10, (NBS_WIDTH/j)*i+dev, NBS_HEIGHT-12, (NBS_WIDTH/j)*i+dev))
			dev +=2
		qp.end()

	def place_holes(self):
		for col in range(9):
			temp = []
			for row in range(9):
				hole = computerHole(self, row, col)
				self.grid.addWidget(hole, row, col)
				temp.append(hole)
			self.holes.append(temp[:])

	def placeShips(self):
		for ship in self.ships:
			temp = []
			if ship[0] == ship[2]:			
				for i in range(ship[4]):	
					self.holes[ship[0]][ship[1]+i].isShip()
					temp.append(self.holes[ship[0]][ship[1]+i])
			else:
				for i in range(ship[4]):	
					self.holes[ship[0]+i][ship[1]].isShip()
					temp.append(self.holes[ship[0]+i][ship[1]])
			temp2 = [temp[:],False]
			self.status.append(temp2)

	def check(self):
		for i in self.status:
			if i[1] == False:
				temp = True			
				for e in i[0]:
					if e.hit == False:
						temp = False
				i[1] = temp
				if i[1] == True:
					for j in i[0]:
						j.sunken()

		end = True
		for i in self.status:
			if i[1] == False:
				end = False
		if end == True:
			reply = winMessage().exec_()
			if reply == QtWidgets.QMessageBox.Yes:
				self.parent.parent.setup()
			elif reply == QtWidgets.QMessageBox.No:
				quit()

	def move(self):
		choice = random.choice(self.choices)
		self.choices.remove(choice)
		self.parent.board.holes[choice[0]][choice[1]].addPeg()
		self.turn = False
		
	def createChoices(self):
		for i in range(9):
			for e in range(9):
				self.choices.append([i,e])
				
class computerHole(QtWidgets.QWidget):
	def __init__(self, parent, e, i):
		QtWidgets.QWidget.__init__(self,parent)
		self.peg = False
		self.ship = False
		self.hit = False
		self.circle = 10
		self.x = i
		self.y = e
		self.parent = parent

	def paintEvent(self, event):
		if self.peg == True and self.ship == True:
			qp = QtGui.QPainter()
			qp.begin(self)
			brush = QtGui.QBrush(QtGui.QColor(255,0,0,255))
			qp.setBrush(brush)
			qp.drawEllipse(self.circle,self.circle,20,20)
			qp.end()
		elif self.peg == True and self.ship == False:
			qp = QtGui.QPainter()
			qp.begin(self)
			brush = QtGui.QBrush(QtGui.QColor(0,255,0,255))
			qp.setBrush(brush)
			qp.drawEllipse(self.circle,self.circle,20,20)
			qp.end()
		else:
			qp = QtGui.QPainter()
			qp.begin(self)
			brush = QtGui.QBrush(QtGui.QColor(255,255,255,255))
			qp.setBrush(brush)
			qp.drawEllipse(self.circle,self.circle,20,20)
			qp.end()

	def mousePressEvent(self, event):
		if self.peg == False and self.parent.turn == False:
			if self.ship == True:
				self.peg = True
				self.hit = True
				self.update()
				self.parent.check()
				self.parent.turn = True
				self.parent.move()
			else:
				self.peg = True
				self.update()
				self.parent.turn = True
				self.parent.move()

	def isShip(self):
		self.ship = True
		self.update()

	def sunken(self):
		p = self.palette()
		p.setBrush(self.backgroundRole(), QtGui.QColor(255,0,0,255))
		self.setPalette(p)
		self.setAutoFillBackground(True)

class playerHole(QtWidgets.QWidget):
	def __init__(self, parent, e, i):
		QtWidgets.QWidget.__init__(self,parent)
		self.parent = parent
		self.peg = False
		self.ship = False
		self.hit = False
		self.circle = 10
		self.x = i
		self.y = e
		self.ship = False

	def paintEvent(self, event):
		if self.peg == True and self.hit == True:
			qp = QtGui.QPainter()
			qp.begin(self)
			brush = QtGui.QBrush(QtGui.QColor(255,0,0,255))
			qp.setBrush(brush)
			qp.drawEllipse(self.circle,self.circle,20,20)
			qp.end()
		elif self.peg == True and self.hit == False:
			qp = QtGui.QPainter()
			qp.begin(self)
			brush = QtGui.QBrush(QtGui.QColor(0,255,0,255))
			qp.setBrush(brush)
			qp.drawEllipse(self.circle,self.circle,20,20)
			qp.end()
		else:
			qp = QtGui.QPainter()
			qp.begin(self)
			brush = QtGui.QBrush(QtGui.QColor(255,255,255,255))
			qp.setBrush(brush)
			qp.drawEllipse(self.circle,self.circle,20,20)
			qp.end()

	def addPeg(self):
		if self.ship == True:
			self.peg = True
			self.hit = True
			self.update()
			self.parent.check()
			self.parent.parent.enemyBoard.turn = False
		else:
			self.peg = True
			self.update()
			self.parent.parent.enemyBoard.turn = False			
	
	def isShip(self):
		self.ship = True
		p = self.palette()
		p.setBrush(self.backgroundRole(), QtGui.QColor(192,192,192,255))
		self.setPalette(p)
		self.setAutoFillBackground(True)
		self.update()

	def sunken(self):
		p = self.palette()
		p.setBrush(self.backgroundRole(), QtGui.QColor(255,0,0,255))
		self.setPalette(p)
        
class quitMessage(QtWidgets.QMessageBox):
    def __init__(self):
        QtWidgets.QMessageBox.__init__(self)
        self.setText("Are you sure you'd like to quit?")
        self.addButton(self.No)  
        self.addButton(self.Yes)      

class winMessage(QtWidgets.QMessageBox):
	def __init__(self):
		QtWidgets.QMessageBox.__init__(self)
		self.setText("Congrats, Would you like to play again?")
		self.addButton(self.Yes)
		self.addButton(self.No)

class loseMessage(QtWidgets.QMessageBox):
	def __init__(self):
		QtWidgets.QMessageBox.__init__(self)
		self.setText("You Lose, Would you like to play again?")
		self.addButton(self.Yes)
		self.addButton(self.No)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = gameWindow()
    app.exec_()
