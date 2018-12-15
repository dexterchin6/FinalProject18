#=============================================================================================================================================#
#[Import Bay]#
from os import system
import time,math,random
#=============================================================================================================================================#
#[Syntax Functions]#
def halfscreen():
    """moves cursor to the vertical center of the screen"""
    system('clear')
    for x in range(12):
        print("")
    return
def enternclear():
    """has the user press enter to continue"""
    print("")
    input("Press Enter to Continue: ")
    return
def rendernclear():
    """ensures text is fully loaded before clearing"""
    time.sleep(1)
    return
def pausenclear():
    """creates a pause before continuing"""
    time.sleep(1.5)
    return
def test():
    """used for finding where errors are"""
    print('test')
    time.sleep(2)
    return
#=============================================================================================================================================#
#[Global Libraries]#
effectives = {
    'classeffectives' : {
        'Melee' : 'Dragon',
        'Dragon' : 'Mage',
        'Mage' : 'Melee',
        'Ranged' : [],
        'Staff' : []
        },
    'weaponeffectives' : {
        'Personal Ability' : [],
        'Sword' : [],
        'Lance' : [],
        'Dragon Stone' : [],
        'Tome' : [],
        'Bow' : [],
        'Dagger' : []
        },
    'movementeffectives' : {
        'Armored' : [],
        'Infantry' : [],
        'Flying' : [],
        'Calavry' : []
        }
    }
counters = {
    'Melee' : ['Melee','Dragon'],
    'Dragon' : ['Dragon','Melee','Staff'],
    'Magic' : ['Magic','Ranged','Staff'],
    'Staff': ['Staff','Magic','Ranged'],
    'Ranged' : ['Ranged','Magic','Staff']
    }
specials = {
    'Robin' : 'Intense power begins radiating outward. The opponent has no time to react before being hit with the reinforced blow.'
    }
specialconfirms = {
    'Robin' : '[Draconic Aura Engaged]'
    }
distant_counters = []

characters = ['Robin','a','b','c','d','e','f','g','h','i']
#=============================================================================================================================================#
#[Data Cores]#
class WeaponData:
    def __init__(self,weapname,weappronoun,weapbio,mgt,bnsspd,bnsdef,bnsres):
        """weapon data constructor"""
        self.weapname = weapname
        self.weappronoun = weappronoun
        self.weapbio = weapbio
        self.mgt = mgt
        self.bnsspd = bnsspd
        self.bnsdef = bnsdef
        self.bnsres = bnsres
class CharacterData:
    def __init__(self,calcname,dataname,brackname,fullname,movetype,classtype,weaptype,pronoun,attspeech,deathspeech,critpronoun,critspeech,bhealth,batt,bspd,bdfnse,bres,bcrit,based,tier,rank,team,bio):
        """character data constructor"""
        self.calcname = calcname
        self.dataname = dataname
        self.brackname = brackname
        self.fullname = fullname
        self.movetype = movetype
        self.classtype = classtype
        self.weaptype = weaptype
        self.pronoun = pronoun
        self.attspeech = attspeech
        self.deathspeech = deathspeech
        self.critpronoun = critpronoun
        self.critspeech = critspeech
        self.bhealth = bhealth
        self.batt = batt
        self.bspd = bspd
        self.bdfnse = bdfnse
        self.bres = bres
        self.bcrit = bcrit
        self.based = based
        self.tier = tier
        self.rank = rank
        self.team = team
        self.bio = bio
        return
    def biography(self):
        """prints all data of a character"""
        def personalbio():
            weapon = eval(eval(self.dataname)['Weapon'])
            system('clear')
            print("--------------------------------------------------------------------")
            print(f"{self.fullname}: {self.tier}")
            print(f"{self.movetype} Unit")
            print(self.based)
            print("")
            print(self.rank)
            print(self.team)
            print("")
            print(self.bio)
            print("")
            print(f"{weapon.weapname}:")
            print(weapon.weapbio)
            print("--------------------------------------------------------------------")
            enternclear()
            return
        def statbio():
            system('clear')
            print("--------------------------------------------------------------------")
            print(self.fullname)
            print(f"{self.classtype} Fighter")
            print("")
            print(f"{eval(self.dataname)['Health']} HP")
            print(f"{eval(self.dataname)['Attack']} ATK")
            print(f"{eval(self.dataname)['Speed']} SPD")
            print(f"{eval(self.dataname)['Defense']} DEF")
            print(f"{eval(self.dataname)['Resistance']} RES")
            print(f"Critical Chance: {eval(self.dataname)['Critical']}%")
            enternclear()
            return
        personalbio()
        statbio()
        return
    def chargain(self,i):
        """sequence of events when a new character is gained"""
        characters.append(self.calcname)
        halfscreen()
        if i == 0:
            print(f"{self.brackname} has joined your list of characters! {self.brackname} will be available for you to use in battle. Any new versions of this character gained throughout the game will also be available for you to use.")
        elif i == 1:
            print(f"{self.brackname} has joined your list of characters! {self.brackname} will be available for you to use in battle.")
        pausenclear()
        self.biography()
        return
