from PyQt5 import QtWidgets, QtCore, QtGui
import computerhole, shared, random

class computer(QtWidgets.QWidget):
	def __init__(self, parent, diff):
		QtWidgets.QWidget.__init__(self, parent)
		#set the size of board
		self.setFixedSize(shared.APP_WIDTH, shared.APP_HEIGHT)
		#set background as water imaqe
		b = QtGui.QBrush(QtGui.QImage('images/water.bmp'))
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
		#choose random ship mapping and place ships
		#room for improvement
		self.ships = random.choice(shared.SHIPS)
		self.status = []
		self.placeShips()
		#store all necessary information
		self.parent = parent
		self.turn = False
		self.hit = False
		self.vertical = True
		self.jump = 1
		self.difficulty = diff

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
				hole = computerhole.computerHole(self)
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
			reply = shared.winMessage().exec_()
			if reply == QtWidgets.QMessageBox.Yes:
				self.parent.parent.setup()
			elif reply == QtWidgets.QMessageBox.No:
				quit()

	#simple function that makes random computer move
	def move(self):
		if self.difficulty == 0:
			choice = random.choice(self.choices)
			self.choices.remove(choice)
			self.parent.player.holes[choice[0]][choice[1]].addPeg()
		elif self.difficulty == 1:
			if self.hit == False:	
				self.vertical = True
				self.jump = 1
				choice = random.choice(self.choices)
				self.choices.remove(choice)
				self.parent.player.holes[choice[0]][choice[1]].addPeg()
				self.hit = self.parent.player.holes[choice[0]][choice[1]].hit
				if self.hit == True:
					self.choice = choice
			elif self.hit == True:
				temp = self.decision()
				while temp == False:
					temp = self.decision()
		elif self.difficulty == 2:
			#Missing third difficulty
			None			

	#decision algorithm only works if ships are not place directly touching
	def decision(self):		
		if self.vertical == True:
			temp = self.choice[:]
			temp[1]+=self.jump
			if temp not in self.choices:
				if self.jump > 0:
					self.jump = -1
					return False
				elif self.jump == -1:
					self.jump = 1
					self.vertical = False
					return False
				elif self.jump < -1:
					print("battleship/computer.py	error 302")
					self.hit = False
			else:
				self.choices.remove(temp)
				self.parent.player.holes[temp[0]][temp[1]].addPeg()
				if self.parent.player.holes[temp[0]][temp[1]].hit == True:
					if self.jump > 0:
						self.jump += 1
					elif self.jump < 0:
						self.jump -= 1
					if self.parent.player.holes[self.choice[0]][self.choice[1]].sunk == True:
						self.hit = False
				elif self.parent.player.holes[temp[0]][temp[1]].hit == False:				
					if self.jump > 0:
						self.jump = -1
					elif self.jump == -1:
						self.jump = 1
						self.vertical = False
					elif self.jump < -1:
						print("battleship/computer.py	error 321")
						self.hit = False
		#Horizontal
		elif self.vertical == False:
			temp = self.choice[:]
			temp[0]+=self.jump
			if temp not in self.choices:
				if self.jump > 0:
					self.jump = -1
					return False
				elif self.jump < 0:
					print("battleship/computer.py	error 332")
					self.hit = False
			else:
				self.choices.remove(temp)
				self.parent.player.holes[temp[0]][temp[1]].addPeg()
				if self.parent.player.holes[temp[0]][temp[1]].hit == True:
					if self.jump > 0:
						self.jump += 1
					elif self.jump < 0:
						self.jump -= 1
					if self.parent.player.holes[self.choice[0]][self.choice[1]].sunk == True:
						self.hit = False
				elif self.parent.player.holes[temp[0]][temp[1]].hit == False:
					if self.jump > 0:
						self.jump = -1
					elif self.jump < 0:
						print("battleship/computer.py	error 348")
						self.hit = False		
		return True
		
	def createChoices(self):
		for i in range(9):
			for e in range(9):
				self.choices.append([i,e])


