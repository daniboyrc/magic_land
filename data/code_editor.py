# coding: utf-8

import pygame
import math
import sys
import os
from pygame.locals import*
from constantes import *
from control import control_feitico

# CONSTANTS

FPS = 30
TEXTHEIGHT = 30
LINHAHEIGHT = 38
STARTX = 0
STARTY = 0
LEFT = 'left'
RIGHT = 'right'
UP = 'up'
DOWN = 'down'

# COLORS

GRAY = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE = (255, 255, 255)
RED = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE = (  0,   0, 255)
YELLOW = (255, 255,   0)
ORANGE = (255, 128,   0)
PURPLE = (255,   0, 255)
CYAN = (  0, 255, 255)
BLACK = (  0,   0,   0)
COMBLUE = (233, 232, 255)

BGCOLOR = WHITE
TEXTCOLOR = BLACK

# MY CONSTANTS
TEXT_BG = 'resources/miscelania/text_area_code_editor.jpg'
SURF_BG = 'resources/miscelania/bg_code_editor.png'

# SURFACES
text_bg = pygame.image.load(TEXT_BG)

def code_editor(screen, id_feitico):
    global FPSCLOCK

    pygame.init()
    FPSCLOCK = pygame.time.Clock()

    windowWidth  = 460
    windowHeight = 450
    lineNumber   = 0
    newChar      = ''
    typeChar     = False
    textString   = ''
    mainList     = []
    mainList.append(textString)
    deleteKey    = False
    returnKey    = False
    insertPoint  = 0
    camerax      = 0
    cameray      = 0
    mouseClicked = False
    mouseX       = 0
    mouseY       = 0
    path         = 'resources/feiticos/'
    ctrlPress    = False

    # SURFACES
    screen.blit(pygame.image.load(SURF_BG), (0, 0))

    displaySurf = pygame.Surface([windowWidth, windowHeight])
    displaySurf.convert()
    pygame.display.update()

    mainFont = Fontes.diploma

    cursorRect = getCursorRect(STARTX, STARTY + (TEXTHEIGHT + (TEXTHEIGHT-LINHAHEIGHT)), mainFont, camerax, cameray)

    # ABRINDO ARQUIVO
    path += str(id_feitico) + '.py'
    try:
        mainList = loadFromDisk(path)
    except:
        pass

# The main game loop detects user input, displays the text on the screen,
# displays the cursor on the screen, and adjusts the camera view if
# necessary.

    while True:
        camerax, cameray = adjustCamera(mainList, lineNumber, insertPoint, cursorRect, mainFont, camerax, cameray, windowWidth, windowHeight)

        newChar, typeChar, deleteKey, returnKey, directionKey, windowWidth, windowHeight, mouseX, mouseY, mouseClicked, ctrlPress = getInput(windowWidth, windowHeight, ctrlPress)

        if newChar == 'exit':
            break
        if newChar == 'save':
            saveToDisk(mainList, path)
        if newChar == 'save_exit':
            saveToDisk(mainList, path)
            break
        if newChar == 'test':
            saveToDisk(mainList, path)
            control_feitico.verifica_feitico(id_feitico)
        if newChar == 'run':
            try:
                os.system('idle-python2.7 -r %s' % path)
            except:
                pass
                
        mainList, lineNumber, insertPoint, cursorRect = displayText(mainFont, newChar, typeChar, mainList, deleteKey, returnKey, lineNumber, insertPoint, directionKey, camerax, cameray, cursorRect, windowWidth, windowHeight, displaySurf, mouseClicked, mouseX, mouseY, screen)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


# Interprets user input and changes mainList, lineNumber, insertPoint
# and cursorRect accordingly.  There is a function called blitAll()
# which blits all strings to the main surface.

