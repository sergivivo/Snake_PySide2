from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from snake import Snake

class SnakeView(QGraphicsView):
    def __init__(self, parent=None):
        super(SnakeView, self).__init__()

        self.boxsize = 20
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def generateMap(self, rows=10, columns=15, updaterate=200):
        self.rows    = rows
        self.columns = columns
        xsize = columns * self.boxsize
        ysize = rows    * self.boxsize

        self.updaterate = updaterate

        # Create scene
        self.scene = QGraphicsScene()

        # Background
        brush = QBrush(QColor(181,214,227,255))
        self.scene.setBackgroundBrush(brush)
        self.scene.setSceneRect(0,0,xsize,ysize)
        self.setFixedSize(xsize,ysize)

        self.snake = Snake(columns, rows)

        # Print game
        self._updateMap()

        self.gameState = False

        self.setScene(self.scene)
        self.resetMatrix()

    def _updateMap(self):
        self.scene.clear()

        # Item
        brush = QBrush(QColor(133,232,94,255))
        xcord = self.snake.item[0] * self.boxsize
        ycord = self.snake.item[1] * self.boxsize
        self.scene.addRect(xcord, ycord, self.boxsize, self.boxsize, brush=brush)

        # Body
        brush = QBrush(QColor(0,193,255,255))
        for b in self.snake.body:
            xcord = b[0] * self.boxsize
            ycord = b[1] * self.boxsize
            self.scene.addRect(xcord, ycord, self.boxsize, self.boxsize, brush=brush)

        # Head
        brush = QBrush(QColor(255,255,255,255))
        xcord = self.snake.head[0] * self.boxsize
        ycord = self.snake.head[1] * self.boxsize
        self.scene.addRect(xcord, ycord, self.boxsize, self.boxsize, brush=brush)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Right:
            self.snake.updateHeading(0)
        elif event.key() == Qt.Key_Up:
            self.snake.updateHeading(1)
        elif event.key() == Qt.Key_Left:
            self.snake.updateHeading(2)
        elif event.key() == Qt.Key_Down:
            self.snake.updateHeading(3)

        if not self.gameState:
            self._startGame()

    def _startGame(self):
        self.gameState = True
        while not self.snake.death and not self.snake.win:
            self.snake.updatePosition()
            self._updateMap()
            self._delay(self.updaterate)
        self.gameState = False

    def _delay(self, milliseconds):
        loop = QEventLoop(self)
        t = QTimer(self)
        t.timeout.connect(loop.exit)
        t.start(milliseconds)
        loop.exec_()
