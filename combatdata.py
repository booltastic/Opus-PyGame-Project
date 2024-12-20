from images import *
from gamedata import *
from drawfunctions import *
from ItemsAndAbilities import *
import pygame

#Unit Locations

#Combat Scene Unit Placement
#Friendly Side
fposition5 = WINDOW_WIDTH * 0.20, WINDOW_HEIGHT * 0.54
fposition4 = WINDOW_WIDTH * 0.26, WINDOW_HEIGHT * 0.54
fposition3 = WINDOW_WIDTH * 0.14, WINDOW_HEIGHT * 0.54
fposition2 = WINDOW_WIDTH * 0.26, WINDOW_HEIGHT * 0.54
fposition1 = WINDOW_WIDTH * 0.38, WINDOW_HEIGHT * 0.54

#Enemy Side
eposition1 = WINDOW_WIDTH * 0.52, WINDOW_HEIGHT * 0.54
eposition2 = WINDOW_WIDTH * 0.64, WINDOW_HEIGHT * 0.54
eposition3 = WINDOW_WIDTH * 0.76, WINDOW_HEIGHT * 0.54
eposition4 = WINDOW_WIDTH * 0.72, WINDOW_HEIGHT * 0.54
eposition5 = WINDOW_WIDTH * 0.78, WINDOW_HEIGHT * 0.54


class Fighter:
    FriendlyAbilitiesTriggeredList = []
    OpponentAbilitiesTriggeredList = []

    def __init__(self, name, health, attack, friendly, unit, helmet=None,
                 chest=None,legs=None,lefthand=None,righthand=None,gloves=None,feet=None):
        self.name = name
        self.health = health
        self.attack = attack
        self.positionint = None
        self.position = None
        self.friendly = friendly
        self.unit = unit
        self.STOBability = False

        #Gear
        self.helmet = helmet
        self.chest = chest #self.chest = GoblinBossArmor
        self.legs = legs
        self.lefthand = lefthand
        self.righthand = righthand
        self.gloves = gloves
        self.feet = feet

        self.gear_list = [self.helmet,self.chest,self.legs,self.lefthand,self.righthand,self.gloves,self.feet]
        self.ability_list = []
        self.modifystats()  # only run for when object is created with gear pre-equipped

        self.takesdamage = False
        self.dealsdamage = False
        self.dieability = False

        # Unit Images
        if self.unit == 'basicgob':
            self.rect = SmallBasicDemon_icon
        if self.unit == 'roboboss':
            self.rect = robo_boss_sprite.animate_Sprite() #sets is_animating to true
        if self.unit == 'robominer':
            self.rect = ShopRobotMiner_icon

    def modifystats(self):
        for x in self.gear_list: #iterates through all gear
            if x is not None: #if gear slot is populated

                self.health += x.health
                self.attack += x.attack
                self.ability_list.append(x.gearability)
                print(self.ability_list)

    def unit_abilities(self):
        # pass
        # #self.ability_list = []
        # # if self.unit == 'robominer':
        # #     if self.STOBability:
        # #         basicrobotability()
        # #         self.STOBability = False #once ability triggers, do this to make it only loop once
        # # if self.unit == 'roboboss':
        # #     if self.takesdamage==True:
        # #         nukeability()
        # #         self.takesdamage=False
        # #         self.dealsdamage = False
        # # else:
        self.takesdamage = False
        self.dealsdamage = False

def check_triggers():

    for x in gameunits.FriendlyUnitList: #about to click continue. both front units have triggers.
        if x.takesdamage or x.dealsdamage:
            GameData.triggersactive=True
            #Fighter.FriendlyAbilitiesTriggeredList.append(x) #append active triggered abiltities (the function) (units abilities with If checks in place)

    for x in gameunits.OpponentUnitList:
        if x.takesdamage or x.dealsdamage:
            GameData.triggersactive=True
            #Fighter.OpponentAbilitiesTriggeredList.append(x)

def reactions(): #Executes any triggers that are activated
    if GameData.triggersactive:
        #print('trigs active in reactions: '+ str(Fighter.FriendlyAbilitiesTriggeredList))
        if GameData.interactionqueue < len(Fighter.FriendlyAbilitiesTriggeredList):  # one ability in queue, if int 0 <= 1, add 1, fix number
            GameData.interactionqueue += 1
            indexfix = GameData.interactionqueue - 1
            GameData.triggeredunit = Fighter.FriendlyAbilitiesTriggeredList[indexfix]
            if GameData.interactionqueue > len(Fighter.FriendlyAbilitiesTriggeredList) :  # loop checks that all STOBs have been run and set to false then moves to elif loop
                GameData.interactionqueue += len(Fighter.FriendlyAbilitiesTriggeredList) #kick out of the loop
                #GameData.combatphase += 1
            else:
                Fighter.FriendlyAbilitiesTriggeredList[indexfix].unit_abilities() #do the thing number in queue

        elif GameData.interactionqueue <= len(Fighter.OpponentAbilitiesTriggeredList) - 1:
            GameData.combatlog = ''
            GameData.interactionqueue += 1
            indexfix = GameData.interactionqueue - 1
            GameData.triggeredunit = Fighter.OpponentAbilitiesTriggeredList[indexfix]
            if GameData.interactionqueue > len(Fighter.OpponentAbilitiesTriggeredList) - 1:  # loops checks all STOBS have been run
                GameData.interactionqueue += len(Fighter.OpponentAbilitiesTriggeredList)
                GameData.combatphase += 1
            else:
                Fighter.OpponentAbilitiesTriggeredList[indexfix].unit_abilities()
        else:
            GameData.triggersactive=False