def displayText(mainFont, newChar, typeChar, mainList, deleteKey, returnKey, lineNumber, insertPoint, directionKey, camerax, cameray, cursorRect, windowWidth, windowHeight, displaySurf, mouseClicked, mouseX, mouseY, screen):
    if returnKey:
        firstString = getStringAtInsertPoint(mainList, lineNumber, insertPoint)
        secondString = getStringAfterInsertPoint(mainList, lineNumber, insertPoint)
        mainList[lineNumber] = firstString
        mainList.insert(lineNumber+1, secondString)
        lineNumber +=1
        returnKey = False
        insertPoint = 0
        cursorRect.x = STARTX
        stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)
        cursorRect.y = stringRect.top

    elif mouseClicked:
        insertPoint, lineNumber, cursorRect = setCursorToClick(mainList, cursorRect, mainFont, camerax, cameray, mouseX, mouseY)

    elif directionKey:
        if directionKey == LEFT:
            if lineNumber == 0:
                if insertPoint > 0:
                    insertPoint -= 1
                    stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)
                    cursorRect.x = stringRect.right
                    cursorRect.y = STARTY

            elif lineNumber > 0:
                if insertPoint == 0:
                    lineNumber -= 1
                    insertPoint = len(mainList[lineNumber])
                    stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)
                    cursorRect.x = stringRect.right
                    cursorRect.y = stringRect.top

                elif insertPoint > 0:
                    insertPoint -= 1
                    stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)

                    if insertPoint == 0:
                        cursorRect.x = STARTX
                        cursorRect.y = stringRect.top
                    else:
                        cursorRect.x = stringRect.right
                        cursorRect.y = stringRect.top

        elif directionKey == RIGHT:
            if insertPoint < len(mainList[lineNumber]):
                insertPoint += 1
                stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)
                cursorRect.x = stringRect.right
                cursorRect.y = stringRect.top

            elif insertPoint >= len(mainList[lineNumber]):
                if len(mainList) > (lineNumber + 1):
                    lineNumber += 1
                    insertPoint = 0
                    stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)
                    cursorRect.x = stringRect.right
                    cursorRect.y = stringRect.top

        elif directionKey == UP:
            if lineNumber > 0:
                if insertPoint == 0:
                    lineNumber -= 1
                    stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)
                    cursorRect.x = STARTX
                    cursorRect.y = stringRect.top

                elif insertPoint > len(mainList[lineNumber - 1]):
                    lineNumber -= 1
                    insertPoint = len(mainList[lineNumber])
                    stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)
                    cursorRect.x = stringRect.right
                    cursorRect.y = stringRect.top

                elif insertPoint <= len(mainList[lineNumber -1]):
                    lineNumber -= 1
                    stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)
                    cursorRect.x = stringRect.right
                    cursorRect.y = stringRect.top

        elif directionKey == DOWN:
            if lineNumber + 1 < len(mainList):
                if insertPoint == 0:
                    lineNumber += 1
                    stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)
                    cursorRect.x = STARTX
                    cursorRect.y = stringRect.top

                elif insertPoint > len(mainList[lineNumber + 1]):
                    lineNumber +=1
                    insertPoint = len(mainList[lineNumber])
                    stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)
                    cursorRect.x = stringRect.right
                    cursorRect.y = stringRect.top
                elif insertPoint <= len(mainList[lineNumber +1]):
                    lineNumber += 1
                    stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)
                    cursorRect.x = stringRect.right
                    cursorRect.y = stringRect.top

    elif typeChar:
        string = mainList[lineNumber]
        stringList = list(string)
        stringList.insert(insertPoint, newChar)
        newString = ''.join(stringList)
        mainList[lineNumber] = newString

        typeChar = False

        if len(newString) > len(string) and newChar != '    ':   ## Prevents alteration keys like shifts from affecting the insertPoint ##
            insertPoint += 1
            stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)
            cursorRect.x = stringRect.right
            cursorRect.y = stringRect.top

        elif newChar == '    ':
            insertPoint += 4
            stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)
            cursorRect.x = stringRect.right
            cursorRect.y = stringRect.top

    elif deleteKey:

        if insertPoint > 0:
            firstString = getStringAtInsertPoint(mainList, lineNumber, insertPoint)
            secondString = getStringAfterInsertPoint(mainList, lineNumber, insertPoint)
            stringList = list(firstString)
            del stringList[insertPoint-1]
            string = ''.join(stringList)
            string += secondString
            mainList[lineNumber] = string

            deleteKey = False
            insertPoint -= 1
            stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)
            cursorRect.x = stringRect.right
            cursorRect.y = stringRect.top

        elif insertPoint <= 0:
            if lineNumber > 0:
                string = getStringAfterInsertPoint(mainList, lineNumber, insertPoint)
                del mainList[lineNumber]
                lineNumber -= 1
                mainList[lineNumber] += string

                deleteKey = False
                insertPoint = len(mainList[lineNumber]) - len(string)
                stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)                
                cursorRect.x = stringRect.right
                cursorRect.y = stringRect.top

    else:
        stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)

        if insertPoint == 0:
            cursorRect.x = STARTX
        elif insertPoint > 0:
            cursorRect.x = stringRect.right
        if lineNumber == 0:
            cursorRect.y = STARTY
        elif lineNumber > 0:
            cursorRect.y = stringRect.top
        else:
            cursorRect.x = stringRect.right

    if cursorRect.left >= STARTX:
        if cursorRect.right <= windowWidth:
            if cursorRect.top >= STARTY:
                if cursorRect.bottom <= (windowHeight - STARTY):
                    blitAll(mainList, mainFont, camerax, cameray, cursorRect, displaySurf, screen)

    return mainList, lineNumber, insertPoint, cursorRect

