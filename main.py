"""
NeoBattleship main.py

"""
import sys, random
from PyQt5 import QtWidgets, QtCore, QtGui

#[x1,y1,x2,y2,length]
SHIPS = [[[4,0,4,3,4],[0,1,2,1,3],[0,3,1,3,2]], [[1,2,4,2,4],[0,4,0,6,3],[4,7,5,7,2]], [[2,0,5,0,4],[6,4,6,6,3],[0,7,0,8,2]], [[8,0,8,3,4],[5,6,7,6,3],[3,2,4,2,2]], [[7,1,7,4,4],[2,2,2,4,3],[4,8,5,8,2]]]

class gameWindow(QtWidgets.QMainWindow):
	def __init__(self):
		QtWidgets.QWidget.__init__(self)
		self.setWindowTitle("NeoBattleship")
		#set up menu bar with options
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
		#set background color
		b = QtGui.QBrush(QtGui.QImage('metal.jpg'))
		p = self.palette()
		p.setBrush(self.backgroundRole(), b)
		self.setPalette(p)
		self.setAutoFillBackground(True)
		self.setup()
		#store parent needed for restart mid-game
		self.parent = parent

	def setup(self):
		self.player = Player(self)
		self.enemy = Computer(self)
		self.grid = QtWidgets.QGridLayout()
		self.setLayout(self.grid)
		self.grid.addWidget(self.enemy, 0,0,1,1)
		self.grid.addWidget(self.player, 0,1,1,1)         