class UnitLists:

    def reset_objects(self):
        UnitLists.playerfighter1 = Fighter('Robot Boy 1', 12, 3, True, 'robominer')
        UnitLists.playerfighter2 = Fighter('Robot Boy 2', 8, 2, True, 'robominer')
        UnitLists.playerfighter3 = Fighter('Robot Boy 3', 8, 2, True, 'robominer')
        UnitLists.goblinenemy1 = Fighter('Spinny Gob 1', 12, 2, False, 'basicgob')
        UnitLists.goblinenemy2 = Fighter('Spinny Gob 2', 8, 2, False, 'basicgob')
        UnitLists.goblinenemy3 = Fighter('Spinny Gob 3', 12, 2, False, 'basicgob')
        UnitLists.MiningBoss = Fighter('Robo-Mining Boss', 12, 15, True, 'roboboss', chest=GoblinBossChestArmor)

    def reset_unitlists(self):
        gameunits.FriendlyUnitList = [UnitLists.MiningBoss]
        gameunits.OpponentUnitList = [UnitLists.goblinenemy1, UnitLists.goblinenemy2, UnitLists.goblinenemy3]

gameunits = UnitLists()
fightActive = False

def get_unit_positions():
    for x in gameunits.FriendlyUnitList:
        # Unit Images
        if x.unit == 'basicgob':
            x.rect = SmallBasicDemon_icon
        if x.unit == 'roboboss':
            x.rect = robo_boss_sprite.animate_Sprite() #sets is_animating to true
        if x.unit == 'robominer':
            x.rect = ShopRobotMiner_icon
        x.positionint = gameunits.FriendlyUnitList.index(x)
        if x.positionint==0:
            x.position = fposition1
        if x.positionint==1:
            x.position = fposition2
        if x.positionint==2:
            x.position = fposition3
        if x.positionint==3:
            x.position = fposition4
        if x.positionint==4:
            x.position = fposition5
    for x in gameunits.OpponentUnitList:
        x.positionint = gameunits.OpponentUnitList.index(x)
        if x.positionint == 0:
            x.position = eposition1
        if x.positionint == 1:
            x.position = eposition2
        if x.positionint == 2:
            x.position = eposition3
        if x.positionint == 3:
            x.position = eposition4
        if x.positionint == 4:
            x.position = eposition5


def draw_battle_positions(rects):
    print('draw bat pos')
    get_unit_positions()
    for x in gameunits.FriendlyUnitList:
        if x.position is not None:
            rects[x] = pygame.Rect((x.position), (small_icon))  # location, size
            screen.blit(x.rect, rects[x])
            get_text_box(x.attack, 50, (x.position[0] + 15, x.position[1] - 20), RED, horiboxscale=float(0.7),
                         vertboxscale=float(0.5))  # width then height
            get_text_box(x.health, 50, (x.position[0] + 70, x.position[1] - 20), BLUE, horiboxscale=float(0.7),
                         vertboxscale=float(0.5))  # width then height
            get_text_box(x.name, 20, (x.position[0] + 40, x.position[1] + 100), BLUE, horiboxscale=float(0.1),
                         vertboxscale=float(0.5))  # width then height
    for x in gameunits.OpponentUnitList:
        if x.position is not None:
            rects[x] = pygame.Rect((x.position), (small_icon))  # location, size
            screen.blit(x.rect, rects[x])
            get_text_box((x.attack), 50, (x.position[0] + 15, x.position[1] - 20), RED, horiboxscale=float(0.7),
                         vertboxscale=float(0.5))
            get_text_box((x.health), 50, (x.position[0] + 70, x.position[1] - 20), BLUE, horiboxscale=float(0.7),
                         vertboxscale=float(0.5))  # width then height
            get_text_box((x.name), 20, (x.position[0] + 40, x.position[1] + 100), BLUE, horiboxscale=float(0.1),
                         vertboxscale=float(0.5))  # width then height
    return rects