# Blits all the strings in mainList to the main surface object 

def blitAll(mainList, mainFont, camerax, cameray, cursorRect, displaySurf, screen):
    displaySurf.blit(text_bg, (0, 0))

    i = 0

    for string in mainList:  ##blitting all the strings in the mainList by iterating through them
        stringRender = mainFont.render(string, True, TEXTCOLOR)
        stringRect = stringRender.get_rect()
        stringRect.x = STARTX - camerax
        stringRect.y = STARTY + (i * (TEXTHEIGHT + (TEXTHEIGHT-LINHAHEIGHT))) - cameray
        displaySurf.blit(stringRender, stringRect)
        i += 1

    drawCursor(mainFont, cursorRect, displaySurf)

    screen.blit(displaySurf, (170, 80))

def adjustCamera(mainList, lineNumber, insertPoint, cursorRect, mainFont, camerax, cameray, windowWidth, windowHeight):

    stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)

    if (stringRect.right + cursorRect.width) > windowWidth:
        camerax += (stringRect.right + cursorRect.width) - windowWidth  
    elif cursorRect.left < STARTX:
        camerax -= (-1)*(cursorRect.left)

    if stringRect.bottom > windowHeight:
        cameray += stringRect.bottom - windowHeight
    elif stringRect.top < 0:
        cameray -= (-1)*(stringRect.top)

    if insertPoint == 0:
        camerax = 0
    if lineNumber == 0:
        cameray = 0

    return camerax, cameray


def drawCursor(mainFont, cursorRect, displaySurf):
    cursor = mainFont.render('l', True, BLACK, BLACK)
    cursorRect.y = cursorRect.y + 2
    cursorRect.w = 2
    cursorRect.h = 25
    pygame.draw.rect(displaySurf, (0), cursorRect)


def getInput(windowWidth, windowHeight, ctrlPress):
    newChar = False
    typeChar = False
    deleteKey = False
    returnKey = False
    directionKey = False
    mouseX = 0
    mouseY = 0
    mouseClicked = False

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == KEYDOWN:
            if event.key == K_BACKSPACE:
                deleteKey = True
            elif event.key == K_LCTRL or event.key == K_RCTRL:
                ctrlPress = True
            elif event.key == K_RETURN:
                returnKey = True
            elif event.key == K_TAB:
                newChar = '    '
                typeChar = True
            elif event.key == K_LEFT:
                directionKey = LEFT
            elif event.key == K_RIGHT:
                directionKey = RIGHT
            elif event.key == K_UP:
                directionKey = UP
            elif event.key == K_DOWN:
                directionKey = DOWN

            # COMMANDS
            elif event.key == K_w and ctrlPress:
                newChar = 'exit'
            elif event.key == K_s and ctrlPress:
                newChar = 'save'
            elif event.key == K_d and ctrlPress:
                newChar = 'save_exit'
            elif event.key == K_f and ctrlPress:
                newChar = 'test'
            elif event.key == K_b and ctrlPress:
                newChar = 'run'
            else:
                newChar = event.unicode
                typeChar = True

        elif event.type == KEYUP:
            if event.key == K_LCTRL:
                ctrlPress = False

        elif event.type == VIDEORESIZE:
            displaySurf = pygame.display.set_mode(event.dict['size'], RESIZABLE)
            windowWidth = event.dict['w']
            windowHeight = event.dict['h']
            displaySurf.fill(WHITE)
            displaySurf.convert()
            pygame.display.update()

        elif event.type == MOUSEBUTTONDOWN:
            mouseX, mouseY = event.pos
            mouseClicked = True

    return newChar, typeChar, deleteKey, returnKey, directionKey, windowWidth, windowHeight, mouseX, mouseY, mouseClicked, ctrlPress


