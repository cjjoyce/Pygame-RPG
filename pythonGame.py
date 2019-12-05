import pygame
import sys
import random
import time
import re
import ctypes
from pygame import *

pygame.init()

# Get the user's monitor dimensions.
user32 = ctypes.windll.user32
monitorWidth = user32.GetSystemMetrics(0)
monitorHeight = user32.GetSystemMetrics(1)

tileSize = 64

gameFont = pygame.font.SysFont('segoeui', int(tileSize / 2))

screenTileWidth = int(monitorWidth / tileSize)
screenTileHeight = int(monitorHeight / tileSize)

screenPixelWidth = tileSize * screenTileWidth
screenPixelHeight = tileSize * screenTileHeight

screenMidpointX = int(screenTileWidth / 2)
screenMidpointY = int(screenTileHeight / 2)

displaySurface = pygame.display.set_mode((screenPixelWidth, screenPixelHeight), pygame.FULLSCREEN, 0)
fps = 60
fpsClock = pygame.time.Clock()

playerDown = pygame.image.load('images\\sprites\\playerDown.png')
playerDown = pygame.transform.scale(playerDown,(tileSize, int(tileSize + (tileSize / 4))))
playerDownStep1 = pygame.image.load('images\\sprites\\playerDownStep1.png')
playerDownStep1 = pygame.transform.scale(playerDownStep1,(tileSize, int(tileSize + (tileSize / 4))))
playerDownStep2 = pygame.image.load('images\\sprites\\playerDownStep2.png')
playerDownStep2 = pygame.transform.scale(playerDownStep2,(tileSize, int(tileSize + (tileSize / 4))))

playerUp = pygame.image.load('images\\sprites\\playerUp.png')
playerUp = pygame.transform.scale(playerUp,(tileSize, int(tileSize + (tileSize / 4))))
playerUpStep1 = pygame.image.load('images\\sprites\\playerUpStep1.png')
playerUpStep1 = pygame.transform.scale(playerUpStep1,(tileSize, int(tileSize + (tileSize / 4))))
playerUpStep2 = pygame.image.load('images\\sprites\\playerUpStep2.png')
playerUpStep2 = pygame.transform.scale(playerUpStep2,(tileSize, int(tileSize + (tileSize / 4))))

playerLeft = pygame.image.load('images\\sprites\\playerLeft.png')
playerLeft = pygame.transform.scale(playerLeft,(tileSize, int(tileSize + (tileSize / 4))))
playerLeftStep1 = pygame.image.load('images\\sprites\\playerLeftStep1.png')
playerLeftStep1 = pygame.transform.scale(playerLeftStep1,(tileSize, int(tileSize + (tileSize / 4))))
playerLeftStep2 = pygame.image.load('images\\sprites\\playerLeftStep2.png')
playerLeftStep2 = pygame.transform.scale(playerLeftStep2,(tileSize, int(tileSize + (tileSize / 4))))

playerRight = pygame.image.load('images\\sprites\\playerRight.png')
playerRight = pygame.transform.scale(playerRight,(tileSize, int(tileSize + (tileSize / 4))))
playerRightStep1 = pygame.image.load('images\\sprites\\playerRightStep1.png')
playerRightStep1 = pygame.transform.scale(playerRightStep1,(tileSize, int(tileSize + (tileSize / 4))))
playerRightStep2 = pygame.image.load('images\\sprites\\playerRightStep2.png')
playerRightStep2 = pygame.transform.scale(playerRightStep2,(tileSize, int(tileSize + (tileSize / 4))))

playerImage = playerDown
cursorImage = pygame.image.load('images\\cursor.png')
cursorImage = pygame.transform.scale(cursorImage,(tileSize, tileSize))
targetImage = pygame.image.load('images\\target.png')
targetImage = pygame.transform.scale(targetImage,(tileSize, tileSize))

def tileCoordinateToPixels(x, y):
    tileX = x * tileSize
    tileY = y * tileSize
    return tileX, tileY

