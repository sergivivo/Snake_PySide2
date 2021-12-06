import random

class Snake():
    def __init__(self, xsize = 15, ysize = 10):
        # Constants
        self.xsize = xsize
        self.ysize = ysize

        # Variables
        self.heading = 0 # 0: east, 1: north, 2: west, 3: south

        self.head = (int(xsize/4), int(ysize/4))
        self.body = []
        self.moves = []

        self._generateItem()
        self.death = False
        self.win = False

    def _generateItem(self):
        empty = [(j,i) for j in range(self.xsize) for i in range(self.ysize)
                if (j,i) not in self.body + [self.head]]
        if empty:
            self.item = random.choice(empty)
        else:
            self.win = True

    def updateHeading(self, heading):
        self.moves.append(heading)

    def updatePosition(self):
        # Save head on body
        if self.moves:
            tocheck = self.moves.pop(0)
            if tocheck % 2 != self.heading % 2:
                self.heading = tocheck
        self.body.append(self.head)

        # Update position of head
        dictionary = {0: (1,0), 1: (0,-1), 2: (-1,0), 3: (0,1)}
        newx = self.head[0] + dictionary[self.heading][0]
        newy = self.head[1] + dictionary[self.heading][1]
        self.head = (newx, newy)

        # Delete tail on body
        if self.head == self.item:
            self._generateItem()
        else:
            self.body.pop(0)
            if self.head in self.body or not (
                    0 <= self.head[0] < self.xsize and 0 <= self.head[1] < self.ysize):
                self.death = True

    def __str__(self):
        s = "▄" + "▄▄" * self.xsize + "▄\n"
        for i in range(self.ysize):
            s += "█"
            for j in range(self.xsize):
                coord = (j,i)
                if self.head == coord:
                    s += "Ｏ"
                elif coord in self.body:
                    s += "＊"
                elif coord == self.item:
                    s += "＠"
                else:
                    s += "　"
            s += "█\n"
        s += "▀" + "▀▀" * self.xsize + "▀"
        return s
