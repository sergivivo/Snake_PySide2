from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

import sys

from snakeview import SnakeView

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()

        # Parameters
        self.rows = 10
        self.columns = 15
        self.updateRate = 150

        # Menu bar
        self.menu = self.menuBar()
        game = self.menu.addMenu("Game")
        rest = QAction("Restart", self)
        conf = QAction("Settings", self)
        rest.triggered.connect(self.generateMap)
        conf.triggered.connect(self.openSettingsWindow)
        game.addAction(rest)
        game.addAction(conf)

        # Snake QGraphicsView
        self.snake = SnakeView(self)
        self.setCentralWidget(self.snake)
        self.generateMap()

    def generateMap(self):
        self.snake.generateMap(self.rows, self.columns, self.updateRate)
        self.setFixedSize(self.sizeHint())

    def openSettingsWindow(self):
        self.settings = Settings(self.rows, self.columns, self.updateRate, self)
        self.settings.sendConfig.connect(self.loadSettings)
        self.settings.show()

    @Slot(int, int, int)
    def loadSettings(self, rows, columns, updateRate):
        self.rows = rows
        self.columns = columns
        self.updateRate = updateRate
        self.generateMap()

class Settings(QDialog):
    sendConfig = Signal(int,int,int)
    def __init__(self, rows, columns, updateRate, parent=None):
        super(Settings, self).__init__()
        self.setWindowTitle("Custom board")

        # Top widget
        twidget = QWidget(self)
        gridlayout = QGridLayout()

        label1 = QLabel("Rows:",self)
        label2 = QLabel("Columns:",self)
        label3 = QLabel("Update rate:",self)
        label1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.spbox1 = QSpinBox(self)
        self.spbox1.setRange(5,40)
        self.spbox1.setValue(rows)
        self.spbox2 = QSpinBox(self)
        self.spbox2.setRange(5,60)
        self.spbox2.setValue(columns)
        self.spbox3 = QSpinBox(self)
        self.spbox3.setRange(50,1000)
        self.spbox3.setValue(updateRate)

        gridlayout.addWidget(label1, 0, 0)
        gridlayout.addWidget(label2, 1, 0)
        gridlayout.addWidget(label3, 2, 0)
        gridlayout.addWidget(self.spbox1, 0, 1)
        gridlayout.addWidget(self.spbox2, 1, 1)
        gridlayout.addWidget(self.spbox3, 2, 1)

        twidget.setLayout(gridlayout)

        # Bottom widget
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        # Full widget
        fwidget = QWidget(self)
        flayout = QVBoxLayout()
        flayout.addWidget(twidget)
        flayout.addWidget(buttonBox)
        fwidget.setLayout(flayout)

        self.setLayout(flayout)

    def accept(self):
        self.sendConfig.emit(self.spbox1.value(), self.spbox2.value(), self.spbox3.value())
        self.close()

if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
