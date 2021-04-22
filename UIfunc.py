from UI.BUTTONClass import button
from UI.NODEClass import NODE
from UI.SLIDERClass import slider
from settings import *


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


def createPath(start, end):
    path = []
    current = end
    while not current.posEqual(start):
        path.append(current)
        current = current.parent
    path.pop(0)
    return path


def reDrawScreen(grid):
    screen.fill(COLOR["GREY"])  # set background color
    # draw grid
    for i in grid:
        for cell in i:
            cell.draw(screen)
    for bnt in buttons.values():
        bnt.draw(screen)

    for s in sliders:
        s.draw()
    pygame.display.update()


def clearPath(grid):
    for i in grid:
        for j in i:
            if j.state == 4 or j.state == 5 or j.state == 6:
                j.resetCell()


def clearALL(grid, walls):
    for i in grid:
        for j in i:
            if j.state != 1 and j.state != 2 and j.state != -1:
                if j.state == 3:
                    walls.remove(j)
                j.resetCell()

def createSlider(name,info):
    return slider(name,info["val"],info["maxi"],info["mini"],info["xpos"],info["ypos"])

def loadSlider():
    for name,s in slidersInfo.items():
        newSlider = createSlider(name,s)
        sliders.append(newSlider)

def sliderClicked():
    pos = pygame.mouse.get_pos()
    for s in sliders:
        if s.button_rect.collidepoint(pos):
            s.hit = True

def createButton(col, row, l, w, color, hl, msg, id):
    return button(col, row, l, w, color, hl, msg, id)

def loadBUttons():
    for key,value in buttonsInfo.items():
        buttons[key] = createButton(value["position"][0], value["position"][1], value["dimension"][0],
                                    value["dimension"][1], value["color"], value["highLight"], value["msg"],
                                    value["id"])
        if key in algs:
            buttons[key].algSet = False

        if key == "BFS":
            # init the default alg
            buttons[key].highLighted = True
            buttons[key].algSet = True


def buttonHover():
    # highlight button when hovering over
    for bnt in buttons.values():
        if bnt.onButton(pygame.mouse.get_pos()):
            bnt.highlightButton()
        else:
            bnt.unhighlightButton()

def buttonClicked(alg):
    # check if one of the button is clicked
    buttonChanged = [False]
    for bnt in buttons.values():
        if bnt.onButton(pygame.mouse.get_pos()):
            if bnt.algSet is None: # not a alg button
                return alg
            if not bnt.algSet:
                bnt.highlightButton()
                alg = bnt.id
                buttonChanged = [True,bnt]
                bnt.algSet = True
                break

    if buttonChanged[0]:
        for bnt in buttons.values():
            if bnt == buttonChanged[1]:
                continue
            else:
                if bnt.algSet is None:
                    continue
                bnt.unhighlightButton()
                bnt.algSet = False
    return alg