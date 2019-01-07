#-----------------------------------------------------------------------------------------------------------------#
import pygame, time
import os
#-----------------------------------------------------------------------------------------------------------------#
pygame.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = str(0) + "," + str(0)
infoObject = pygame.display.Info()
displayWidth = infoObject.current_w
displayHeight = infoObject.current_h
windowRatio = 1366/displayWidth
gameDisplay = pygame.display.set_mode((displayWidth,displayHeight))
pygame.display.set_caption('Midnight Rising')
clock = pygame.time.Clock()
font = pygame.font.SysFont('lucidasans',15)

battleImageSize = 500

black = (0,0,0)
white = (255,255,255)
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
def skirmish(attacker,defender):
    """sequence of events during a skirmish"""
    #code for the introduction animation sequence#
    imageBox,imageBoxRect = resizeImage(pygame.image.load("BattleBox.png"),int(750/windowRatio))
    imageAtt,imageAttRect = resizeImage(attacker.imgBattle,battleImageSize)
    imageDef,imageDefRect = resizeImage(defender.imgBattle,battleImageSize) 
    imageDef = pygame.transform.flip(imageDef,True,False)
    imageBox_y = 0 - int(imageBox.get_size()[1]/2)
    imageAtt_x = 0 - imageAtt.get_size()[0]
    imageDef_x = displayWidth + imageDef.get_size()[0]
    while imageAtt_x <= 0 or imageBox_y <= displayHeight/2 or imageDef_x >= displayWidth:
        imageSpeed = int(displayWidth/16)
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
    def critscene(imageBox,imageBoxRect,imageAtt,imageAttRect,imageDef,imageDefRect,imageSpeed):
        """sequence of events for the critical hit animation"""
        imageAtt_x = imageAttRect.x
        while imageAtt_x >= 0 - imageAtt.get_size()[0]:
            imageAtt_x -= imageSpeed
            gameDisplay.fill(white)
            imageBoxRect.center = (displayWidth/2,displayHeight/2)
            gameDisplay.blit(imageBox,imageBoxRect)
            imageAttRect.midleft = (imageAtt_x,displayHeight/2)
            gameDisplay.blit(imageAtt,imageAttRect) 
            imageDefRect.midright = (displayWidth,displayHeight/2)
            gameDisplay.blit(imageDef,imageDefRect)
            pygame.display.flip()

    outputMessage(f"{attacker.nameBattle} is attacking {defender.nameBattle}!",black,displayWidth/2,(displayHeight/2 * 0.5) * windowRatio)
    critscene(imageBox,imageBoxRect,imageAtt,imageAttRect,imageDef,imageDefRect,imageSpeed)


    pygame.display.flip()
    time.sleep(5)
    return
#-----------------------------------------------------------------------------------------------------------------#
class Character:
    def __init__(self,imgBattle,nameBattle):
        """character class constructor"""
        self.imgBattle = imgBattle
        self.nameBattle = nameBattle
        return

OrigLaslow = Character(pygame.image.load("Laslow.png").convert_alpha(),"[Laslow]")
OrigRobin = Character(pygame.image.load("Robin.png").convert_alpha(),"[Robin]")
SpringLucina = Character(pygame.image.load("SpringLucina.png").convert_alpha(),"[SP! Lucina]")
#-----------------------------------------------------------------------------------------------------------------#
run = True
while run:
    clock.tick(60)
    pygame.event.pump()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
    gameDisplay.fill(white)
    
    skirmish(OrigLaslow,OrigRobin)
    run = False
    
pygame.quit()
quit()

#python UnknownIndigo.py