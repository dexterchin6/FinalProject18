#-----------------------------------------------------------------------------------------------------------------#
#[Import Bay]#
import pygame
from pygame.locals import *
import time
import os
import random
#-----------------------------------------------------------------------------------------------------------------#
#[Setup Global Variables]#
pygame.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = str(0) + "," + str(0)
displayWidth = 800
displayHeight = 600
gameDisplay = pygame.display.set_mode((displayWidth,displayHeight))
pygame.display.set_caption('Midnight Rising')
clock = pygame.time.Clock()

imageBattleSize = 75

font = pygame.font.SysFont('lucidasans',15)
black = (0,0,0)
blue = (32,178,170)
blueDark = (0,0,200)
brown = (139,69,19)
red = (210,0,0)
white = (255,255,255)
#-----------------------------------------------------------------------------------------------------------------#
#[Global Variables]#
def boardOne(i):
    """battlefield layout for the first battle"""
    board = []
    c1 = []
    c2 = []
    c3 = []
    c4 = []
    c5 = []
    c6 = []
    boardWidth = 6
    boardHeight = 6
    for x in range(boardHeight):
        c1.append("Empty")
    board.append(c1)
    for x in range(boardHeight):
        c2.append("Empty")
    board.append(c2)
    for x in range(boardHeight):
        c3.append("Empty")
    board.append(c3)
    for x in range(boardHeight):
        c4.append("Empty")
    board.append(c4)
    for x in range(boardHeight):
        c5.append("Empty")
    board.append(c5)
    for x in range(boardHeight):
        c6.append("Empty")
    board.append(c6)
    board[1][0] = "Obstacle"
    if i == 0:
        return board,boardWidth,boardHeight
    if i == 1:
        return board
board,boardWidth,boardHeight = boardOne(0)
tileWidth = tileHeight = int(imageBattleSize*1.25)
marginX = 0 + (displayWidth - boardWidth*tileWidth)/2
marginY = 0 + (displayHeight - boardHeight*tileHeight)/2
#-----------------------------------------------------------------------------------------------------------------#
#[Global Functions]#
def outputMessage(text,color,textWidth,textHeight):
    """outputs text onto the window"""
    def text_objects(text,color):
        """sequence of events to render the text surface to be put on the window"""
        textSurface = font.render(text,True,color)
        return textSurface,textSurface.get_rect()
    textSurface,textRect = text_objects(text,color)
    textRect.topleft = (textWidth,textHeight)
    gameDisplay.blit(textSurface,textRect)
    return
def resizeImage(image,imageWidth):
    """resizes image to required width"""
    w,h = image.get_size()
    imageHeight = int((h * imageWidth)/w)
    scaledImage = pygame.transform.scale(image,(imageWidth,imageHeight))
    return scaledImage,scaledImage.get_rect()
