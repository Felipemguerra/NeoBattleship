"""
NeoBattleship main.py

"""
import sys, pickle
from PyQt5 import QtWidgets, QtCore, QtGui

NBS_HEIGHT = 800/2
NBS_WIDTH = 800/2

#NBS_HEIGHT = NBS_HEIGHT
#NBS_WIDTH = NBS_WIDTH

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
        #self.new_btn = startNewGameBtn(self)
        #self.quit_btn = quitBtn(self)

        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)

        #self.grid.addWidget(self.gameGrid, 1, 1, 1, 4)
        self.grid.addWidget(self.board, 2, 1, 1, 4)
        self.grid.addWidget(self.enemyBoard, 1, 1, 1, 4)
        #self.grid.addWidget(self.new_btn, 3, 1, 1, 1)
        #self.grid.addWidget(self.quit_btn, 3, 2, 1, 1)           

class waterBoard(QtWidgets.QWidget):

    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        self.hole = []
        """
        Later on we can change this to new sizes based on screen aspect ratio and screen resolution
        it will dynamically change all of the other sizes as well.
        """
        self.setFixedSize(NBS_WIDTH, NBS_HEIGHT)
        p = self.palette()
        p.setColor(self.backgroundRole(), QtGui.QColor(0,100,145,255))
        self.setPalette(p)
        self.setAutoFillBackground(True)
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.setSpacing(0)
        self.place_spots()
        

    def paintEvent(self, event):
        points_list =  [QtCore.QPoint(10,10), QtCore.QPoint(10,NBS_HEIGHT-10),
                        QtCore.QPoint(NBS_WIDTH-10,NBS_HEIGHT-10), QtCore.QPoint(NBS_WIDTH-10,10)]
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

        j = 10
        hlines = []
        vlines = []
        for i in range(j):
            hline = QtCore.QLineF(20, (NBS_WIDTH/j)*i+20, NBS_HEIGHT-20, (NBS_WIDTH/j)*i+20)
            vline = QtCore.QLineF((NBS_HEIGHT/j)*i+20, 20, (NBS_HEIGHT/j)*i+20, NBS_WIDTH-20)
            hlines.append(hline) 
            vlines.append(vline)

        qp = QtGui.QPainter()
        qp.begin(self)
        brush = QtGui.QBrush()
        brush.setTextureImage(QtGui.QImage("water2_256.bmp"))
        qp.setBrush(brush)
        qp.drawPolygon(square)
        qp.drawLines(hlines)
        qp.drawLines(vlines) 
        qp.end()


    def place_spots(self):
        for row in range(5):
            row_list = []
            rowLayout = QtWidgets.QHBoxLayout()
            self.vbox.addLayout(rowLayout)
            rowLayout.addStretch(1)
            for col in range(5):
                spot = gridSpot(self)
                rowLayout.addWidget(spot,0)
            rowLayout.addStretch(1)


class gridSpot(QtWidgets.QWidget):
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)
        self.spot = None

    def addPeg(self):
        self.peg = Peg(self)
        self.grid.addWidget(self.peg)

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self) 
        brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
        qp.setBrush(brush)
        qp.drawEllipse(QtCore.QPointF(60,45), 6, 6)
        qp.end()

    def minimumSizeHint(self):
        return QtCore.QSize(120,90)   

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
