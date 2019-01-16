def skirmish(attacker,defender,ph,pa,ps,pd,pr,pc,eh,ea,es,ed,er,ec):
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
            if attacker.classtype in effectives[defender.classtype]:
                m = 1.4
                c = 1
            else:
                if attacker.nameWeapon in effectives[defender.classtype] or attacker.nameWeapon in effectives[defender.movetype] or attacker.nameWeapon in effectives[defender.weapontype]:
                    m = 1.4
                    w = 1
                elif attacker.weapontype == 'Bow' and defender.movetype == 'Flying':
                    m = 1.4
                    w = 1
            if c == 1:
                outputMessage(f"{attacker.nameBattle} has an advantage over {defender.nameBattle}.",black,displayWidth/2,displayHeight*0.35)
            elif w == 1:
                outputMessage(f"{attacker.nameBattle}`s weapon grants an advantage over {defender.nameBattle}.",black,displayWidth/2,displayHeight*0.35)
            pygame.display.flip()
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
                outputMessage(f"{attacker.nameBattle} has landed a critical hit! {attacker.speechCritical}",black,displayWidth/2,displayHeight*h)
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
                outputMessage(attacker.speechCritical,white,int(displayWidth * 2/3),displayHeight/3)
                pygame.display.flip()
                pygame.time.delay(2000)
                outputMessage(attacker.nameCritical,white,int(displayWidth * 2/3),displayHeight/2)
                pygame.display.flip()
            return mCritical
        def damageCalculate(damage,health,mCritical):
            """calculates defender health after attacker attacks"""
            ifc = 0
            if mCritical = 1.5:
                    h = 0.45
                else:
                    h = 0.4
            if damage > 0:
                health = int(health - damage)
                outputMessage(f"{attacker.nameBattle} did {damage} damage!",black,displayWidth/2,displayHeight*h)
            else:
                outputMessage(f"{attacker.nameBattle} did no damage!",black,displayWidth/2,displayHeight*h)
            if health > 0:
                outputMessage(f"{defender.nameBattle} has {health} health left.",black,displayWidth/2,displayHeight*(h + 0.5))
            else:
                ifc = 1
                outputMessage(f"{defender.nameBattle} has no more health left. {defender.speechDeath}",black,displayWidth/2,displayHeight*(h + 0.5))
            return health,ifc    
        if i == 0:
            outputMessage(f"{attacker.nameBattle} is attacking {defender.nameBattle} with {attacker.nameWeapon}! {attacker.speechAttack}",black,displayWidth/2,displayHeight*0.3)
        elif i == 1:
            outputMessage(f"{attacker.nameBattle} is performing a follow-up attack! {attacker.speechAttack}",black,displayWidth/2,displayHeight*0.3)
        pygame.display.flip()
        mEfficiency = efficiency()
        mCritical = criticalChanceRev(pc,mEfficiency)
        if attacker.classtype in ['Infantry','Ranged']:
            block = pd
        elif attacker.classtype in ['Magic','Dragon','Staff']:
            block = pr
        dam = ea*mEfficiency*mCritical
        dam -= block
        ph,ifc = damageCalculate(dam,ph,mCritical)
        pygame.display.flip()
        return pa,pc,eh,ea,es,ed,er,ec,ifc
    def ifcounter(ifc):
        """determines if there is a counterattack"""
        cc = 0
        if ifc = 1 and defender.classtype in counters[attacker.classtype]:
            cc = 1
        elif ifc = 1 and defender.nameWeapon in distantCounters:
            cc = 1
        return cc
    def counter(ph,pa,ps,pd,pr,pc,ea,ec,i):
        """sequence of events during the counterattack"""
        def efficiencyRev():
             """determines if the defender has an advantage"""
            c = w = 0
            m = 1
            if defender.classtype in effectives[attacker.classtype]:
                m = 1.4
                c = 1
            else:
                if defender.nameWeapon in effectives[attacker.classtype] or defender.nameWeapon in effectives[attacker.movetype] or defender.nameWeapon in effectives[attacker.weapontype]:
                    m = 1.4
                    w = 1
                elif defender.weapontype == 'Bow' and attacker.movetype == 'Flying':
                    m = 1.4
                    w = 1
            if c == 1:
                outputMessage(f"{defender.nameBattle} has an advantage over {attacker.nameBattle}.",black,displayWidth/2,displayHeight*0.35)
            elif w == 1:
                outputMessage(f"{defender.nameBattle}`s weapon grants an advantage over {attacker.nameBattle}.",black,displayWidth/2,displayHeight*0.35)
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
                outputMessage(f"{defender.nameBattle} has landed a critical hit! {defender.speechCritical}",black,displayWidth/2,displayHeight*h)
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
                outputMessage(defender.speechCritical,white,int(displayWidth * 2/3),displayHeight/3)
                pygame.display.flip()
                pygame.time.delay(2000)
                outputMessage(defender.nameCritical,white,int(displayWidth * 2/3),displayHeight/2)
                pygame.display.flip()
            return mCritical
        def damageCalculateRev(damage,health,mCritical):
            """calculates attacker health after defender attacks"""
            if mCritical = 1.5:
                    h = 0.45
                else:
                    h = 0.4
            if damage > 0:
                health = int(health - damage)
                outputMessage(f"{defender.nameBattle} did {damage} damage!",black,displayWidth/2,displayHeight*h)
            else:
                outputMessage(f"{defender.nameBattle} did no damage!",black,displayWidth/2,displayHeight*h)
            if health > 0:
                outputMessage(f"{attacker.nameBattle} has {health} health left.",black,displayWidth/2,displayHeight*(h + 0.5))
            else:
                ifc = 1
                outputMessage(f"{attacker.nameBattle} has no more health left. {attacker.speechDeath}",black,displayWidth/2,displayHeight*(h + 0.5))
            return health   
        if i = 0:       
            outputMessage(f"{defender.nameBattle} is striking back! {defender.speechAttack}",black,displayWidth/2,displayHeight*0.3)
        elif i == 1:
            outputMessage(f"{defender.nameBattle} is performing a second counterattack!",black,displayWidth/2,displayHeight*0.3)
        mEfficiency = efficiencyRev()
        mCritical = criticalChanceRev(ec,mEfficiency)
        if defender.classtype in ['Infantry','Ranged']:
            block = pd
        elif defender.classtype in ['Magic','Dragon','Staff']:
            block = pr
        dam = ea*mEfficiency*mCritical
        dam -= block
        ph = damageCalculateRev(dam,ph,mCritical)
        pygame.display.flip()
        return ph,pa,ps,pd,pr,pc,ea,ec
    pa,pc,eh,ea,es,ed,er,ec,ifc = initial(pa,pc,eh,ea,es,ed,er,ec,0)
    cc = ifcounter(ifc)
    if cc == 1:
        blackgroundReset()
        ph,pa,ps,pd,pr,pc,ea,ec = counter(ph,pa,ps,pd,pr,pc,ea,ec,0)
    ues = es + 10
    if ps >= ues:
        backgroundReset()
        pa,pc,eh,ea,es,ed,er,ec,ifc = initial(pa,pc,eh,ea,es,ed,er,ec,1)
    ups = ps + 10
    if es >= ups:
        backgroundReset()
        ph,pa,ps,pd,pr,pc,ea,ec = counter(ph,pa,ps,pd,pr,pc,ea,ec,1)
    return
