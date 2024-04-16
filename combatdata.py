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
        if self.unit == 'basicgob':
            self.rect = SmallBasicDemon_icon
        if self.unit == 'roboboss':
            self.rect = robot_boss_image
        if self.unit == 'robominer':
            self.rect = ShopRobotMiner_icon
        #self.unit_abilities()

    # def unit_abilities(self):
    #     self.ability_list = []
    #     if self.unit == 'basicgob':
    #         basicgobability()


class UnitLists:
    def __init__(self):
        self.FriendlyUnitList = []
        self.OpponentUnitList = []

gameunits = UnitLists()
fightActive = False

playerfighter1 = Fighter('Robot Boy1', 12, 3, True, 'robominer')
playerfighter2 = Fighter('Robot Boy2', 8, 2, True, 'robominer')
playerfighter3 = Fighter('Robot Boy3', 8, 2, True, 'robominer')
goblinenemy1 = Fighter('Spinny Gob1', 12, 2, False, 'roboboss')
goblinenemy2 = Fighter('Spinny Gob2', 8, 2, False, 'basicgob')
goblinenemy3 = Fighter('Spinny Gob3', 12, 2, False, 'roboboss')

gameunits.FriendlyUnitList = [playerfighter1, playerfighter2, playerfighter3]
gameunits.OpponentUnitList = [goblinenemy1, goblinenemy2, goblinenemy3]

def get_unit_positions():
    for x in gameunits.FriendlyUnitList:
        x.positionint = gameunits.FriendlyUnitList.index(x)
        #print(gameunits.FriendlyUnitList)
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
    return rects


def continueCombat(): # high level combat flow
    GameData.combatphase += 1
    if GameData.combatphase == 1: #initially will be 0
        startofbattlephase() #runs below STOB phase
    if GameData.combatphase == 2:
        damagephase()
        GameData.combatphase -= 1


def startofbattlephase():
    #print(GameData.combatphase)

    basicrobotability() #subtract 1 hp, no conditions
    basicrobotability()
    basicrobotability()
    # function to go through all STOB abilities

    # for x in gameunits.FriendlyUnitList:
    #     pass



def basicrobotability():
    gameunits.OpponentUnitList[0].health -= 1
    print(gameunits.FriendlyUnitList[0].name + ' dealt 1 damage to '+gameunits.OpponentUnitList[0].name)

def damagephase():
    if gameunits.OpponentUnitList[0].health > 0:
        gameunits.OpponentUnitList[0].health -= gameunits.FriendlyUnitList[0].attack
    if gameunits.OpponentUnitList[0].health <= 0:
        gameunits.OpponentUnitList.pop(0)  # remove from list
    if gameunits.FriendlyUnitList[0].health > 0:
        gameunits.FriendlyUnitList[0].health -= gameunits.OpponentUnitList[0].attack
    if gameunits.FriendlyUnitList[0].health <= 0:
        gameunits.FriendlyUnitList.pop(0)  # remove from list