def tree_building_rects_and_images():
    draw_background(treebuildingscene)
    rects = {}
    rects['fightbutton'] = draw_fight_button()
    rects['backbutton'] = draw_back_button()

    robo_boss_sprite.start_animate_Sprite()
    draw_battle_positions(rects)

    if GameData.introfighttext == 0:
        get_text_box('Hey! I said dont come here! Stand back kid, Ill handle this!', 40,
                     (WINDOW_WIDTH / 2, WINDOW_HEIGHT * 0.35),
                     RED)
    get_text_box(GameData.combatlog, 40,
                 (WINDOW_WIDTH / 2, WINDOW_HEIGHT * 0.2),
                 RED)
    get_text_box(GameData.combatlog2, 40,
                 (WINDOW_WIDTH / 2, WINDOW_HEIGHT * 0.25),
                 RED)
    if GameData.introfight == 1:
        get_text_box('Get the hell out of here before they come back!', 40,
                     (WINDOW_WIDTH / 2, WINDOW_HEIGHT * 0.35),
                     RED)
    return rects


def continueCombat(): # high level combat flow
    # print(GameData.triggersactive)
    # print(Fighter.FriendlyAbilitiesTriggeredList)
    # print(Fighter.OpponentAbilitiesTriggeredList)
    check_triggers()
    reactions()
    #print(GameData.triggersactive)
    if GameData.triggersactive == False:
        if GameData.combatphase == 0: #initially will be 0
            startofbattlephase() #runs below STOB phase
        if GameData.combatphase == 1:
            damagephase()
            GameData.combatphase -= 1
    if len(gameunits.OpponentUnitList) == 0 or len(gameunits.FriendlyUnitList) == 0:  # both teams have at least 1 unit alive
        GameData.fightActive = False
        GameData.introfight = 1

    # else:
    #     for x in attackqueue: #all units with True triggers
    #         x.triggeredability


def startofbattlephase():

    if GameData.fcombatstep<=len(gameunits.FriendlyUnitList)-1: #from index 0-2 (1-3 in list of units)
        GameData.fcombatstep += 1
        indexfix = GameData.fcombatstep-1
        GameData.triggeredunit = gameunits.FriendlyUnitList[indexfix]
        if gameunits.FriendlyUnitList[indexfix].STOBability==False: #loop checks that all STOBs have been run and set to false then moves to elif loop
            GameData.fcombatstep += len(gameunits.FriendlyUnitList)
            GameData.combatphase += 1
        else:
            gameunits.FriendlyUnitList[indexfix].unit_abilities()

    elif GameData.ecombatstep<=len(gameunits.OpponentUnitList)-1:
        GameData.combatlog = ''
        GameData.ecombatstep += 1
        indexfix = GameData.ecombatstep - 1
        GameData.triggeredunit = gameunits.OpponentUnitList[indexfix]
        if gameunits.OpponentUnitList[indexfix].STOBability==False: #loops checks all STOBS have been run
            GameData.ecombatstep += len(gameunits.OpponentUnitList)
            GameData.combatphase += 1
        else:
            gameunits.OpponentUnitList[indexfix].unit_abilities()

    else:

        GameData.combatphase += 1
        GameData.combatlog = ''
        GameData.combatlog2 = ''

#make generic list of keywords so they can be toggled and run an effect. add attributes to init with if true run this function then set off. damaged, deals damage, dies for now.

def damagephase():
    gameunits.FriendlyUnitList[0].dealsdamage = True
    gameunits.FriendlyUnitList[0].takesdamage = True
    gameunits.OpponentUnitList[0].dealsdamage = True
    gameunits.OpponentUnitList[0].takesdamage = True
    if gameunits.OpponentUnitList[0].health > 0:
        gameunits.OpponentUnitList[0].health -= gameunits.FriendlyUnitList[0].attack
    if gameunits.FriendlyUnitList[0].health > 0:
        gameunits.FriendlyUnitList[0].health -= gameunits.OpponentUnitList[0].attack
    GameData.combatlog = (
                'Attack Phase: ' + str(gameunits.FriendlyUnitList[0].name) + ' dealt ' + str(gameunits.OpponentUnitList[0].attack) +' damage to ' + gameunits.OpponentUnitList[0].name)
    GameData.combatlog2 = (
                'Attack Phase: ' + str(gameunits.OpponentUnitList[0].name) + ' dealt ' + str(gameunits.FriendlyUnitList[0].attack) +' damage to ' + gameunits.FriendlyUnitList[0].name)
    if gameunits.OpponentUnitList[0].health <= 0:
        gameunits.OpponentUnitList.pop(0)  # remove from list
    if gameunits.FriendlyUnitList[0].health <= 0:
        gameunits.FriendlyUnitList.pop(0)  # remove from list

    # else:
    #     GameData.fightActive=False