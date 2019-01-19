#-----------------------------------------------------------------------------------------------------------------#
import pygame,random,os
#-----------------------------------------------------------------------------------------------------------------#
pygame.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = str(0) + "," + str(0)
displayWidth = 1000
displayHeight = 600
gameDisplay = pygame.display.set_mode((displayWidth,displayHeight))
pygame.display.set_caption('Midnight Rising')
clock = pygame.time.Clock()
font = pygame.font.SysFont("lucidasans",15)
battleImageSize = 50

black = (0,0,0)
white = (255,255,255)
brown = (139,69,19)
blue = (114,188,212)
blueDark = (0,0,205)
red = (255,0,0)

def boardy(i):
    board = []
    c1 = []
    c2 = []
    c3 = []
    c4 = []
    boardWidth = 3
    boardHeight = 3
    for x in range(4):
        c1.append("Empty")
    board.append(c1)
    for x in range(4):
        c2.append("Empty")
    board.append(c2)
    for x in range(4):
        c3.append("Empty")
    board.append(c3)
    for x in range(4):
        c4.append("Empty")
    board.append(c4)
    board[1][0] = "Obstacle"
    if i == 0:
        return board,boardWidth,boardHeight
    if i == 1:
        return board
#-----------------------------------------------------------------------------------------------------------------#
class Character:
    def __init__(self,imageSkirmish,imageBattle,nameSkirmish):
        """character class constructor"""
        self.imageSkirmish = imageSkirmish
        self.imageBattle = imageBattle
        self.nameSkirmish = nameSkirmish
        return

OrigLaslow = Character(pygame.image.load("Images/Laslow.png").convert_alpha(),pygame.image.load("Images/LaslowChibi.png").convert_alpha(),"[Laslow]")
OrigRobin = Character(pygame.image.load("Images/Robin.png").convert_alpha(),'',"[Robin]")
SpringLucina = Character(pygame.image.load("Images/SpringLucina.png").convert_alpha(),pygame.image.load("Images/SpringLucinaChibi.png").convert_alpha(),"[SP! Lucina]")
#-----------------------------------------------------------------------------------------------------------------#
def outputMessage(text,color,textWidth,textHeight):
    """outputs text onto the window"""
    def text_objects(text,color):
        """sequence of events to render the text surface to be put on the window"""
        textSurface = font.render(text,True,color)
        return textSurface,textSurface.get_rect()
    textSurface,textRect = text_objects(text,color)
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
board,boardWidth,boardHeight = boardy(0)
tileWidth = tileHeight = int(battleImageSize*1.25)
teamPlayer = [OrigLaslow,SpringLucina]
teamEnemy = [OrigRobin]

