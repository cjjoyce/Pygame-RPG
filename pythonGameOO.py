import pygame
import sys
import re
from pygame import *

class Player():
    def __init__(self, location, direction):
        self.location = game.tileCoordinatesToPixels(location[0], location[1]) # Tuple containing the Player's X and Y Coordinates.
        self.rect = pygame.Rect(self.location, (game.tileSize, game.tileSize)) # Pygame Rectangle object which uses the player's location and the game's tilesize.
        self.direct = direction # String which states the direction that the Player is facing.
        self.path = [] # List in which Pygame Rectangle objects are added during the execution of Player.createPath() method and used during the Player.move() method.
        self.frame = 0 # Integer which increments every time the Player takes a step which is used for animating the Player sprite during the Player.move() method.
        self.sprites = [] # List of sprites which are added during the execution of Player.setSprite() method and used to animate the Player sprite in the Player.move() method.
        self.dt = 0 # Integer used to slow the Player's movement.
        
        self.setSprite()    # Load sprites and set initial sprite.

    def updateSize(self, oldTileSize):
        scale = (oldTileSize / game.tileSize)
        self.rect = pygame.Rect((int(self.rect.x / scale), int(self.rect.y / scale)), (game.tileSize, game.tileSize))
        self.setSprite()
        #self.image = pygame.transform.scale(self.image, (game.tileSize, int(game.tileSize + (game.tileSize / 4))))

    def setSprite(self):
        # Load all sprite images and scale based on the Game's tilesize.
        playerUp = pygame.image.load('images\\sprites\\playerUp.png')
        playerUp = pygame.transform.scale(playerUp,(game.tileSize, int(game.tileSize + (game.tileSize / 4))))
        playerUpStep1 = pygame.image.load('images\\sprites\\playerUpStep1.png')
        playerUpStep1 = pygame.transform.scale(playerUpStep1,(game.tileSize, int(game.tileSize + (game.tileSize / 4))))
        playerUpStep2 = pygame.image.load('images\\sprites\\playerUpStep2.png')
        playerUpStep2 = pygame.transform.scale(playerUpStep2,(game.tileSize, int(game.tileSize + (game.tileSize / 4))))
        
        playerDown = pygame.image.load('images\\sprites\\playerDown.png')
        playerDown = pygame.transform.scale(playerDown,(game.tileSize, int(game.tileSize + (game.tileSize / 4))))
        playerDownStep1 = pygame.image.load('images\\sprites\\playerDownStep1.png')
        playerDownStep1 = pygame.transform.scale(playerDownStep1,(game.tileSize, int(game.tileSize + (game.tileSize / 4))))
        playerDownStep2 = pygame.image.load('images\\sprites\\playerDownStep2.png')
        playerDownStep2 = pygame.transform.scale(playerDownStep2,(game.tileSize, int(game.tileSize + (game.tileSize / 4))))

        playerLeft = pygame.image.load('images\\sprites\\playerLeft.png')
        playerLeft = pygame.transform.scale(playerLeft,(game.tileSize, int(game.tileSize + (game.tileSize / 4))))
        playerLeftStep1 = pygame.image.load('images\\sprites\\playerLeftStep1.png')
        playerLeftStep1 = pygame.transform.scale(playerLeftStep1,(game.tileSize, int(game.tileSize + (game.tileSize / 4))))
        playerLeftStep2 = pygame.image.load('images\\sprites\\playerLeftStep2.png')
        playerLeftStep2 = pygame.transform.scale(playerLeftStep2,(game.tileSize, int(game.tileSize + (game.tileSize / 4))))

        playerRight = pygame.image.load('images\\sprites\\playerRight.png')
        playerRight = pygame.transform.scale(playerRight,(game.tileSize, int(game.tileSize + (game.tileSize / 4))))
        playerRightStep1 = pygame.image.load('images\\sprites\\playerRightStep1.png')
        playerRightStep1 = pygame.transform.scale(playerRightStep1,(game.tileSize, int(game.tileSize + (game.tileSize / 4))))
        playerRightStep2 = pygame.image.load('images\\sprites\\playerRightStep2.png')
        playerRightStep2 = pygame.transform.scale(playerRightStep2,(game.tileSize, int(game.tileSize + (game.tileSize / 4))))

        # Set sprite based on the direction the player is facing.
        if self.direct == 'up':
            self.image = playerUp
        elif self.direct == 'down':
            self.image = playerDown
        elif self.direct == 'left':
            self.image = playerLeft
        elif self.direct == 'right':
            self.image = playerRight

        # Player.sprites is updated as a two-dimensional list containing a list of sprites for each Player direction.
        upSprites = [playerUp, playerUpStep1, playerUpStep2]
        downSprites = [playerDown, playerDownStep1, playerDownStep2]
        leftSprites = [playerLeft, playerLeftStep1, playerLeftStep2]
        rightSprites = [playerRight, playerRightStep1, playerRightStep2]
        
        self.sprites = [upSprites, downSprites, leftSprites, rightSprites]
        
    def createPath(self, cursorObj, mapObj):
        self.path = game.aStar(self.rect, cursorObj.rect, mapObj.obstacles, mapObj.dimensions)

    def drawPath(self):
        for i in range(len(self.path)):
            if i == len(self.path) - 1:
                break
            if i == 0:
                pygame.draw.line(game.surface, (0, 0, 0), (self.rect.x + game.tileSize / 2, self.rect.y + game.tileSize / 2), (self.path[i+1].x + game.tileSize / 2, self.path[i+1].y + game.tileSize / 2))
            else:
                pygame.draw.line(game.surface, (0, 0, 0), (self.path[i].x + game.tileSize / 2, self.path[i].y + game.tileSize / 2), (self.path[i+1].x + game.tileSize / 2, self.path[i+1].y + game.tileSize / 2), 1)

    def drawRect(self):
        pygame.draw.rect(game.surface, (0, 255, 0), self.rect)

    def displaySprite(self):
        game.surface.blit(self.image, (self.rect.x, self.rect.y - game.tileSize / 4))
        
    def move(self):
        self.dt += 1
        if self.dt % 7 == 0:
            if self.rect.y > self.path[1].y:
                self.rect.y -= (game.tileSize / 4)
                self.direct = 'up'
            elif self.rect.y < self.path[1].y:
                self.rect.y += (game.tileSize / 4)
                self.direct = 'down'
            elif self.rect.x > self.path[1].x:
                self.rect.x -= (game.tileSize / 4)
                self.direct = 'left'                
            elif self.rect.x < self.path[1].x:
                self.rect.x += (game.tileSize / 4)
                self.direct = 'right'

            if self.rect.x == self.path[1].x and self.rect.y == self.path[1].y:
                self.path.pop(0)
            else:
                if self.direct == 'up':
                    if self.frame == 0:
                        self.image = self.sprites[0][0]
                    elif self.frame == 1:
                        self.image = self.sprites[0][1]
                    elif self.frame == 2:
                        self.image = self.sprites[0][0]
                    elif self.frame == 3:
                        self.image = self.sprites[0][2]
                        
                elif self.direct == 'down':
                    if self.frame == 0:
                        self.image = self.sprites[1][0]
                    elif self.frame == 1:
                        self.image = self.sprites[1][1]
                    elif self.frame == 2:
                        self.image = self.sprites[1][0]
                    elif self.frame == 3:
                        self.image = self.sprites[1][2]
                        
                elif self.direct == 'left':
                    if self.frame == 0:
                        self.image = self.sprites[2][0]
                    elif self.frame == 1:
                        self.image = self.sprites[2][1]
                    elif self.frame == 2:
                        self.image = self.sprites[2][0]
                    elif self.frame == 3:
                        self.image = self.sprites[2][2]
                        
                elif self.direct == 'right':
                    if self.frame == 0:
                        self.image = self.sprites[3][0]
                    elif self.frame == 1:
                        self.image = self.sprites[3][1]
                    elif self.frame == 2:
                        self.image = self.sprites[3][0]
                    elif self.frame == 3:
                        self.image = self.sprites[3][2]

                self.frame += 1
                if self.frame == 4:
                    self.frame = 0

        

