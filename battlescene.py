from images import *
from config import *

def tree_building_rects_and_images(self):
    self.draw_background(treebuildingscene)
    rects = {}
    rects['backbutton'] = self.draw_back_button()
    rects['fightbutton'] = self.draw_fight_button()

    if self.player1health > 0:
        rects['Robot_Companion'] = pygame.Rect((WINDOW_WIDTH * 0.33, WINDOW_HEIGHT * 0.54),
                                               (medium_icon))  # location, size
        self.screen.blit(ShopRobotMiner_icon, rects['Robot_Companion'])
        self.get_text_box((self.player1health), 50,
                          (WINDOW_WIDTH * 0.4, WINDOW_HEIGHT * (0.48)),
                          RED)
    if self.player2health > 0:
        rects['small_basic_demon'] = pygame.Rect((WINDOW_WIDTH * 0.53, WINDOW_HEIGHT * 0.54),
                                                 (medium_icon))  # location, size
        self.screen.blit(SmallBasicDemon_icon, rects['small_basic_demon'])
        self.get_text_box((self.player2health), 50,
                          (WINDOW_WIDTH * 0.6, WINDOW_HEIGHT * (0.48)),
                          RED)

    if self.player1health <= 0 or self.player2health <= 0:
        if self.player1health <= 0:
            self.get_text_box((self.player1name + ' has died!'), 50,
                              (WINDOW_WIDTH * 0.22, WINDOW_HEIGHT * (0.48)),
                              OPAQUERED)

        if self.player2health <= 0:
            self.get_text_box((self.player2name + ' has died!'), 50,
                              (WINDOW_WIDTH * 0.66, WINDOW_HEIGHT * 0.48),
                              OPAQUERED)
        self.fightActive = False
    else:
        self.fightActive = True
    return rects


def tree_building_events(self, rects):  # treat this as a combat function
    if rects['fightbutton'].collidepoint(self.event.pos):
        if self.fightActive:
            self.basicattackPhase()
    if rects['backbutton'].collidepoint(self.event.pos):
        self.state = 'TOWN'