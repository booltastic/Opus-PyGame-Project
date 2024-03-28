

class GameData:
    state = 'INTRO'
    laststate = 'INTRO'
    shard = 0
    totalmined = 0
    sshard = 0
    minerstr = 1
    workers = 0
    minerstrcost = 0
    workercost = 0
    fightActive = False
    counter = 0

class Fighter:
    def __init__(self, name,health,attack):
        self.name = name
        self.health = health
        self.attack = attack

mainplayer = Fighter('Robot Boy',10,3)
goblinenemy1 = Fighter('Spinny Gob', 12, 2)