#=============================================================================================================================================#
#[Battle Cores]#
def pickteam():
    """sequence of events to pick teams for battle"""
    def pick():
        """sequence of events to pick the player`s team"""
        def notsuitableyn():
            """sequence of events when user input is not 'y' or 'n'"""
            print("")
            print("That is not a suitable answer. Enter either 'Y' or 'N'.")
            enternclear()
            return
        def print_curparty(party):
            """prints the player`s current party"""
            print(f"Current party: {party}")
            print("")
            return
        namecompare = {
            'Robin' : 'Robin',
            'a' : 'a',
            'b' : 'b',
            'c' : 'c',
            'd' : 'd',
            'e' : 'e',
            'f' : 'f',
            'g' : 'g',
            'h' : 'h',
            'i' : 'i'
            }
        playerparty = []
        ncompare = []
        available = characters
        d = dd = 0
        while True:
            if d == 1:
                break
            if len(playerparty) == 0:
                while True:
                    system('clear')
                    print(available)
                    print("")
                    c = input("Choose a character to put into battle (Names are CaSe SeNsItIvE): ")
                    if c not in available:
                        print("")
                        print("That character is not available.")
                        enternclear()
                    else:
                        ncompare.append(namecompare[c])
                        playerparty.append(c)
                        available.remove(c)
                        rendernclear()
                        halfscreen()
                        print(f"{c} has been added to your party!")
                        print("")
                        print_curparty(playerparty)
                        rendernclear()
                        break
            while len(playerparty) >= 1:
                if len(playerparty) == 8:
                    while True:
                        system('clear')
                        print_curparty(playerparty)
                        print("")
                        c2 = input("Confirm team? [Y/N]: ").lower()
                        if c2 == 'y':
                            d = 1
                            dd = 1
                            break
                        elif c2 == 'n':
                            break
                        else:
                            notsuitableyn()
                    if dd == 1:
                        break
                    if len(playerparty) == 8:
                        while True:
                            system('clear')
                            print_curparty(playerparty)
                            c3 = input("Choose a character to remove (Names are CaSe SeNsItIvE): ")
                            if c3 not in playerparty:
                                print("")
                                print("That character is not in your party.")
                                enternclear()
                            else:
                                playerparty.remove(c3)
                                available.append(c3)
                                ncompare.remove(namecompare[c3])
                                print("")
                                print("{c3} has left your party.")
                                break
                system('clear')
                print_curparty(playerparty)
                c4 = input("Add or remove a character? [Add/Remove]: ").lower()
                if c4 == 'add':
                    while True:
                        system('clear')
                        print(f"Available characters: {available}")
                        print("")
                        print_curparty(playerparty)
                        c5 = input("Choose a character to put into battle (Names are CaSeSeNsItIvE): ")
                        if c5 not in available:
                            print("")
                            print("That character is not available.")
                            enternclear()
                        elif namecompare[c5] in ncompare:
                            print("A version of that character has already been chosen. You cannot have multiple versions of the same character in your party.")
                            enternclear()
                        else:
                            ncompare.append(namecompare[c5])
                            playerparty.append(c5)
                            available.remove(c5)
                            pausenclear()
                            halfscreen()
                            print(f"{c5} has been added to your party!")
                            print("")
                            print_curparty(playerparty)
                            pausenclear()
                            break
                elif c4 == 'remove':
                    while True:
                        system('clear')
                        print_curparty(playerparty)
                        c6 = input("Choose to remove either a character or 'Noone' (Names are CaSe SeNsItIvE): ").lower()
                        if c6 == 'noone':
                            break
                        elif c6 not in playerparty:
                            print("That character is not in your party.")
                            enternclear()
                        else:
                            playerparty.remove(c6)
                            available.append(c6)
                            ncompare.remove(namecompare[c6])
                            print("")
                            print("{c6} has left your party.")
                            break
                else:
                    notsuitableyn()
        return playerparty
    if len(characters) <= 8:
        playerparty = characters
    else:
        playerparty = pick()
    return playerparty
