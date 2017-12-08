"""
NeoBattleship main.py

"""
import sys, board, shared
from PyQt5 import QtWidgets, QtGui

class gameWindow(QtWidgets.QMainWindow):
	def __init__(self):
		QtWidgets.QWidget.__init__(self)
		self.setWindowTitle("NeoBattleship")
		#set up menu bar with options
		exit_action = QtWidgets.QAction("Exit", self)
		exit_action.triggered.connect(self.close)
		restart_action = QtWidgets.QAction("Restart", self)
		restart_action.triggered.connect(self.setup)
		medium_diff = QtWidgets.QAction("Medium", self)
		medium_diff.triggered.connect(self.set_medium)
		easy_diff = QtWidgets.QAction("Easy", self)
		easy_diff.triggered.connect(self.set_easy)
		menu_bar = self.menuBar()
		menu_bar.setNativeMenuBar(False)
		file_menu = menu_bar.addMenu("Options")
		file_menu.addAction(exit_action) 
		file_menu.addAction(restart_action)
		submenu = file_menu.addMenu("Difficulty")
		submenu.addAction(easy_diff)
		submenu.addAction(medium_diff)
		#default difficulty set to medium
		self.diff = 1	
		self.setup()

	def setup(self):	
		self.game_grid = board.gameboard(self, self.diff)
		self.setCentralWidget(self.game_grid)        
		self.show()

	def set_hard(self):
		self.diff = 2
		self.setup()

	def set_medium(self):
		self.diff = 1
		self.setup()
	
	def set_easy(self):
		self.diff = 0
		self.setup()
	
	def closeEvent(self, event):
		reply = quitMessage().exec_()
		if reply == QtWidgets.QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()

	def close(self):
		reply = quitMessage().exec_()
		if reply == QtWidgets.QMessageBox.Yes:
			QtWidgets.qApp.quit()

class quitMessage(QtWidgets.QMessageBox):
    def __init__(self):
        QtWidgets.QMessageBox.__init__(self)
        self.setText("Are you sure you'd like to quit?")
        self.addButton(self.No)  
        self.addButton(self.Yes)      

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	shared.set(app)
	main_window = gameWindow()
	app.exec_()