class Map():
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.obstacles = self.createRectangleList('maps\\' + self.name + '\\obstacles.txt')
        self.defaultBackgroundImage = pygame.image.load('maps\\' + self.name + '\\mapBackground.png')
        self.defaultDimensions = (self.defaultBackgroundImage.get_width(), self.defaultBackgroundImage.get_height())
        self.backgroundImage = pygame.transform.scale(self.defaultBackgroundImage,(int((self.defaultDimensions[0] / 32) * game.tileSize), int((self.defaultDimensions[1] / 32) * game.tileSize)))
        self.dimensions = (self.backgroundImage.get_width(), self.backgroundImage.get_height())
        
    def updateSize(self):
        self.backgroundImage = pygame.transform.scale(self.defaultBackgroundImage,(int((self.defaultDimensions[0] / 32) * game.tileSize), int((self.defaultDimensions[1] / 32) * game.tileSize)))
        self.dimensions = (self.backgroundImage.get_width(), self.backgroundImage.get_height())
        self.obstacles = self.createRectangleList('maps\\' + self.name + '\\obstacles.txt')
        
    def createRectangleList(self, fileName):
        file = open(fileName, 'r')
        lines = file.readlines()
        rectangleList = []

        # Retrieve values from text file and append to rectangleList
        for i in range(int(len(lines) / 5)):
            tileX, tileY = game.tileCoordinatesToPixels(int(lines[i * 5 + 1]), int(lines[i * 5 + 2]))
            width, height = game.tileCoordinatesToPixels(int(lines[i * 5 + 3]), int(lines[i * 5 + 4]))
            rectangleList.append(pygame.Rect(tileX, tileY, width, height))

        file.close()
        return rectangleList
    
    def drawObstacles(self, colour, width=0):
        for i in self.obstacles[:]:
            pygame.draw.rect(game.surface, colour, i, width)

    def displayBackgroundImage(self):
        game.surface.blit(self.backgroundImage,(self.location[0], self.location[1]))

