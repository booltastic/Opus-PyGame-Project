from images import *
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
        self.unit_abilities()

    def unit_abilities(self):
        self.ability_list = []
        if self.unit == 'basicgob':
            basicgobability()


def basicgobability():
    if combatphase == 1:
        gameunits.FriendlyUnitList[0].health -= 1

class UnitLists:
    def __init__(self):
        self.FriendlyUnitList = []
        self.OpponentUnitList = []

gameunits = UnitLists()
fightActive = False

playerfighter1 = Fighter('Robot Boy1', 12, 3, True, 'roboboss')
playerfighter2 = Fighter('Robot Boy2', 8, 2, True, 'robominer')
playerfighter3 = Fighter('Robot Boy3', 8, 2, True, 'basicgob')
goblinenemy1 = Fighter('Spinny Gob1', 12, 2, False, 'roboboss')
goblinenemy2 = Fighter('Spinny Gob2', 8, 2, False, 'basicgob')
goblinenemy3 = Fighter('Spinny Gob3', 12, 2, False, 'roboboss')
gameunits.FriendlyUnitList = [playerfighter1, playerfighter2]
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
