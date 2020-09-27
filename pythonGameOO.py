import pygame
import sys
import re
import random
from pygame import *

class Character():
    def __init__(self, location, direction, spriteSet):
        self.location = game.tileCoordinatesToPixels(location[0], location[1]) # Tuple containing the Character's X and Y Coordinates.
        self.rect = pygame.Rect(self.location, (game.tileSize, game.tileSize)) # Pygame Rectangle object which uses the Character's location and the Game's tilesize.
        self.direct = direction # String which states the direction that the Character is facing.
        self.spriteSet = spriteSet
        self.path = [] # List in which Pygame Rectangle objects are added during the execution of Player.createPath() method and used during the Player.move() method.
        self.frame = 0 # Integer which increments every time the Character takes a step which is used for animating the Character sprite during the Character.animateMovement() method.
        self.sprites = [] # List of sprites which are added during the execution of Character.setSprite() method and used to animate the Player sprite in the Character.animateMovement() method.
        self.dt = 0 # Integer used to slow the Character's movement.
        self.isMoving = False
        
        self.setSprite() # Load sprites and set initial sprite.

    def setSprite(self):
        # Load all sprite images and scale based on the Game's tilesize.
        spriteUp = pygame.image.load('images\\sprites\\' + self.spriteSet + '\\' + self.spriteSet + 'Up.png')
        spriteUp = pygame.transform.scale(spriteUp,(game.tileSize, int(game.tileSize + (game.tileSize / 4))))
        spriteUpStep1 = pygame.image.load('images\\sprites\\' + self.spriteSet + '\\' + self.spriteSet + 'UpStep1.png')
        spriteUpStep1 = pygame.transform.scale(spriteUpStep1,(game.tileSize, int(game.tileSize + (game.tileSize / 4))))
        spriteUpStep2 = pygame.image.load('images\\sprites\\' + self.spriteSet + '\\' + self.spriteSet + 'UpStep2.png')
        spriteUpStep2 = pygame.transform.scale(spriteUpStep2,(game.tileSize, int(game.tileSize + (game.tileSize / 4))))
        
        spriteDown = pygame.image.load('images\\sprites\\' + self.spriteSet + '\\' + self.spriteSet + 'Down.png')
        spriteDown = pygame.transform.scale(spriteDown,(game.tileSize, int(game.tileSize + (game.tileSize / 4))))
        spriteDownStep1 = pygame.image.load('images\\sprites\\' + self.spriteSet + '\\' + self.spriteSet + 'DownStep1.png')
        spriteDownStep1 = pygame.transform.scale(spriteDownStep1,(game.tileSize, int(game.tileSize + (game.tileSize / 4))))
        spriteDownStep2 = pygame.image.load('images\\sprites\\' + self.spriteSet + '\\' + self.spriteSet + 'DownStep2.png')
        spriteDownStep2 = pygame.transform.scale(spriteDownStep2,(game.tileSize, int(game.tileSize + (game.tileSize / 4))))

        spriteLeft = pygame.image.load('images\\sprites\\' + self.spriteSet + '\\' + self.spriteSet + 'Left.png')
        spriteLeft = pygame.transform.scale(spriteLeft,(game.tileSize, int(game.tileSize + (game.tileSize / 4))))
        spriteLeftStep1 = pygame.image.load('images\\sprites\\' + self.spriteSet + '\\' + self.spriteSet + 'LeftStep1.png')
        spriteLeftStep1 = pygame.transform.scale(spriteLeftStep1,(game.tileSize, int(game.tileSize + (game.tileSize / 4))))
        spriteLeftStep2 = pygame.image.load('images\\sprites\\' + self.spriteSet + '\\' + self.spriteSet + 'LeftStep2.png')
        spriteLeftStep2 = pygame.transform.scale(spriteLeftStep2,(game.tileSize, int(game.tileSize + (game.tileSize / 4))))

        spriteRight = pygame.image.load('images\\sprites\\' + self.spriteSet + '\\' + self.spriteSet + 'Right.png')
        spriteRight = pygame.transform.scale(spriteRight,(game.tileSize, int(game.tileSize + (game.tileSize / 4))))
        spriteRightStep1 = pygame.image.load('images\\sprites\\' + self.spriteSet + '\\' + self.spriteSet + 'RightStep1.png')
        spriteRightStep1 = pygame.transform.scale(spriteRightStep1,(game.tileSize, int(game.tileSize + (game.tileSize / 4))))
        spriteRightStep2 = pygame.image.load('images\\sprites\\' + self.spriteSet + '\\' + self.spriteSet + 'RightStep2.png')
        spriteRightStep2 = pygame.transform.scale(spriteRightStep2,(game.tileSize, int(game.tileSize + (game.tileSize / 4))))

        # Set sprite based on the direction the character is facing.
        if self.direct == 'up':
            self.image = spriteUp
        elif self.direct == 'down':
            self.image = spriteDown
        elif self.direct == 'left':
            self.image = spriteLeft
        elif self.direct == 'right':
            self.image = spriteRight

        # sprite.sprites is updated as a two-dimensional list containing a list of sprites for each Character direction.
        upSprites = [spriteUp, spriteUpStep1, spriteUpStep2]
        downSprites = [spriteDown, spriteDownStep1, spriteDownStep2]
        leftSprites = [spriteLeft, spriteLeftStep1, spriteLeftStep2]
        rightSprites = [spriteRight, spriteRightStep1, spriteRightStep2]
        
        self.sprites = [upSprites, downSprites, leftSprites, rightSprites]

    def updateSize(self, oldTileSize):
        scale = (oldTileSize / game.tileSize)
        self.rect = pygame.Rect((int(self.rect.x / scale), int(self.rect.y / scale)), (game.tileSize, game.tileSize))
        self.setSprite()
        #self.image = pygame.transform.scale(self.image, (game.tileSize, int(game.tileSize + (game.tileSize / 4))))

    def drawRect(self, colour=(0,0,0), width=0): # Draw the Character's rect object.
        pygame.draw.rect(game.surface, colour, self.rect, width)
        
    def displaySprite(self): # Displays the Character's sprite. Default sprite height is 40.
        game.surface.blit(self.image, (self.rect.x, self.rect.y - game.tileSize / 4))

    def animateMovement(self):
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
            
