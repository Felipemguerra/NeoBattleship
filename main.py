"""
NeoBattleship main.py

"""
import sys, pickle
from PyQt5 import QtWidgets, QtCore, QtGui

NBS_HEIGHT = 720/2
NBS_WIDTH = 960/2

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
        self.setup()

    def setup(self):
        self.board = waterBoard(self)
        self.enemyBoard = waterBoard(self)
        #self.gameGrid = playGrid(self)
        self.new_btn = startNewGameBtn(self)
        self.quit_btn = quitBtn(self)

        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)

        #self.grid.addWidget(self.gameGrid, 1, 1, 1, 4)
        self.grid.addWidget(self.board, 1, 1, 1, 4)
        self.grid.addWidget(self.enemyBoard, 2, 1, 1, 4)
        self.grid.addWidget(self.new_btn, 3, 1, 1, 1)
        self.grid.addWidget(self.quit_btn, 3, 2, 1, 1)           

class waterBoard(QtWidgets.QWidget):

    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        """
        Later on we can change this to new sizes based on screen aspect ratio and screen resolution
        it will dynamically change all of the other sizes as well.
        """
        self.setFixedSize(NBS_WIDTH, NBS_HEIGHT)
        p = self.palette()
        p.setColor(self.backgroundRole(), QtGui.QColor(0,100,145,255))
        self.setPalette(p)
        self.setAutoFillBackground(True)

    def paintEvent(self, event):
        points_list =  [QtCore.QPoint(20,20), QtCore.QPoint(20,NBS_HEIGHT-20),
                        QtCore.QPoint(NBS_WIDTH-20,NBS_HEIGHT-20), QtCore.QPoint(NBS_WIDTH-20,20)]
        square = QtGui.QPolygon(points_list)
        #hline = QtCore.QLine(20,40,NBS_WIDTH-20,40)
        #vline = QtCore.QLine(40,20,40,NBS_HEIGHT-20)  

        """
        Here we are generating a pair of x,y coords to draw a line between
        We're going to need two sets, one to draw horizontal lines, and one for vertical lines
        
        The gist of it here is that our range is the number of lines generated, with the 'length' of each line
        being non-changing values over each loop so that it connects to both ends of our board
        If we divide up our length into equal sections, then multiply that by i+1 so as to not draw extra lines
        We will get evenly spaced lines each offset by +20 to align with our game board
        """

        hlines = []
        for i in range(10):
            line = QtCore.QLineF(20, (NBS_HEIGHT/10)*(i+1)+20, NBS_WIDTH-20, (NBS_HEIGHT/10)*(i+1)+20)
            hlines.append(line)
        
        vlines = []
        for i in range(10):
            line = QtCore.QLineF((NBS_WIDTH/10)*(i+1)+20, 20, (NBS_WIDTH/10)*(i+1)+20, NBS_HEIGHT-20) 
            vlines.append(line) 


        qp = QtGui.QPainter()
        qp.begin(self)
        brush = QtGui.QBrush()
        brush.setTextureImage(QtGui.QImage("water2_256.bmp"))
        qp.setBrush(brush)
        qp.drawPolygon(square)
        qp.drawLines(hlines)
        qp.drawLines(vlines) 
        qp.end()



"""
class playGrid(QtWidgets.QWidget):
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        self.setFixedSize(NBS_HEIGHT,NBS_WIDTH)

    def paintEvent(self, event):
        hline = QtCore.QLine(0,0,0,NBS_HEIGHT-20)
        wline = QtCore.QLine(0,0,NBS_WIDTH-20,0)
        qp = QtGui.QPainter()
        qp.begin(self)
        
        qp.drawLine(hline)
        qp.drawLine(wline)
        qp.end()
"""
    
	
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