def skirmish(attacker,defender,uh,ua,us,ud,ur,uc,eh,ea,es,ed,er,ec):
    """sequence of events during a skirmish"""
    def rnd(val):
        """rounds a value to one decimal place"""
        val = math.ceil(val*1)/1
        return val
    def attack(ua,uc,eh,ea,es,ed,er,ec,i):
        """sequence of events during the initial attack"""
        def eff():
            """determines if attacker has an advantage"""
            m = c = w = 0
            if attacker.classtype in effectives['classeffectives']:
                m = 1.4
                c = 1
            else:
                weapon = eval(eval(attacker.dataname)['Weapon'])
                if weapon in effectives['weaponeffectives'][defender.weaptype]:
                    m = 1.4
                    w = 1
                elif weapon in effectives['movementeffectives'][defender.movetype]:
                    m = 1.4
                    w = 1
                else:
                    m = 1
            if c == 1:
                print(f"{attacker.brackname} has type advantage over {defender.bracktype}.")
            elif w == 1:
                print(f"{attacker.brackname}`s weapon grants an advantage over {defender.brackname}.")
            return m
        def critchance(critrate):
            """determines if attacker hit is a critical hit"""
            critm = 1
            critn = random.randint(0,100)
            if critn <= critrate:
                critm = 1.5
                print("")
                print(f"{attacker.brackname} has landed a critical hit! {attacker.critspeech}, {attacker.critpronoun}.")
                print("--------------------------------------------------------------------------------------------------------------")
                time.sleep(2)
                system('clear')
                time.sleep(2)
                halfscreen()
                print(specials[attacker.calcname])
                time.sleep(3)
                print(" ")
                print(specialconfirms[attacker.calcname])
                time.sleep(3)
                system('clear')
                time.sleep(1)
                print("--------------------------------------------------------------------------------------------------------------")
                print(f"{defender.brackname} was struck forecefully!")
            return critm
        def dmg(damage,health):
            """calculates defender health after attack"""
            def check(health):
                """determines if defender is still alive after attack"""
                if 0 > health:
                    print("")
                    print(f"{defender.brackname} has no more health left. {defender.deathspeech}.")
                else:
                    print("")
                    print(f"{defender.brackname} has {health} health left.")
                return
            if 0 > damage:
                print("")
                print(f"{attacker.brackname} did no damage!")
            else:
                health = health - damage
                health = rnd(health)
                print("")
                print(f"{attacker.brackname} did {damage} damage!")
                check(damage,health)
            return health
        print("--------------------------------------------------------------------------------------------------------------")
        equipweap = eval(eval(attacker.dataname)['Weapon'])
        if i == 0:
            print(f"{attacker.brackname} is attacking {defender.brackname} with {equipweap.weappronoun}! {attacker.attspeech}, {attacker.pronoun}.")
        elif i == 1:
            print(f"{attacker.brackname} is performing a followup attack! {attacker.attspeech}, {attacker.pronoun}.")
        m = eff()
        critm = critchance(uc)
        if attacker.classtype in ['Melee','Ranged']:
            bloc = ed
        elif attacker.classtype in ['Magic','Dragon','Staff']:
            bloc = er
        damage = rnd((ua*m*critm) - bloc)
        eh = dmg(damage,eh)
        return eh,ea,es,ed,er,ec
    def ifcounter(health):
        """determines if there is a counterattack"""
        cc = 0
        if 0 < health and defender.classtype in counters[attacker.classtype]:
            cc = 1
        elif 0 < health and eval(attacker.dataname)['Weapon'] in distant_counters:
            cc = 1
        return cc
    def counter(uh,ua,us,ud,ur,uc,ea,ec,i):
        """sequence of events during a counterattack"""
        def effrev():
            """determines if defender has an advantage"""
            m = c = w = 0
            if defender.classtype in effectives['classeffectives'][attacker.classtype]:
                m = 1.4
                c = 1
            else:
                weapon = eval(eval(defender.dataname)['Weapon'])
                if weapon in effectives['weaponeffectives'][attacker.weaptype]:
                    m = 1.4
                    w = 1
                elif weapon in effectives['movementeffectives'][attacker.movetype]:
                    m = 1.4
                    w = 1
                elif defender.weaptype == 'Bow' and attacker.movetype == 'Flying':
                    m = 1.4
                    w = 1
                else:
                    m = 1
            if c == 1:
                print(f"{attacker.brackname} has type advantage over {defender.brackname}.")
            elif w == 1:
                print(f"{attacker.brackname}`s weapon grants an advantage over {defender.brackname}.")
            return m
        def critchancerev(critrate):
            """determines if defender hit is a critical hit"""
            critm = 1
            critn = random.randint(0,100)
            if critn <= critrate:
                critm = 1.5
                print("")
                print(f"{defender.brackname} has landed a critical hit! {defender.critspeech}, {defender.critpronoun}.")
                print("--------------------------------------------------------------------------------------------------------------")
                time.sleep(2)
                system('clear')
                time.sleep(2)
                halfscreen()
                print(specials[defender.calcname])
                time.sleep(3)
                print(" ")
                print(specialconfirms[defender.calcname])
                time.sleep(3)
                system('clear')
                time.sleep(1)
                print("--------------------------------------------------------------------------------------------------------------")
                print(f"{attacker.brackname} was struck forecefully!")
            return critm
        def dmgrev(damage,health):
            """calculates attacker health after counterattack"""
            def checkrev(health):
                """determines if attacker is still alive"""
                if 0 > health:
                    print("")
                    print(f"{attacker.brackname} has no more health left.{attacker.deathspeech}.")
                else:
                    print("")
                    print(f"{attacker.brackname} has {health} health left.")
                return
            if 0 > damage:
                print("")
                print(f"{defender.brackname} did no damage!")
            else:
                health = health - damage
                health = rnd(health)
                print("")
                print(f"{defender.brackname} did {damage} damage!")
                checkrev(damage,health)
            return health
        print("--------------------------------------------------------------------------------------------------------------")
        if i == 0:
            print(f"{defender.name} is striking back! {defender.attspeech}, {defender.pronoun}.")
        elif i == 1:
            print(f"{defender.name} is performing a followup counterattack! {defender.attspeech}, {defender.pronoun}.")
        m = effrev()
        critm = critchancerev(ec)
        if defender.classtype in ['Melee','Ranged']:
            bloc = ud
        elif defender.classtype in ['Magic','Dragon','Staff']:
            bloc = ur
        damage = rnd((ea*m*critm) - bloc)
        uh = dmgrev(damage,uh)
        return uh,ua,us,ud,ur,uc
    system('clear')
    eh,ea,es,ed,er,ec = attack(ua,uc,eh,ea,es,ed,er,ec,0)
    cc = ifcounter(eh)
    if cc == 1:
        print("")
        uh,ua,us,ud,ur,uc = counter(uh,ua,us,ud,ur,uc,ea,ec,0)
    ues = es + 10
    if ues < us:
        system('clear')
        eh,ea,es,ed,er,ec = attack(ua,uc,eh,ea,es,ed,er,ec,1)
    uus = us + 10
    if uus < es:
        if ues > us:
            print("")
        else:
            system('clear')
        uh,ua,us,ud,ur,uc = counter(uh,ua,us,ud,ur,uc,ea,ec,1)
    return uh,ua,us,ud,ur,uc,eh,ea,es,ed,er,ec
