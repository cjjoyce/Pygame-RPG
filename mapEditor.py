import pygame
import sys
import random
import time
import re
import os
from pygame import *
pygame.init()

displaySurface = pygame.display.set_mode((100, 100), 0, 32)
pygame.display.set_caption('Map Editor')
fps = 60
fpsClock = pygame.time.Clock()
pygame.key.set_repeat(1, 250)
tileSize = 32
mapPixelWidth = tileSize * 30
mapPixelHeight = tileSize * 20

cursorColour = (255, 255, 255)
def tileCoordinateToPixels(x, y):
    tileX = x * tileSize
    tileY = y * tileSize
    return tileX, tileY

def tilePixelsToCoordinates(x, y):
    tileX = x / tileSize
    tileY = y / tileSize
    return tileX, tileY

def replaceLine(fileName, lineNum, text):
    lines = open(fileName, 'r').readlines()
    lines[lineNum] = text
    out = open(fileName, 'w')
    out.writelines(lines)
    out.close()

def addLine(fileName, text):
    f = open(fileName, 'a')
    f.write(text)
    f.close()

def clearFile(fileName):
    f = open(fileName, "w")
    f.seek(0)
    f.truncate()

def saveMap(fileName, currentMap):
    clearFile(fileName)
    for i in range(len(currentMap)):
        x, y = tilePixelsToCoordinates(currentMap[i].x, currentMap[i].y)
        width, height = tilePixelsToCoordinates(currentMap[i].width, currentMap[i].height)
        lineString = str(int(x)) + "," + str(int(y)) + "," + str(int(width)) + "," + str(int(height))
        # Don't add a new line at the end of the file
        if i < len(currentMap) - 1:
            lineString += "\n"
        addLine(fileName, lineString)

# Load map tiles from a text file into a list of rectangles
def createRectangleList(fileName):
    file = open(fileName, 'r')
    lines = file.readlines()
    rectangleList = []
    # Retrieve values from text file and append to rectangleList
    for i in range(len(lines)):
        lineString = lines[i]
        x, y, width, height = lineString.split(",")
        tileX, tileY = tileCoordinateToPixels(int(x), int(y))
        width, height = tileCoordinateToPixels(int(width), int(height))
        rectangleList.append(pygame.Rect(tileX, tileY, width, height))

    file.close()
    return rectangleList

# Draw all rectangles from a rectangle list
def drawRectangleList(rectangleList, colour, width=0):
    for i in range(len(rectangleList)):
        pygame.draw.rect(displaySurface, colour, rectangleList[i], width)

def createNewMap(newMapName):
    path = os.getcwd()
    os.mkdir(path + '\\maps\\' + newMapName)
    f = open("maps\\" + newMapName + "\\obstacles.txt","w+")
    f.close
    f = open("maps\\" + newMapName + "\\portals.txt","w+")
    f.close

def mapSelector(event, currentScreen):
    currentMap = ''
    mapSelections = ''
    rectangleMaps = ''
    mapImage = ''
    selectedMap = "exampleMap"

    selectedLayer = 'Obstacles'
    cursorColour = (255, 0, 0)
    obstacleMap = createRectangleList('maps\\' + selectedMap + '\\obstacles.txt')
    portalMap = createRectangleList('maps\\' + selectedMap + '\\portals.txt')

    currentMap = obstacleMap
    rectangleMaps = (currentMap, obstacleMap, portalMap)
    print("Map layer file loaded.")
    
    mapImage = pygame.image.load('maps\\' + selectedMap + '\\mapBackground.png')
    mapImage = pygame.transform.scale(mapImage,(mapPixelWidth, mapPixelHeight))
    print("Map image file Loaded.")

    print("Obstacles: " + str(len(obstacleMap)) + ", Portals: " + str(len(portalMap)))
    mapSelections = (selectedMap, selectedLayer, cursorColour)
    displaySurface = pygame.display.set_mode((mapPixelWidth, mapPixelHeight), 0, 32)
    currentScreen = 'mapEditor'

    return currentScreen, mapSelections, rectangleMaps, mapImage