def tilePixelsToCoordinates(x, y):
    tileX = x / tileSize
    tileY = y / tileSize
    return (tileX, tileY)

def replaceLine(fileName, lineNum, text):
    lines = open(fileName, 'r').readlines()
    lines[lineNum] = text
    out = open(fileName, 'w')
    out.writelines(lines)
    out.close()

def saveGame(fileName, saveVariables):
    fileNum = 1
    currentMapName, currentMapX, currentMapY, playerX, playerY = saveVariables
    playerX = int(playerX / tileSize)
    playerY = int(playerY / tileSize)
    currentMapX = int(currentMapX / tileSize)
    currentMapY = int(currentMapY / tileSize)
    replaceLine(fileName, 0, str(fileNum) + '\n')
    replaceLine(fileName, 1, str(currentMapName) + '\n')
    replaceLine(fileName, 2, str(currentMapX) + '\n')
    replaceLine(fileName, 3, str(currentMapY) + '\n')
    replaceLine(fileName, 4, str(playerX) + '\n')
    replaceLine(fileName, 5, str(playerY) + '\n')

def loadGame(fileName):
    file = open(fileName, 'r')
    lines = file.readlines()
    fileNum = int(lines[0])
    currentObstacleMap = lines[1]
    backgroundLocation = [int(lines[2]), int(lines[3])]
    playerLocation = [int(lines[4]), int(lines[5])]
    file.close()

    return (fileNum, currentObstacleMap, backgroundLocation, playerLocation)

# Load map tiles from a text file into a list of rectangles
def createRectangleList(fileName):
    file = open(fileName, 'r')
    lines = file.readlines()
    rectangleList = []

    # Retrieve values from text file and append to rectangleList
    for i in range(int(len(lines) / 5)):
        tileX, tileY = tileCoordinateToPixels(int(lines[i * 5 + 1]), int(lines[i * 5 + 2]))
        width, height = tileCoordinateToPixels(int(lines[i * 5 + 3]), int(lines[i * 5 + 4]))
        rectangleList.append(pygame.Rect(tileX, tileY, width, height))

    file.close()
    return rectangleList

# Draw all rectangles from a specified collision map
def drawRectangleList(collisionMap, colour, mapLocation, width=0):
    mapX, mapY = mapLocation
    for i in collisionMap[:]:
        i.x -= abs(mapX)
        i.y -= abs(mapY)
        pygame.draw.rect(displaySurface, colour, i, width)
        i.x += abs(mapX)
        i.y += abs(mapY)

def displayIntro(event, currentScreen, keyHeld):
    pygame.mouse.set_visible(False)
    pygame.display.set_caption(' - Created by Charles Joyce')
    pygame.display.set_icon(pygame.image.load('images\icon.png'))
    displaySurface.blit(menuImage['titleMenu'], (0,0))
    if event.type == MOUSEBUTTONDOWN:
        if event.button == 1:
            pygame.mouse.set_pos(480,320)
            currentScreen = 'mainMenu'
            keyHeld = True
    return currentScreen, keyHeld

def checkCollisions(rectangleList, playerRect, playerVariables):
    playerX, playerY, playerDirection = playerVariables
    for i in rectangleList[:]:
        if playerRect.colliderect(i):
            if playerDirection == 'up':
                playerY += tileSize     
            elif playerDirection == 'down':
                playerY -= tileSize
            elif playerDirection == 'left':
                playerX += tileSize
            elif playerDirection == 'right':
                playerX -= tileSize
            break
    return playerX, playerY

