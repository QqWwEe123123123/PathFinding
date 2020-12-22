from ASTARClass import Astar
from BFSClass import BFS
from NODEClass import NODE
from main import *


def createGrid():
    grid = [[NODE(j, i, CELLSIZE) for i in range(width)] for j in range(height)]
    # border
    for i in range(width):
        grid[0][i].setCell(-1, COLOR["BLACK"], True)
        grid[height - 1][i].setCell(-1, COLOR["BLACK"], True)
    for j in range(height):
        grid[j][0].setCell(-1, COLOR["BLACK"], True)
        grid[j][width - 1].setCell(-1, COLOR["BLACK"], True)
    return grid


def getMousePos():
    mouseCol, mouseRow = pygame.mouse.get_pos()
    mouseX, mouseY = mouseCol // CELLSIZE, mouseRow // CELLSIZE
    return mouseY, mouseX


def valid(x, y):
    return 0 < x < width - 1 and 0 < y < height - 1


def drawPath(alg, start, end, walls, grid):
    path = []
    clearPath(grid)
    if alg == "BFS":
        path = BFS(start, end, walls, grid).main()
    elif alg == "Astar":
        path = Astar(start, end, walls, grid).main()

    initStartEnd(start, end)
    if path is None:
        return False
    for node in path:
        node.setCell(4, COLOR["PURPLE"], True)
    return True


def createPath(start, end):
    path = []
    current = end
    while not current.posEqual(start):
        path.append(current)
        current = current.parent
    path.pop(0)
    return path


def initStartEnd(start, end):
    start.setCell(1, COLOR["GREEN"], True)
    end.setCell(2, COLOR["RED"], True)


def reDrawGrid(grid):
    screen.fill(COLOR["GREY"])  # set background color
    # draw grid
    for i in grid:
        for cell in i:
            cell.draw(screen)
    pygame.display.update()


def clearPath(grid):
    for i in grid:
        for j in i:
            if j.state == 4 or j.state == 5 or j.state == 6:
                j.resetCell()
