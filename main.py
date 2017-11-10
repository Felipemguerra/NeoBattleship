"""
NeoBattleship main.py

"""
import sys, pickle
from PyQt5 import QtWidgets, QtCore, QtGui


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
        self.new_btn = startNewGameBtn(self)
        self.quit_btn = quitBtn(self)

        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)

        self.grid.addWidget(self.board, 1, 1, 1, 4)
        self.grid.addWidget(self.new_btn, 2, 1, 1, 1)
        self.grid.addWidget(self.quit_btn, 2, 2, 1, 1)           

class waterBoard(QtWidgets.QWidget):
    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        """
        Later on we can change this to new sizes based on screen aspect ratio and screen resolution
        """
        self.setFixedSize(960, 720)
        p = self.palette()
        p.setColor(self.backgroundRole(), QtGui.QColor(0,100,145,255))
        self.setPalette(p)
        self.setAutoFillBackground(True)

    def paintEvent(self, event):
        points_list =  [QtCore.QPoint(20,20), QtCore.QPoint(20,700),
                        QtCore.QPoint(940,700), QtCore.QPoint(940,20)]
        square = QtGui.QPolygon(points_list)
        qp = QtGui.QPainter()
        qp.begin(self)
        pen = qp.pen()
        pen.setColor(QtCore.Qt.transparent)
        qp.setPen(pen)
        brush = QtGui.QBrush()
        brush.setTextureImage(QtGui.QImage("water2_256.bmp"))
        qp.setBrush(brush)
        qp.drawPolygon(square)
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