class NPC(Character):
    def __init__(self, location, direction, spriteSet, behaviour, wanderRange):
        super().__init__(location, direction, spriteSet)
        self.behaviour = behaviour
        self.wanderRange = wanderRange
        
    def drawWanderRange(self):
        # Draw the NPC's starting position
        pygame.draw.rect(game.surface,(0, 255, 255), (self.location, (game.tileSize, game.tileSize)), 1)
        # Draw the NPC's wander range
        pygame.draw.rect(game.surface, (0, 255, 255), ((self.location[0] - (self.wanderRange * game.tileSize), self.location[1] - (self.wanderRange * game.tileSize)), (game.tileSize + ((self.wanderRange * game.tileSize)*2), (game.tileSize + ((self.wanderRange * game.tileSize)*2)))), 1)
        
    def doBehaviour(self, mapObj):
        if self.behaviour == 'wander':
            self.wander(mapObj)
        elif self.behaviour == 'followPlayer':
            self.followPlayer()
        
    def wander(self, mapObj): # NPC moves around randomly.
        self.dt += 1
        if self.dt % 7 == 0:
            if self.isMoving == False:
                i = random.randint(0, 8)
                if i == 1:
                    self.direct = 'up'
                    self.isMoving = True
                elif i == 2:
                    self.direct = 'down'
                    self.isMoving = True
                elif i == 3:
                    self.direct = 'left'
                    self.isMoving = True
                elif i == 4:
                    self.direct = 'right'
                    self.isMoving = True
                    
            if self.isMoving == True:
                if self.direct == 'up':
                    self.rect.y -= (game.tileSize / 4)
                    for i in mapObj.obstacles[:]:
                        if self.rect.colliderect(i) or self.rect.y < self.location[1] - (self.wanderRange * game.tileSize):
                            self.rect.y += (game.tileSize / 4)
                            self.isMoving = False
                elif self.direct == 'down':
                    self.rect.y += (game.tileSize / 4)
                    for i in mapObj.obstacles[:]:
                        if self.rect.colliderect(i) or self.rect.y > self.location[1] + (self.wanderRange * game.tileSize):
                            self.rect.y -= (game.tileSize / 4)
                            self.isMoving = False
                elif self.direct == 'left':
                    self.rect.x -= (game.tileSize / 4)
                    for i in mapObj.obstacles[:]:
                        if self.rect.colliderect(i) or self.rect.x < self.location[0] - (self.wanderRange * game.tileSize):
                            self.rect.x += (game.tileSize / 4)
                            self.isMoving = False
                elif self.direct == 'right':
                    self.rect.x += (game.tileSize / 4)
                    for i in mapObj.obstacles[:]:
                        if self.rect.colliderect(i) or self.rect.x > self.location[0] + (self.wanderRange * game.tileSize):
                            self.rect.x -= (game.tileSize / 4)
                            self.isMoving = False
                if self.rect.x % game.tileSize == 0 and self.rect.y % game.tileSize == 0:
                    self.isMoving = False
                    
                self.animateMovement()
    
    def talk(self, message): # Displays an NPC message on the screen.
        pass

    def followPlayer(self): # NPC follows the player.
        pass