def loadMapFiles(mapName, tileSize):
    mapName = mapName.strip()
    try:
        obstacleMap = createRectangleList('maps\\' + mapName + '\\obstacles.txt')
    except:
        print("Wall Map file not found or incorrect format.")
        obstacleMap = []
    try:
        mapBackgroundImage = pygame.image.load('maps\\' + mapName + '\\mapBackground.png')
    except:
        mapBackgroundImage = pygame.image.load('maps\\defaultMap.png')

    try:
        mapForegroundImage = pygame.image.load('maps\\' + mapName + '\\mapForeground.png')
    except:
        mapForegroundImage = pygame.image.load('maps\\defaultMap.png')

    mapPixelWidth = mapBackgroundImage.get_width()
    mapPixelHeight = mapBackgroundImage.get_height()
    mapBackgroundImage = pygame.transform.scale(mapBackgroundImage,(int((mapPixelWidth / 32) * tileSize), int((mapPixelHeight / 32) * tileSize)))
    mapForegroundImage = pygame.transform.scale(mapForegroundImage,(int((mapPixelWidth / 32) * tileSize), int((mapPixelHeight / 32) * tileSize)))
    mapPixelWidth = mapBackgroundImage.get_width()
    mapPixelHeight = mapBackgroundImage.get_height()

    mapImages = (mapBackgroundImage, mapForegroundImage)
    mapDimensions = (mapPixelWidth, mapPixelHeight)

    return obstacleMap, mapImages, mapDimensions

def loadMap(currentMapName, tileSize):
    currentObstacleMap, currentMapImages, currentMapDimensions = loadMapFiles(currentMapName, tileSize) 
            
    currentMap = (currentMapName, currentObstacleMap, currentMapImages, currentMapDimensions)
    return currentMap

def getNeighbours(node):
    neighbours = []
    for x in range(-1, 2, 1):
        for y in range(-1, 2, 1):
            if x == 0 and y == 0:
                continue
            checkX = node.x + (x * tileSize)
            checkY = node.y + (y * tileSize)

            if checkX >= 0 and checkX < mapPixelWidth and checkY >= 0 and checkY < mapPixelHeight:
                neighbours.append(pygame.Rect(checkX, checkY, tileSize, tileSize))
    return neighbours

def getDistance(rectA, rectB):
    xDistance = abs((rectA.x)/32 - (rectB.x)/32)
    yDistance = abs((rectA.y)/32 - (rectB.y)/32)

    if xDistance > yDistance:
        return 14 * yDistance + 10 * (xDistance - yDistance)
    else:
        return 14 * xDistance + 10 * (yDistance - xDistance)
    
def calculateCosts(node, startNode, targetNode):
    gCost = getDistance(node, startNode)
    hCost = getDistance(node, targetNode)
    fCost = gCost + hCost
    return gCost, hCost, fCost


class Node():
    def __init__(self, parent=None, rect=None, obstacle=False):
        self.parent = parent
        self.rect = rect
        self.obstacle = obstacle

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.rect == other.rect

def aStar(startRect, targetRect, obstacleMap, mapDimensions):
    mapPixelWidth, mapPixelHeight = mapDimensions
    startNode = Node(None, startRect, None)
    startNode.g = startNode.h = startNode.f = 0
    targetNode = Node(None, targetRect, None)
    targetNode.g = targetNode.h = targetNode.f = 0

    for obstacle in obstacleMap[:]:
        if targetRect.colliderect(obstacle):
            return []
    
    openSet = []
    closedSet = []
    openSet.append(startNode)

    
    while len(openSet) > 0:
        currentNode = openSet[0];
        currentIndex = 0
        for index, i in enumerate(openSet):
            if i.f < currentNode.f:
                currentNode = i
                currentIndex = index

        openSet.pop(currentIndex)
        closedSet.append(currentNode)

        if currentNode == targetNode:
            path = []
            current = currentNode
            while current is not None:
                path.append(current.rect)
                current = current.parent
            return path[::-1]
        
        children = []
        for x in range(-1, 2, 1):
            for y in range(-1, 2, 1):
                if (x == 0 and y == 0) or (x == -1 and y == -1) or (x == 1 and y == 1) or (x == -1 and y == 1) or (x == 1 and y == -1):
                    continue
                checkX = currentNode.rect.x + (x * tileSize)
                checkY = currentNode.rect.y + (y * tileSize)
                newObstacle = False
                for obstacle in obstacleMap[:]:
                    if pygame.Rect(checkX, checkY, tileSize, tileSize).colliderect(obstacle):
                        newObstacle = True
                        break
                if checkX >= 0 and checkX < mapPixelWidth and checkY >= 0 and checkY < mapPixelHeight:
                    newRect = pygame.Rect(checkX, checkY, tileSize, tileSize)

                    newNode = Node(currentNode, newRect, newObstacle)
                        
                    if newNode.obstacle == False:
                        children.append(newNode)
        for child in children:
            for closedChild in closedSet:
                if child == closedChild:
                    break
            else:

                child.g = currentNode.g + 1
                child.h = getDistance(child.rect, targetNode.rect)
                child.f = child.g + child.h

                for openNode in openSet:
                    if child == openNode and child.g >= openNode.g:
                        break
                else:
                    openSet.append(child)
    return []

    
   