def battle(board,teamPlayer,teamEnemy):
    """sequence of events during a battle"""
    def printBoard(teamPlayer,board,i,boardVisual=None):
        """prints an updated version of the board"""
        def fillBackground():
            """places an image as the background"""
            gameDisplay.fill(black)
            imageBackground = pygame.image.load("Images/Cloud.png").convert_alpha()
            imageBackground = pygame.transform.scale(imageBackground,(displayWidth,displayHeight))
            imageBackgroundRect = imageBackground.get_rect()
            imageBackgroundRect.center = (displayWidth/2,displayHeight/2)
            gameDisplay.blit(imageBackground,imageBackgroundRect)
            return
        fillBackground()
        if i == 0 or i == 1:
            x = 0 
            for column in board:
                y = 0
                for row in column:
                    if row != "Obstacle":
                        imageBattle,imageBattleRect = resizeImage(pygame.image.load("Images/Grass.png").convert_alpha(),int(battleImageSize*1.25))
                        imageBattleRect = (x,y)
                        gameDisplay.blit(imageBattle,imageBattleRect)
                    else:
                        pygame.draw.rect(gameDisplay,brown,(x,y,tileWidth,tileHeight))
                    y += tileHeight
                x += tileWidth
        if i == 1:
            x = 0
            for column in boardVisual:
                y = 0
                for row in column:
                    if row == "Potential":
                        pygame.draw.rect(gameDisplay,blue,(x,y,tileWidth,tileHeight))
                    elif row == "Target":
                        pygame.draw.rect(gameDisplay,red,x,y,tileWidth,tileHeight)
                    y += tileHeight
                x += tileWidth
        for item in teamPlayer:
            imageBattle,imageBattleRect = resizeImage(item.imageBattle,battleImageSize)
            try: 
                positionTemporary[item]
            except: 
                imageBattleRect = (positionCurrent[item][0]*tileWidth,positionCurrent[item][1]*tileHeight)
            else:
                pygame.draw.rect(gameDisplay,blueDark,(positionCurrent[item][0]*tileWidth,positionCurrent[item][1]*tileHeight,tileWidth,tileHeight))
                pygame.draw.rect(gameDisplay,blue,(positionTemporary[item][0]*tileWidth,positionTemporary[item][1]*tileHeight,tileWidth,tileHeight))
                imageBattleRect = (positionTemporary[item][0]*tileWidth,positionTemporary[item][1]*tileHeight)
            gameDisplay.blit(imageBattle,imageBattleRect)
        pygame.display.flip()
        return
    def moveCharacter(coord=None):
        """sequence of events for moving a character"""
        boardVisual = boardy(1)
        if coord != None:
            positionTemporary.update({currentObject:coord})
        try:
            board[positionTemporary[currentObject][0]][positionTemporary[currentObject][1] + 1]
        except:
            pass
        else:
            if board[positionTemporary[currentObject][0]][positionTemporary[currentObject][1] + 1] == "Empty":
                boardVisual[positionTemporary[currentObject][0]][positionTemporary[currentObject][1] + 1] = "Potential"
        try:
            board[positionTemporary[currentObject][0]][positionTemporary[currentObject][1] - 1]
        except:
            pass
        else:
            if (positionTemporary[currentObject][1] - 1) < 0:
                pass
            else:
                if board[positionTemporary[currentObject][0]][positionTemporary[currentObject][1] - 1] == "Empty":
                    boardVisual[positionTemporary[currentObject][0]][positionTemporary[currentObject][1] - 1] = "Potential"
        try:
            board[positionTemporary[currentObject][0] + 1][positionTemporary[currentObject][1]]
        except:
            pass
        else:
            if board[positionTemporary[currentObject][0] + 1][positionTemporary[currentObject][1]] == "Empty":
                boardVisual[positionTemporary[currentObject][0] + 1][positionTemporary[currentObject][1]] = "Potential"
        try:
            board[positionTemporary[currentObject][0] - 1][positionTemporary[currentObject][1]]
        except:
            pass
        else:
            if (positionTemporary[currentObject][0] - 1) < 0:
                pass
            else:
                if board[positionTemporary[currentObject][0] - 1][positionTemporary[currentObject][1]] == "Empty":
                    boardVisual[positionTemporary[currentObject][0] - 1][positionTemporary[currentObject][1]] = "Potential"
        printBoard(teamPlayer,board,1,boardVisual)
        arrowControl = True
        return arrowControl,boardVisual
    positionCurrent = {}
    positionTemporary = {}  
    currentObject = ""
    boardVisual = ""
    coord = ""
    moveCount = 3
    arrowControl = False
    for item in teamPlayer:
        while True:
            cx = random.randint(0,boardWidth)        
            cy = boardHeight 
            if board[cx][cy] == "Empty":
                break
        board[cx][cy] = item
        positionCurrent.update({item:[cx,cy]})
    printBoard(teamPlayer,board,0)
    operate = True
    while operate and len(teamPlayer) > 0 and len(teamEnemy) > 0:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    operate = False
                    global run
                    run = False
                if arrowControl == True:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                        arrowControl = False
                        if event.key == pygame.K_UP:
                            try:
                                boardVisual[positionTemporary[currentObject][0]][positionTemporary[currentObject][1] - 1]
                            except:
                                pass
                            else:
                                if boardVisual[positionTemporary[currentObject][0]][positionTemporary[currentObject][1] - 1] == "Potential":
                                    coord = [positionTemporary[currentObject][0],positionTemporary[currentObject][1] - 1]
                                    # positionTemporary.update({currentObject:[positionTemporary[currentObject][0],positionTemporary[currentObject][1] - 1]})
                        elif event.key == pygame.K_DOWN:
                            try:
                                boardVisual[positionTemporary[currentObject][0]][positionTemporary[currentObject][1] + 1]
                            except:
                                pass
                            else:
                                if boardVisual[positionTemporary[currentObject][0]][positionTemporary[currentObject][1] + 1] == "Potential": 
                                    pass
                        elif event.key == pygame.K_RIGHT:
                            try:
                                boardVisual[positionTemporary[currentObject][0] + 1][positionTemporary[currentObject][1]]
                            except:
                                pass
                            else:
                                if boardVisual[positionTemporary[currentObject][0] + 1][positionTemporary[currentObject][1]] == "Potential":
                                    pass
                        elif event.key == pygame.K_LEFT:
                            try:
                                boardVisual[positionTemporary[currentObject][0] - 1][positionTemporary[currentObject][1]]
                            except:
                                pass
                            else:    
                                if boardVisual[positionTemporary[currentObject][0] - 1][positionTemporary[currentObject][1]] == "Potential":
                                    pass
                        if moveCount > 0:
                            moveCount -= 1
                            arrowControl,boardVisual = moveCharacter(coord)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                columnSelected = pos[0] // tileWidth
                rowSelected = pos[1] // tileHeight
                try:
                    board[columnSelected][rowSelected]
                except:
                    pass
                else:                   
                    if board[columnSelected][rowSelected] == "Empty":
                        positionTemporary = {}
                        currentObject = ""
                        boardVisual = ""
                        arrowControl = False
                        printBoard(teamPlayer,board,0)
                    elif board[columnSelected][rowSelected] != "Empty" and board[columnSelected][rowSelected] != "Obstacle" and board[columnSelected][rowSelected] != currentObject:
                        positionTemporary = {}
                        moveCount = 3
                        boardVisual = boardy(1)
                        boardVisual[columnSelected][rowSelected] = board[columnSelected][rowSelected]
                        currentObject = boardVisual[columnSelected][rowSelected]
                        positionTemporary.update({currentObject:[columnSelected,rowSelected]})
                        arrowControl,boardVisual = moveCharacter()
    return
#-----------------------------------------------------------------------------------------------------------------#
run = True
while run:
    clock.tick(60)
    gameDisplay.fill(black)
    battle(board,teamPlayer,teamEnemy)
    run = False
pygame.quit()
quit()



