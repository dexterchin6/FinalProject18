import pygame,time
import os,random
#-----------------------------------------------------------------------------------------------------------------#
pygame.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = str(0) + "," + str(0)
infoObject = pygame.display.Info()
displayWidth = 800
displayHeight = 600
windowRatio = 1366/displayWidth
gameDisplay = pygame.display.set_mode((displayWidth,displayHeight))
pygame.display.set_caption('Midnight Rising')
clock = pygame.time.Clock()
font = pygame.font.SysFont('lucidasans',15)

battleImageSize = 50
skirmishImageSize = 500

black = (0,0,0)
white = (255,255,255)
brown = (139,69,19)
blue = (114,188,212)
#-----------------------------------------------------------------------------------------------------------------#
def outputMessage(txt,color,textw,texth):
    """outputs text onto the window"""
    def text_objects(txt,color):
        """sequence of events to render the text surface to be put on the window"""
        textSurface = font.render(txt,True,color)
        return textSurface,textSurface.get_rect()
    textSurf,textRect = text_objects(txt,color)
    textRect.midtop = (textw,texth)
    gameDisplay.blit(textSurf,textRect)
    return
def resizeImage(image,imageWidth):
    """resizes image based on difference in original window to current window"""
    w,h = image.get_size()
    #scales image to standard image size#
    imageHeight = int((h * imageWidth)/w)
    scaleImage = pygame.transform.scale(image,(imageWidth,imageHeight))
    #scales image based on current computer aspect ratio#
    newWidth = int(imageWidth/windowRatio)
    newHeight = int((imageHeight * newWidth)/imageWidth)
    newImage = pygame.transform.scale(scaleImage,(newWidth,newHeight))
    return newImage,newImage.get_rect()
#-----------------------------------------------------------------------------------------------------------------#
class Character:
    def __init__(self,imageSkirmish,imageBattle,nameSkirmish):
        """character class constructor"""
        self.imageSkirmish = imageSkirmish
        self.imageBattle = imageBattle
        self.nameSkirmish = nameSkirmish
        return
OrigLaslow = Character(pygame.image.load("Images/Laslow.png").convert_alpha(),pygame.image.load("Images/LaslowChibi.png").convert_alpha(),"[Laslow]")
OrigRobin = Character(pygame.image.load("Images/Robin.png").convert_alpha(),pygame.image.load("Images/RobinChibi.png").convert_alpha(),"[Robin]")
SpringLucina = Character(pygame.image.load("Images/SpringLucina.png").convert_alpha(),pygame.image.load("Images/SpringLucinaChibi.png").convert_alpha(),"[SP! Lucina]")
#-----------------------------------------------------------------------------------------------------------------#
def board2():
    board = []
    c1 = []
    c2 = []
    c3 = []
    for x in range(3):
        c1.append('Empty')
    board.append(c1)
    for x in range(3):
        c2.append('Empty')
    board.append(c2)
    for x in range(3):
        c3.append('Empty')
    board.append(c3)
    board[1][0] = 'Obstacle'
    return board