class Player(Character):
    def createPath(self, cursorObj, mapObj): # Creates a route around the Map's obstacles from the Player rect to the Cursor rect.
        self.path = game.aStar(self.rect, cursorObj.rect, mapObj.obstacles, mapObj.dimensions)

    def drawPath(self): # Draws a line of the route created in the createPath() method.
        for i in range(len(self.path)):
            if i == len(self.path) - 1:
                break
            if i == 0: # Draw a line from the centre of Player.rect to the centre of the first rect of Player.path.
                pygame.draw.line(game.surface, (0, 0, 0), (self.rect.x + game.tileSize / 2, self.rect.y + game.tileSize / 2), (self.path[i+1].x + game.tileSize / 2, self.path[i+1].y + game.tileSize / 2))
            else: # Draw a line from the centre of the current rect in Player.path to the centre of the next rect in Player.path.
                pygame.draw.line(game.surface, (0, 0, 0), (self.path[i].x + game.tileSize / 2, self.path[i].y + game.tileSize / 2), (self.path[i+1].x + game.tileSize / 2, self.path[i+1].y + game.tileSize / 2), 1)
        
    def followPath(self):
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
                self.animateMovement()

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
        
    # Load map tiles from a text file into a list of rectangles
    def createRectangleList(self, fileName):
        file = open(fileName, 'r')
        lines = file.readlines()
        rectangleList = []
        # Retrieve values from text file and append to rectangleList
        for i in range(len(lines)):
            lineString = lines[i]
            x, y, width, height = lineString.split(",")
            tileX, tileY = game.tileCoordinatesToPixels(int(x), int(y))
            width, height = game.tileCoordinatesToPixels(int(width), int(height))
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
    def __init__(self, tileSize=32):
        self.tileSize = tileSize # Width and height of each tile in pixels. Default tile size is 32.
        self.surface = pygame.display.set_mode((tileSize * 30, tileSize * 20))
        self.npcList = []
        
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

    def initArea(self, file):
        mapName, mapLocation, playerLocation = self.loadSave("saves\\" + file + ".txt")
        self.tilemap = Map(mapName, mapLocation)
        self.player = Player(playerLocation, 'down', 'player')
        npc1 = NPC((10, 11), 'up', 'player', 'wander', 2)
        npc2 = NPC((9, 15), 'up', 'player', 'wander', 1)
        npc3 = NPC((24, 9), 'up', 'player', 'wander', 3)
        self.npcList.append(npc1)
        self.npcList.append(npc2)
        self.npcList.append(npc3)
        self.cursor = Cursor()

    def loadSave(self, fileName):
        file = open(fileName, 'r')
        lines = file.readlines()
        fileNum = int(lines[0])
        mapName = lines[1].strip()
        mapLocation = [int(lines[2]), int(lines[3])]
        playerLocation = [int(lines[4]), int(lines[5])]
        file.close()

        return mapName, mapLocation, playerLocation
    
    def closeGame(self):
        pygame.quit()
        sys.exit()
        
    def main(self):
        self.initArea("save_data")
        
        fpsClock = pygame.time.Clock()
        mouse1Init = False
        mouse3Init = False

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.closeGame()
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
                self.player.followPath()
                self.player.drawPath()
            else:
                self.player.setSprite()
            
            self.player.drawRect((0, 255, 0))
            
            for i in self.npcList[:]:
                i.doBehaviour(self.tilemap)
                i.drawRect((0, 255, 255))
                i.displaySprite()

            self.player.displaySprite()
            
            for i in self.npcList[:]:
                i.drawWanderRange()

            
            pygame.draw.rect(game.surface, (0,0,0), self.cursor.rect, 2)
            self.cursor.update()
            pygame.display.set_caption('x: ' + str(self.cursor.rect.x / game.tileSize) + ' y: ' + str(self.cursor.rect.y / game.tileSize))
            pygame.display.update()
            fpsClock.tick(60)


if __name__ == '__main__':
    pygame.init()
    game = Game(36)
    game.main()
