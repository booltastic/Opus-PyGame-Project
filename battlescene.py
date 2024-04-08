from drawfunctions import *
from combatdata import *

def draw_battle_positions(rects):

    get_unit_positions()
    for x in gameunits.FriendlyUnitList:
        if x.position is not None:
            rects[x] = pygame.Rect((x.position), (small_icon))  # location, size
            screen.blit(x.rect, rects[x])
            get_text_box(x.attack, 50, (x.position[0]+15, x.position[1]-20), RED, horiboxscale=float(0.7),vertboxscale=float(0.5)) #width then height
            get_text_box(x.health, 50, (x.position[0] + 70, x.position[1] - 20), BLUE, horiboxscale=float(0.7),vertboxscale=float(0.5))  # width then height
    for x in gameunits.OpponentUnitList:
        if x.position is not None:
            rects[x] = pygame.Rect((x.position), (small_icon))  # location, size
            screen.blit(x.rect, rects[x])
            get_text_box((x.attack), 50, (x.position[0]+15, x.position[1]-20), RED, horiboxscale=float(0.7),vertboxscale=float(0.5))
            get_text_box((x.health), 50, (x.position[0] + 70, x.position[1] - 20), BLUE, horiboxscale=float(0.7),vertboxscale=float(0.5))  # width then height
    return rects

def tree_building_rects_and_images():
    draw_background(treebuildingscene)
    rects = {}
    rects['backbutton'] = draw_back_button()
    rects['fightbutton'] = draw_fight_button()

    draw_battle_positions(rects)

    return rects

def basicattackPhase():
    # if len(gameunits.OpponentUnitList) >= 1 or len(gameunits.FriendlyUnitList) >= 1:
    #     fightActive = True
    # else:
    #     fightActive = False
    if gameunits.OpponentUnitList[0].health > 0:
        gameunits.OpponentUnitList[0].health -= gameunits.FriendlyUnitList[0].attack
    if gameunits.OpponentUnitList[0].health <= 0:
        gameunits.OpponentUnitList.pop(0)
    if gameunits.FriendlyUnitList[0].health > 0:
        gameunits.FriendlyUnitList[0].health -= gameunits.OpponentUnitList[0].attack
    if gameunits.FriendlyUnitList[0].health <= 0:
        gameunits.FriendlyUnitList.pop(0)
        #OpponentUnitList[0]
    #print(OpponentUnitList[0].health)
    #print(OpponentUnitList[0].position)

    #goblinenemy1.health -= mainplayer.attack