class Player(QtWidgets.QWidget):
	def __init__(self, parent):
		QtWidgets.QWidget.__init__(self, parent)
		#set the size of board
		self.setFixedSize(APP_WIDTH, APP_HEIGHT)
		#set background as water imaqe
		b = QtGui.QBrush(QtGui.QImage('water.bmp'))
		p = self.palette()
		p.setBrush(self.backgroundRole(), b)
		self.setPalette(p)
		self.setAutoFillBackground(True)
		#create grid layout and populate with hole widgets
		self.grid = QtWidgets.QGridLayout()
		self.setLayout(self.grid)
		self.grid.setSpacing(0)
		self.holes = []
		self.place_holes()
		#choose random ship mapping and place ships
		#room for improvement
		self.ships = random.choice(SHIPS)
		self.status = []	
		self.placeShips()
		#store parent
		self.parent = parent

	#draw grid
	def paintEvent(self, event):
		qp = QtGui.QPainter()
		qp.begin(self)
		pen = qp.pen()
		pen.setColor(QtGui.QColor(255,255,255,255))
		qp.setPen(pen)
		for i in range(9):		
			qp.drawLine(QtCore.QLine(self.holes[i][0].x(), self.holes[i][0].y(), self.holes[i][8].x(), self.holes[i][8].y() + self.holes[i][8].height()))
			qp.drawLine(QtCore.QLine(self.holes[0][i].x(), self.holes[0][i].y(), self.holes[8][i].x() + self.holes[8][i].width(), self.holes[8][i].y()))

		qp.drawLine(QtCore.QLine(self.holes[8][0].x() + self.holes[8][0].width(), self.holes[8][0].y(),self.holes[8][0].x() + self.holes[8][0].width(), self.holes[8][8].y() + self.holes[i][8].height()))
		qp.drawLine(QtCore.QLine(self.holes[0][8].x(), self.holes[0][8].y() + self.holes[0][8].height(), self.holes[8][8].x() + self.holes[8][8].width(), self.holes[8][8].y() + self.holes[8][8].height()))
		qp.end()

	#populate grid layout with widgets
	def place_holes(self):
		for row in range(9):
			temp = []
			for col in range(9):
				hole = playerHole(self)
				self.grid.addWidget(hole, col, row)
				temp.append(hole)
			self.holes.append(temp[:])

	#use random ship layout and mark necessary
	#widgets
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

	#Called after computer turn
	#checks ships and marks and sunken if necessary
	#check if computer has won
	#call lose message if necessary
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
		#set the size of board
		self.setFixedSize(APP_WIDTH, APP_HEIGHT)
		#set background as water imaqe
		b = QtGui.QBrush(QtGui.QImage('water.bmp'))
		p = self.palette()
		p.setBrush(self.backgroundRole(), b)
		self.setPalette(p)
		self.setAutoFillBackground(True)
		#create grid layout and populate with hole widgets
		self.grid = QtWidgets.QGridLayout()
		self.setLayout(self.grid)
		self.grid.setSpacing(0)
		self.holes = []	
		self.place_holes()
		#create grid in order to keep track of computer moves
		self.choices = []
		self.createChoices()
		#choose random ship mapping	and place ships
		#room for improvement
		self.ships = random.choice(SHIPS)
		self.status = []
		self.placeShips()
		#store parent and turn tracker
		self.parent = parent
		self.turn = False
		#self.hit = False
		#self.vertical = True
		#self.jump = 1

	#draw grid
	def paintEvent(self, event):
		qp = QtGui.QPainter()
		qp.begin(self)
		pen = qp.pen()
		pen.setColor(QtGui.QColor(255,255,255,255))
		qp.setPen(pen)
		for i in range(9):		
			qp.drawLine(QtCore.QLine(self.holes[i][0].x(), self.holes[i][0].y(), self.holes[i][8].x(), self.holes[i][8].y() + self.holes[i][8].height()))
			qp.drawLine(QtCore.QLine(self.holes[0][i].x(), self.holes[0][i].y(), self.holes[8][i].x() + self.holes[8][i].width(), self.holes[8][i].y()))

		qp.drawLine(QtCore.QLine(self.holes[8][0].x() + self.holes[8][0].width(), self.holes[8][0].y(),self.holes[8][0].x() + self.holes[8][0].width(), self.holes[8][8].y() + self.holes[i][8].height()))
		qp.drawLine(QtCore.QLine(self.holes[0][8].x(), self.holes[0][8].y() + self.holes[0][8].height(), self.holes[8][8].x() + self.holes[8][8].width(), self.holes[8][8].y() + self.holes[8][8].height()))
		qp.end()

	#populate grid layout with widgets
	def place_holes(self):
		for row in range(9):
			temp = []
			for col in range(9):
				hole = computerHole(self)
				self.grid.addWidget(hole, col, row)
				temp.append(hole)
			self.holes.append(temp[:])

	#use random ship layout and mark necessary widgets
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

	#Called after player turn
	#checks ships and marks and sunken if necessary
	#check if player has won
	#call win message if necessary
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

	#simple function that makes random computer move
	#room for improvement
	def move(self):
		#if self.hit == False:	
		#self.vertical = True
		choice = random.choice(self.choices)
		self.choices.remove(choice)
		self.hit = self.parent.player.holes[choice[0]][choice[1]].addPeg()
		#if self.hit == True:
		#	self.choice = choice
		"""elif self.hit == True:		
			if self.vertical == True:
				if self.jump == 1:
					temp = self.choice[:]
					temp[1]+=self.jump
					if temp not in self.choices:
						self.jump = -1
						return False
					elif temp[1] > 8:
						self.jump = -1
						return False
					else:
						self.choices.remove(temp)
						self.hit = self.parent.player.holes[temp[0]][temp[1]].addPeg()
						if self.hit == False:
							self.hit = True
							self.jump = -1
						else:
							if self.holes[temp[0]][temp[1]].sunk == True:
								self.hit = False
								self.jump = 1
								return True
							else:
								self.jump += 1
				elif self.jump == -1:
					temp = self.choice[:]
					temp[1]+=self.jump
					if temp not in self.choices:
						self.vertical = False
						self.jump = 1
						return False
					elif temp[1] < 0:
						self.vertical = False
						self.jump = 1
						return False
					else:
						self.choices.remove(temp)
						self.hit = self.parent.player.holes[temp[0]][temp[1]].addPeg()						
						if self.hit == False:
							self.hit = True
							self.vertical = False
							self.jump = 1
						else:
							if self.holes[temp[0]][temp[1]].sunk == True:
								self.hit = False
								self.jump = 1
								return True
							else:
								self.jump -= 1				

				else:
					temp = self.choice[:]
					temp[1]+=self.jump
					if temp not in self.choices:
						if self.jump > 0:
							self.jump = -1
							return False
					elif temp[1] > 8:
						self.jump = -1
					elif temp[1] < 0:
						if self.holes[temp[0]][temp[1]].sunk == True:
							self.hit = False
							self.jump = 1
							return True
					else:	
						self.choices.remove(temp)
						self.hit = self.parent.player.holes[temp[0]][temp[1]].addPeg()
						if self.hit == True:
							if self.jump > 0:
								self.jump+=1
							else:
								self.jump-=1
							if self.holes[temp[0]][temp[1]].sunk == True:
								self.hit = False
								return True
						else:
							if self.holes[temp[0]][temp[1]].sunk == True:
								self.hit = False
								self.jump = 1
								return True
							else:
								self.hit = True
								self.jump = -1
			elif self.vertical == False:
				if self.jump == 1:
					temp = self.choice[:]
					temp[0]+=self.jump
					if temp not in self.choices:
						self.jump = -1
						return False
					elif temp[0] > 8:
						self.jump = -1
					else:
						self.choices.remove(temp)
						self.hit = self.parent.player.holes[temp[0]][temp[1]].addPeg()
						if self.hit == False:
							self.hit = True
							self.jump = -1
						else:
							if self.holes[temp[0]][temp[1]].sunk == True:
								self.hit = False
								self.jump = 1
								return True
							else:
								self.jump += 1				
				elif self.jump == -1:
					temp = self.choice[:]
					temp[0]+=self.jump
					if temp not in self.choices:
						self.jump = 1
						self.hit = False
						return False
					self.choices.remove(temp)
					self.hit = self.parent.player.holes[temp[0]][temp[1]].addPeg()
					if self.holes[temp[0]][temp[1]].sunk == True:
						self.hit = False
						self.jump = 1
						return True
					else:
						self.jump -= 1
				else:
					temp = self.choice[:] 
					temp[0]+=self.jump
					if temp not in self.choices:
						if self.jump > 0:
							self.jump = -1
							return False
						else:
							self.jump = 1
							self.hit = False
							return False
					elif temp[0] > 8:
						self.jump = -1	
					elif temp[0] < 0:
						if self.holes[temp[0]][temp[1]].sunk == True:
							self.hit = False
							self.jump = 1
							return True			
					else:
						self.choices.remove(temp)
						self.hit = self.parent.player.holes[temp[0]][temp[1]].addPeg()
						if self.hit == True:
							if self.jump > 0:
								self.jump+=1
							else:
								self.jump-=1
							if self.holes[temp[0]][temp[1]].sunk == True:
								self.hit = False
								self.jump= 1
								return True
						else:
							if self.holes[temp[0]][temp[1]].sunk == True:
								self.hit = False
								self.jump = 1
								return True
							else:
								self.hit = True
								self.jump = -1				

			return True"""
		
	def createChoices(self):
		for i in range(9):
			for e in range(9):
				self.choices.append([i,e])
				
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
		self.circle = (APP_HEIGHT*2)/(self.width()/2)
		
	#draw hole depending on status of hole
	#hit = red
	#miss = green
	#unvisited = white
	def paintEvent(self, event):
		if self.peg == True and self.ship == True and self.sunk == False:
			qp = QtGui.QPainter()
			qp.begin(self)
			brush = QtGui.QBrush(QtGui.QImage('explosion.jpg'))
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
			if self.ship == True:
				self.peg = True
				self.hit = True
				self.update()
				self.parent.check()
			else:
				self.peg = True
				self.update()

			self.parent.turn = True
			#temp = self.parent.move()
			self.parent.move()
			"""while temp == False:
				self.parent.turn = True
				temp = self.parent.move()"""
			self.parent.turn = False

	#Used by parent function to keep track of ship widgets
	def isShip(self):
		self.ship = True
		self.update()

	#color ship red when it sinks
	def sunken(self):
		self.sunk = True
		b = QtGui.QBrush(QtGui.QImage('explosion.jpg'))
		p = self.palette()
		p.setBrush(self.backgroundRole(), b)
		self.setPalette(p)
		self.setAutoFillBackground(True)

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
		self.circle = (APP_HEIGHT*2)/(self.width()/2)

	#draw hole depending on status of hole
	#hit = red
	#miss = green
	#unvisited = white
	def paintEvent(self, event):
		if self.peg == True and self.hit == True and self.sunk == False:
			qp = QtGui.QPainter()
			qp.begin(self)
			brush = QtGui.QBrush(QtGui.QImage('explosion.jpg'))
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
			return True
		else:
			self.peg = True
			self.update()
			self.parent.parent.enemy.turn = False
			return False			
	
	#Used by parent function to keep track of ship widgets
	#makes player ships visible
	def isShip(self):
		self.ship = True
		b = QtGui.QBrush(QtGui.QImage('ship.jpg'))
		p = self.palette()
		p.setBrush(self.backgroundRole(), b)
		self.setPalette(p)
		self.setAutoFillBackground(True)
		self.update()

	#color ship red when it sinks
	def sunken(self):
		self.sunk = True
		b = QtGui.QBrush(QtGui.QImage('explosion.jpg'))
		p = self.palette()
		p.setBrush(self.backgroundRole(), b)
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

if __name__ == "__main__":
		app = QtWidgets.QApplication(sys.argv)
		size =  app.desktop().screenGeometry()
		APP_HEIGHT = size.width()/3
		APP_WIDTH = size.width()/3
		main_window = gameWindow()
		app.exec_()