#=============================================================================================================================================#
#[Weapon Library]#
Elwind = WeaponData('Elwind','an Elwind spell','A simple spell that causes green burns to the enemy.',8,0,0,0)
#=============================================================================================================================================#
#[Character Library]#
OrigRobin = CharacterData('Robin','OrigRobinData','[Robin]','[Robin]','Flying','Magic','Personal Ability','she shouted','"You think you can beat me!"','"Ugh.."','she says','"Get out of my sight."',27,14,17,23,15,5,'Based on FEH`s "Mystery Tactician" Robin','Tier I','Combatant','Legions Volara','Is often overconfident in her endeavors. Has an eye for a certain Falchion wielder. Lost bits of memory after being taken by the Fell Dragon.')
OrigRobinWeapon = Elwind
OrigRobinData = {
    'Weapon' : OrigRobinWeapon.weapname,
    'Health' : OrigRobin.bhealth,
    'Attack' : OrigRobin.batt + OrigRobinWeapon.mgt,
    'Speed' : OrigRobin.bspd + OrigRobinWeapon.bnsspd,
    'Defense' : OrigRobin.bdfnse + OrigRobinWeapon.bnsdef,
    'Resistance' : OrigRobin.bres + OrigRobinWeapon.bnsres,
    'Critical' : OrigRobin.bcrit
    }
#=============================================================================================================================================#
pickteam()













