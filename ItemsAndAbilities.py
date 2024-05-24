from gamedata import *
from combatdata import *

# def basicrobotability():
#     GameData.triggeredunit.dealsdamage = True
#     gameunits.OpponentUnitList[0].takesdamage = True
#     gameunits.OpponentUnitList[0].health -= 1
#     GameData.combatlog = ''
#     GameData.combatlog2 = ''
#     GameData.combatlog=('Start of Battle: ' + str(GameData.triggeredunit.name) + ' dealt 1 damage to '+gameunits.OpponentUnitList[0].name)
#
# def nukeability(): #have abilities be functions like this, named something specific?
#     GameData.triggeredunit.dealsdamage = True #triggers go first, as units will depop after effects. could make fainting tricky
#     gameunits.OpponentUnitList[0].takesdamage = True
#     gameunits.OpponentUnitList[-1].health -= 5
#     GameData.combatlog = ''
#     GameData.combatlog2 = ''
#     GameData.combatlog=('Damaged Reaction: ' + str(GameData.triggeredunit.name) + ' dealt 5 damage to '+gameunits.OpponentUnitList[-1].name)

class Item:
    def __init__(self, health, attack, gearability=None):
        self.health = health
        self.attack = attack
        self.gearability = gearability

GoblinBossChestArmor = Item(0,0)
# GoblinBossChestArmor = Item(0,0, nukeability)