# These functions involve the string the cursor happens to be on.
# By using the lineNumber, the program knows which string to
# manipulate.  lineNumber = 0 is the first line, and so on.
# The cursor's left position is always locked to the right of whatever
# stringRect it is next to.

def getStringRect(string, lineNumber, camerax, cameray):
    stringRect = string.get_rect()
    stringRect.x = STARTX - camerax
    stringRect.y = STARTY + (lineNumber * (TEXTHEIGHT + (TEXTHEIGHT-LINHAHEIGHT))) - cameray

    return stringRect

def getStringAtInsertPoint(mainList, lineNumber, insertPoint):
    string = mainList[lineNumber]
    stringList = list(string)
    newStringList = stringList[0:insertPoint]
    newString = ''.join(newStringList)

    return newString

def getStringAfterInsertPoint(mainList, lineNumber, insertPoint):
    string = mainList[lineNumber]
    stringList = list(string)
    newStringList = stringList[insertPoint:]
    newString = ''.join(newStringList)

    return newString


def getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray):
    string = getStringAtInsertPoint(mainList, lineNumber, insertPoint)
    stringRender = mainFont.render(string, True, TEXTCOLOR, BGCOLOR)
    stringRect = getStringRect(stringRender, lineNumber, camerax, cameray)

    return stringRect


# Miscelaneous Functions.  getCursorRect is used to produce the
# cursors's rect object.


def getCursorRect(cursorX, cursorY, mainFont, camerax, cameray):
    cursor = mainFont.render('', True, BLACK)
    cursorRect = cursor.get_rect()
    cursorRect.w = 3
    cursorRect.x = cursorX - camerax
    cursorRect.y = cursorY - cameray

    return cursorRect


# These three functions, setCursorToClick(), getLineNumberOfClick(), and
# get insertPointAtMouseX() allow the user to set the cursor location
# by clicking the mouse at the spot they want to go.


def setCursorToClick(mainList, cursorRect, mainFont, camerax, cameray, mouseX, mouseY):
    lineNumber = getLineNumberOfClick(mouseY, cameray, mainList)
    insertPoint = getInsertPointAtMouseX(mouseX, mouseY, lineNumber, mainList, mainFont, camerax, cameray)
    stringRect = getStringRectAtInsertPoint(mainList, lineNumber, insertPoint, mainFont, camerax, cameray)

    if insertPoint == 0:
        cursorRect.x = STARTX
    elif insertPoint > 0:
        cursorRect.x = stringRect.right

    cursorRect.y = stringRect.top

    return insertPoint, lineNumber, cursorRect


def getLineNumberOfClick(mouseY, cameray, mainList):
    clickLineNumber = (mouseY + cameray) / float(TEXTHEIGHT+ (TEXTHEIGHT-LINHAHEIGHT))
    if clickLineNumber > len(mainList):
        lineNumber = (len(mainList)) - 1
    elif clickLineNumber <= len(mainList):
        floorLineNumber = math.floor(clickLineNumber)
        lineNumber = int(floorLineNumber)

    return lineNumber


def getInsertPointAtMouseX(mouseX, mouseY, lineNumber, mainList, mainFont, camerax, cameray):
    string = mainList[lineNumber]
    newInsertPoint = 0

    if (mouseY + cameray) > ((lineNumber + 1) * (TEXTHEIGHT + TEXTHEIGHT-LINHAHEIGHT)):
        insertPoint = len(mainList[lineNumber])
        return insertPoint

    for insertPoint in string:
        stringRect = getStringRectAtInsertPoint(mainList, lineNumber, newInsertPoint, mainFont, camerax, cameray)
        if mouseX >= stringRect.left:
            if mouseX < stringRect.right:
                if newInsertPoint > 0:
                    return newInsertPoint - 1

        newInsertPoint += 1

    else:
        return newInsertPoint


def saveToDisk(mainList, saveDirectory):
    saveFile = open(saveDirectory, 'w')

    for string in mainList:
        saveFile.write(string + '\n')

    saveFile.close()


def loadFromDisk(loadDirectory):
    mainList = []
    saveFile = open(loadDirectory, 'r')

    for line in saveFile:
        mainList.append(line)

    saveFile.close()

    i = 0
    while i < len(mainList):
        stringList = list(mainList[i])
        stringList.pop()
        mainList[i] = ''.join(stringList)
        i += 1

    return mainList