#-----------------------------------------------------------------------------------------------------------------#
#[Game Core]#
def battle(board,boardWidth,boardHeight,teamPlayer):
    """sequence of events during a battle"""
    def boardPrint():
        """prints an updated version of the board"""
        def printInformation():
            """prints a field biography of the character selected"""
            infoAssets.draw(gameDisplay)
            outputMessage(currentObject.nameFull,black,int(infoSheet.rect.x + ((infoSheet.image.get_size()[0])/2)*0.15),int(displayHeight*0.18))
            outputMessage(currentObject.tier,black,int(infoSheet.rect.x + ((infoSheet.image.get_size()[0])/2)*0.15),int(displayHeight*0.21))
            outputMessage(currentObject.team,black,int(infoSheet.rect.x + ((infoSheet.image.get_size()[0])/2)*0.15),int(displayHeight*0.24))
            outputMessage(f"Class: {currentObject.classType}",black,int(infoSheet.rect.x + ((infoSheet.image.get_size()[0])/2)*0.15),int(displayHeight*0.30))
            outputMessage(f"Weapon: {currentObject.weaponType}",black,int(infoSheet.rect.x + ((infoSheet.image.get_size()[0])/2)*0.15),int(displayHeight*0.33))
            outputMessage(f"{currentObject.moveType} Unit",black,int(infoSheet.rect.x + ((infoSheet.image.get_size()[0])/2)*0.15),int(displayHeight*0.36))
            outputMessage(f"Health: {currentObject.health}",black,int(infoSheet.rect.x + ((infoSheet.image.get_size()[0])/2)*0.15),int(displayHeight*0.42))
            outputMessage(f"ATK: {currentObject.attack}",black,int(infoSheet.rect.x + ((infoSheet.image.get_size()[0])/2)*0.15),int(displayHeight*0.45))
            outputMessage(f"SPD: {currentObject.speed}",black,int(infoSheet.rect.x + ((infoSheet.image.get_size()[0])/2)*0.15),int(displayHeight*0.49))
            outputMessage(f"DEF: {currentObject.defense}",black,int(infoSheet.rect.x + ((infoSheet.image.get_size()[0])/2)*0.15),int(displayHeight*0.51))
            outputMessage(f"RES: {currentObject.resistance}",black,int(infoSheet.rect.x + ((infoSheet.image.get_size()[0])/2)*0.15),int(displayHeight*0.54))
            outputMessage(f"CRIT: {currentObject.critical}%",black,int(infoSheet.rect.x + ((infoSheet.image.get_size()[0])/2)*0.15),int(displayHeight*0.57))
            outputMessage(f"{currentObject.nameWeapon}:",black,int(infoSheet.rect.x + ((infoSheet.image.get_size()[0])/2)*0.15),int(displayHeight*0.63))
            outputMessage(currentObject.biographyWeapon,black,int(infoSheet.rect.x + ((infoSheet.image.get_size()[0])/2)*0.15),int(displayHeight*0.66))
            if currentObject in teamPlayer:
                if movesLeftNo == True:
                    outputMessage("This character cannot move anymore.",black,int(infoSheet.rect.x + ((infoSheet.image.get_size()[0])/2)*0.15),int(displayHeight*0.72))
                    outputMessage("Press 'C' to complete action.",black,int(infoSheet.rect.x + ((infoSheet.image.get_size()[0])/2)*0.15),int(displayHeight*0.75))
                else:
                    outputMessage(f"{movesLeft} move(s) left.",black,int(infoSheet.rect.x + ((infoSheet.image.get_size()[0])/2)*0.15),int(displayHeight*0.72))
                if attackReady == True:
                    outputMessage("Press 'F' to attack",black,int(infoSheet.rect.x + ((infoSheet.image.get_size()[0])/2)*0.15),int(displayHeight*0.81))
            return
        rects = imageAssets.draw(gameDisplay)
        markerAssets.draw(gameDisplay)    
        if tileOneExists == True or tileTwoExists == True or tileThreeExists == True or tileFourExists == True:
            tileAssetBase.rect.x = boardBoundary.rect.x + literalPositionCurrent[currentObject][0]
            tileAssetBase.rect.y = boardBoundary.rect.y + literalPositionCurrent[currentObject][1]
            tileBase.add(currentObject)
            tileBase.draw(gameDisplay)
        if tileOneExists == True:
            virtualAssetOne.draw(gameDisplay)
        if tileTwoExists == True:
            virtualAssetTwo.draw(gameDisplay)
        if tileThreeExists == True:
            virtualAssetThree.draw(gameDisplay)
        if tileFourExists == True:
            virtualAssetFour.draw(gameDisplay)
        if tileTargetOneExists == True:
            targetAssetOne.add(currentEnemyUp)
            targetAssetOne.draw(gameDisplay)
        if tileTargetTwoExists == True:
            targetAssetTwo.add(currentEnemyLeft)
            targetAssetTwo.draw(gameDisplay)
        if tileTargetThreeExists == True:
            targetAssetThree.add(currentEnemyDown)
            targetAssetThree.draw(gameDisplay)
        if tileTargetFourExists == True:
            targetAssetFour.add(currentEnemyRight)
            targetAssetFour.draw(gameDisplay)
        if printInfo == True:
            printInformation()    
        pygame.display.update(rects)     
        return    
    def boardCheck():
        """ensures assets do not move when player reaches the map limits"""
        if mapStarter.rect.y >= 0:
            mapStarter.rect.y = 0
            boxBoundary.rect.y = 0 + (mapStarter.image.get_size()[1] - boxBoundary.image.get_size()[1])/2
            boardBoundary.rect.y = 0 + (mapStarter.image.get_size()[1] - boardBoundary.image.get_size()[1])/2
        if mapStarter.rect.y <= displayHeight - mapStarter.image.get_size()[1]:
            mapStarter.rect.y = displayHeight - mapStarter.image.get_size()[1]
            boxBoundary.rect.y = displayHeight - ((mapStarter.image.get_size()[1] - boxBoundary.image.get_size()[1])/2) - boxBoundary.image.get_size()[1]
            boardBoundary.rect.y = displayHeight - ((mapStarter.image.get_size()[1] - boardBoundary.image.get_size()[1])/2) - boardBoundary.image.get_size()[1]
        if mapStarter.rect.x >= 0:
            mapStarter.rect.x = 0
            boxBoundary.rect.x = 0 + (mapStarter.image.get_size()[0] - boxBoundary.image.get_size()[0])/2
            boardBoundary.rect.x = 0 + (mapStarter.image.get_size()[0] - boardBoundary.image.get_size()[0])/2
        if mapStarter.rect.x <= displayWidth - mapStarter.image.get_size()[0]:
            mapStarter.rect.x = displayWidth - mapStarter.image.get_size()[0]
            boxBoundary.rect.x = displayWidth - ((mapStarter.image.get_size()[0] - boxBoundary.image.get_size()[0])/2) - boxBoundary.image.get_size()[0]
            boardBoundary.rect.x = displayWidth - ((mapStarter.image.get_size()[1] - boardBoundary.image.get_size()[1])/2) - boardBoundary.image.get_size()[0]
        for character in teamPlayer:
            if character == currentObject:
                character.rect.y = boardBoundary.rect.y + literalPositionTemporary[currentObject][1]
                character.rect.x = boardBoundary.rect.x + literalPositionTemporary[currentObject][0]
            else:
                character.rect.y = boardBoundary.rect.y + literalPositionCurrent[character][1]
                character.rect.x = boardBoundary.rect.x + literalPositionCurrent[character][0]
        for character in teamEnemy:
            character.rect.y = boardBoundary.rect.y + literalPositionCurrent[character][1]
            character.rect.x = boardBoundary.rect.x + literalPositionCurrent[character][0]
        if tileOneExists == True:
            tileVirtualOne.rect.x = currentObject.rect.x
            tileVirtualOne.rect.y = currentObject.rect.y - tileHeight
        if tileTwoExists == True:
            tileVirtualTwo.rect.x = currentObject.rect.x - tileWidth
            tileVirtualTwo.rect.y = currentObject.rect.y
        if tileThreeExists == True:
            tileVirtualThree.rect.x = currentObject.rect.x
            tileVirtualThree.rect.y = currentObject.rect.y + tileHeight
        if tileFourExists == True:
            tileVirtualFour.rect.x = currentObject.rect.x + tileWidth
            tileVirtualFour.rect.y = currentObject.rect.y
        if tileTargetOneExists == True:
            tileTargetOne.rect.x = currentEnemyUp.rect.x
            tileTargetOne.rect.y = currentEnemyUp.rect.y
        if tileTargetTwoExists == True:
            tileTargetTwo.rect.x = currentEnemyLeft.rect.x
            tileTargetTwo.rect.y = currentEnemyLeft.rect.y
        if tileTargetThreeExists == True:
            tileTargetThree.rect.x = currentEnemyDown.rect.x
            tileTargetThree.rect.y = currentEnemyDown.rect.y
        if tileTargetFourExists == True:
            tileTargetFour.rect.x = currentEnemyRight.rect.x
            tileTargetFour.rect.y = currentEnemyRight.rect.y
        return
    def moveCharacter(coordinateX,coordinateY,tileOneExists,tileTwoExists,tileThreeExists,tileFourExists,i):
        """sequence of events for moving a character"""
        currentEnemyUp = currentEnemyDown = currentEnemyLeft = currentEnemyRight = ""
        tileOneExists = tileTwoExists = tileThreeExists = tileFourExists = tileTargetOneExists = tileTargetTwoExists = tileTargetThreeExists = tileTargetFourExists = False
        if i == 0:
            arrowControl = True
        elif i == 1:
            arrowControl = False
        boardVisual = boardOne(1)
        try:
            board[boardPositionTemporary[currentObject][0]][boardPositionTemporary[currentObject][1] - 1]
        except:
            pass
        else:
            if boardPositionTemporary[currentObject][1] - 1 < 0:
                pass
            else:
                if board[boardPositionTemporary[currentObject][0]][boardPositionTemporary[currentObject][1] - 1] == "Empty":
                    boardVisual[boardPositionTemporary[currentObject][0]][boardPositionTemporary[currentObject][1] - 1] = "Potential"
                    tileVirtualOne.rect.x = currentObject.rect.x 
                    tileVirtualOne.rect.y = currentObject.rect.y - tileHeight
                    tileOneExists = True
                else:
                    tileOneExists = False
                if board[boardPositionTemporary[currentObject][0]][boardPositionTemporary[currentObject][1] - 1] in teamEnemy:
                    boardVisual[boardPositionTemporary[currentObject][0]][boardPositionTemporary[currentObject][1] - 1] = "Target"
                    tileTargetOne.rect.x = currentObject.rect.x 
                    tileTargetOne.rect.y = currentObject.rect.y - tileHeight
                    currentEnemyUp = board[boardPositionTemporary[currentObject][0]][boardPositionTemporary[currentObject][1] - 1]
                    tileTargetOneExists = True
                else:
                    tileTargetOneExists = False
        try:
            board[boardPositionTemporary[currentObject][0]][boardPositionTemporary[currentObject][1] + 1]
        except:
            pass
        else:
            if board[boardPositionTemporary[currentObject][0]][boardPositionTemporary[currentObject][1] + 1] == "Empty":
                boardVisual[boardPositionTemporary[currentObject][0]][boardPositionTemporary[currentObject][1] + 1] = "Potential"
                tileVirtualThree.rect.x = currentObject.rect.x 
                tileVirtualThree.rect.y = currentObject.rect.y + tileHeight
                tileThreeExists = True
            else:
                tileThreeExists = False
            if board[boardPositionTemporary[currentObject][0]][boardPositionTemporary[currentObject][1] + 1] in teamEnemy:
                boardVisual[boardPositionTemporary[currentObject][0]][boardPositionTemporary[currentObject][1] + 1] = "Target"
                tileTargetThree.rect.x = currentObject.rect.x 
                tileTargetThree.rect.y = currentObject.rect.y + tileHeight
                currentEnemyDown = board[boardPositionTemporary[currentObject][0]][boardPositionTemporary[currentObject][1] + 1]
                tileTargetThreeExists = True
            else:
                tileTargetThreeExists = False
        try:
            board[boardPositionTemporary[currentObject][0] - 1][boardPositionTemporary[currentObject][1]]
        except:
            pass
        else:
            if boardPositionTemporary[currentObject][0] - 1 < 0:
                pass
            else:
                if board[boardPositionTemporary[currentObject][0] - 1][boardPositionTemporary[currentObject][1]] == "Empty":
                    boardVisual[boardPositionTemporary[currentObject][0] - 1][boardPositionTemporary[currentObject][1]] = "Potential"
                    tileVirtualTwo.rect.x = currentObject.rect.x - tileWidth
                    tileVirtualTwo.rect.y = currentObject.rect.y
                    tileTwoExists = True
                else:
                    tileTwoExists = False
                if board[boardPositionTemporary[currentObject][0] - 1][boardPositionTemporary[currentObject][1]] in teamEnemy:
                    boardVisual[boardPositionTemporary[currentObject][0] - 1][boardPositionTemporary[currentObject][1]] = "Target"
                    tileTargetTwo.rect.x = currentObject.rect.x - tileWidth
                    tileTargetTwo.rect.y = currentObject.rect.y
                    currentEnemyLeft = board[boardPositionTemporary[currentObject][0] - 1][boardPositionTemporary[currentObject][1]]
                    tileTargetTwoExists = True
                else:
                    tileTargetTwoExists = False
        try:
            board[boardPositionTemporary[currentObject][0] + 1][boardPositionTemporary[currentObject][1]]
        except:
            pass
        else:
            if board[boardPositionTemporary[currentObject][0] + 1][boardPositionTemporary[currentObject][1]] == "Empty":
                boardVisual[boardPositionTemporary[currentObject][0] + 1][boardPositionTemporary[currentObject][1]] = "Potential"
                tileVirtualFour.rect.x = currentObject.rect.x + tileHeight
                tileVirtualFour.rect.y = currentObject.rect.y
                tileFourExists = True
            else:
                tileFourExists = False
            if board[boardPositionTemporary[currentObject][0] + 1][boardPositionTemporary[currentObject][1]] in teamEnemy:
                boardVisual[boardPositionTemporary[currentObject][0] + 1][boardPositionTemporary[currentObject][1]] = "Target"
                tileTargetTwo.rect.x = currentObject.rect.x + tileWidth
                tileTargetTwo.rect.y = currentObject.rect.y
                currentEnemyRight = board[boardPositionTemporary[currentObject][0] + 1][boardPositionTemporary[currentObject][1]]
                tileTargetFourExists = True
            else:
                tileTargetFourExists = False
        return arrowControl,boardVisual,tileOneExists,tileTwoExists,tileThreeExists,tileFourExists,tileTargetOneExists,tileTargetTwoExists,tileTargetThreeExists,tileTargetFourExists,currentEnemyUp,currentEnemyDown,currentEnemyLeft,currentEnemyRight
    literalPositionCurrent = {}
    boardPositionCurrent = {}
    arrowControl = False
    printInfo = False
    samePosition = False
    movesLeftNo = False
    turnEnd = False
    combatLone = False
    attackReady = False
    movesLeft = 0
    currentObject = ""
    tileOneExists = tileTwoExists = tileThreeExists = tileFourExists = tileTargetOneExists = tileTargetTwoExists = tileTargetThreeExists = tileTargetFourExists = False
    moveUp = moveDown = moveLeft = moveRight = False
    for character in teamPlayer:
        while True:
            chosenX = 2
            chosenY = boardHeight - 1
            if board[chosenX][chosenY] == "Empty":
                break
        board[chosenX][chosenY] = character
        boardPositionCurrent.update({character:[chosenX,chosenY]})
        character.rect.x = (chosenX*tileWidth) + marginX
        character.rect.y = (chosenY*tileHeight) + marginY
        literalPositionCurrent.update({character:[character.rect.x - boardBoundary.rect.x,character.rect.y - boardBoundary.rect.y]})
    for character in teamEnemy:
        while True:
            chosenX = 1
            chosenY = 4
            if board[chosenX][chosenY] == "Empty":
                break
        board[chosenX][chosenY] = character
        boardPositionCurrent.update({character:[chosenX,chosenY]})
        character.rect.x = (chosenX*tileWidth) + marginX
        character.rect.y = (chosenY*tileHeight) + marginY
        literalPositionCurrent.update({character:[character.rect.x - boardBoundary.rect.x,character.rect.y - boardBoundary.rect.y]})
    operateMaster = True
    while teamPlayer != 0 and teamEnemy != 0 and operateMaster == True:
        tPlayer = teamPlayer
        operate = True
        while operate and len(tPlayer) != 0:
            clock.tick(300)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    operate = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    if position[0] < boardBoundary.rect.x or position[0] > boardBoundary.rect.x + boardBoundary.image.get_size()[0] or position[1] < boardBoundary.rect.y or position[1] > boardBoundary.rect.y + boardBoundary.image.get_size()[1]:
                        pass
                    else:
                        columnSelected = int((position[0] - (0 + boardBoundary.rect.x))/tileWidth)
                        rowSelected = int((position[1] - (0 + boardBoundary.rect.y))/tileHeight)
                        if board[columnSelected][rowSelected] in teamPlayer and board[columnSelected][rowSelected] != currentObject:    
                            movesLeftNo = False
                            attackReady = False
                            tileOneExists = tileTwoExists = tileThreeExists = tileFourExists = False
                            currentObject = board[columnSelected][rowSelected]
                            movesLeft = currentObject.moveCount
                            literalPositionTemporary = {}
                            literalPositionTemporary.update({currentObject:[literalPositionCurrent[currentObject][0],literalPositionCurrent[currentObject][1]]})
                            boardPositionTemporary = {}
                            boardPositionTemporary.update({currentObject:[boardPositionCurrent[currentObject][0],boardPositionCurrent[currentObject][1]]})
                            mapStarter.autonomousMovement(int(displayWidth/2 - boardBoundary.rect.x),int(displayHeight/2 - boardBoundary.rect.y),int(position[0] - (0 + boardBoundary.rect.x) + displayWidth*0.17),position[1] - (0 + boardBoundary.rect.y),boardPrint,boardCheck)    
                            arrowControl,boardVisual,tileOneExists,tileTwoExists,tileThreeExists,tileFourExists,tileTargetOneExists,tileTargetTwoExists,tileTargetThreeExists,tileTargetFourExists,currentEnemyUp,currentEnemyDown,currentEnemyLeft,currentEnemyRight = moveCharacter(columnSelected,rowSelected,tileOneExists,tileTwoExists,tileThreeExists,tileFourExists,0)
                            printInfo = True
                        elif board[columnSelected][rowSelected] in teamEnemy:
                            tileOneExists = tileTwoExists = tileThreeExists = tileFourExists = tileTargetOneExists = tileTargetTwoExists = tileTargetThreeExists = tileTargetFourExists = False
                            currentObject = board[columnSelected][rowSelected]
                            mapStarter.autonomousMovement(int(displayWidth/2 - boardBoundary.rect.x),int(displayHeight/2 - boardBoundary.rect.y),int(position[0] - (0 + boardBoundary.rect.x) + displayWidth*0.17),position[1] - (0 + boardBoundary.rect.y),boardPrint,boardCheck)    
                            printInfo = True 
                        elif board[columnSelected][rowSelected] == "Empty" or board[columnSelected][rowSelected] == "Obstacle":
                            literalPositionTemporary = {}
                            boardPositionTemporary = {}
                            tileOneExists = tileTwoExists = tileThreeExists = tileFourExists = tileTargetOneExists = tileTargetTwoExists = tileTargetThreeExists = tileTargetFourExists = False
                            arrowControl = False
                            printInfo = False
                            samePosition = False
                            attackReady = False
                            movesLeft = 0
                            currentObject = ""
                            imageAssets.update(4)
                            boardPrint()
                elif event.type == pygame.KEYDOWN:
                    samePosition = False
                    if event.key == pygame.K_ESCAPE:
                        operate = False
                        operateMaster = False
                    elif event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        if arrowControl == True or combatLone == True:
                            if event.key == pygame.K_UP:
                                try:
                                    boardVisual[boardPositionTemporary[currentObject][0]][boardPositionTemporary[currentObject][1] - 1]
                                except:
                                    pass
                                else:
                                    if boardVisual[boardPositionTemporary[currentObject][0]][boardPositionTemporary[currentObject][1] - 1] == "Target":
                                        attackReady = True
                                        samePosition = True
                                        currentEnemy = currentEnemyUp
                                    else:
                                        attackReady = False
                                        if arrowControl == True:
                                            arrowControl = False
                                            if boardVisual[boardPositionTemporary[currentObject][0]][boardPositionTemporary[currentObject][1] - 1] == "Potential":
                                                boardPositionTemporary.update({currentObject:[boardPositionTemporary[currentObject][0],boardPositionTemporary[currentObject][1] - 1]})
                                                literalPositionTemporary.update({currentObject:[literalPositionTemporary[currentObject][0],literalPositionTemporary[currentObject][1] - tileHeight]})
                                            else:
                                                samePosition = True                                   
                            elif event.key == pygame.K_DOWN:
                                try: 
                                    boardVisual[boardPositionTemporary[currentObject][0]][boardPositionTemporary[currentObject][1] + 1]
                                except:
                                    pass
                                else:
                                    if boardVisual[boardPositionTemporary[currentObject][0]][boardPositionTemporary[currentObject][1] + 1] == "Target":
                                        attackReady = True
                                        samePosition = True
                                        currentEnemy = currentEnemyDown
                                    else:
                                        attackReady = False
                                        if arrowControl == True:
                                            arrowControl = False
                                            if boardVisual[boardPositionTemporary[currentObject][0]][boardPositionTemporary[currentObject][1] + 1] == "Potential":
                                                boardPositionTemporary.update({currentObject:[boardPositionTemporary[currentObject][0],boardPositionTemporary[currentObject][1] + 1]})
                                                literalPositionTemporary.update({currentObject:[literalPositionTemporary[currentObject][0],literalPositionTemporary[currentObject][1] + tileHeight]})
                                            else:
                                                samePosition = True                                  
                            elif event.key == pygame.K_LEFT:
                                try: 
                                    boardVisual[boardPositionTemporary[currentObject][0] - 1][boardPositionTemporary[currentObject][1]]
                                except:
                                    pass
                                else:
                                    if boardVisual[boardPositionTemporary[currentObject][0] - 1][boardPositionTemporary[currentObject][1]] == "Target":
                                        attackReady = True
                                        samePosition = True
                                        currentEnemy = currentEnemyLeft
                                    else:
                                        attackReady = False
                                        if arrowControl == True:
                                            arrowControl = False
                                            if boardVisual[boardPositionTemporary[currentObject][0] - 1][boardPositionTemporary[currentObject][1]] == "Potential":                               
                                                boardPositionTemporary.update({currentObject:[boardPositionTemporary[currentObject][0] - 1,boardPositionTemporary[currentObject][1]]})
                                                literalPositionTemporary.update({currentObject:[literalPositionTemporary[currentObject][0] - tileHeight,literalPositionTemporary[currentObject][1]]})
                                            else:
                                                samePosition = True                                 
                            elif event.key == pygame.K_RIGHT:
                                try: 
                                    boardVisual[boardPositionTemporary[currentObject][0] + 1][boardPositionTemporary[currentObject][1]]
                                except:
                                    pass
                                else:
                                    if boardVisual[boardPositionTemporary[currentObject][0] + 1][boardPositionTemporary[currentObject][1]] == "Target":
                                        attackReady = True
                                        samePosition = True
                                        currentEnemy = currentEnemyRight
                                    else:
                                        attackReady = False
                                        if arrowControl == True:
                                            arrowControl = False
                                            if boardVisual[boardPositionTemporary[currentObject][0] + 1][boardPositionTemporary[currentObject][1]] == "Potential":                               
                                                boardPositionTemporary.update({currentObject:[boardPositionTemporary[currentObject][0] + 1,boardPositionTemporary[currentObject][1]]})
                                                literalPositionTemporary.update({currentObject:[literalPositionTemporary[currentObject][0] + tileHeight,literalPositionTemporary[currentObject][1]]})
                                            else:
                                                samePosition = True                      
                            if movesLeft >= 0:
                                movesLeftNo = False
                                turnEnd = False
                                combatLone = False
                                if movesLeft == 0:
                                    movesLeftNo = True
                                    turnEnd = True
                                    combatLone = True
                                    tileOneExists = tileTwoExists = tileThreeExists = tileFourExists = tileTargetOneExists = tileTargetTwoExists = tileTargetThreeExists = tileTargetFourExists = False
                                    arrowControl,boardVisual,tileOneExists,tileTwoExists,tileThreeExists,tileFourExists,tileTargetOneExists,tileTargetTwoExists,tileTargetThreeExists,tileTargetFourExists,currentEnemyUp,currentEnemyDown,currentEnemyLeft,currentEnemyRight = moveCharacter(boardPositionTemporary[currentObject][0],boardPositionTemporary[currentObject][1],tileOneExists,tileTwoExists,tileThreeExists,tileFourExists,1)
                                    imageAssets.update(4)
                                    boardPrint()                    
                                else:
                                    if samePosition == False:
                                        movesLeft -= 1
                                    tileOneExists = tileTwoExists = tileThreeExists = tileFourExists = tileTargetOneExists = tileTargetTwoExists = tileTargetThreeExists = tileTargetFourExists = False
                                    imageAssets.update(4)
                                    boardPrint()
                                    arrowControl,boardVisual,tileOneExists,tileTwoExists,tileThreeExists,tileFourExists,tileTargetOneExists,tileTargetTwoExists,tileTargetThreeExists,tileTargetFourExists,currentEnemyUp,currentEnemyDown,currentEnemyLeft,currentEnemyRight = moveCharacter(boardPositionTemporary[currentObject][0],boardPositionTemporary[currentObject][1],tileOneExists,tileTwoExists,tileThreeExists,tileFourExists,0)
                    elif event.key == pygame.K_w:
                        moveUp = True
                    elif event.key == pygame.K_s:
                        moveDown = True
                    elif event.key == pygame.K_a:
                        moveLeft = True
                    elif event.key == pygame.K_d:
                        moveRight = True
                    elif event.key == pygame.K_c and turnEnd == True:
                        board[boardPositionCurrent[currentObject][0]][boardPositionCurrent[currentObject][1]] = "Empty"
                        boardPositionCurrent.update({currentObject:[boardPositionTemporary[currentObject][0],boardPositionTemporary[currentObject][1]]})
                        literalPositionCurrent.update({currentObject:[literalPositionTemporary[currentObject][0],literalPositionTemporary[currentObject][1]]})
                        board[boardPositionTemporary[currentObject][0]][boardPositionTemporary[currentObject][1]] = currentObject
                        tPlayer.remove(currentObject)
                        literalPositionTemporary = {}
                        boardPositionTemporary = {}
                        tileOneExists = tileTwoExists = tileThreeExists = tileFourExists = tileTargetOneExists = tileTargetTwoExists = tileTargetThreeExists = tileTargetFourExists = False
                        arrowControl = False
                        printInfo = False
                        samePosition = False
                        movesLeftNo = False
                        turnEnd = False
                        combatLone = False
                        movesLeft = 0
                        currentObject = ""
                        imageAssets.update(4)
                        boardPrint()   
                    elif event.key == pygame.K_f and attackReady == True:
                        print(currentEnemy)
                    elif event.key == pygame.K_t:
                        print(arrowControl)
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        moveUp = False
                    elif event.key == pygame.K_s:
                        moveDown = False
                    elif event.key == pygame.K_a:
                        moveLeft = False
                    elif event.key == pygame.K_d:
                        moveRight = False
            if moveUp == True:
                imageAssets.update(0)   
            elif moveDown == True:
                imageAssets.update(1)
            if moveLeft == True:
                imageAssets.update(2)
            elif moveRight == True:
                imageAssets.update(3) 
            boardCheck()
            imageAssets.update(4)
            boardPrint()
    return