def startGame(event, currentScreen, gameVariables, userInputs):

    #Unpack Parameter Variables
    mapVariables, playerVariables = gameVariables
    currentMapName, currentObstacleMap, currentMapImages, currentMapPixelDimensions, currentMapLocation = mapVariables
    
    currentMapBackgroundImage, currentMapForegroundImage = currentMapImages
    currentMapPixelWidth, currentMapPixelHeight = currentMapPixelDimensions

    
    playerX, playerY, playerDirection, movePath, playerMove, playerDelay, playerImage, frame = playerVariables

    mouseButton1, mouseButton3, escapeKey = userInputs
    mouse1Held, mouse1Init = mouseButton1
    
    escapeKeyHeld, escapeKeyInit = escapeKey
    currentMapX, currentMapY = currentMapLocation
    (mouseX, mouseY) = pygame.mouse.get_pos()
    (mouseXCoord, mouseYCoord) = tilePixelsToCoordinates(mouseX, mouseY)
    mouseXCoord = int(mouseXCoord)
    mouseYCoord = int(mouseYCoord)
    pygame.display.set_caption('X: ' + str(mouseXCoord) + ', Y: ' + str(mouseYCoord) + ' - ' + currentMapName)
    pygame.mouse.set_visible(False)
    playerRect = pygame.Rect(playerX, playerY, tileSize, tileSize)
    cursorRect = pygame.Rect(mouseXCoord*tileSize, mouseYCoord*tileSize, tileSize, tileSize)

    
    if len(movePath) > 1:
        playerDelay += 1
        if (playerDelay % 7) == 0:
            if -currentMapX + playerX == movePath[1].x and -currentMapY + playerY == movePath[1].y:
                movePath.pop(0)
            if len(movePath) > 1:
                if -currentMapX + playerX < movePath[1].x:
                    if playerDirection != 'right':
                        playerImage = playerRight
                        playerDirection = 'right'
                        
                    if playerX < screenMidpointX * tileSize or currentMapBackgroundImage.get_width() <= screenPixelWidth:
                        playerX += tileSize / 4
                    else:
                        currentMapX -= tileSize / 4
                elif -currentMapX + playerX > movePath[1].x:
                    if playerDirection != 'left':
                        playerImage = playerLeft
                        playerDirection = 'left'

                    if playerX > screenMidpointX * tileSize or currentMapBackgroundImage.get_width() <= screenPixelWidth:
                        playerX -= tileSize / 4
                    else:
                        currentMapX += tileSize / 4
                elif -currentMapY + playerY < movePath[1].y:
                    if playerDirection != 'down':
                        playerImage = playerDown
                        playerDirection = 'down'

                    if playerY < screenMidpointY * tileSize or currentMapBackgroundImage.get_height() <= screenPixelHeight:
                        playerY += tileSize / 4
                    else:
                        currentMapY -= tileSize / 4
                        
                elif -currentMapY + playerY > movePath[1].y:
                    if playerDirection != 'up':
                        playerImage = playerUp
                        playerDirection = 'up'
                    
                    if playerY > screenMidpointY * tileSize or currentMapBackgroundImage.get_height() <= screenPixelHeight:
                        playerY -= tileSize / 4
                    else:
                        currentMapY += tileSize / 4

                if currentMapBackgroundImage.get_width() > screenPixelWidth:
                    if currentMapX > 0:
                        currentMapX = 0
                        playerX -= tileSize / 4
                    if currentMapX < screenPixelWidth - currentMapBackgroundImage.get_width():
                        currentMapX = screenPixelWidth - currentMapBackgroundImage.get_width()
                        playerX += tileSize / 4
                        
                
                if currentMapBackgroundImage.get_height() > screenPixelHeight:
                    if currentMapY > 0:
                        currentMapY = 0
                        playerY -= tileSize / 4
                    if currentMapY < screenPixelHeight - currentMapBackgroundImage.get_height():
                        currentMapY = screenPixelHeight - currentMapBackgroundImage.get_height()
                        playerY += tileSize / 4

                    
                ## Animate player walking
                if playerDirection == 'down':
                    if frame == 0:
                        playerImage = playerDown
                        frame += 1
                    elif frame == 1:
                        playerImage = playerDownStep1
                        frame += 1
                    elif frame == 2:
                        playerImage = playerDown
                        frame += 1
                    elif frame == 3:
                        playerImage = playerDownStep2
                        frame = 0
                elif playerDirection == 'up':
                    if frame == 0:
                        playerImage = playerUp
                        frame += 1
                    elif frame == 1:
                        playerImage = playerUpStep1
                        frame += 1
                    elif frame == 2:
                        playerImage = playerUp
                        frame += 1
                    elif frame == 3:
                        playerImage = playerUpStep2
                        frame = 0
                        
                elif playerDirection == 'left':
                    if frame == 0:
                        playerImage = playerLeft
                        frame += 1
                    elif frame == 1:
                        playerImage = playerLeftStep1
                        frame += 1
                    elif frame == 2:
                        playerImage = playerLeft
                        frame += 1
                    elif frame == 3:
                        playerImage = playerLeftStep2
                        frame = 0
                elif playerDirection == 'right':
                    if frame == 0:
                        playerImage = playerRight
                        frame += 1
                    elif frame == 1:
                        playerImage = playerRightStep1
                        frame += 1
                    elif frame == 2:
                        playerImage = playerRight
                        frame += 1
                    elif frame == 3:
                        playerImage = playerRightStep2
                        frame = 0
        
    else:
        if playerDirection == 'down':
            playerImage = playerDown
        elif playerDirection == 'up':
            playerImage = playerUp
        elif playerDirection == 'left':
            playerImage = playerLeft
        elif playerDirection == 'right':
            playerImage = playerRight

    if len(movePath) <= 1:
        movePath = []
        if playerDirection == 'up':
            while playerY % tileSize != 0:
                playerY -= tileSize / 4
            while currentMapY % tileSize != 0:
                currentMapY += tileSize / 4
        elif playerDirection == 'down':
            while playerY % tileSize != 0:
                playerY += tileSize / 4
            while currentMapY % tileSize != 0:
                currentMapY -= tileSize / 4
        elif playerDirection == 'right':
            while playerX % tileSize != 0:
                playerX += tileSize / 4
            while currentMapX % tileSize != 0:
                currentMapX -= tileSize / 4
        elif playerDirection == 'left':
            while playerX % tileSize != 0:
                playerX -= tileSize / 4        
            while currentMapX % tileSize != 0:
                currentMapX += tileSize / 4
                
    if mouse1Init: # If mouse button 1 has been clicked, create a path between the player and the cursor if possible.
        newPlayerRect = pygame.Rect(abs(currentMapX) + playerRect.x, abs(currentMapY) + playerRect.y, tileSize, tileSize)
        targetRect = pygame.Rect(abs(currentMapX) + cursorRect.x, abs(currentMapY) + cursorRect.y, tileSize, tileSize)
        movePath = aStar(newPlayerRect, targetRect, currentObstacleMap, currentMapPixelDimensions)
        playerDelay = 0
        mouse1Init = False

    if escapeKeyInit: # If ESC key has been pressed, save and quit.
        escapeKeyInit = False
        saveFile = 'saves\\save_data.txt'
        saveVariables = (currentMapName, currentMapX, currentMapY, playerX, playerY)
        saveGame(saveFile, saveVariables)
        pygame.quit()
        sys.exit()
        


    currentMapLocation = (currentMapX, currentMapY)
    
    pygame.draw.rect(displaySurface, (50, 50, 50), (0, 0, currentMapPixelWidth, currentMapPixelHeight))

    drawRectangleList(currentObstacleMap, (200, 0, 0), currentMapLocation)
    drawRectangleList(currentObstacleMap, (255, 0, 0), currentMapLocation, 2)
    for i in range(len(currentObstacleMap)):
        obstacleString = "#" + str(i)
        obstacleText = gameFont.render(obstacleString, True, (255, 255, 255))
        displaySurface.blit(obstacleText, (currentObstacleMap[i].x + currentMapX, currentObstacleMap[i].y + currentMapY))

    displaySurface.blit(currentMapBackgroundImage, (currentMapX, currentMapY))
        
    playerRect = pygame.Rect((playerX, playerY - (tileSize / 2)), (tileSize, tileSize + (tileSize / 2)))
    if len(movePath) > 0:
        for i in range(len(movePath)):
            if i == len(movePath) - 1:
                break
            if i == 0:
                pygame.draw.line(displaySurface, (0, 0, 0), (playerX + tileSize / 2, playerY + tileSize / 2), (movePath[i+1].x + currentMapX + tileSize / 2, movePath[i+1].y + currentMapY + tileSize / 2))    
            else:
                pygame.draw.line(displaySurface, (0, 0, 0), (movePath[i].x + currentMapX + tileSize / 2, movePath[i].y + currentMapY + tileSize / 2), (movePath[i+1].x + currentMapX + tileSize / 2, movePath[i+1].y + currentMapY + tileSize / 2), 1)
        displaySurface.blit(targetImage, (movePath[-1].x + currentMapX, movePath[-1].y + currentMapY, tileSize, tileSize))
        
    displaySurface.blit(playerImage, (playerRect.x, playerRect.y + (tileSize / 4)))
    
    playerNameString = "Player"
    playerNameText = gameFont.render(playerNameString, True, (255, 255, 255))
    pygame.draw.rect(displaySurface,(0, 0, 0), ((playerRect.x + playerRect.width / 2) - (gameFont.size(playerNameString)[0] / 2), playerRect.y - gameFont.size(playerNameString)[1] / 2, gameFont.size(playerNameString)[0], gameFont.size(playerNameString)[1]))
    displaySurface.blit(playerNameText,((playerRect.x + playerRect.width/2) - (gameFont.size(playerNameString)[0] / 2), playerRect.y - gameFont.size(playerNameString)[1] / 2))

    displaySurface.blit(currentMapForegroundImage, (currentMapX, currentMapY))

    displaySurface.blit(cursorImage, (cursorRect.x, cursorRect.y))

    controlsString = "Press Esc to Save and Quit"
    controlsText = gameFont.render(controlsString, True, (255,255,255))
    controlsTextShadow = gameFont.render(controlsString, True, (0,0,0))
    if currentMapBackgroundImage.get_width() < screenPixelWidth:
        displaySurface.blit(controlsTextShadow, (currentMapBackgroundImage.get_width()/2 - (gameFont.size(controlsString)[0] / 2) + 2, gameFont.size(controlsString)[1] / 2 + 1))
        displaySurface.blit(controlsText, (currentMapBackgroundImage.get_width()/2 - (gameFont.size(controlsString)[0] / 2), gameFont.size(controlsString)[1] / 2))

    else:
        displaySurface.blit(controlsTextShadow,((screenMidpointX * tileSize + (tileSize / 2)) - (gameFont.size(controlsString)[0] / 2) + 2, gameFont.size(controlsString)[1] / 2 + 1))
        displaySurface.blit(controlsText,((screenMidpointX * tileSize + (tileSize / 2)) - (gameFont.size(controlsString)[0] / 2), gameFont.size(controlsString)[1] / 2))
    
    currentMapLocation = (currentMapX, currentMapY)
    
    currentMapImages = (currentMapBackgroundImage, currentMapForegroundImage)
    currentMapPixelDimensions = (currentMapPixelWidth, currentMapPixelHeight)    

    #Pack Return Variables
    playerVariables = (playerX, playerY, playerDirection, movePath, playerMove, playerDelay, playerImage, frame)
    mapVariables = (currentMapName, currentObstacleMap, currentMapImages, currentMapPixelDimensions, currentMapLocation)
    gameVariables = (mapVariables, playerVariables)
    mouseButton1 = (mouse1Held, mouse1Init)
    escapeKey = (escapeKeyHeld, escapeKeyInit)
    userInputs = (mouseButton1, mouseButton3, escapeKey)
    return currentScreen, gameVariables, userInputs


