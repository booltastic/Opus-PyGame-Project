import pygame
import os
import sys
import random
#from intro_scene import *
from images import *

# Initialize Pygame
pygame.init()
pygame.mixer.init()

#You are hired to mine this mysterious shard. There's some sort of value you're unaware of. You get better, and start to
# recruit your own miners. Over time, the mine depletes. But you can venture further...

class systemhandler:
    def __init__(self):

        # Set up the display
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Practice Clicker Game")
        self.clock = pygame.time.Clock()
        self.FPS = 30
        self.timecounter = 0
        self.counter = 0  # play time
        self.thirdFPS = 0
        self.timer = 0
        self.stimer = 0
        self.saveprogress = True
        self.gamesavesuccessful = False
        # Set Colors
        self.CLEAR = pygame.Color(0, 0, 0, 0)
        self.WHITE = pygame.Color(255, 255, 255)
        self.BLACK = pygame.Color(0, 0, 0)
        self.OPAQUEBLACK = pygame.Color(0,0,0,140)
        self.RED = pygame.Color(255, 0, 0)
        self.OPAQUERED = pygame.Color(255,0,0,160)
        self.GREEN = pygame.Color(0, 255, 0)
        self.BLUE = pygame.Color(0, 0, 255)
        self.LIBLUE = pygame.Color(0, 128, 255)

        # Global Variables
        self.titlestring = 'The Clicker Game'
        self.state = 'INTRO'
        self.laststate = 'INTRO'
        self.promptnumber = 0

        self.shard = 0
        self.totalmined = 0
        self.sshard = 0
        self.mouseclick = 0
        self.minerstr = 1
        self.minerstrcost = 0
        self.str_up = 0
        self.strength = 1
        self.good_click = 0
        self.sshard_found = 0
        self.workercost = 0
        self.workers = 0
        self.worker_hired = 0
        self.workerlimit = 10

        # Player Inventory
        player_inventory = []
        self.player1name = 'Robot Boy'
        self.player1health = 10
        self.player1attack = 3

        self.player2name = 'Demgob'
        self.player2health = 12
        self.player2attack = 2

        # self.mini_icon = (WINDOW_HEIGHT*0.1,WINDOW_HEIGHT*0.1)
        # small_icon = (WINDOW_HEIGHT*0.15,WINDOW_HEIGHT*0.15)
        # medium_icon = (WINDOW_HEIGHT*0.2,WINDOW_HEIGHT*0.2)
        # large_icon = ((WINDOW_HEIGHT*0.5,WINDOW_HEIGHT*0.5))

        self.mouse_clicked = pygame.mouse.get_pressed()[0]  # check once for happy mouse status function
        self.mouse_pos = pygame.mouse.get_pos()

        self.play_game()

    def get_mouse_status(self):
        self.mouse_clicked = pygame.mouse.get_pressed()[0] #continuously is checking each frame
        self.mouse_pos = pygame.mouse.get_pos()

    def darken_on_click(self, rect, icon, darkenedicon):
        if self.mouse_clicked and rect.collidepoint(self.mouse_pos):
            self.screen.blit(darkenedicon, rect)
        else:
            self.screen.blit(icon, rect)

    def game_timer(self, ):
        self.counter += 1

    # Drawing scene backgrounds
    def draw_background(self, locationimage):
        background_image = pygame.transform.scale(locationimage, (WINDOW_HEIGHT, WINDOW_HEIGHT))
        background_rect = background_image.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.screen.blit(background_image, background_rect)

    #Draw settings icon
    def draw_settings_icon(self):
        if self.counter>60:
            settings_rect = settings_icon.get_rect(center=(WINDOW_WIDTH * 0.937, WINDOW_HEIGHT * 0.065))
            self.screen.blit(settings_icon, settings_rect)
            return settings_rect

    # Next Button
    def draw_button(self, buttontext):
        text_font = pygame.font.Font(None, int(40*fontscale))
        buttonstring = text_font.render(str(buttontext), True, self.WHITE)  # rendering text as object/image
        button_rect = buttonstring.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT*0.92))  # gets rect of the text shape, placed at a location
        button_rect = button_rect.inflate(button_rect.width * 1.2,button_rect.height * 1.2)  # inflated to clickable size
        buttontextspot = buttonstring.get_rect(center=button_rect.center)
        pygame.draw.rect(self.screen, self.BLUE, button_rect)  # draw rect
        self.screen.blit(buttonstring, buttontextspot)  # draw next text
        return button_rect

    def draw_next_button(self):
        button_rect=self.draw_button('Next')
        return button_rect

    def draw_fight_button(self):
        button_rect=self.draw_button('Fight')
        return button_rect

    def draw_back_button(self):
        button_rect=self.draw_button('Back')
        return button_rect

    # Drawing location icons
    def draw_location_icon(self, locationiconimage):
        icon_rect = pygame.Rect((WINDOW_WIDTH*0.8822, WINDOW_HEIGHT*0.843), (small_icon))  # location, size
        return_icon_image = pygame.transform.scale(locationiconimage, (small_icon))
        self.screen.blit(return_icon_image, icon_rect)
        return icon_rect

    def draw_speaker_icon(self, speakerimage):
        speaker_rect = pygame.Rect((WINDOW_WIDTH * 0.22, WINDOW_HEIGHT * 0.68),
                                    (small_icon))  # location, size
        speaker_icon_image = pygame.transform.scale(speakerimage, (small_icon))
        self.screen.blit(speaker_icon_image, speaker_rect)

    def draw_packpack_icon(self):
        if self.state not in ('INTRO', 'SETTINGS', 'LOADGAME'):
            backpack_rect = pygame.Rect((WINDOW_WIDTH * 0.006, WINDOW_HEIGHT * 0.68),(small_icon))  # location, size
            backpack_icon_image = pygame.transform.scale(backpack_icon, (small_icon))
            self.screen.blit(backpack_icon_image, backpack_rect)
            return backpack_rect

    def draw_stats_icon(self):
        if self.state not in ('INTRO', 'SETTINGS', 'LOADGAME'):
            statistics_rect = pygame.Rect((WINDOW_WIDTH * 0.006, WINDOW_HEIGHT * 0.84),
                                    (small_icon))  # location, size
            statistics_icon_image = pygame.transform.scale(stats_icon, (small_icon))
            self.screen.blit(statistics_icon_image, statistics_rect)
            return statistics_rect

    # Make shard
    def make_click_shard(self):
        self.shard += (self.minerstr / 2)
        self.totalmined += (self.minerstr / 2)
        sshard_chance = random.randint(1, 300)
        if sshard_chance >= (50 - self.minerstr):
            self.sshard_found = 1
            if self.minerstr < 10:
                self.sshard += 1
            if self.minerstr >= 15:
                self.sshard += 2

    def auto_miners(self):
        if self.workers >= 1:
            self.shard += self.workers / 60
            self.totalmined += self.workers / 60
            sshard_chance = random.randint(1, 3000)
            if sshard_chance >= (3000 - (self.workers)):
                self.sshard += 1

    def get_cost(self):
        cost_texts = {}
        #self.minerstrcost = int(self.minerstr * 25)
        self.minerstrcost = int(25 * (2**(1/5))**(self.minerstr-1))
        #self.workercost = int(self.workers * 1.75) + 5
        self.workercost = int(5*(5**(1/3))**(self.workers-1))
        cost_texts['str_upgrade_text'] = ['Mining Strength +1!', 'Not enough Shards!']
        cost_texts['worker_hired_text'] = ['New worker recruited!',
                                           'Not enough Special Shards!', 'Worker limit reached (Current limit '+str(self.workerlimit) + ')']
        return cost_texts

    def draw_inventory(self):
        shard_string = 'Shards: ' + str(int(self.shard))
        self.get_text_box(shard_string, 35, (WINDOW_WIDTH*0.5, WINDOW_HEIGHT*0.5), self.BLACK, 'center',1)

        # Special Shards
        sshard_string = 'Special Shards: ' + str(int(self.sshard))
        self.get_text_box(sshard_string, 35, (WINDOW_WIDTH*0.5, WINDOW_HEIGHT*0.6), self.BLACK, 'center',1)

    def draw_statistics(self):
        #Shards
        totalmined_string = 'Total Shards Mined: ' + str(int(self.totalmined))
        self.get_text_box(totalmined_string, 35, (WINDOW_WIDTH*0.5, WINDOW_HEIGHT*0.4), self.BLACK, 'center', 1)

        # # Workers
        worker_string = 'Workers: ' + str(int(self.workers))
        self.get_text_box(worker_string, 35, (WINDOW_WIDTH*0.5, WINDOW_HEIGHT*0.5), self.BLACK, 'center',1)
        #
        # # Mining Strength
        minestr_string = 'Mining Strength: ' + str(int(self.minerstr))
        self.get_text_box(minestr_string, 35, (WINDOW_WIDTH*0.5, WINDOW_HEIGHT*0.6), self.BLACK, 'center',1)

    def draw_mainclicktarget(self):
        #self.get_mouse_status()
        timer = int(self.counter/3)
        for i in range(0,1):
            if timer % 3 == i:
                glowing_background_rect = background_glow_icon1.get_rect(center=screen_center)
                self.screen.blit(background_glow_icon1, glowing_background_rect)
        for i in range(1,2):
            if timer % 3 == i:
                glowing_background_rect = background_glow_icon2.get_rect(center=screen_center)
                self.screen.blit(background_glow_icon2, glowing_background_rect)
        for i in range(2,3):
            if timer % 3 == i:
                glowing_background_rect = background_glow_icon3.get_rect(center=screen_center)
                self.screen.blit(background_glow_icon3, glowing_background_rect)

        glowingrockicon_rect = glowingrockicon.get_rect(center=screen_center)
        self.darken_on_click(glowingrockicon_rect, glowingrockicon, glowingrockicon2)

        return glowingrockicon_rect

    def get_text_box(self, drawntext, fontsize, textlocation, color, alignment='center',vertboxscale=float(1), horiboxscale=float(0.15)):  # made for rects loops
        boxtext = drawntext
        boxtextfont = pygame.font.Font(None, int(fontsize*(fontscale)))
        renderedtext = boxtextfont.render(str(boxtext), True, self.WHITE)  # renders text image
        if alignment == 'left':
            colliderect = renderedtext.get_rect(
                midleft=textlocation)  # create rect the size of the text at chosen location. sets ratio of size, and where we want the center
        else:
            colliderect = renderedtext.get_rect(
                center=textlocation)
        colliderect = colliderect.inflate(colliderect.width*horiboxscale,
                                          colliderect.height*vertboxscale)  # inflate that rect in place to twice its size, this is what gets clicked
        # pygame.draw.rect(self.screen, color,
        #                  colliderect)  # draws the rect renderedrect, this cannot be passed to collidepoint though (just drawing it)
        renderedtextrect = renderedtext.get_rect(
            center=colliderect.center)  # this rect is creating a text sized rect and placing it at the center of the big rect, so its already centered.
        surface=pygame.Surface(colliderect.size,pygame.SRCALPHA)
        pygame.draw.rect(surface, color,
                         surface.get_rect())
        self.screen.blit(surface,colliderect)
        self.screen.blit(renderedtext, renderedtextrect)
        return colliderect  # if applicable. only used if you need to click it

    ### SCENES ###
    def change_state(self, new_state):
        if self.state not in ('LOADGAME','SETTINGS','BACKPACK','STATISTICS'):
            self.laststate = self.state
        self.state = new_state

    def draw_scene(self, sceneinput):  # argument passed through is State
        if sceneinput == 'INTRO':
            return self.intro_rects_and_images()  # these return rect dicts where each item should be a rect. draw_scene is equal to versatile rects now
        if sceneinput == 'LOADGAME':
            return self.loadgame_rects_and_images()
        if sceneinput == 'SETTINGS':
            return self.settings_page()
        if sceneinput == 'TUTORIAL':
            return self.tutorial_rects_and_images()
        if sceneinput == 'MINELEVEL1':
            return self.mine_level_1_rects_and_images()
        if sceneinput == 'TOWN':
            return self.town_rects_and_images()
        if sceneinput == 'MINERSGUILD':
            return self.miners_guild_rects_and_images()
        if sceneinput == 'BACKPACK':
            return self.backpack_rects_and_images()
        if sceneinput == 'STATISTICS':
            return self.statistics_rects_and_images()
        if sceneinput == 'TREEBUILDING':
            return self.tree_building_rects_and_images()

    def intro_rects_and_images(self):
        rects = {}
        introstring = 'Welcome to Mine.Cafe!'
        newgametext = ['New Game', 'Load Game']
        timer = int(self.counter)
        background_image = pygame.transform.scale(introimage, (WINDOW_HEIGHT, WINDOW_HEIGHT))
        if timer < 60:
            HEIGHT = WINDOW_HEIGHT*(1.5-(timer/60)) #blit exactly off screen. at 0.5, it will be centered. want it to take 60 frames.
        else:
            HEIGHT = WINDOW_HEIGHT/2
        background_rect = background_image.get_rect(center=(WINDOW_WIDTH / 2, HEIGHT))
        self.screen.blit(background_image, background_rect)
        if timer > 60:
            self.get_text_box(introstring,50,(WINDOW_WIDTH/2, WINDOW_HEIGHT*0.23), self.OPAQUERED)
            rects['new_game_rect'] = self.get_text_box(newgametext[0], 50, (WINDOW_WIDTH*0.35, WINDOW_HEIGHT*0.53), self.BLUE)
            rects['load_game_rect'] = self.get_text_box(newgametext[1], 50, (WINDOW_WIDTH*0.65, WINDOW_HEIGHT*0.53), self.BLUE)
        return rects

    def intro_events(self, rects):
        if self.counter>60:
            if rects['new_game_rect'].collidepoint(self.event.pos):
                self.change_state('TUTORIAL')
            if rects['load_game_rect'].collidepoint(self.event.pos):
                self.change_state('LOADGAME')

    def statistics_rects_and_images(self):
        rects = {}
        self.draw_background(stats_page_image)
        self.draw_statistics()
        rects['back_button']=self.draw_back_button()
        return rects

    def statistics_events(self, rects):
        if rects['back_button'].collidepoint(self.event.pos):
            self.state=self.laststate

    def backpack_rects_and_images(self):
        rects = {}
        self.draw_background(backpackscreenimage)
        self.draw_inventory()
        rects['back_button'] = self.draw_back_button()
        return rects

    def backpack_events(self, rects):
        if rects['back_button'].collidepoint(self.event.pos):
            self.state=self.laststate

    def settings_page(self):
        self.draw_background(loadgamescreenimage)
        rects={}
        if self.laststate != 'INTRO':
            rects['save_game_rect']=self.get_text_box('Save Game', 40,
                         (WINDOW_WIDTH / 2, WINDOW_HEIGHT * 0.3),
                         self.OPAQUERED)
            rects['load_game_rect']=self.get_text_box('Load Game', 40,
                         (WINDOW_WIDTH / 2, WINDOW_HEIGHT * 0.5),
                         self.OPAQUERED)
            if self.saveprogress == False:
                self.get_text_box('Brooo cmon you just started XD', 40,
                             (WINDOW_WIDTH / 2, WINDOW_HEIGHT * 0.8),
                             self.OPAQUERED)
                self.gamesavesuccessful = False
            if self.gamesavesuccessful == True:
                self.get_text_box('Game saved successfully', 40,
                             (WINDOW_WIDTH / 2, WINDOW_HEIGHT * 0.8),
                             self.OPAQUERED)
                self.saveprogress = True
        if self.laststate == 'INTRO':
            self.get_text_box('(more settings will eventually live here)', 40,
                         (WINDOW_WIDTH / 2, WINDOW_HEIGHT * 0.5),
                         self.OPAQUERED)
        rects['back_button'] = self.draw_back_button()
        return rects

    def settings_page_events(self, rects):
        if self.laststate != 'INTRO':
            if rects['load_game_rect'].collidepoint(self.event.pos):
                self.saveprogress = True
                self.gamesavesuccessful = False
                self.change_state('LOADGAME')
            if rects['save_game_rect'].collidepoint(self.event.pos):
                savestatelist = self.totalmined, self.shard, self.sshard, self.workers, self.minerstr
                if savestatelist == (0, 0, 0, 0, 1):
                    self.saveprogress = False
                else:
                    with open('Saved Game.txt', 'w') as file:
                        file.write(str(savestatelist))
                    self.gamesavesuccessful = True
        if rects['back_button'].collidepoint(self.event.pos):
            self.saveprogress = True
            self.gamesavesuccessful = False
            if self.laststate == 'INTRO':
                self.state = 'INTRO'
            else:
                self.state=self.laststate

    def loadgame_rects_and_images(self):
        self.draw_background(loadgamescreenimage)
        rects={}
        rects['back_button'] = self.draw_back_button()
        files_with_string = []
        for file in os.listdir():
            if 'Saved Game' in file or 'Autosaved Game' in file:  # Check if the file is a text file
                files_with_string.append(file)
        numberoffiles = len(files_with_string)
        if numberoffiles>0:
            for savefile in files_with_string:
                rects[savefile]=self.get_text_box(savefile.split('.txt')[0], 40, (WINDOW_WIDTH / 2, WINDOW_HEIGHT * (0.3+(int(files_with_string.index(savefile))*0.2))),
                     self.OPAQUERED)
        else:
            self.get_text_box('No save files found!', 40,
                         (WINDOW_WIDTH / 2, WINDOW_HEIGHT * 0.3),
                          self.OPAQUERED)
        return rects

    def loadgame_events(self, rects):
        for file in rects:
            if rects[file].collidepoint(self.event.pos) and 'back_button' not in file:
                with open(file, 'r') as savefile:
                    content = savefile.read().split('(')[1]
                    content = content.split(')')[0]
                    content = content.split(', ')
                    if len(content) == 0:
                        pass
                    self.totalmined, self.shard, self.sshard, self.workers, self.minerstr = float(content[0]), float(content[1]), float(
                        content[2]), float(
                        content[3]), float(content[4])
                    self.change_state('TOWN')
        if rects['back_button'].collidepoint(self.event.pos):
            self.saveprogress = True
            self.gamesavesuccessful = False
            if self.laststate == 'INTRO':
                self.state = 'INTRO'
            else:
                self.state = 'SETTINGS'


    def tutorial_rects_and_images(self):  # where basically everything is drawn and established
        self.tuttext = ['Welcome to the Mines of Esswun, kid!', 'We need you to mine these blue shards.',
                   "Don't ask questions. Just mine!",
                   'Click on that glowing rock over there to mine it!',
                   'Your shards and other loot will be stored in this bag', 'You can see your stats here',
                   "When you're done for the day, return to town here",
                   'Now get mining! We need those shards!']
        rects = {}
        self.draw_background(level1minesceneimage)
        self.draw_mainclicktarget()
        self.draw_location_icon(towniconimage)
        if self.promptnumber < len(self.tuttext):
            self.get_text_box(self.tuttext[self.promptnumber], 40, Text_Location_TalkCenter, self.OPAQUERED, horiboxscale=0.1, vertboxscale=3, alignment='left')
            self.draw_speaker_icon(robot_boss_image)
            if self.promptnumber == 4:
                backpack_rect = pygame.Rect((WINDOW_WIDTH * 0.006, WINDOW_HEIGHT * 0.63),
                                            (medium_icon))  # location, size
                backpack_icon_image = pygame.transform.scale(backpack_icon, (medium_icon))
                self.screen.blit(backpack_icon_image, backpack_rect)
            if self.promptnumber == 5:
                statistics_rect = pygame.Rect((WINDOW_WIDTH * 0.006, WINDOW_HEIGHT * 0.79),
                                              (medium_icon))  # location, size
                statistics_icon_image = pygame.transform.scale(stats_icon, (medium_icon))
                self.screen.blit(statistics_icon_image, statistics_rect)
            if self.promptnumber == 6:
                icon_rect = pygame.Rect((WINDOW_WIDTH * 0.845, WINDOW_HEIGHT * 0.795),
                                        (medium_icon))  # location, size
                return_icon_image = pygame.transform.scale(towniconimage, (medium_icon))
                self.screen.blit(return_icon_image, icon_rect)
        rects['next_button'] = self.draw_next_button()
        return rects

    def tutorial_events(self, rects):
        if rects['next_button'].collidepoint(self.event.pos):
            self.increment_number()
            if self.promptnumber >= len(self.tuttext):
                self.change_state('MINELEVEL1')

    def mine_level_1_rects_and_images(self):
        rects = {}
        self.draw_background(level1minesceneimage)
        rects['mainclicktarget'] = self.draw_mainclicktarget()
        rects['corner_location_icon'] = self.draw_location_icon(towniconimage)
        if self.good_click == 1:
            self.timer += 1
            self.get_text_box('Mined some shards!', 30,
                         (WINDOW_WIDTH * 0.5, WINDOW_HEIGHT * (0.4-(0.15*(self.timer/60)))), self.OPAQUERED)
            if self.timer >= 60:
                self.timer = 0
                self.good_click = 0
        if self.sshard_found == 1:
            self.stimer += 1
            self.get_text_box('Found a special shard!', 30,
                         (WINDOW_WIDTH * 0.5, WINDOW_HEIGHT * (0.4-(0.15*(self.stimer/60)))), self.OPAQUERED)
            if self.stimer >= 60:
                self.stimer = 0
                self.sshard_found = 0
        return rects

    def mine_level_1_events(self, rects):
        if rects['corner_location_icon'].collidepoint(self.event.pos):
            self.good_click = 0
            self.sshard_found = 0
            self.change_state('TOWN')
        if rects['mainclicktarget'].collidepoint(self.event.pos):
            self.timer = 0
            self.good_click = 1
            self.make_click_shard()

    def town_rects_and_images(self):
        rects = {}
        self.draw_background(quainttownimage)
        rects['minersguild_rect'] = pygame.Rect((WINDOW_WIDTH*0.59, WINDOW_HEIGHT*0.34),
                                                (medium_icon))  # location, size
        self.screen.blit(minersguildicon, rects['minersguild_rect'])

        rects['level1mine_rect'] = pygame.Rect((WINDOW_WIDTH*0.43, WINDOW_HEIGHT*0.65),
                                                (medium_icon))  # location, size
        self.screen.blit(level1minesceneimageicon, rects['level1mine_rect'])

        rects['treebuilding_rect'] = pygame.Rect((WINDOW_WIDTH*0.266, WINDOW_HEIGHT*0.34),
                                                (medium_icon))  # location, size
        self.screen.blit(treebuildingicon, rects['treebuilding_rect'])

        town_text = ['Back to the mines',"Miner's Guild", 'Strange Tree Building']
        self.get_text_box(town_text[0], 30,
                     (WINDOW_WIDTH * 0.5, WINDOW_HEIGHT * 0.89), self.OPAQUERED)
        self.get_text_box(town_text[1], 30,
                     (WINDOW_WIDTH * 0.66, WINDOW_HEIGHT * 0.58), self.OPAQUERED)
        self.get_text_box(town_text[2], 30,
                     (WINDOW_WIDTH * 0.34, WINDOW_HEIGHT * 0.58), self.OPAQUERED)
        return rects

    def town_events(self, rects):
        if rects['level1mine_rect'].collidepoint(self.event.pos):
            self.change_state('MINELEVEL1')
        if rects['minersguild_rect'].collidepoint(self.event.pos):
            self.change_state('MINERSGUILD')
        if rects['treebuilding_rect'].collidepoint(self.event.pos):
            self.change_state('TREEBUILDING')

    def tree_building_rects_and_images(self):
        self.draw_background(treebuildingscene)
        rects = {}

        rects['fightbutton']=self.draw_fight_button()
        if self.player1health > 0:
            rects['Robot_Companion'] = pygame.Rect((WINDOW_WIDTH*0.33, WINDOW_HEIGHT*0.54),
                                                    (medium_icon))  # location, size
            self.screen.blit(ShopRobotMiner_icon, rects['Robot_Companion'])
            self.get_text_box((self.player1health), 50,
                         (WINDOW_WIDTH * 0.4, WINDOW_HEIGHT * (0.48)),
                         self.RED)
        if self.player2health > 0:
            rects['small_basic_demon'] = pygame.Rect((WINDOW_WIDTH*0.53, WINDOW_HEIGHT*0.54),
                                                    (medium_icon))  # location, size
            self.screen.blit(SmallBasicDemon_icon, rects['small_basic_demon'])
            self.get_text_box((self.player2health), 50,
                         (WINDOW_WIDTH * 0.6, WINDOW_HEIGHT * (0.48)),
                         self.RED)

        if self.player1health <= 0 or self.player2health <= 0:
            if self.player1health <= 0:
                self.get_text_box((self.player1name + ' has died!'), 50,
                             (WINDOW_WIDTH * 0.22, WINDOW_HEIGHT * (0.48)),
                             self.OPAQUERED)

            if self.player2health <= 0:
                self.get_text_box((self.player2name + ' has died!'), 50,
                             (WINDOW_WIDTH * 0.66, WINDOW_HEIGHT * 0.48),
                             self.OPAQUERED)
            self.fightActive = False
        else:
            self.fightActive = True
        return rects

    def tree_building_events(self, rects): #treat this as a combat function
        if rects['fightbutton'].collidepoint(self.event.pos):
            if self.fightActive:
                self.basicattackPhase()

    def basicattackPhase(self):
        self.player1health -= self.player2attack
        self.player2health -= self.player1attack

    def miners_guild_rects_and_images(self):
        self.mouse_clicked = pygame.mouse.get_pressed()[0] #continuously is checking each frame
        self.mouse_pos = pygame.mouse.get_pos()
        rects = {}
        cost_texts = self.get_cost()  # just running get_cost and reading values
        self.draw_background(minersguildimage)

        #Rects
        rects['corner_location_icon'] = self.draw_location_icon(towniconimage)
        rects['ShopRobotMiner_rect'] = pygame.Rect((WINDOW_WIDTH*0.2, WINDOW_HEIGHT*0.3),
                                                medium_icon)
        rects['str_up_rect'] = pygame.Rect((WINDOW_WIDTH*0.435, WINDOW_HEIGHT*0.3), medium_icon)  # location, size
        rects['hire_worker_rect'] = pygame.Rect((WINDOW_WIDTH*0.68, WINDOW_HEIGHT*0.3),
                                                medium_icon)  # location, size
        #Text
        minerswelcome = ['Welcome to the Miner\'s Guild!', 'Spend your shards to upgrade your mining skill']
        descripts = ['Cute little robot guy','Increase amount of shards mined per click (Costs '+ str(self.minerstrcost)+' Shards)','Hire worker for passive Shard mining (Costs '+str(self.workercost)+' Special Shards)']
        self.get_text_box(minerswelcome[0], 30, (WINDOW_WIDTH*0.5,WINDOW_HEIGHT*0.635), self.OPAQUERED, horiboxscale=0.09)
        self.get_text_box(minerswelcome[1], 30, (WINDOW_WIDTH*0.5,WINDOW_HEIGHT*0.72), self.OPAQUERED, horiboxscale=0.09)
        if rects['ShopRobotMiner_rect'].collidepoint(self.mouse_pos):
            self.get_text_box(descripts[0], 30, (WINDOW_WIDTH * 0.5, WINDOW_HEIGHT * 0.55),
                     self.OPAQUERED, horiboxscale=0.09)
        if rects['str_up_rect'].collidepoint(self.mouse_pos):
            self.get_text_box(descripts[1], 30, (WINDOW_WIDTH * 0.5, WINDOW_HEIGHT * 0.55),
                         self.OPAQUERED, horiboxscale=0.09)
        if rects['hire_worker_rect'].collidepoint(self.mouse_pos):
            self.get_text_box(descripts[2], 30, (WINDOW_WIDTH * 0.5, WINDOW_HEIGHT * 0.55),
                         self.OPAQUERED, horiboxscale=0.09)

        #Blits
        self.darken_on_click(rects['str_up_rect'], strength_up_icon, darkenedstrength_up_icon)
        self.darken_on_click(rects['hire_worker_rect'], hire_worker_icon, darkenedhire_worker_icon)
        self.darken_on_click(rects['ShopRobotMiner_rect'], ShopRobotMiner_icon, DarkenedShopRobotMiner_icon)

        if self.str_up == 1:
            self.get_text_box(cost_texts['str_upgrade_text'][0], 30, (WINDOW_WIDTH*0.5,WINDOW_HEIGHT*0.25), self.OPAQUERED)
            self.timer += 1
            self.worker_hired = 0
            if self.timer >= 90:
                self.str_up, self.timer = 0, 0
        elif self.str_up == 2:
            self.get_text_box(cost_texts['str_upgrade_text'][1], 30, (WINDOW_WIDTH*0.5,WINDOW_HEIGHT*0.25), self.OPAQUERED)
            self.timer += 1
            if self.timer >= 90:
                self.str_up, self.timer = 0, 0
        if self.worker_hired == 1:
            self.get_text_box(cost_texts['worker_hired_text'][0], 30, (WINDOW_WIDTH*0.5,WINDOW_HEIGHT*0.25), self.OPAQUERED)
            self.timer += 1
            self.str_up = 0
            if self.timer >= 90:
                self.worker_hired, self.timer = 0, 0
        elif self.worker_hired == 2:
            self.get_text_box(cost_texts['worker_hired_text'][1], 30, (WINDOW_WIDTH*0.5,WINDOW_HEIGHT*0.25), self.OPAQUERED)
            self.timer += 1
            self.str_up = 0
            if self.timer >= 90:
                self.worker_hired, self.timer = 0, 0
        elif self.worker_hired == 3:
            self.get_text_box(cost_texts['worker_hired_text'][2], 30,
                         (WINDOW_WIDTH * 0.5, WINDOW_HEIGHT * 0.25), self.OPAQUERED)
            self.timer += 1
            self.str_up = 0
            if self.timer >= 90:
                self.worker_hired, self.timer = 0, 0
        return rects

    def miners_guild_events(self, rects):
        if rects['str_up_rect'].collidepoint(self.event.pos):
            self.timer = 0
            self.worker_hired = 0
            if self.shard >= self.minerstrcost:
                self.shard -= self.minerstrcost
                self.minerstr += 1
                self.str_up = 1  # (1 for yes, generate success text)
            else:
                self.str_up = 2  # (2 for no)

        if rects['hire_worker_rect'].collidepoint(self.event.pos):
            self.timer = 0
            self.str_up = 0
            if self.sshard >= self.workercost and self.workers<self.workerlimit:
                self.sshard -= self.workercost
                self.worker_hired = 1
                self.workers += 1
            elif self.sshard >= self.workercost and self.workers>=self.workerlimit: #notifys worker limit reached
                self.worker_hired = 3
            else:
                self.worker_hired = 2
        if rects['corner_location_icon'].collidepoint(self.event.pos):
            self.change_state('TOWN')
            self.str_up = 0
            self.worker_hired = 0

    def increment_number(self):
        self.promptnumber += 1

    # Game loop
    def play_game(self):
        running = True
        while running:
            # Clear the screen
            self.screen.fill(self.BLACK)  # Passively fills all blank space
            # Event handling
            self.game_timer()  # total frame number
            self.auto_miners()
            self.backpack_rect = self.draw_packpack_icon()
            self.statistics_rect = self.draw_stats_icon()
            self.settings_rect = self.draw_settings_icon()
            rects = self.draw_scene(self.state)

            for self.event in pygame.event.get():
                if self.event.type == pygame.QUIT:  # should be the only IF, so the game will always close first. i think
                    with open('Autosaved Game.txt', 'w') as file:
                        savestatelist = self.totalmined, self.shard, self.sshard, self.workers, self.minerstr
                        file.write(str(savestatelist))
                    running = False
                elif self.event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state == 'INTRO':
                        self.intro_events(rects)
                        if self.counter>60:
                            if self.settings_rect.collidepoint(self.event.pos):
                                self.change_state('SETTINGS')
                    elif self.settings_rect.collidepoint(self.event.pos):
                        self.change_state('SETTINGS')
                    elif self.state not in ('INTRO', 'SETTINGS', 'LOADGAME', 'TUTORIAL','BACKPACK') and self.backpack_rect.collidepoint(self.event.pos):
                        self.change_state('BACKPACK')
                    elif self.state not in ('INTRO', 'SETTINGS', 'LOADGAME', 'TUTORIAL','STATISTICS') and self.statistics_rect.collidepoint(self.event.pos):
                        self.change_state('STATISTICS')
                    elif self.state == 'BACKPACK' and self.backpack_rect.collidepoint(self.event.pos):
                        self.state=self.laststate
                    elif self.state == 'STATISTICS' and self.statistics_rect.collidepoint(self.event.pos):
                        self.state=self.laststate
                    elif self.state == 'LOADGAME':
                        self.loadgame_events(rects)
                    elif self.state == 'SETTINGS':
                        self.settings_page_events(rects)
                    elif self.state == 'STATISTICS':
                        self.statistics_events(rects)
                    elif self.state == 'BACKPACK':
                        self.backpack_events(rects)
                    elif self.state == 'TUTORIAL':
                        self.tutorial_events(rects)
                    elif self.state == 'TOWN':
                        self.town_events(rects)
                    elif self.state == 'MINELEVEL1':
                        self.mine_level_1_events(rects)
                    elif self.state == 'MINERSGUILD':
                        self.miners_guild_events(rects)
                    elif self.state == 'TREEBUILDING':
                        self.tree_building_events(rects)

            # Update the display
            pygame.display.flip()
            self.clock.tick(self.FPS)

playgame = systemhandler()

# Quit Pygame
# pygame.quit()
# sys.exit()