width = height = int(battleImageSize*1.25/windowRatio)
board1 = board2()
pteam = ['OrigLaslow','SpringLucina']
def battle(board,pteam):
    def fillBackground():
        gameDisplay.fill(black)
        imageBack = pygame.image.load("Images/Grass.png").convert_alpha()
        imageBack = pygame.transform.scale(imageBack,(displayWidth,displayHeight))
        imageBackRect = imageBack.get_rect()
        imageBackRect.center = (displayWidth/2,displayHeight/2)
        gameDisplay.blit(imageBack,imageBackRect)
    def print_board(i):
        fillBackground()
        x = 0
        for column in board:
            y = 0
            for row in column:
                if row != 'Obstacle':
                    imageBattle,imageBattleRect = resizeImage(pygame.image.load("Images/Grass.png").convert_alpha(),int(battleImageSize*1.25))
                    imageBattleRect = (x,y)
                    gameDisplay.blit(imageBattle,imageBattleRect)
                else:
                    pygame.draw.rect(gameDisplay,brown,(x,y,width,height))
                y += height
            x += width
        if i == 0:
            for item in pteam:
                board[position[item][0]][position[item][1]] = item
                imageBattle,imageBattleRect = resizeImage(eval(item).imageBattle,battleImageSize)
                imageBattleRect = (position[item][0]*width,position[item][1]*height)
                gameDisplay.blit(imageBattle,imageBattleRect)
        elif i == 1:
            for item in pteam:
                board[position[item][0]][position[item][1]] = item
                imageBattle,imageBattleRect = resizeImage(eval(item).imageBattle,battleImageSize)
                try:
                    imageBattleRect = (positionTemporary[item][0]*width,positionTemporary[item][1]*height)
                except:
                    imageBattleRect = (position[item][0]*width,position[item][1]*height)
                finally:
                    gameDisplay.blit(imageBattle,imageBattleRect)
        pygame.display.flip()
        return
    position = {}
    positionTemporary = {}
    controlArrow = False
    for item in pteam:
        while True:
            x = random.randint(0,2)
            y = 2
            if board[x][y] == 'Empty':
                board[x][y] = item
                break
        position.update({item:[x,y]})
    print_board(0)
    go = True
    while go:
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    go = False
                    global run 
                    run = False
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    if controlArrow == True:
                        if event.key == pygame.K_UP:
                            if boardVisual[columnSelected][rowSelected - 1] == 'Potential':
                                positionTemporary.update({currentObject:[columnSelected,rowSelected - 1]})
                                print_board(1)
                        elif event.key == pygame.K_DOWN:
                            if boardVisual[columnSelected][rowSelected + 1] == 'Potential':
                                positionTemporary.update({currentObject:[columnSelected,rowSelected + 1]})
                                print_board(1)
                        elif event.key == pygame.K_LEFT:
                            if boardVisual[columnSelected - 1][rowSelected] == 'Potential':
                                positionTemporary.update({currentObject:[columnSelected - 1,rowSelected]})
                                print_board(1)
                        elif event.key == pygame.K_RIGHT:
                            if boardVisual[columnSelected + 1][rowSelected] == 'Potential':
                                positionTemporary.update({currentObject:[columnSelected + 1,rowSelected]})
                                print_board(1)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                columnSelected = pos[0] // width
                rowSelected = pos[1] // height
                try:
                    board[columnSelected][rowSelected]
                except:
                    pass
                else:
                    controlArrow = False
                    currentObject = ''
                    print_board(0)
                    if board[columnSelected][rowSelected] != 'Empty' and board[columnSelected][rowSelected] != 'Obstacle' and board[columnSelected][rowSelected] != currentObject:
                        positionTemporary = {}
                        boardVisual = board2()
                        boardVisual[columnSelected][rowSelected] = board[columnSelected][rowSelected]
                        currentObject = boardVisual[columnSelected][rowSelected]
                        pygame.draw.rect(gameDisplay,blue,(columnSelected*width,rowSelected*height,width,height))
                        try:
                            boardVisual[columnSelected][rowSelected + 1]
                        except:
                            pass
                        else:
                            if board[columnSelected][rowSelected + 1] == 'Empty':
                                boardVisual[columnSelected][rowSelected + 1] = 'Potential'
                                pygame.draw.rect(gameDisplay,blue,(columnSelected*width,(rowSelected + 1)*height,width,height))
                        try:
                            boardVisual[columnSelected][rowSelected - 1]
                        except:
                            pass
                        else:
                            if board[columnSelected][rowSelected - 1] == 'Empty':
                                boardVisual[columnSelected][rowSelected - 1] = 'Potential'
                                pygame.draw.rect(gameDisplay,blue,(columnSelected*width,(rowSelected - 1)*height,width,height))
                        try:
                            boardVisual[columnSelected - 1][rowSelected]
                        except:
                            pass
                        else:
                            if board[columnSelected - 1][rowSelected] == 'Empty':
                                boardVisual[columnSelected - 1][rowSelected] = 'Potential'
                                pygame.draw.rect(gameDisplay,blue,((columnSelected - 1)*width,rowSelected*height,width,height))
                        try:
                            boardVisual[columnSelected + 1][rowSelected]
                        except:
                            pass
                        else:
                            if board[columnSelected + 1][rowSelected] == 'Empty':
                                boardVisual[columnSelected + 1][rowSelected] = 'Potential'
                                pygame.draw.rect(gameDisplay,blue,((columnSelected + 1)*width,rowSelected*height,width,height))
                        imageBattle,imageBattleRect = resizeImage(eval(currentObject).imageBattle,battleImageSize)
                        imageBattleRect = (columnSelected*width,rowSelected*height)
                        gameDisplay.blit(imageBattle,imageBattleRect)
                        pygame.display.flip()
                        controlArrow = True
    return
#-----------------------------------------------------------------------------------------------------------------#
run = True
while run:
    clock.tick(60)
    gameDisplay.fill(black)
    battle(board1,pteam)
pygame.quit()
quit()