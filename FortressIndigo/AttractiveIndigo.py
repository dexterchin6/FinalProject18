#=============================================================================================================================================#
#[Import Bay]#
import os,time,math,random
#=============================================================================================================================================#
#[Syntax Functions]#
def halfscreen():
    """moves cursor to the vertical center of the screen"""
    for x in range(12):
        print("")
    return
def enternclear():
    """has the user press enter to continue"""
    print("")
    input("Press Enter to Continue: ")
    return
def pausenclear():
    """creates a pause before continuing"""
    time.sleep(4)
    return
def notsuitableyn():
    """sequence of events when user input is not 'y' or 'n'"""
    print("")
    print("That is not a suitable answer. Enter either 'Y' or 'N'.")
    enternclear()
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

characters = []
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
#=============================================================================================================================================#
#[Battle Cores]#
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
                os.system('clear')
                time.sleep(2)
                halfscreen()
                print(specials[attacker.calcname])
                time.sleep(3)
                print(" ")
                print(specialconfirms[attacker.calcname])
                time.sleep(3)
                os.system('clear')
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
                os.system('clear')
                time.sleep(2)
                halfscreen()
                print(specials[defender.calcname])
                time.sleep(3)
                print(" ")
                print(specialconfirms[defender.calcname])
                time.sleep(3)
                os.system('clear')
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
    os.system('clear')
    eh,ea,es,ed,er,ec = attack(ua,uc,eh,ea,es,ed,er,ec,0)
    cc = ifcounter(eh)
    if cc == 1:
        print("")
        uh,ua,us,ud,ur,uc = counter(uh,ua,us,ud,ur,uc,ea,ec,0)
    ues = es + 10
    if ues < us:
        os.system('clear')
        eh,ea,es,ed,er,ec = attack(ua,uc,eh,ea,es,ed,er,ec,1)
    uus = us + 10
    if uus < es:
        if ues > us:
            os.system('clear')
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














