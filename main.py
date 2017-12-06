"""
NeoBattleship main.py

"""
import sys, pickle
from PyQt5 import QtWidgets, QtCore, QtGui

NBS_HEIGHT = 800/2
NBS_WIDTH = 800/2

class gameWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setup()

    def setup(self):
        self.setWindowTitle("NeoBattleship - Naval Simulator")

        self.game_grid = gameGrid(self)
        self.setCentralWidget(self.game_grid)
        
        exit_action = QtWidgets.QAction("Exit", self)
        exit_action.triggered.connect(QtWidgets.qApp.quit)
        start_game = QtWidgets.QAction("Start New Game", self)
        start_game.triggered.connect(self.startNewGame)
        
        
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)
        file_menu = menu_bar.addMenu("Options")
        file_menu.addAction(exit_action)
        file_menu.addAction(start_game)      

        self.show()
        
    def closeEvent(self, event):
        reply = quitMessage().exec_()
        if (reply == QtWidgets.QMessageBox.Yes):
            event.accept()
        else:
            event.ignore()

    def startNewGame(self, event):
        reply = startNewGameMessage().exec_()
        if (reply == QtWidgets.QMessageBox.Yes):
            event.accept()#Does nothing for now
        else:
            event.ignore()#Does nothing for now
            
class gameGrid(QtWidgets.QWidget):
	def __init__(self, parent):
		QtWidgets.QWidget.__init__(self)
		p = self.palette()
		p.setColor(self.backgroundRole(), QtGui.QColor(150,150,150,255))
		self.setPalette(p)
		self.setAutoFillBackground(True)
		self.setup()

	def setup(self):
		self.board = Player(self)
		self.enemyBoard = Computer(self)
		#self.new_btn = startNewGameBtn(self)
		#self.quit_btn = quitBtn(self)
		self.grid = QtWidgets.QGridLayout()
		self.setLayout(self.grid)
		self.grid.addWidget(self.enemyBoard, 0,0,1,1)
		self.grid.addWidget(self.board, 1,0,1,1)		
		#self.grid.addWidget(self.new_btn, 2, 0, 1, 1)
		#self.grid.addWidget(self.quit_btn, 3, 0, 1, 1)           

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
		self.holes = []		
		self.place_holes()
		#self.twoship = twoShip(self, [1,0], [2,0])
		#self.threeship = threeShip(self, [0,1], [2,1])
		#self.fourship = fourShip(self, [0,2], [3,2])
		#self.place_ships()

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

	def place_ships(self):
		for row in range(9):
			for col in range(9):
				self.holes[row][col].placement = False

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
		self.holes = []		
		self.place_holes()
		#possible function to get ships placements
		#[x1,y1,x2,y2,length]
		self.ships = [[4,0,4,3,4],[0,1,2,1,3],[0,2,1,2,2]]
		self.positions = []
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
				hole = computerHole(self, row, col)
				self.grid.addWidget(hole, row, col)
				temp.append(hole)
			self.holes.append(temp[:])

	def placeShips(self):
		for ship in self.ships:
			if ship[0] == ship[2]:			
				for i in range(ship[4]):	
					self.holes[ship[0]][i].isShip()
			else:
				for i in range(ship[4]):	
					self.holes[i][ship[1]].isShip()

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

	def checkPositions(self):
		if len(self.positions) == 0:
			reply = winMessage().exec_()
			if (reply == QtWidgets.QMessageBox.Ok):
				quit()
				
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
		if self.peg == False:
			if self.ship == True:
				self.peg = True
				self.hit = True
				self.update()
				self.parent.positions.remove([self.x,self.y])
				self.parent.checkPositions()
			else:
				self.peg = True
				self.update()			

	def isShip(self):
		self.ship = True
		self.update()

class playerHole(QtWidgets.QWidget):
	def __init__(self, parent, e, i):
		QtWidgets.QWidget.__init__(self,parent)
		self.peg = False
		self.ship = False
		self.hit = False
		self.circle = 10
		self.placement = True
		self.x = i
		self.y = e

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
		self.peg = True
		self.update()

	def mousePressEvent(self, event):
		if self.placement == True:
			p = self.palette()
			p.setColor(self.backgroundRole(), QtGui.QColor(192,192,192,255))
			self.setPalette(p)
			self.setAutoFillBackground(True)
			self.placement = False

"""class twoShip(QtWidgets.QWidget):
	def __init__(self, parent, p1, p2):
		QtWidgets.QWidget.__init__(self, parent)
		self.resize(parent.size())
		self.points = []
		self.vertical = False
		if p1[0] == p2[0]:
			self.vertical = True	
			for i in range(2):	
				self.points.append([0,i])
		else:
			self.vertical = False
			for i in range(2):
				self.points.append([i,0])

	def paintEvent(self, event):
		qp = QtGui.QPainter()
		qp.begin(self)
		brush = QtGui.QBrush(QtGui.QColor(192,192,192,150))
		qp.setBrush(brush)
		if self.vertical == True:
			qp.drawEllipse(self.points[0][0]+15, self.points[0][1]+12, 30, 80)
		else:
			qp.drawEllipse(self.points[0][0]+12, self.points[0][1]+15, 80, 30)
		qp.end()

class threeShip(QtWidgets.QWidget):

class =fourShip(QtWidgets.QWidget):

"""

"""class startNewGameBtn(QtWidgets.QPushButton):
	def __init__(self, parent):
		QtWidgets.QPushButton.__init__(self, parent)
		self.setText("Start New Game")
		self.setMaximumSize(150,100)
        
class quitBtn(QtWidgets.QPushButton):
	def __init__(self, parent):
		QtWidgets.QPushButton.__init__(self, parent)
		self.clicked.connect(QtWidgets.qApp.quit)
		self.setText("Quit")
		self.setMaximumSize(100,100)
"""        
class quitMessage(QtWidgets.QMessageBox):
    def __init__(self):
        QtWidgets.QMessageBox.__init__(self)
        self.setText("Are you sure you'd like to quit?")
        self.addButton(self.No)  
        self.addButton(self.Yes)   

class startNewGameMessage(QtWidgets.QMessageBox):
    def __init__(self):
        QtWidgets.QMessageBox.__init__(self)
        self.setText("Are you sure you'd like to start a new game?")
        self.addButton(self.No)  
        self.addButton(self.Yes)    

class winMessage(QtWidgets.QMessageBox):
	def __init__(self):
		QtWidgets.QMessageBox.__init__(self)
		self.setText("Congrats")
		self.addButton(self.Ok) 

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = gameWindow()
    app.exec_()