def main():
    gameVariables = ''
    saveFile = 'saves\\save_data.txt'
    loadedGame = loadGame(saveFile)
    mouse1Held = mouse1Init = False
    mouse3Held = mouse3Init = False
    mouseButton1 = (mouse1Held, mouse1Init)
    mouseButton3 = (mouse3Held, mouse3Init)
    escapeKeyHeld = escapeKeyInit = False
    escapeKey = (escapeKeyHeld, escapeKeyInit)
    userInputs = (mouseButton1, mouseButton3, escapeKey)
    playerImage = playerDown

    currentScreen = 'startGame'
    
    currentMapName = loadedGame[1].strip()
    currentMap = loadMap(currentMapName, tileSize)
    
    currentMapX, currentMapY = tileCoordinateToPixels(loadedGame[2][0], loadedGame[2][1])
    playerX, playerY = tileCoordinateToPixels(loadedGame[3][0], loadedGame[3][1])
        
    currentMapName, currentObstacleMap, currentMapImages, currentMapDimensions = currentMap
    currentMapBackgroundImage, currentMapForegroundImage = currentMapImages
    if currentMapBackgroundImage.get_width() < screenPixelWidth:
        currentMapX = 0
    if currentMapBackgroundImage.get_height() < screenPixelHeight:
        currentMapY = 0
    currentMapLocation = (currentMapX, currentMapY)
    mapVariables = (currentMapName, currentObstacleMap, currentMapImages, currentMapDimensions, currentMapLocation)
    
    playerVariables = (playerX, playerY, '', '', False, '', playerImage, 0)
    gameVariables = (mapVariables, playerVariables)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse1Held = True
                    mouse1Init = True
                    mouseButton1 = (mouse1Held, mouse1Init)
                    userInputs = (mouseButton1, (False, False), (False, False))
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    mouse1Held = False
                    mouse1Init = False
                    mouseButton1 = (mouse1Held, mouse1Init)
                    userInputs = (mouseButton1, (False, False), (False, False))
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    escapeKeyHeld = True
                    escapeKeyInit = True
                    escapeKey = (escapeKeyHeld, escapeKeyInit)
                    userInputs = ((False, False), (False, False), escapeKey)
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    escapeKeyHeld = False
                    escapeKeyInit = False
                    escapeKey = (escapeKeyHeld, escapeKeyInit)
                    userInputs = ((False, False), (False, False), escapeKey)
            if event.type == KEYUP:
                keyHeld = False
                

        if currentScreen == 'startGame':
            currentScreen, gameVariables, userInputs = startGame(event, currentScreen, gameVariables, userInputs)
    
        pygame.display.update()
        fpsClock.tick(60)
main()