def mapEditor(event, currentScreen, mapSelections, rectangleMaps, keyHeld, mapImage, displayImage, clickAndDrag, userInputs):
    (mouseX, mouseY) = pygame.mouse.get_pos()
    (mouseXCoord, mouseYCoord) = tilePixelsToCoordinates(mouseX, mouseY)
    mouseXCoord = int(mouseXCoord)
    mouseYCoord = int(mouseYCoord)
    
    cursorRect = pygame.Rect(mouseXCoord * tileSize, mouseYCoord * tileSize, tileSize, tileSize)
    startRect, endRect, dragRect = clickAndDrag
    selectedMap, selectedLayer, cursorColour = mapSelections
    currentMap, obstacleMap, portalMap = rectangleMaps
    mouseButton1, mouseButton3 = userInputs
    mouse1Held, mouse1Init = mouseButton1
    mouse3Held, mouse3Init = mouseButton3
    pygame.display.set_caption('Map Editor - Map: ' + selectedMap + ', Layer: ' + selectedLayer + ' (' + str(len(currentMap)) + ')' + ' - X: ' + str(mouseXCoord) + ', Y: ' + str(mouseYCoord) + ' | SPACE: Save, ESC: Quit, L/R Arrows: Change Layer, Up Arrow: Toggle Image')
    
    if mouse3Held:
        if mouse3Init:
            for i in currentMap[:]:
                if (mouseXCoord * tileSize == i.x) and (mouseYCoord * tileSize == i.y):
                    currentMap.remove(i)
            mouse3Init = False
            
    if mouse1Held:
        if mouse1Init:
            startRect = pygame.Rect(mouseXCoord * tileSize, mouseYCoord * tileSize, tileSize, tileSize)
            mouse1Init = False
        dragRect.x = startRect.x
        dragRect.y = startRect.y
        if cursorRect.x >= startRect.x and cursorRect.y >= startRect.y:
            dragRect.width = abs(cursorRect.x - startRect.x) + tileSize
            dragRect.height = abs(cursorRect.y - startRect.y) + tileSize
        elif cursorRect.x < startRect.x and cursorRect.y > startRect.y:
            dragRect.width = abs(cursorRect.x - startRect.x) + tileSize
            dragRect.x = cursorRect.x
            dragRect.height = abs(cursorRect.y - startRect.y) + tileSize
        elif cursorRect.x > startRect.x and cursorRect.y < startRect.y:
            dragRect.width = abs(cursorRect.x - startRect.x) + tileSize
            dragRect.height = abs(cursorRect.y - startRect.y) + tileSize
            dragRect.y = cursorRect.y
        else:
            dragRect.width = abs(cursorRect.x - startRect.x) + tileSize
            dragRect.height = abs(cursorRect.y - startRect.y) + tileSize
            dragRect.x = cursorRect.x
            dragRect.y = cursorRect.y
        
    if mouse1Held == False and mouse1Init:
        endRect = pygame.Rect(mouseXCoord * tileSize, mouseYCoord * tileSize, tileSize, tileSize)
        if endRect.x >= startRect.x and endRect.y >= startRect.y:
            startRect.width = abs(endRect.x - startRect.x) + tileSize
            startRect.height = abs(endRect.y - startRect.y) + tileSize
            currentMap.append(startRect)
        elif endRect.x < startRect.x and endRect.y > startRect.y:
            startRect.width = abs(endRect.x - startRect.x) + tileSize
            startRect.x = endRect.x
            startRect.height = abs(endRect.y - startRect.y) + tileSize
            currentMap.append(startRect)
        elif endRect.x > startRect.x and endRect.y < startRect.y:
            startRect.width = abs(endRect.x - startRect.x) + tileSize
            startRect.height = abs(endRect.y - startRect.y) + tileSize
            startRect.y = endRect.y
            currentMap.append(startRect)
        else:
            startRect.width = abs(endRect.x - startRect.x) + tileSize
            startRect.height = abs(endRect.y - startRect.y) + tileSize
            startRect.x = endRect.x
            startRect.y = endRect.y
            currentMap.append(startRect)
        mouse1Init = False
                    
    if event.type == KEYDOWN:
        if event.key == (K_ESCAPE):
            pygame.quit()
            sys.exit()

        if event.key == (K_SPACE) and keyHeld == False:
            keyHeld = True
            try:
                saveMap('maps\\' + selectedMap + '\\obstacles.txt', obstacleMap)
                saveMap('maps\\' + selectedMap + '\\portals.txt', portalMap)
                print("Map saved successfully to: maps" + '\\' + selectedMap)
            except:
                print("Failed to save map.")

        if event.key == (K_LEFT) and keyHeld == False:
            keyHeld = True
            if selectedLayer == 'Obstacles':
                selectedLayer = 'Portals'
                obstacleMap = currentMap
                currentMap = portalMap
                cursorColour = (0, 0, 255)
                
            elif selectedLayer == 'Portals':
                selectedLayer = 'Obstacles'
                portalMap = currentMap
                currentMap = obstacleMap
                cursorColour = (255, 0, 0)

        if event.key == (K_RIGHT) and keyHeld == False:
            keyHeld = True
            if selectedLayer == 'Obstacles':
                selectedLayer = 'Portals'
                obstacleMap = currentMap
                currentMap = portalMap
                cursorColour = (0, 0, 255)
                
            elif selectedLayer == 'Portals':
                selectedLayer = 'Obstacles'
                portalMap = currentMap
                currentMap = obstacleMap
                cursorColour = (255, 0, 0)
                
        if event.key == (K_UP) and keyHeld == False:
            keyHeld = True
            if displayImage == False:
                displayImage = True
            else:
                displayImage = False

    if event.type == KEYUP:
        keyHeld = False
        
    pygame.draw.rect(displaySurface, (64, 64, 64), (0, 0, mapPixelWidth, mapPixelHeight))
    drawRectangleList(obstacleMap, (200, 0, 0))
    drawRectangleList(portalMap, (0, 0, 200))
    drawRectangleList(obstacleMap, (255, 0, 0), 2)
    drawRectangleList(portalMap, (0, 0, 255), 2)
    if mouse1Held:
        pygame.draw.rect(displaySurface, (255, 255, 255), dragRect)
        pygame.draw.rect(displaySurface, (0, 0, 0), dragRect, 2)
    if displayImage == True:
        blit_alpha(displaySurface, mapImage, (0, 0), 128)
    pygame.draw.rect(displaySurface, (cursorColour), ((mouseXCoord) * tileSize, (mouseYCoord) * tileSize, tileSize, tileSize))
    mapSelections = (selectedMap, selectedLayer, cursorColour)
    clickAndDrag = startRect, endRect, dragRect
    rectangleMaps = (currentMap, obstacleMap, portalMap)
    mouseButton1 = (mouse1Held, mouse1Init)
    mouseButton3 = (mouse3Held, mouse3Init)
    userInputs = (mouseButton1, mouseButton3)
    return currentScreen, mapSelections, rectangleMaps, keyHeld, mapImage, displayImage, clickAndDrag, userInputs

