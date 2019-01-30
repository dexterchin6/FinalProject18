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
#aligns window to the top of the screen
os.environ['SDL_VIDEO_WINDOW_POS'] = str(0) + "," + str(0)
displayWidth = 800
displayHeight = 600
windowRatio = 1366/displayWidth
gameDisplay = pygame.display.set_mode((displayWidth,displayHeight))
pygame.display.set_caption('Test Game')
clock = pygame.time.Clock()

imageBattleSize = 75
battleImageSize = int(500/windowRatio)
#color and font asset bank
font = pygame.font.SysFont('lucidasans',15)
black = (0,0,0)
blue = (32,178,170)
blueDark = (0,0,200)
brown = (139,69,19)
red = (210,0,0)
white = (255,255,255)
#-----------------------------------------------------------------------------------------------------------------#
#[Global Variables]#
#the following are definitions of global variables for later use in the battle function
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
distantCounters = []
effectives = {
  "Melee":"Dragon",
  "Dragon":["Magic","Staff"],
  "Magic":"Melee",
  "Ranged":[],
  "Staff":[],
  "Armored":[],
  "Infantry":[],
  "Flying":[],
  "Calvary":[],
  "Axe":[],
  "Sword":[],
  "Lance":[],
  "Dragonstone":[],
  "Tome":[],
  "Bow":[],
  "Dagger":[],
  "Personal Ability":[]
}
counters = {
  "Melee":["Melee","Dragon"],
  "Dragon":["Dragon","Melee","Staff"],
  "Magic":["Magic","Ranged","Staff"],
  "Staff":["Staff","Magic","Ranged"],
  "Ranged":["Ranged","Magic","Staff"]
}
#-----------------------------------------------------------------------------------------------------------------#
#[Global Functions]#
def outputMessage(text,color,textWidth,textHeight,i):
    """outputs text onto the window"""
    def text_objects(text,color):
        """sequence of events to render the text surface to be put on the window"""
        textSurface = font.render(text,True,color)
        return textSurface,textSurface.get_rect()
    textSurface,textRect = text_objects(text,color)
    if i == 0:
        textRect.topleft = (textWidth,textHeight)
    if i == 1:
        textRect.midtop = (textWidth,textHeight)
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
            outputMessage(currentObject.nameFull,black,int(infoSheet.rect.x + ((infoSheet.image.get_size()[0])/2)*0.15),int(displayHeight*0.18),0)
            outputMessage(currentObject.tier,black,int(infoSheet.rect.x + ((infoSheet.image.get_size()[0])/2)*0.15),int(displayHeight*0.21),0)
            outputMessage(currentObject.team,black,int(infoSheet.rect.x + ((infoSheet.image.get_size()[0])/2)*0.15),int(displayHeight*0.24),0)
            outputMessage(f"Class: {currentObject.classType}",black,int(infoSheet.rect.x + ((infoSheet.image.get_size()[0])/2)*0.15),int(displayHeight*0.30),0)
            outputMessage(f"Weapon: {currentObject.weaponType}",black,int(infoSheet.rect.x + ((infoSheet.image.get_size()[0])/2)*0.15),int(displayHeight*0.33),0)
            outputMessage(f"{currentObject.moveType} Unit",black,int(infoSheet.rect.x + ((infoSheet.image.get_size()[0])/2)*0.15),int(displayHeight*0.36),0)
            outputMessage(f"HLT: {statsTemporary[currentObject][0]}",black,int(infoSheet.rect.x + ((infoSheet.image.get_size()[0])/2)*0.15),int(displayHeight*0.42),0)
            outputMessage(f"ATK: {statsTemporary[currentObject][1]}",black,int(infoSheet.rect.x + ((infoSheet.image.get_size()[0])/2)*0.15),int(displayHeight*0.45),0)
            outputMessage(f"SPD: {statsTemporary[currentObject][2]}",black,int(infoSheet.rect.x + ((infoSheet.image.get_size()[0])/2)*0.15),int(displayHeight*0.48),0)
            outputMessage(f"DEF: {statsTemporary[currentObject][3]}",black,int(infoSheet.rect.x + ((infoSheet.image.get_size()[0])/2)*0.15),int(displayHeight*0.51),0)
            outputMessage(f"RES: {statsTemporary[currentObject][4]}",black,int(infoSheet.rect.x + ((infoSheet.image.get_size()[0])/2)*0.15),int(displayHeight*0.54),0)
            outputMessage(f"CRT: {statsTemporary[currentObject][5]}%",black,int(infoSheet.rect.x + ((infoSheet.image.get_size()[0])/2)*0.15),int(displayHeight*0.57),0)
            outputMessage(f"{currentObject.nameWeapon}:",black,int(infoSheet.rect.x + ((infoSheet.image.get_size()[0])/2)*0.15),int(displayHeight*0.63),0)
            outputMessage(currentObject.biographyWeapon,black,int(infoSheet.rect.x + ((infoSheet.image.get_size()[0])/2)*0.15),int(displayHeight*0.66),0)
            if currentObject in teamPlayer:
                if movesLeftNo == True:
                    outputMessage("This character cannot move anymore.",black,int(infoSheet.rect.x + ((infoSheet.image.get_size()[0])/2)*0.15),int(displayHeight*0.72),0)
                    outputMessage("Press 'C' to complete action.",black,int(infoSheet.rect.x + ((infoSheet.image.get_size()[0])/2)*0.15),int(displayHeight*0.75),0)
                else:
                    outputMessage(f"{movesLeft} move(s) left.",black,int(infoSheet.rect.x + ((infoSheet.image.get_size()[0])/2)*0.15),int(displayHeight*0.72),0)
                if attackReady == True:
                    outputMessage("Press 'F' to attack",black,int(infoSheet.rect.x + ((infoSheet.image.get_size()[0])/2)*0.15),int(displayHeight*0.81),0)
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
    def skirmish(attacker,defender,ph,pa,ps,pd,pr,pc,eh,ea,es,ed,er,ec):
        """sequence of events during a skirmish"""
        #code for the introduction animation sequence#
        imageBox,imageBoxRect = resizeImage(pygame.image.load("Images/BattleBox.png"),int(displayWidth*0.8))
        imageAtt,imageAttRect = resizeImage(attacker.imageSkirmish,battleImageSize)
        imageDef,imageDefRect = resizeImage(defender.imageSkirmish,battleImageSize) 
        imageDef = pygame.transform.flip(imageDef,True,False)
        imageBox_y = 0 - int(imageBox.get_size()[1]/2)
        imageAtt_x = 0 - imageAtt.get_size()[0]
        imageDef_x = displayWidth + imageDef.get_size()[0]
        while imageAtt_x <= 0 or imageBox_y <= displayHeight/2 or imageDef_x >= displayWidth:
            imageSpeed = int(displayWidth/200)
            gameDisplay.fill(white)
            imageBoxRect.center = (displayWidth/2,imageBox_y)
            gameDisplay.blit(imageBox,imageBoxRect)
            imageAttRect.midleft = (imageAtt_x,displayHeight/2)
            gameDisplay.blit(imageAtt,imageAttRect) 
            imageDefRect.midright = (imageDef_x,displayHeight/2)
            gameDisplay.blit(imageDef,imageDefRect)
            pygame.display.flip()
            if imageAtt_x == 0 and imageDef_x == displayWidth and imageBox_y == displayHeight/2:
                break
            elif imageAtt_x == 0 and imageDef_x == displayWidth and imageBox_y is not displayHeight/2:
                imageAtt_x += 0
                imageDef_x -= 0 
                test_y = int(abs(displayHeight/2 - imageBox_y))
                if test_y <= imageSpeed:
                    imageBox_y = displayHeight/2
                else:
                    imageBox_y += imageSpeed
            elif imageAtt_x is not 0 and imageDef_x is not displayWidth and imageBox_y == displayHeight/2:
                test_x = abs(0 - imageAtt_x) 
                imageBox_y += 0
                if test_x <= imageSpeed: 
                    imageAtt_x = 0
                    imageDef_x = displayWidth
                else:
                    imageAtt_x += imageSpeed
                    imageDef_x -= imageSpeed
            else:
                test_x = abs(0 - imageAtt_x) 
                if test_x <= imageSpeed: 
                    imageAtt_x = 0
                    imageDef_x = displayWidth
                else:
                    imageAtt_x += imageSpeed
                    imageDef_x -= imageSpeed
                test_y = displayHeight/2 - imageBox_y
                if test_y <= imageSpeed:
                    imageBox_y = displayHeight/2
                else:
                    imageBox_y += imageSpeed
        #code for the skirmish mechanics#
        deathPlayer = ""
        deathEnemy = ""
        def backgroundReset():
            """replaces the background to a blank slate"""
            gameDisplay.fill(white)
            imageBoxRect.center = (displayWidth/2,displayHeight/2)
            gameDisplay.blit(imageBox,imageBoxRect)
            imageAttRect.midleft = (0,displayHeight/2)
            gameDisplay.blit(imageAtt,imageAttRect) 
            imageDefRect.midright = (displayWidth,displayHeight/2)
            gameDisplay.blit(imageDef,imageDefRect)
            pygame.display.flip()
            return
        def initial(pa,pc,eh,ea,es,ed,er,ec,i):
            """sequence of events during the inital attack"""
            def efficiency():
                """determines if the attacker has an advantage"""
                c = w = 0
                m = 1
                if attacker.classType in effectives[defender.classType]:
                    m = 1.4
                    c = 1
                else:
                    if attacker.nameWeapon in effectives[defender.classType] or attacker.nameWeapon in effectives[defender.moveType] or attacker.nameWeapon in effectives[defender.weaponType]:
                        m = 1.4
                        w = 1
                    elif attacker.weaponType == 'Bow' and defender.moveType == 'Flying':
                        m = 1.4
                        w = 1
                if c == 1:
                    outputMessage(f"{attacker.nameBattle} has an advantage over {defender.nameBattle}.",black,displayWidth/2,displayHeight*0.35,1)
                elif w == 1:
                    outputMessage(f"{attacker.nameBattle}`s weapon grants an advantage over {defender.nameBattle}.",black,displayWidth/2,displayHeight*0.35,1)
                pygame.display.flip()
                pygame.time.delay(2000)      
                return m
            def criticalChance(Critical,mEfficiency):
                """determines if the attack is a critical attack"""
                mCritical = 1
                numberCritical = random.randint(1,100)
                if numberCritical >= 1 and numberCritical <= Critical:
                    mCritical = 1.5
                    if mEfficiency == 1.4:
                        h = 0.4
                    else:
                        h = 0.35
                    outputMessage(f"{attacker.nameBattle} has landed a critical hit! {attacker.speechCritical}",black,displayWidth/2,displayHeight*h,1)
                    imageAtt,imageAttRect = resizeImage(attacker.imageBattle,battleImageSize)
                    imageAtt_x = 0 - int(imageAtt.get_size()[0]/2)
                    while imageAtt_x != int(displayWidth/3):
                        gameDisplay.fill(black)
                        imageAttRect.center = (imageAtt_x,displayHeight/2)
                        gameDisplay.blit(imageAtt,imageAttRect) 
                        imageAtt_x += imageSpeed
                        test_x = int(displayWidth/3) - imageAtt_x
                        if test_x <= imageSpeed:
                            imageAtt_x = int(displayWidth/3)
                            gameDisplay.fill(black)
                            imageAttRect.center = (imageAtt_x,displayHeight/2)
                            gameDisplay.blit(imageAtt,imageAttRect)
                        pygame.display.flip()
                        pygame.time.delay(2000)      
                    outputMessage(attacker.speechCritical,white,int(displayWidth * 2/3),displayHeight/3,1)
                    pygame.display.flip()
                    pygame.time.delay(2000)
                    outputMessage(attacker.nameCritical,white,int(displayWidth * 2/3),displayHeight/2,1)
                    pygame.display.flip()
                    pygame.time.delay(2000)      
                return mCritical
            def damageCalculate(damage,health,mCritical):
                """calculates defender health after attacker attacks"""
                ifc = 0
                deathEnemy = ""
                if mCritical == 1.5:
                    h = 0.45
                else:
                    h = 0.4
                if damage > 0:
                    health = int(health - damage)
                    outputMessage(f"{attacker.nameBattle} did {damage} damage!",black,displayWidth/2,displayHeight*h,1)
                else:
                    outputMessage(f"{attacker.nameBattle} did no damage!",black,displayWidth/2,displayHeight*h,1)
                if health > 0:
                    outputMessage(f"{defender.nameBattle} has {health} health left.",black,displayWidth/2,displayHeight*(h + 0.05),1)
                else:
                    ifc = 1
                    outputMessage(f"{defender.nameBattle} has no more health left.",black,displayWidth/2,displayHeight*(h + 0.05),1)
                    deathEnemy = defender
                return health,ifc,deathEnemy    
            if i == 0:
                outputMessage(f"{attacker.nameBattle} is attacking {defender.nameBattle} with {attacker.nameWeapon}!",black,displayWidth/2,displayHeight*0.3,1)
            elif i == 1:
                outputMessage(f"{attacker.nameBattle} is performing a follow-up attack! {attacker.speechAttack}",black,displayWidth/2,displayHeight*0.3,1)     
            mEfficiency = efficiency()
            mCritical = criticalChance(pc,mEfficiency)
            if attacker.classType in ["Infantry","Ranged"]:
                block = pd
            elif attacker.classType in ["Magic","Dragon","Staff"]:
                block = pr
            dam = ea*mEfficiency*mCritical
            dam -= block
            dam = int(dam)
            eh,ifc,deathEnemy = damageCalculate(dam,eh,mCritical)
            pygame.display.flip()
            pygame.time.delay(2000)
            return pa,pc,eh,ea,es,ed,er,ec,ifc,deathEnemy
        def ifcounter(ifc):
            """determines if there is a counterattack"""
            cc = 0
            if ifc == 1 and defender.classType in counters[attacker.classType]:
                cc = 1
            elif ifc == 1 and defender.nameWeapon in distantCounters:
                cc = 1
            return cc
        def counter(ph,pa,ps,pd,pr,pc,ea,ec,i):
            """sequence of events during the counterattack"""
            def efficiencyRev():
                """determines if the defender has an advantage"""
                c = w = 0
                m = 1
                if defender.classType in effectives[attacker.classType]:
                    m = 1.4
                    c = 1
                else:
                    if defender.nameWeapon in effectives[attacker.classType] or defender.nameWeapon in effectives[attacker.moveType] or defender.nameWeapon in effectives[attacker.weaponType]:
                        m = 1.4
                        w = 1
                    elif defender.weaponType == 'Bow' and attacker.moveType == 'Flying':
                        m = 1.4
                        w = 1
                if c == 1:
                    outputMessage(f"{defender.nameBattle} has an advantage over {attacker.nameBattle}.",black,displayWidth/2,displayHeight*0.35,1)
                elif w == 1:
                    outputMessage(f"{defender.nameBattle}`s weapon grants an advantage over {attacker.nameBattle}.",black,displayWidth/2,displayHeight*0.35,1)
                pygame.display.flip()
                return m
            def criticalChanceRev(Critical,mEfficiency):
                """determines if the counterattack is a critical hit"""
                mCritical = 1
                numberCritical = random.randint(1,100)
                if numberCritical >= 1 and numberCritical <= Critical:
                    mCritical = 1.5
                    if mEfficiency == 1.4:
                        h = 0.4
                    else:
                        h = 0.35
                    outputMessage(f"{defender.nameBattle} has landed a critical hit! {defender.speechCritical}",black,displayWidth/2,displayHeight*h,1)
                    imageDef,imageDefRect = resizeImage(defender.imageBattle,battleImageSize)
                    imageDef_x = 0 - int(imageDef.get_size()[0]/2)
                    while imageDef_x != int(displayWidth/3):
                        gameDisplay.fill(black)
                        imageDefRect.center = (imageDef_x,displayHeight/2)
                        gameDisplay.blit(imageDef,imageDefRect) 
                        imageDef_x += imageSpeed
                        test_x = int(displayWidth/3) - imageDef_x
                        if test_x <= imageSpeed:
                            imageDef_x = int(displayWidth/3)
                            gameDisplay.fill(black)
                            imageAttRect.center = (imageDef_x,displayHeight/2)
                            gameDisplay.blit(imageDef,imageDefRect)
                        pygame.display.flip()
                    outputMessage(defender.speechCritical,white,int(displayWidth * 2/3),displayHeight/3,1)
                    pygame.display.flip()
                    pygame.time.delay(2000)
                    outputMessage(defender.nameCritical,white,int(displayWidth * 2/3),displayHeight/2,1)
                    pygame.display.flip()
                return mCritical
            def damageCalculateRev(damage,health,mCritical):
                """calculates attacker health after defender attacks"""
                deathPlayer = ""
                if mCritical == 1.5:
                    h = 0.45
                else:
                    h = 0.4
                if damage > 0:
                    health = int(health - damage)
                    outputMessage(f"{defender.nameBattle} did {damage} damage!",black,displayWidth/2,displayHeight*h,1)
                else:
                    outputMessage(f"{defender.nameBattle} did no damage!",black,displayWidth/2,displayHeight*h,1)
                if health > 0:
                    outputMessage(f"{attacker.nameBattle} has {health} health left.",black,displayWidth/2,displayHeight*(h + 0.05),1)
                else:
                    ifc = 1
                    outputMessage(f"{attacker.nameBattle} has no more health left. {attacker.speechDeath}",black,displayWidth/2,displayHeight*(h + 0.05),1)
                    deathPlayer = attacker
                return health,deathplayer   
            if i == 0:       
                outputMessage(f"{defender.nameBattle} is striking back! {defender.speechAttack}",black,displayWidth/2,displayHeight*0.3,1)
            elif i == 1:
                outputMessage(f"{defender.nameBattle} is performing a second counterattack!",black,displayWidth/2,displayHeight*0.3,1)
            mEfficiency = efficiencyRev()
            mCritical = criticalChanceRev(ec,mEfficiency)
            if defender.classType in ['Infantry','Ranged']:
                block = pd
            elif defender.classType in ['Magic','Dragon','Staff']:
                block = pr
            dam = ea*mEfficiency*mCritical
            dam -= block
            ph,deathplayer = damageCalculateRev(dam,ph,mCritical)
            pygame.display.flip()
            return ph,pa,ps,pd,pr,pc,ea,ec,deathPlayer
        pa,pc,eh,ea,es,ed,er,ec,ifc,deathEnemy = initial(pa,pc,eh,ea,es,ed,er,ec,0)
        cc = ifcounter(ifc)
        if cc == 1:
            blackgroundReset()
            ph,pa,ps,pd,pr,pc,ea,ec,deathPlayer = counter(ph,pa,ps,pd,pr,pc,ea,ec,0)
        ues = es + 10
        if ps >= ues:
            backgroundReset()
            pa,pc,eh,ea,es,ed,er,ec,ifc,deathEnemy = initial(pa,pc,eh,ea,es,ed,er,ec,1)
        ups = ps + 10
        if es >= ups:
            backgroundReset()
            ph,pa,ps,pd,pr,pc,ea,ec,deathPlayer = counter(ph,pa,ps,pd,pr,pc,ea,ec,1)
        return ph,pa,ps,pd,pr,pc,eh,ea,es,ed,er,ec,deathPlayer,deathEnemy
    statsTemporary = {}
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
    k = 0
    for character in teamPlayer:
        chosenX = k
        chosenY = boardHeight - 1
        board[chosenX][chosenY] = character
        boardPositionCurrent.update({character:[chosenX,chosenY]})
        character.rect.x = (chosenX*tileWidth) + marginX
        character.rect.y = (chosenY*tileHeight) + marginY
        literalPositionCurrent.update({character:[character.rect.x - boardBoundary.rect.x,character.rect.y - boardBoundary.rect.y]})
        statsTemporary.update({character:[character.health,character.attack,character.speed,character.defense,character.resistance,character.critical]})
        k += 1
    k = boardWidth - 1
    for character in teamEnemy:
        chosenX = k
        chosenY = 0
        board[chosenX][chosenY] = character
        boardPositionCurrent.update({character:[chosenX,chosenY]})
        character.rect.x = (chosenX*tileWidth) + marginX
        character.rect.y = (chosenY*tileHeight) + marginY
        literalPositionCurrent.update({character:[character.rect.x - boardBoundary.rect.x,character.rect.y - boardBoundary.rect.y]})
        statsTemporary.update({character:[character.health,character.attack,character.speed,character.defense,character.resistance,character.critical]})
        k -= 1
    operateMaster = True
    while teamPlayer != 0 and teamEnemy != 0 and operateMaster == True:
        tPlayer = []
        for item in teamPlayer:
            tPlayer.append(item)
        operate = True
        while operate and len(tPlayer) > 0:
            clock.tick(60)
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
                            if movesLeft >= 1 and samePosition == False:
                                movesLeftNo = False
                                turnEnd = False
                                combatLone = False
                                print(samePosition)
                                if movesLeft == 1:
                                    movesLeftNo = True
                                    turnEnd = True
                                    combatLone = True
                                    tileOneExists = tileTwoExists = tileThreeExists = tileFourExists = tileTargetOneExists = tileTargetTwoExists = tileTargetThreeExists = tileTargetFourExists = False
                                    arrowControl,boardVisual,tileOneExists,tileTwoExists,tileThreeExists,tileFourExists,tileTargetOneExists,tileTargetTwoExists,tileTargetThreeExists,tileTargetFourExists,currentEnemyUp,currentEnemyDown,currentEnemyLeft,currentEnemyRight = moveCharacter(boardPositionTemporary[currentObject][0],boardPositionTemporary[currentObject][1],tileOneExists,tileTwoExists,tileThreeExists,tileFourExists,1)
                                    imageAssets.update(4)
                                    boardPrint()                    
                                else:
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
                        playerHealth = statsTemporary[currentObject][0]
                        playerAttack = statsTemporary[currentObject][1]
                        playerSpeed = statsTemporary[currentObject][2]
                        playerDefense = statsTemporary[currentObject][3]
                        playerResistance = statsTemporary[currentObject][4]
                        playerCritical = statsTemporary[currentObject][5]
                        enemyHealth = statsTemporary[currentEnemy][0]
                        enemyAttack = statsTemporary[currentEnemy][1]
                        enemySpeed = statsTemporary[currentEnemy][2]
                        enemyDefense = statsTemporary[currentEnemy][3]
                        enemyResistance = statsTemporary[currentEnemy][4]
                        enemyCritical = statsTemporary[currentEnemy][5]
                        playerHealth,playerAttack,playerSpeed,playerDefense,playerResistance,playerCritical,enemyHealth,enemyAttack,enemySpeed,enemyDefense,enemyResistance,enemyCritical,deathPlayer,deathEnemy = skirmish(currentObject,currentEnemy,playerHealth,playerAttack,playerSpeed,playerDefense,playerResistance,playerCritical,enemyHealth,enemyAttack,enemySpeed,enemyDefense,enemyResistance,enemyCritical)
                        print('yo')
                        print(deathEnemy)
                        if deathPlayer in teamPlayer:
                            teamPlayer.remove(deathPlayer)
                            board[boardPositionCurrent[deathPlayer][0]][boardPositionCurrent[deathPlayer][1]] = "Empty"
                            del boardPositionCurrent[deathPlayer]
                            del literalPositionCurrent[deathPlayer]
                            if len(teamPlayer) == 0:
                                operateMaster = False
                        else:
                            statsTemporary.update({currentObject:[playerHealth,playerAttack,playerSpeed,playerDefense,playerResistance,playerCritical]})
                        if deathEnemy in teamEnemy:
                            teamEnemy.remove(deathEnemy)
                            board[boardPositionCurrent[deathEnemy][0]][boardPositionCurrent[deathEnemy][1]] = "Empty"
                            del boardPositionCurrent[deathEnemy]
                            del literalPositionCurrent[deathEnemy]
                            if len(teamEnemy) == 0:
                                operateMaster = False
                        else:
                            statsTemporary.update({currentEnemy:[enemyHealth,enemyAttack,enemySpeed,enemyDefense,enemyResistance,enemyCritical]})
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
                    elif event.key == pygame.K_t:
                        print(board)
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
        while operate:
            for item in teamEnemy:
                enemyBattle = False
                directionList = ["Down","Left","Right"]
                moveCount = item.moveCount
                while moveCount > 0:     
                    direction = random.choice(directionList)
                    samePosition = False
                    if direction == "Down":
                        try:
                            board[boardPositionCurrent[item][0]][boardPositionCurrent[item][1] + 1]
                        except:
                            pass
                        else: 
                            if board[boardPositionCurrent[item][0]][boardPositionCurrent[item][1] + 1] == "Empty":
                                board[boardPositionCurrent[item][0]][boardPositionCurrent[item][1]] = "Empty"
                                boardPositionCurrent.update({item:[boardPositionCurrent[item][0],boardPositionCurrent[item][1] + 1]})
                                board[boardPositionCurrent[item][0]][boardPositionCurrent[item][1]] = item
                                literalPositionCurrent.update({item:[literalPositionCurrent[item][0],literalPositionCurrent[item][1] + tileHeight]})
                    elif direction == "Left":
                        if boardPositionCurrent[item][0] - 1 < 0: 
                            samePosition = True
                            pass
                        else:
                            try:
                                board[boardPositionCurrent[item][0] - 1][boardPositionCurrent[item][1]]
                            except:
                                pass
                            else: 
                                if board[boardPositionCurrent[item][0] - 1][boardPositionCurrent[item][1]] == "Empty":
                                    board[boardPositionCurrent[item][0]][boardPositionCurrent[item][1]] = "Empty"
                                    boardPositionCurrent.update({item:[boardPositionCurrent[item][0] - 1,boardPositionCurrent[item][1]]})
                                    board[boardPositionCurrent[item][0]][boardPositionCurrent[item][1]] = item
                                    literalPositionCurrent.update({item:[literalPositionCurrent[item][0] - tileWidth,literalPositionCurrent[item][1]]})
                    elif direction == "Right":
                        try:
                            board[boardPositionCurrent[item][0] + 1][boardPositionCurrent[item][1]]
                        except:
                            pass
                        else: 
                            if board[boardPositionCurrent[item][0] + 1][boardPositionCurrent[item][1]] == "Empty":
                                board[boardPositionCurrent[item][0]][boardPositionCurrent[item][1]] = "Empty"
                                boardPositionCurrent.update({item:[boardPositionCurrent[item][0] + 1,boardPositionCurrent[item][1]]})
                                board[boardPositionCurrent[item][0]][boardPositionCurrent[item][1]] = item
                                literalPositionCurrent.update({item:[literalPositionCurrent[item][0] + tileWidth,literalPositionCurrent[item][1]]})
                    imageAssets.update(4)
                    boardPrint()
                    if samePosition == True:
                        pass
                    else:
                        moveCount -= 1
                    try:
                        board[boardPositionCurrent[item][0]][boardPositionCurrent[item][1] - 1]
                    except:
                        pass
                    else:
                        if board[boardPositionCurrent[item][0]][boardPositionCurrent[item][1] - 1] in teamPlayer:
                            currentEnemy = board[boardPositionCurrent[item][0]][boardPositionCurrent[item][1] - 1]
                            enemyBattle = True
                    try:
                        board[boardPositionCurrent[item][0]][boardPositionCurrent[item][1] + 1]
                    except:
                        pass
                    else:
                        if board[boardPositionCurrent[item][0]][boardPositionCurrent[item][1] + 1] in teamPlayer:
                            currentEnemy = board[boardPositionCurrent[item][0]][boardPositionCurrent[item][1] + 1]
                            enemyBattle = True
                    try:
                        board[boardPositionCurrent[item][0] - 1][boardPositionCurrent[item][1]]
                    except:
                        pass
                    else:
                        if board[boardPositionCurrent[item][0] - 1][boardPositionCurrent[item][1]] in teamPlayer:
                            currentEnemy = board[boardPositionCurrent[item][0] - 1][boardPositionCurrent[item][1]]
                            enemyBattle = True
                    try:
                        board[boardPositionCurrent[item][0] - 1][boardPositionCurrent[item][1]]
                    except:
                        pass
                    else:
                        if board[boardPositionCurrent[item][0] - 1][boardPositionCurrent[item][1]] in teamPlayer:
                            currentEnemy = board[boardPositionCurrent[item][0] - 1][boardPositionCurrent[item][1]]
                            enemyBattle = True
                    if enemyBattle == True:
                        playerHealth = statsTemporary[item][0]
                        playerAttack = statsTemporary[item][1]
                        playerSpeed = statsTemporary[item][2]
                        playerDefense = statsTemporary[item][3]
                        playerResistance = statsTemporary[item][4]
                        playerCritical = statsTemporary[item][5]
                        enemyHealth = statsTemporary[currentEnemy][0]
                        enemyAttack = statsTemporary[currentEnemy][1]
                        enemySpeed = statsTemporary[currentEnemy][2]
                        enemyDefense = statsTemporary[currentEnemy][3]
                        enemyResistance = statsTemporary[currentEnemy][4]
                        enemyCritical = statsTemporary[currentEnemy][5]
                        playerHealth,playerAttack,playerSpeed,playerDefense,playerResistance,playerCritical,enemyHealth,enemyAttack,enemySpeed,enemyDefense,enemyResistance,enemyCritical,deathPlayer,deathEnemy = skirmish(item,currentEnemy,playerHealth,playerAttack,playerSpeed,playerDefense,playerResistance,playerCritical,enemyHealth,enemyAttack,enemySpeed,enemyDefense,enemyResistance,enemyCritical)
                        if deathEnemy in teamPlayer:
                            teamPlayer.remove(deathPlayer)
                            board[boardPositionCurrent[deathPlayer][0]][boardPositionCurrent[deathPlayer][1]] = "Empty"
                            del boardPositionCurrent[deathPlayer]
                            del literalPositionCurrent[deathPlayer]
                        else:
                            statsTemporary.update({currentObject:[playerHealth,playerAttack,playerSpeed,playerDefense,playerResistance,playerCritical]})
                        if deathPlayer in teamEnemy:
                            teamEnemy.remove(deathEnemy)
                            board[boardPositionCurrent[enemyPlayer][0]][boardPositionCurrent[enemyPlayer][1]] = "Empty"
                            del boardPositionCurrent[enemyPlayer]
                            del literalPositionCurrent[enemyPlayer]
                        else:
                            statsTemporary.update({currentEnemy:[enemyHealth,enemyAttack,enemySpeed,enemyDefense,enemyResistance,enemyCritical]})
                        break
            operate = False
            break
    gameDisplay.fill(white)
    outputMessage("You win",black,displayWidth/2,displayHeight/2,1)
    pygame.display.flip()
    pygame.time.delay(5000)
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
    def __init__(self,image,imageSkirmish,nameBattle,nameFull,tier,rank,team,biography,classType,moveType,moveCount,health,attack,speed,defense,resistance,critical,weaponType,nameWeapon,biographyWeapon,speechAttack,speechCritical):
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
        self.speechAttack = speechAttack
        self.speechCritical = speechCritical
OrigRobin = Character(pygame.image.load("Images/RobinChibi.png").convert_alpha(),pygame.image.load("Images/RobinSkirmish.png").convert_alpha(),"Robin","Robin","Tier I","Resistance Counter","VIFB-U0168 Oblivion","Based on FEH's 'High Deliverer' Robin","Magic","Infantry",2,12,15,8,7,12,2,"Tome","Blarraven","A standard tome.","Time to tip the scales!","Here's how it's done!")
OrigNinian = Character(pygame.image.load("Images/NinianChibi.png").convert_alpha(),pygame.image.load("Images/NinianSkirmish.png").convert_alpha(),"Ninian","Ninian","Tier I","Dancer","VIFB-U0027 Aurora","Based on FEH's 'Oracle of Destiny' Ninian","Dragon","Infantry",2,15,13,7,12,11,4,"Dragonstone","Water Breath","A reflective stone from the ocean.","May this make a difference!","Behold my power!")
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