class Cursor():
    def __init__(self):
        self.x = pygame.mouse.get_pos()[0]
        self.y = pygame.mouse.get_pos()[1]
        self.rect = pygame.Rect((int(self.x / game.tileSize) * game.tileSize, int(self.y / game.tileSize) * game.tileSize), (game.tileSize, game.tileSize))
    def update(self):
        self.x = pygame.mouse.get_pos()[0]
        self.y = pygame.mouse.get_pos()[1]
        self.rect = pygame.Rect((int(self.x / game.tileSize) * game.tileSize, int(self.y / game.tileSize) * game.tileSize), (game.tileSize, game.tileSize))

class Node(): # Used by the Game.aStar() Method to represent a tile.
    def __init__(self, parent=None, rect=None, obstacle=False):
        self.parent = parent
        self.rect = rect
        self.obstacle = obstacle 

        self.g = 0 # Node's G Cost (Distance to Start node)
        self.h = 0 # Node's H Cost (Distance to Target node)
        self.f = 0 # G cost + H Cost

    def __eq__(self, other):
        return self.rect == other.rect

class Game():
    def __init__(self, tileSize):
        self.tileSize = tileSize
        self.surface = pygame.display.set_mode((960, 640))
        
    def tileCoordinatesToPixels(self, x, y):
        tileX = x * self.tileSize
        tileY = y * self.tileSize
        return tileX, tileY

    def tilePixelsToCoordinates(self, x, y):
        tileX = x / self.tileSize
        tileY = y / self.tileSize
        return (tileX, tileY)

    def getNeighbours(self, node):
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

    def getDistance(self, rectA, rectB):
        xDistance = abs((rectA.x)/32 - (rectB.x)/32)
        yDistance = abs((rectA.y)/32 - (rectB.y)/32)

        if xDistance > yDistance:
            return 14 * yDistance + 10 * (xDistance - yDistance)
        else:
            return 14 * xDistance + 10 * (yDistance - xDistance)
        
    def calculateCosts(self, node, startNode, targetNode):
        gCost = getDistance(node, startNode)
        hCost = getDistance(node, targetNode)
        fCost = gCost + hCost
        return gCost, hCost, fCost

    def aStar(self, startRect, targetRect, obstacleMap, mapDimensions):
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
                    checkX = currentNode.rect.x + (x * self.tileSize)
                    checkY = currentNode.rect.y + (y * self.tileSize)
                    newObstacle = False
                    for obstacle in obstacleMap[:]:
                        if pygame.Rect(checkX, checkY, self.tileSize, self.tileSize).colliderect(obstacle):
                            newObstacle = True
                            break
                    if checkX >= 0 and checkX < mapPixelWidth and checkY >= 0 and checkY < mapPixelHeight:
                        newRect = pygame.Rect(checkX, checkY, self.tileSize, self.tileSize)

                        newNode = Node(currentNode, newRect, newObstacle)
                            
                        if newNode.obstacle == False:
                            children.append(newNode)
            for child in children:
                for closedChild in closedSet:
                    if child == closedChild:
                        break
                else:

                    child.g = currentNode.g + 1
                    child.h = self.getDistance(child.rect, targetNode.rect)
                    child.f = child.g + child.h

                    for openNode in openSet:
                        if child == openNode and child.g >= openNode.g:
                            break
                    else:
                        openSet.append(child)
        return []

    def initArea(self, mapName):
        self.tilemap = Map(mapName, (0, 0))
        self.player = Player((6, 8), 'down')
        self.cursor = Cursor()

    def main(self):
        self.initArea("exampleMap")
        
        fpsClock = pygame.time.Clock()
        mouse1Init = False
        mouse3Init = False

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse1Held = True
                        mouse1Init = True
                        
                    if event.button == 3:
                        mouse3Held = True
                        mouse3Init = True
                        
                if event.type == MOUSEBUTTONUP:
                    if event.button == 1:
                        mouse1Held = False
                        mouse1Init = False
                        
                    if event.button == 3:
                        mouse3Held = False
                        mouse3Init = False
                        
            pygame.draw.rect(game.surface, (255,255,255), (0,0,960,640))
            self.tilemap.drawObstacles((0, 0, 255))
            if mouse1Init:
                mouse1Init = False
                self.player.createPath(self.cursor, self.tilemap)
            if mouse3Init:
                mouse3Init = False
                oldTileSize = game.tileSize
                game.tileSize = 16
                self.player.updateSize(oldTileSize)
                self.tilemap.updateSize()
                
            self.tilemap.displayBackgroundImage()
            
            if len(self.player.path) > 1:
                self.player.move()
                self.player.drawPath()
            else:
                self.player.setSprite()
        
            self.player.displaySprite()
            pygame.draw.rect(game.surface, (255,0,0), self.cursor.rect, 2)
            self.cursor.update()
            pygame.display.update()
            fpsClock.tick(60)


if __name__ == '__main__':
    pygame.init()
    game = Game(32)
    game.main()
