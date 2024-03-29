from images import *
from config import *
from drawfunctions import *
from gamedata import *

def tree_building_rects_and_images():
    draw_background(treebuildingscene)
    rects = {}
    rects['backbutton'] = draw_back_button()
    rects['fightbutton'] = draw_fight_button()
    fightphase = 1

    #Draw player first position
    if mainplayer.health > 0:
        rects['Robot_Companion'] = pygame.Rect((WINDOW_WIDTH * 0.33, WINDOW_HEIGHT * 0.54),
                                               (medium_icon))  # location, size
        screen.blit(ShopRobotMiner_icon, rects['Robot_Companion'])
        get_text_box((mainplayer.health), 50,
                          (WINDOW_WIDTH * 0.4, WINDOW_HEIGHT * (0.48)),
                          RED)

    #Draw enemy player first position
    if goblinenemy1.health > 0:
        rects['small_basic_demon'] = pygame.Rect((WINDOW_WIDTH * 0.53, WINDOW_HEIGHT * 0.54),
                                                 (medium_icon))  # location, size
        screen.blit(SmallBasicDemon_icon, rects['small_basic_demon'])
        get_text_box((goblinenemy1.health), 50,
                          (WINDOW_WIDTH * 0.6, WINDOW_HEIGHT * (0.48)),
                          RED)

    #Text that pops up when first position dies
    if mainplayer.health <= 0 or goblinenemy1.health <= 0:
        if mainplayer.health <= 0:
            get_text_box((mainplayer.name + ' has died!'), 50,
                              (WINDOW_WIDTH * 0.22, WINDOW_HEIGHT * (0.48)),
                              OPAQUERED)

        if goblinenemy1.health <= 0:
            get_text_box((goblinenemy1.name + ' has died!'), 50,
                              (WINDOW_WIDTH * 0.66, WINDOW_HEIGHT * 0.48),
                              OPAQUERED)
        GameData.fightActive = False
    else:
        GameData.fightActive = True
    return rects

round=0
def basicattackPhase():

    mainplayer.health -= goblinenemy1.attack
    goblinenemy1.health -= mainplayer.attack

