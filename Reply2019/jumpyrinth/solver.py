from enum import Enum

FILENAME = '2c464e58-9121-11e9-aec5-34415dec71f2.txt'


class Box:
    START = '$'
    END = '@'
    NOTHING = '#'
    PREPEND = '('
    APPEND = ')'
    REMOVE_FIRST = '-'
    REMOVE_LAST = '+'
    REVERSE = '%'
    PUSH_RIGHT = '['
    PUSH_LEFT = ']'
    PUSH_UP = '*'
    PUSH_DOWN = '.'
    MOVE_LEFT = '<'
    MOVE_RIGHT = '>'
    MOVE_UP = '^'
    MOVE_DOWN = 'v'


class Direction(Enum):
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4


class Status(Enum):
    PLAYING = 1
    DONE = 2
    FAILED = 3


class Player:
    def __init__(self, x, y):
        self.stack = []
        self.position = lambda: None
        self.position.x = x
        self.position.y = y
        self.flag = ''

    def pop(self):
        c = self.stack[-1]
        self.stack = self.stack[:-1]
        return c

    def push(self, char):
        self.stack.append(char)

    def prepend(self, char):
        self.flag = char + self.flag

    def append(self, char):
        self.flag = self.flag + char

    def removeFirst(self):
        self.flag = self.flag[1:]

    def removeLast(self):
        self.flag = self.flag[:-1]

    def reverse(self):
        self.flag = self.flag[::-1]

    def move(self, x, y):
        self.position.x = x
        self.position.y = y


def getMap(filename):
    with open(filename) as f:
        map = f.readlines()
    map = [[char for char in line] for line in map]
    transposed = []
    symbols = []
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] not in symbols:
                symbols.append(map[y][x])
            try:
                transposed[x].append(map[y][x])
            except IndexError:
                transposed.append([])
                transposed[x].append(map[y][x])
    return transposed


def findFlag(map, player):
    actionStatus = doAction(map, player)
    while actionStatus == Status.PLAYING:
        actionStatus = doAction(map, player)
    if actionStatus == Status.DONE:
        return player.flag
    elif actionStatus == Status.FAILED:
        return 'FAIL!'


def findStart(map, seed):
    count = 0
    for x in range(len(map)):
        for y in range(len(map[x])):
            if map[x][y] == Box.START:
                if count == seed:
                    return (x, y)
                else:
                    count += 1
    return None


def readNum(map, position, direction):
    x = position.x
    y = position.y
    if(direction == Direction.UP):
        xMod = 0
        yMod = -1
    elif(direction == Direction.DOWN):
        xMod = 0
        yMod = 1
    elif(direction == Direction.RIGHT):
        xMod = 1
        yMod = 0
    elif(direction == Direction.LEFT):
        xMod = -1
        yMod = 0

    x += xMod
    y += yMod
    c = map[x][y]
    num = ''
    while c >= '0' and c <= '9':
        num += c
        x += xMod
        y += yMod
        c = map[x][y]

    return int(num)


def doAction(map, player):
    box = map[player.position.x][player.position.y]
    if(box == Box.START):
        player.position.y += 1
    elif (box == Box.END):
        return Status.DONE
    elif (box == Box.NOTHING):
        return Status.FAILED
    elif (box == Box.PREPEND):
        mov = readNum(map, player.position, Direction.RIGHT)
        player.position.x -= mov
        player.prepend(player.pop())
    elif (box == Box.APPEND):
        mov = readNum(map, player.position, Direction.LEFT)
        player.position.x += mov
        player.append(player.pop())
    elif (box == Box.REMOVE_FIRST):
        mov = readNum(map, player.position, Direction.DOWN)
        player.position.y -= mov
        player.removeFirst()
    elif (box == Box.REMOVE_LAST):
        mov = readNum(map, player.position, Direction.UP)
        player.position.y += mov
        player.removeLast()
    elif (box == Box.REVERSE):
        player.position.y += 1
        player.reverse()
    elif (box == Box.PUSH_RIGHT):
        player.push(map[player.position.x + 1][player.position.y])
        player.position.x += 2
    elif (box == Box.PUSH_LEFT):
        player.push(map[player.position.x - 1][player.position.y])
        player.position.x -= 2
    elif (box == Box.PUSH_UP):
        player.push(map[player.position.x][player.position.y - 1])
        player.position.y -= 2
    elif (box == Box.PUSH_DOWN):
        player.push(map[player.position.x][player.position.y + 1])
        player.position.y += 2
    elif (box == Box.MOVE_RIGHT):
        mov = readNum(map, player.position, Direction.LEFT)
        player.position.x += mov
    elif (box == Box.MOVE_LEFT):
        mov = readNum(map, player.position, Direction.RIGHT)
        player.position.x -= mov
    elif (box == Box.MOVE_UP):
        mov = readNum(map, player.position, Direction.DOWN)
        player.position.y -= mov
    elif (box == Box.MOVE_DOWN):
        mov = readNum(map, player.position, Direction.UP)
        player.position.y += mov
    return Status.PLAYING


def main():
    map = getMap(FILENAME)
    seed = 0
    start = findStart(map, seed)
    while start is not None:
        player = Player(*start)
        print(findFlag(map, player))
        seed += 1
        start = findStart(map, seed)


if __name__ == '__main__':
    print("")
    print('START')
    print("")
    print("------------------------------------------------------------------")
    print("")
    main()
    print("")
    print("------------------------------------------------------------------")
    print("")
    print('END')
    print("")