def blit_alpha(target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)        
        target.blit(temp, location)

def main():
    keyHeld = False
    displayImage = True
    clickAndDrag = pygame.Rect(-1, -1, tileSize, tileSize), pygame.Rect(-1, -1, tileSize, tileSize), pygame.Rect(-1, -1, tileSize, tileSize)
    currentScreen = 'mapSelector'
    userInputs = ((False, False), (False, False))
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
                    userInputs = (mouseButton1, (False, False))
                if event.button == 3:
                    mouse3Held = True
                    mouse3Init = True
                    mouseButton3 = (mouse3Held, mouse3Init)
                    userInputs = ((False, False), mouseButton3)
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    mouse1Held = False
                    mouse1Init = True
                    mouseButton1 = (mouse1Held, mouse1Init)
                    userInputs = (mouseButton1, (False, False))
                if event.button == 3:
                    mouse3Held = False
                    mouse3Init = True
                    mouseButton3 = (mouse3Held, mouse3Init)
                    userInputs = ((False, False), mouseButton3)
        if currentScreen == 'mapSelector':
            currentScreen, mapSelections, rectangleMaps, mapImage = mapSelector(event, currentScreen)
        elif currentScreen == 'mapEditor':
            currentScreen, mapSelections, rectangleMaps, keyHeld, mapImage, displayImage, clickAndDrag, userInputs = mapEditor(event, currentScreen, mapSelections, rectangleMaps, keyHeld, mapImage, displayImage, clickAndDrag, userInputs)
        pygame.display.update()
        fpsClock.tick(fps)

main()
