from config import *
#Unit Locations

#Combat Scene Unit Placement
#Friendly Side
position1 = WINDOW_WIDTH * 0.20, WINDOW_HEIGHT * 0.54
position2 = WINDOW_WIDTH * 0.26, WINDOW_HEIGHT * 0.54
position3 = WINDOW_WIDTH * 0.14, WINDOW_HEIGHT * 0.54
position4 = WINDOW_WIDTH * 0.26, WINDOW_HEIGHT * 0.54
position5 = WINDOW_WIDTH * 0.38, WINDOW_HEIGHT * 0.54

#Enemy Side
position6 = WINDOW_WIDTH * 0.52, WINDOW_HEIGHT * 0.54
position7 = WINDOW_WIDTH * 0.64, WINDOW_HEIGHT * 0.54
position8 = WINDOW_WIDTH * 0.76, WINDOW_HEIGHT * 0.54
position9 = WINDOW_WIDTH * 0.72, WINDOW_HEIGHT * 0.54
position10 = WINDOW_WIDTH * 0.78, WINDOW_HEIGHT * 0.54

class Fighter:
    #playerteam = []

    def __init__(self, name,health,attack, position):
        self.name = name
        self.health = health
        self.attack = attack
        self.position = position

playerfighter1 = Fighter('Robot Boy1',10,3, position5)
playerfighter2 = Fighter('Robot Boy2',8,2, position4)
playerfighter3 = Fighter('Robot Boy2',8,2, position3)
goblinenemy1 = Fighter('Spinny Gob1', 12, 2, position6)
goblinenemy2 = Fighter('Spinny Gob2', 12, 2, position7)
goblinenemy3 = Fighter('Spinny Gob2', 12, 2, position8)

FriendlyUnitList = [playerfighter1, playerfighter2]
OpponentUnitList = [goblinenemy1, goblinenemy2]