#-----------------------------------------------------------------------------------------------------------------#
#[Asset Library]#
markerAssets = pygame.sprite.Group()
class Pinpoint(pygame.sprite.Sprite):
    def __init__(self,locationX,locationY):
        """initializer for target marker class"""
        super().__init__()
        self.image = pygame.Surface((50,50),pygame.SRCALPHA,32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (locationX,locationY)
        return
marker = Pinpoint(displayWidth/2,displayHeight/2)
markerThird = Pinpoint(int(displayWidth/3),displayHeight/2)
markerAssets.add(marker,markerThird)
infoAssets = pygame.sprite.GroupSingle()
class infoBoard(pygame.sprite.Sprite):
    def __init__(self):
        """initializer for the information board class"""
        super().__init__()
        self.image = pygame.image.load("Images/BattleBox.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(int(displayWidth*0.4),int(displayHeight*0.75)))
        self.rect = self.image.get_rect()
        self.rect.center = (displayWidth*0.75,displayHeight/2)
        return
infoSheet = infoBoard()
infoAssets.add(infoSheet)
class Base(pygame.sprite.DirtySprite):
    def __init__(self):
        """initializer for the base parent class"""
        pygame.sprite.DirtySprite.__init__(self)
    def update(self,i):
        """defines the map offset"""
        if i == 0:
            self.rect.y += 1
        elif i == 1:
            self.rect.y -= 1
        elif i == 2:
            self.rect.x += 1
        elif i == 3:
            self.rect.x -= 1
        elif i == 4:
            self.rect.x += 0
            self.rect.y += 0
        self.dirty = 1
        return
class VirtualTile(Base):
    def __init__(self,color,tileWidth,tileHeight):
        """initializer for the virtual tile sbuclass"""
        Base.__init__(self)
        self.image = pygame.Surface((tileWidth,tileHeight))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (self.rect.x,self.rect.y)
        return
virtualAssetOne = pygame.sprite.GroupSingle()
tileVirtualOne = VirtualTile(blue,tileWidth,tileHeight)
virtualAssetOne.add(tileVirtualOne)
virtualAssetTwo = pygame.sprite.GroupSingle()
tileVirtualTwo = VirtualTile(blue,tileWidth,tileHeight)
virtualAssetTwo.add(tileVirtualTwo)
virtualAssetThree = pygame.sprite.GroupSingle()
tileVirtualThree = VirtualTile(blue,tileWidth,tileHeight)
virtualAssetThree.add(tileVirtualThree)
virtualAssetFour = pygame.sprite.GroupSingle()
tileVirtualFour = VirtualTile(blue,tileWidth,tileHeight)
virtualAssetFour.add(tileVirtualFour)
imageAssets = pygame.sprite.LayeredDirty()        
tileBase = pygame.sprite.Group()
tileAssetBase = VirtualTile(blueDark,tileWidth,tileHeight)
tileBase.add(tileAssetBase)
targetAssetOne = pygame.sprite.Group()
tileTargetOne = VirtualTile(red,tileWidth,tileHeight)
targetAssetOne.add(tileTargetOne)
targetAssetTwo = pygame.sprite.Group()
tileTargetTwo = VirtualTile(red,tileWidth,tileHeight)
targetAssetTwo.add(tileTargetTwo)
targetAssetThree = pygame.sprite.Group()
tileTargetThree = VirtualTile(red,tileWidth,tileHeight)
targetAssetThree.add(tileTargetThree)
targetAssetFour = pygame.sprite.Group()
tileTargetFour = VirtualTile(red,tileWidth,tileHeight)
targetAssetFour.add(tileTargetFour)
class Sprite(Base):
    def __init__(self,image):
        """initialzier for the sprite parent class"""
        Base.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        return
class Map(Sprite):
    def __init__(self,image):
        """initializer for the map subclass"""
        Sprite.__init__(self,image)
        self.rect.center = (displayWidth/2,displayHeight/2)
        return
    def autonomousMovement(self,origX,origY,newX,newY,boardPrint,boardCheck):
        while newX != origX or newY != origY:  
            autoUp = autoDown = autoLeft = autoRight = False
            if newX > origX:
                origX += 1
                autoRight = True
            if origX > newX:
                origX -= 1
                autoLeft = True
            if newY > origY:
                origY += 1
                autoUp = True
            if origY > newY:
                origY -= 1
                autoDown = True       
            if autoUp == True:
                imageAssets.update(1)
            if autoDown == True:
                imageAssets.update(0)
            if autoLeft == True:
                imageAssets.update(2)
            if autoRight == True:
                imageAssets.update(3)
            boardCheck()
            boardPrint()
        return
mapStarter = Map(pygame.image.load("Images/Map2.png").convert())
imageAssets.add(mapStarter)
class mapBoundary(Sprite):
    def __init__(self,image,width,height):
        """initializer for the boundary subclass"""
        Sprite.__init__(self,image)
        imageWidth,imageHeight = self.image.get_size()
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(self.image,(self.width,self.height))
        self.rect = self.image.get_rect()
        self.rect.center = (displayWidth/2,displayHeight/2)
        return
boxBoundary = mapBoundary(pygame.image.load("Images/Boundary.png").convert(),int(boardWidth*tileWidth*1.005),int(boardHeight*tileHeight*1.005))
imageAssets.add(boxBoundary)
boardBoundary = mapBoundary(pygame.image.load("Images/board4Map2.png").convert(),int(boardWidth*tileWidth),int(boardHeight*tileHeight))
imageAssets.add(boardBoundary)
class CharacterImage(Sprite):
    def __init__(self,image):
        """initializer for the sprite sub-parent class"""
        Sprite.__init__(self,image)
        imageWidth,imageHeight = self.image.get_size()
        self.width = imageBattleSize
        self.height = int((imageHeight*self.width)/imageWidth)
        self.image = pygame.transform.scale(self.image,(self.width,self.height))
        return
class Character(CharacterImage):
    def __init__(self,image,imageSkirmish,nameBattle,nameFull,tier,rank,team,biography,classType,moveType,moveCount,health,attack,speed,defense,resistance,critical,weaponType,nameWeapon,biographyWeapon):
        """initializer for the character subclass"""
        CharacterImage.__init__(self,image)
        self.imageBattle = self.image
        self.imageBattleRect = self.imageBattle.get_rect()
        self.imageBattleRect.center = (self.imageBattleRect.x,self.imageBattleRect.y)
        self.imageSkirmish = imageSkirmish
        self.imageSkirmishRect = imageSkirmish.get_rect()
        self.imageSkirmishRect.center = (self.imageSkirmishRect.x,self.imageSkirmishRect.y)
        self.nameBattle = nameBattle
        self.nameFull = nameFull
        self.tier = tier
        self.rank = rank
        self.team = team
        self.biography = biography
        self.classType = classType
        self.moveType = moveType
        self.moveCount = moveCount
        self.health = health
        self.attack = attack
        self.speed = speed
        self.defense = defense
        self.resistance = resistance
        self.critical = critical
        self.weaponType = weaponType
        self.nameWeapon = nameWeapon
        self.biographyWeapon = biographyWeapon
OrigRobin = Character(pygame.image.load("Images/RobinChibi.png").convert_alpha(),pygame.image.load("Images/RobinSkirmish.png").convert_alpha(),"Robin","Robin","Tier I","Resistance Counter","VIFB-U0168 Oblivion","Based on FEH's 'High Deliverer' Robin","Mage","Infantry",2,16,10,8,9,12,2,"Tome","Blarraven","A standard tome.")
OrigNinian = Character(pygame.image.load("Images/NinianChibi.png").convert_alpha(),pygame.image.load("Images/NinianSkirmish.png").convert_alpha(),"Ninian","Ninian","Tier I","Dancer","VIFB-U0027 Aurora","Based on FEH's 'Oracle of Destiny' Ninian","Dragon","Infantry",2,14,8,7,15,10,4,"Dragonstone","Water Breath","A reflective stone from the ocean.")
#-----------------------------------------------------------------------------------------------------------------#
background = pygame.Surface((displayWidth,displayHeight))
background.fill(white)
teamPlayer = [OrigRobin]
teamEnemy = [OrigNinian]

for item in teamPlayer:
    imageAssets.add(item)
for item in teamEnemy:
    imageAssets.add(item)

run = True
while run:
    imageAssets.clear(gameDisplay,background)
    battle(board,boardWidth,boardHeight,teamPlayer)
    run = False
pygame.quit()
quit()



