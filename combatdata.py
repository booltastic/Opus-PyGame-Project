from images import *
from gamedata import *
from drawfunctions import *
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
    def __init__(self, name, health, attack, friendly, unit):
        self.name = name
        self.health = health
        self.attack = attack
        self.positionint = None
        self.position = None
        self.friendly = friendly
        self.unit = unit
        self.STOBabilitynull = True
        if self.unit == 'basicgob':
            self.rect = SmallBasicDemon_icon
        if self.unit == 'roboboss':
            self.rect = robot_boss_image
        if self.unit == 'robominer':
            self.rect = ShopRobotMiner_icon

        #self.unit_abilities()

    def unit_abilities(self):
        self.ability_list = []
        if self.unit == 'robominer':
            basicrobotability()
            self.STOBabilitynull = False
        if self.unit == 'roboboss':
            basicrobotability()


class UnitLists:

    def reset_objects(self):
        UnitLists.playerfighter1 = Fighter('Robot Boy 1', 12, 3, True, 'robominer')
        UnitLists.playerfighter2 = Fighter('Robot Boy 2', 8, 2, True, 'robominer')
        UnitLists.playerfighter3 = Fighter('Robot Boy 3', 8, 2, True, 'robominer')
        UnitLists.goblinenemy1 = Fighter('Spinny Gob 1', 12, 2, False, 'basicgob')
        UnitLists.goblinenemy2 = Fighter('Spinny Gob 2', 8, 2, False, 'basicgob')
        UnitLists.goblinenemy3 = Fighter('Spinny Gob 3', 12, 2, False, 'basicgob')
        UnitLists.MiningBoss = Fighter('Robo-Mining Boss', 40, 15, True, 'roboboss')

    def reset_unitlists(self):
        gameunits.FriendlyUnitList = [UnitLists.MiningBoss]
        gameunits.OpponentUnitList = [UnitLists.goblinenemy1, UnitLists.goblinenemy2, UnitLists.goblinenemy3]

gameunits = UnitLists()
fightActive = False

def basicrobotability():
    gameunits.OpponentUnitList[0].health -= 1
    GameData.combatlog=('Start of Battle: ' + str(GameData.triggeredunit) + ' dealt 1 damage to '+gameunits.OpponentUnitList[0].name)

def nukeability(): #have abilities be functions like this, named something specific?
    gameunits.OpponentUnitList[0].health -= 1
    GameData.combatlog=('Start of Battle: ' + str(GameData.triggeredunit) + ' dealt 1 damage to '+gameunits.OpponentUnitList[0].name)


def get_unit_positions():
    for x in gameunits.FriendlyUnitList:
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
    get_unit_positions()
    for x in gameunits.FriendlyUnitList:
        if x.position is not None:
            rects[x] = pygame.Rect((x.position), (small_icon))  # location, size
            screen.blit(x.rect, rects[x])
            get_text_box(x.attack, 50, (x.position[0] + 15, x.position[1] - 20), RED, horiboxscale=float(0.7),
                         vertboxscale=float(0.5))  # width then height
            get_text_box(x.health, 50, (x.position[0] + 70, x.position[1] - 20), BLUE, horiboxscale=float(0.7),
                         vertboxscale=float(0.5))  # width then height
    for x in gameunits.OpponentUnitList:
        if x.position is not None:
            rects[x] = pygame.Rect((x.position), (small_icon))  # location, size
            screen.blit(x.rect, rects[x])
            get_text_box((x.attack), 50, (x.position[0] + 15, x.position[1] - 20), RED, horiboxscale=float(0.7),
                         vertboxscale=float(0.5))
            get_text_box((x.health), 50, (x.position[0] + 70, x.position[1] - 20), BLUE, horiboxscale=float(0.7),
                         vertboxscale=float(0.5))  # width then height
    return rects


def tree_building_rects_and_images():
    draw_background(treebuildingscene)
    rects = {}
    rects['fightbutton'] = draw_fight_button()
    rects['backbutton'] = draw_back_button()

    draw_battle_positions(rects)
    get_text_box(GameData.combatlog, 40,
                 (WINDOW_WIDTH / 2, WINDOW_HEIGHT * 0.2),
                 RED)
    return rects


def continueCombat(): # high level combat flow

    if GameData.combatphase == 0: #initially will be 0
        startofbattlephase() #runs below STOB phase
    if GameData.combatphase == 1:
        damagephase()
        GameData.combatphase -= 1


def startofbattlephase():

    if GameData.fcombatstep<=len(gameunits.FriendlyUnitList)-1: #from index 0-2 (1-3 in list)
        GameData.fcombatstep += 1
        indexfix = GameData.fcombatstep-1
        GameData.triggeredunit = gameunits.FriendlyUnitList[indexfix].name
        if gameunits.FriendlyUnitList[indexfix].STOBabilitynull:
            GameData.fcombatstep += len(gameunits.FriendlyUnitList)
            GameData.combatphase += 1
        else:
            gameunits.FriendlyUnitList[indexfix].unit_abilities()

    elif GameData.ecombatstep<=len(gameunits.OpponentUnitList)-1: #currently iterates through empty list
        GameData.combatlog = ''
        GameData.ecombatstep += 1
        indexfix = GameData.ecombatstep - 1
        GameData.triggeredunit = gameunits.OpponentUnitList[indexfix].name
        if gameunits.OpponentUnitList[indexfix].STOBabilitynull:
            GameData.ecombatstep += len(gameunits.OpponentUnitList)
            GameData.combatphase += 1
        else:
            gameunits.OpponentUnitList[indexfix].unit_abilities()

    else:
        GameData.combatphase += 1
        GameData.combatlog = ''

def damagephase():

    if gameunits.OpponentUnitList[0].health > 0:
        gameunits.OpponentUnitList[0].health -= gameunits.FriendlyUnitList[0].attack
    if gameunits.FriendlyUnitList[0].health > 0:
        gameunits.FriendlyUnitList[0].health -= gameunits.OpponentUnitList[0].attack

    if gameunits.OpponentUnitList[0].health <= 0:
        gameunits.OpponentUnitList.pop(0)  # remove from list
    if gameunits.FriendlyUnitList[0].health <= 0:
        gameunits.FriendlyUnitList.pop(0)  # remove from list
    # else:
    #     GameData.fightActive=False