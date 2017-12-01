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
        
        
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)
        file_menu = menu_bar.addMenu("Options")
        file_menu.addAction(exit_action)      

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
		p.setColor(self.backgroundRole(), QtGui.QColor(150,177,210,255))
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
		#self.grid.addWidget(self.new_btn, 3, 1, 1, 1)
		#self.grid.addWidget(self.quit_btn, 3, 2, 1, 1)           

class Player(QtWidgets.QWidget):
	def __init__(self, parent):
		QtWidgets.QWidget.__init__(self, parent)
		self.setFixedSize(NBS_WIDTH, NBS_HEIGHT)
		self.grid = QtWidgets.QGridLayout()
		self.setLayout(self.grid)
		self.grid.setSpacing(0)
		self.holes = []		
		self.place_holes()

	def paintEvent(self, event):
		qp = QtGui.QPainter()
		qp.begin(self)
		j = 10
		dev = 10
		for i in range(j):
			qp.drawLine(QtCore.QLineF((NBS_WIDTH/j)*i+dev, 10, (NBS_WIDTH/j)*i+dev, NBS_HEIGHT-12))
			qp.drawLine(QtCore.QLineF(10, (NBS_WIDTH/j)*i+dev, NBS_HEIGHT-12, (NBS_WIDTH/j)*i+dev))
			dev +=2
			
		qp.end()

	def place_holes(self):
		for i in range(9):
			row = []
			for e in range(9):
				hole = playerHole(self)
				self.grid.addWidget(hole,i,e)
				row.append(hole)
			self.holes.append(row[:])

class Computer(QtWidgets.QWidget):
	def __init__(self, parent):
		QtWidgets.QWidget.__init__(self, parent)
		self.setFixedSize(NBS_WIDTH, NBS_HEIGHT)
		self.grid = QtWidgets.QGridLayout()
		self.setLayout(self.grid)
		self.grid.setSpacing(0)
		self.holes = []		
		self.place_holes()

	def paintEvent(self, event):
		qp = QtGui.QPainter()
		qp.begin(self)
		j = 10
		dev = 10
		for i in range(j):
			qp.drawLine(QtCore.QLineF((NBS_WIDTH/j)*i+dev, 10, (NBS_WIDTH/j)*i+dev, NBS_HEIGHT-12))
			qp.drawLine(QtCore.QLineF(10, (NBS_WIDTH/j)*i+dev, NBS_HEIGHT-12, (NBS_WIDTH/j)*i+dev))
			dev +=2
			
		qp.end()

	def place_holes(self):
		for i in range(9):
			row = []
			for e in range(9):
				hole = computerHole(self)
				self.grid.addWidget(hole,i,e)
				row.append(hole)
			self.holes.append(row[:])

class computerHole(QtWidgets.QWidget):
	def __init__(self, parent):
		QtWidgets.QWidget.__init__(self,parent)
		self.peg = False
		self.hit = False
		self.x = 10
		self.y = 10

	def paintEvent(self, event):
		if self.peg == True and self.hit == True:
			qp = QtGui.QPainter()
			qp.begin(self)
			brush = QtGui.QBrush(QtGui.QColor(255,0,0,255))
			qp.setBrush(brush)
			qp.drawEllipse(self.x,self.y,20,20)
			qp.end()
		elif self.peg == True and self.hit == False:
			qp = QtGui.QPainter()
			qp.begin(self)
			brush = QtGui.QBrush(QtGui.QColor(0,255,0,255))
			qp.setBrush(brush)
			qp.drawEllipse(self.x,self.y,20,20)
			qp.end()
		else:
			qp = QtGui.QPainter()
			qp.begin(self)
			brush = QtGui.QBrush(QtGui.QColor(0,0,0,255))
			qp.setBrush(brush)
			qp.drawEllipse(self.x,self.y,20,20)
			qp.end()

	def mousePressEvent(self, event):
		if self.peg == False:
			self.peg = True
			self.update()

class playerHole(QtWidgets.QWidget):
	def __init__(self, parent):
		QtWidgets.QWidget.__init__(self,parent)
		self.peg = False
		self.hit = False
		self.x = 10
		self.y = 10

	def paintEvent(self, event):
		if self.peg == True and self.hit == True:
			qp = QtGui.QPainter()
			qp.begin(self)
			brush = QtGui.QBrush(QtGui.QColor(255,0,0,255))
			qp.setBrush(brush)
			qp.drawEllipse(self.x,self.y,20,20)
			qp.end()
		elif self.peg == True and self.hit == False:
			qp = QtGui.QPainter()
			qp.begin(self)
			brush = QtGui.QBrush(QtGui.QColor(0,255,0,255))
			qp.setBrush(brush)
			qp.drawEllipse(self.x,self.y,20,20)
			qp.end()
		else:
			qp = QtGui.QPainter()
			qp.begin(self)
			brush = QtGui.QBrush(QtGui.QColor(0,0,0,255))
			qp.setBrush(brush)
			qp.drawEllipse(self.x,self.y,20,20)
			qp.end()

	def addPeg(self):
		self.peg = True
		self.update()

class ship(QtWidgets.QWidget):
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        self.resize(parent.size())

    def paintEvent(self, even):
        qp = QtGui.QPainter()
        qp.begin(self)
        brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
        brush.setColor(QtCore.Qt.red)
        qp.setBrush(brush)
        qp.drawEllipse(QtCore.QPointF(self.width()/2, self.height()/2, 10, 10))
        qp.end() 
	
class startNewGameBtn(QtWidgets.QPushButton):
    def __init__(self, parent):
        QtWidgets.QPushButton.__init__(self, parent)
        self.setText("Start New Game")
        self.move(20, 160)
        
class quitBtn(QtWidgets.QPushButton):
    def __init__(self, parent):
        QtWidgets.QPushButton.__init__(self, parent)
        self.clicked.connect(QtWidgets.qApp.quit)
        self.setText("Quit")
        self.move(150, 160)       
        
class quitMessage(QtWidgets.QMessageBox):
    def __init__(self):
        QtWidgets.QMessageBox.__init__(self)
        self.setText("Are you sure you'd like to quit?")
        self.addButton(self.No)  
        self.addButton(self.Yes)      


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = gameWindow()
    app.exec_()
