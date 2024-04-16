import os
import sys
import random
from battlescene import *
from gamedata import *
from config import *
from drawfunctions import *
from combatdata import *
import pygame

class SystemHandler:
    def __init__(self):
        #self.state = 'INTRO'
        #self.counter = 0
        # Set up the display
        pygame.display.set_caption("Practice Clicker Game")
        self.clock = pygame.time.Clock()
        self.FPS = 30
        self.thirdFPS = 0
        self.timer = 0
        self.stimer = 0
        self.saveprogress = True
        self.gamesavesuccessful = False
        self.quitstate = False

        # Global Variables
        self.titlestring = 'The Clicker Game'
        self.promptnumber = 0
        self.mouseclick = 0
        self.str_up = 0
        self.strength = 1
        self.good_click = 0
        self.sshard_found = 0
        self.worker_hired = 0
        self.workerlimit = 10

        self.mouse_clicked = pygame.mouse.get_pressed()[0]  # check once for happy mouse status function
        self.mouse_pos = pygame.mouse.get_pos()

        # self.play_game()

    def get_mouse_status(self):
        self.mouse_clicked = pygame.mouse.get_pressed()[0] #continuously is checking each frame
        self.mouse_pos = pygame.mouse.get_pos()

    # Make shard
    def make_click_shard(self):
        GameData.shard += (GameData.minerstr / 2)
        GameData.totalmined += (GameData.minerstr / 2)
        sshard_chance = random.randint(1, 300)
        if sshard_chance >= (50 - GameData.minerstr):
            self.sshard_found = 1
            if GameData.minerstr < 10:
                GameData.sshard += 1
            if GameData.minerstr >= 15:
                GameData.sshard += 2

    def auto_miners(self):
        if GameData.workers >= 1:
            GameData.shard += GameData.workers / 60
            GameData.totalmined += GameData.workers / 60
            sshard_chance = random.randint(1, 3000)
            if sshard_chance >= (3000 - (GameData.workers)):
                GameData.shard += 1

    def get_cost(self):
        cost_texts = {}
        #self.minerstrcost = int(self.minerstr * 25)
        GameData.minerstrcost = int(25 * (2**(1/5))**(GameData.minerstr-1))
        #self.workercost = int(self.workers * 1.75) + 5
        GameData.workercost = int(5*(5**(1/3))**(GameData.workers-1))
        cost_texts['str_upgrade_text'] = ['Mining Strength +1!', 'Not enough Shards!']
        cost_texts['worker_hired_text'] = ['New worker recruited!',
                                           'Not enough Special Shards!', 'Worker limit reached (Current limit '+str(self.workerlimit) + ')']
        return cost_texts

    ### SCENES ###


    def change_state(self, new_state):
        if GameData.state not in ('LOADGAME','SETTINGS','BACKPACK','STATISTICS'):
            GameData.laststate = GameData.state
        GameData.state = new_state

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
            return tree_building_rects_and_images()

    def statistics_rects_and_images(self):
        rects = {}
        draw_background(stats_page_image)
        draw_statistics()
        rects['back_button']=draw_back_button()
        return rects

    def statistics_events(self, rects):
        if rects['back_button'].collidepoint(self.event.pos):
            GameData.state=GameData.laststate

    def backpack_rects_and_images(self):
        rects = {}
        draw_background(backpackscreenimage)
        draw_inventory()
        rects['back_button'] = draw_back_button()
        return rects

    def backpack_events(self, rects):
        if rects['back_button'].collidepoint(self.event.pos):
            GameData.state=GameData.laststate

    def settings_page(self):
        draw_background(loadgamescreenimage)
        rects={}

        if GameData.laststate != 'INTRO':
            rects['save_game_rect']=get_text_box('Save Game', 40,
                         (WINDOW_WIDTH / 2, WINDOW_HEIGHT * 0.3),
                         OPAQUERED)
            rects['load_game_rect']=get_text_box('Load Game', 40,
                         (WINDOW_WIDTH / 2, WINDOW_HEIGHT * 0.5),
                         OPAQUERED)
            if self.saveprogress == False:
                get_text_box('Brooo cmon you just started XD', 40,
                             (WINDOW_WIDTH / 2, WINDOW_HEIGHT * 0.9),
                             OPAQUERED)
                self.gamesavesuccessful = False
            if self.gamesavesuccessful == True:
                get_text_box('Game saved successfully', 40,
                             (WINDOW_WIDTH / 2, WINDOW_HEIGHT * 0.8),
                             OPAQUERED)
                self.saveprogress = True
        if GameData.laststate == 'INTRO':
            get_text_box('(more settings will eventually live here)', 40,
                         (WINDOW_WIDTH / 2, WINDOW_HEIGHT * 0.5),
                         OPAQUERED)
        rects['back_button'] = draw_back_button()
        rects['quit_game'] = get_text_box('Quit Game', 40,
                                          (WINDOW_WIDTH / 2, WINDOW_HEIGHT * 0.7),
                                          OPAQUERED)
        return rects

    def settings_page_events(self, rects):
        if GameData.laststate != 'INTRO':
            if rects['load_game_rect'].collidepoint(self.event.pos):
                self.saveprogress = True
                self.gamesavesuccessful = False
                self.change_state('LOADGAME')
            if rects['save_game_rect'].collidepoint(self.event.pos):
                savestatelist = GameData.totalmined, GameData.shard, GameData.shard, GameData.workers, GameData.minerstr
                if savestatelist == (0, 0, 0, 0, 1):
                    self.saveprogress = False
                else:
                    with open('Saved Game.txt', 'w') as file:
                        file.write(str(savestatelist))
                    self.gamesavesuccessful = True
        if rects['back_button'].collidepoint(self.event.pos):
            self.saveprogress = True
            self.gamesavesuccessful = False
            if GameData.laststate == 'INTRO':
                GameData.state = 'INTRO'
            else:
                GameData.state=GameData.laststate
        if rects['quit_game'].collidepoint(self.event.pos):
            self.quitstate = True


    def loadgame_rects_and_images(self):
        draw_background(loadgamescreenimage)
        rects={}
        rects['back_button'] = draw_back_button()
        files_with_string = []
        for file in os.listdir():
            if 'Saved Game' in file or 'Autosaved Game' in file:  # Check if the file is a text file
                files_with_string.append(file)
        numberoffiles = len(files_with_string)
        if numberoffiles>0:
            for savefile in files_with_string:
                rects[savefile]=get_text_box(savefile.split('.txt')[0], 40, (WINDOW_WIDTH / 2, WINDOW_HEIGHT * (0.3+(int(files_with_string.index(savefile))*0.2))),
                     OPAQUERED)
        else:
            get_text_box('No save files found!', 40,
                         (WINDOW_WIDTH / 2, WINDOW_HEIGHT * 0.3),
                          OPAQUERED)
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
                    GameData.totalmined, GameData.shard, GameData.shard, GameData.workers, GameData.minerstr = float(content[0]), float(content[1]), float(
                        content[2]), float(
                        content[3]), float(content[4])
                    self.change_state('TOWN')
        if rects['back_button'].collidepoint(self.event.pos):
            self.saveprogress = True
            self.gamesavesuccessful = False
            if GameData.laststate == 'INTRO':
                GameData.state = 'INTRO'
            else:
                GameData.state = 'SETTINGS'

    def intro_rects_and_images(self):
        rects = {}
        introstring = 'Welcome to Mine.Cafe!'
        newgametext = ['New Game', 'Load Game']
        #timer = int(GameData.counter)
        background_image = pygame.transform.scale(introimage, (WINDOW_HEIGHT, WINDOW_HEIGHT))
        if GameData.counter < 60:
            HEIGHT = WINDOW_HEIGHT*(1.5-(GameData.counter/60)) #blit exactly off screen. at 0.5, it will be centered. want it to take 60 frames.
        else:
            HEIGHT = WINDOW_HEIGHT/2
        background_rect = background_image.get_rect(center=(WINDOW_WIDTH / 2, HEIGHT))
        screen.blit(background_image, background_rect)
        if GameData.counter > 60:
            get_text_box(introstring,50,(WINDOW_WIDTH/2, WINDOW_HEIGHT*0.23), OPAQUERED)
            rects['new_game_rect'] = get_text_box(newgametext[0], 50, (WINDOW_WIDTH*0.35, WINDOW_HEIGHT*0.53), BLUE)
            rects['load_game_rect'] = get_text_box(newgametext[1], 50, (WINDOW_WIDTH*0.65, WINDOW_HEIGHT*0.53), BLUE)
        return rects

    def intro_events(self, rects):
        if GameData.counter>60:
            if rects['new_game_rect'].collidepoint(self.event.pos):
                self.change_state('TUTORIAL')
            if rects['load_game_rect'].collidepoint(self.event.pos):
                self.change_state('LOADGAME')

    def tutorial_rects_and_images(self):  # where basically everything is drawn and established
        self.tuttext = ['Welcome to the Mines of Esswun, kid!', 'We need you to mine these blue shards.',
                   "Don't ask questions. Just mine!",
                   'Click on that glowing rock over there to mine it!',
                   'Your shards and other loot will be stored in this bag', 'You can see your stats here',
                   "When you're done for the day, return to town here",
                   'Now get mining! We need those shards!']
        rects = {}
        draw_background(level1minesceneimage)
        draw_mainclicktarget()
        draw_location_icon(towniconimage)
        if self.promptnumber < len(self.tuttext):
            get_text_box(self.tuttext[self.promptnumber], 40, Text_Location_TalkCenter, OPAQUERED, horiboxscale=0.1, vertboxscale=3, alignment='left')
            draw_speaker_icon(robot_boss_image)
            if self.promptnumber == 4:
                backpack_rect = pygame.Rect((WINDOW_WIDTH * 0.006, WINDOW_HEIGHT * 0.63),
                                            (medium_icon))  # location, size
                backpack_icon_image = pygame.transform.scale(backpack_icon, (medium_icon))
                screen.blit(backpack_icon_image, backpack_rect)
            if self.promptnumber == 5:
                statistics_rect = pygame.Rect((WINDOW_WIDTH * 0.006, WINDOW_HEIGHT * 0.79),
                                              (medium_icon))  # location, size
                statistics_icon_image = pygame.transform.scale(stats_icon, (medium_icon))
                screen.blit(statistics_icon_image, statistics_rect)
            if self.promptnumber == 6:
                icon_rect = pygame.Rect((WINDOW_WIDTH * 0.845, WINDOW_HEIGHT * 0.795),
                                        (medium_icon))  # location, size
                return_icon_image = pygame.transform.scale(towniconimage, (medium_icon))
                screen.blit(return_icon_image, icon_rect)
        rects['next_button'] = draw_next_button()
        return rects

    def tutorial_events(self, rects):
        if rects['next_button'].collidepoint(self.event.pos):
            self.increment_number()
            if self.promptnumber >= len(self.tuttext):
                self.change_state('MINELEVEL1')

    def mine_level_1_rects_and_images(self):
        rects = {}
        draw_background(level1minesceneimage)
        rects['mainclicktarget'] = draw_mainclicktarget()
        rects['corner_location_icon'] = draw_location_icon(towniconimage)
        if self.good_click == 1:
            self.timer += 1
            get_text_box('Mined some shards!', 30,
                         (WINDOW_WIDTH * 0.5, WINDOW_HEIGHT * (0.4-(0.15*(self.timer/60)))), OPAQUERED)
            if self.timer >= 60:
                self.timer = 0
                self.good_click = 0
        if self.sshard_found == 1:
            self.stimer += 1
            get_text_box('Found a special shard!', 30,
                         (WINDOW_WIDTH * 0.5, WINDOW_HEIGHT * (0.4-(0.15*(self.stimer/60)))), OPAQUERED)
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
        draw_background(quainttownimage)
        rects['minersguild_rect'] = pygame.Rect((WINDOW_WIDTH*0.59, WINDOW_HEIGHT*0.34),
                                                (medium_icon))  # location, size
        screen.blit(minersguildicon, rects['minersguild_rect'])

        rects['level1mine_rect'] = pygame.Rect((WINDOW_WIDTH*0.43, WINDOW_HEIGHT*0.65),
                                                (medium_icon))  # location, size
        screen.blit(level1minesceneimageicon, rects['level1mine_rect'])

        rects['treebuilding_rect'] = pygame.Rect((WINDOW_WIDTH*0.266, WINDOW_HEIGHT*0.34),
                                                (medium_icon))  # location, size
        screen.blit(treebuildingicon, rects['treebuilding_rect'])

        town_text = ['Back to the mines',"Miner's Guild", 'Strange Tree Building']
        get_text_box(town_text[0], 30,
                     (WINDOW_WIDTH * 0.5, WINDOW_HEIGHT * 0.89), OPAQUERED)
        get_text_box(town_text[1], 30,
                     (WINDOW_WIDTH * 0.66, WINDOW_HEIGHT * 0.58), OPAQUERED)
        get_text_box(town_text[2], 30,
                     (WINDOW_WIDTH * 0.34, WINDOW_HEIGHT * 0.58), OPAQUERED)
        return rects

    def town_events(self, rects):
        if rects['level1mine_rect'].collidepoint(self.event.pos):
            self.change_state('MINELEVEL1')
        if rects['minersguild_rect'].collidepoint(self.event.pos):
            self.change_state('MINERSGUILD')
        if rects['treebuilding_rect'].collidepoint(self.event.pos):
            self.change_state('TREEBUILDING')


    def miners_guild_rects_and_images(self):
        self.mouse_clicked = pygame.mouse.get_pressed()[0] #continuously is checking each frame
        self.mouse_pos = pygame.mouse.get_pos()
        rects = {}
        cost_texts = self.get_cost()  # just running get_cost and reading values
        draw_background(minersguildimage)

        #Rects
        rects['corner_location_icon'] = draw_location_icon(towniconimage)
        rects['ShopRobotMiner_rect'] = pygame.Rect((WINDOW_WIDTH*0.2, WINDOW_HEIGHT*0.3),
                                                medium_icon)
        rects['str_up_rect'] = pygame.Rect((WINDOW_WIDTH*0.435, WINDOW_HEIGHT*0.3), medium_icon)  # location, size
        rects['hire_worker_rect'] = pygame.Rect((WINDOW_WIDTH*0.68, WINDOW_HEIGHT*0.3),
                                                medium_icon)  # location, size
        #Text
        minerswelcome = ['Welcome to the Miner\'s Guild!', 'Spend your shards to upgrade your mining skill']
        descripts = ['Cute little robot guy','Increase amount of shards mined per click (Costs '+ str(GameData.minerstrcost)+' Shards)','Hire worker for passive Shard mining (Costs '+str(GameData.workercost)+' Special Shards)']
        get_text_box(minerswelcome[0], 30, (WINDOW_WIDTH*0.5,WINDOW_HEIGHT*0.635), OPAQUERED, horiboxscale=0.09)
        get_text_box(minerswelcome[1], 30, (WINDOW_WIDTH*0.5,WINDOW_HEIGHT*0.72), OPAQUERED, horiboxscale=0.09)
        if rects['ShopRobotMiner_rect'].collidepoint(self.mouse_pos):
            get_text_box(descripts[0], 30, (WINDOW_WIDTH * 0.5, WINDOW_HEIGHT * 0.55),
                     OPAQUERED, horiboxscale=0.09)
        if rects['str_up_rect'].collidepoint(self.mouse_pos):
            get_text_box(descripts[1], 30, (WINDOW_WIDTH * 0.5, WINDOW_HEIGHT * 0.55),
                         OPAQUERED, horiboxscale=0.09)
        if rects['hire_worker_rect'].collidepoint(self.mouse_pos):
            get_text_box(descripts[2], 30, (WINDOW_WIDTH * 0.5, WINDOW_HEIGHT * 0.55),
                         OPAQUERED, horiboxscale=0.09)

        #Blits
        darken_on_click(rects['str_up_rect'], strength_up_icon, darkenedstrength_up_icon)
        darken_on_click(rects['hire_worker_rect'], hire_worker_icon, darkenedhire_worker_icon)
        darken_on_click(rects['ShopRobotMiner_rect'], ShopRobotMiner_icon, DarkenedShopRobotMiner_icon)

        if self.str_up == 1:
            get_text_box(cost_texts['str_upgrade_text'][0], 30, (WINDOW_WIDTH*0.5,WINDOW_HEIGHT*0.25), OPAQUERED)
            self.timer += 1
            self.worker_hired = 0
            if self.timer >= 90:
                self.str_up, self.timer = 0, 0
        elif self.str_up == 2:
            get_text_box(cost_texts['str_upgrade_text'][1], 30, (WINDOW_WIDTH*0.5,WINDOW_HEIGHT*0.25), OPAQUERED)
            self.timer += 1
            if self.timer >= 90:
                self.str_up, self.timer = 0, 0
        if self.worker_hired == 1:
            get_text_box(cost_texts['worker_hired_text'][0], 30, (WINDOW_WIDTH*0.5,WINDOW_HEIGHT*0.25), OPAQUERED)
            self.timer += 1
            self.str_up = 0
            if self.timer >= 90:
                self.worker_hired, self.timer = 0, 0
        elif self.worker_hired == 2:
            get_text_box(cost_texts['worker_hired_text'][1], 30, (WINDOW_WIDTH*0.5,WINDOW_HEIGHT*0.25), OPAQUERED)
            self.timer += 1
            self.str_up = 0
            if self.timer >= 90:
                self.worker_hired, self.timer = 0, 0
        elif self.worker_hired == 3:
            get_text_box(cost_texts['worker_hired_text'][2], 30,
                         (WINDOW_WIDTH * 0.5, WINDOW_HEIGHT * 0.25), OPAQUERED)
            self.timer += 1
            self.str_up = 0
            if self.timer >= 90:
                self.worker_hired, self.timer = 0, 0
        return rects

    def miners_guild_events(self, rects):
        if rects['str_up_rect'].collidepoint(self.event.pos):
            self.timer = 0
            self.worker_hired = 0
            if GameData.shard >= GameData.minerstrcost:
                GameData.shard -= GameData.minerstrcost
                GameData.minerstr += 1
                self.str_up = 1  # (1 for yes, generate success text)
            else:
                self.str_up = 2  # (2 for no)

        if rects['hire_worker_rect'].collidepoint(self.event.pos):
            self.timer = 0
            self.str_up = 0
            if GameData.shard >= GameData.workercost and GameData.workers<self.workerlimit:
                GameData.shard -= GameData.workercost
                self.worker_hired = 1
                GameData.workers += 1
            elif GameData.shard >= GameData.workercost and GameData.workers>=self.workerlimit: #notifys worker limit reached
                self.worker_hired = 3
            else:
                self.worker_hired = 2
        if rects['corner_location_icon'].collidepoint(self.event.pos):
            self.change_state('TOWN')
            self.str_up = 0
            self.worker_hired = 0

    def tree_building_events(self, rects):  # treat this as a combat function
        if rects['fightbutton'].collidepoint(self.event.pos):
            if len(gameunits.OpponentUnitList) >= 1 and len(gameunits.FriendlyUnitList) >= 1: #both teams have at least 1 unit alive
                fightActive = True
            else:
                fightActive = False
            if fightActive:
                continueCombat()
        if rects['backbutton'].collidepoint(self.event.pos):
            GameData.state = 'TOWN'

    def increment_number(self):
        self.promptnumber += 1

    # Game loop
    def play_game(self):
        running = True
        pygame.event.wait()
        while running:
            # Clear the screen
            screen.fill(BLACK)  # Passively fills all blank space
            # Event handling
            #self.game_timer()  # total frame number
            GameData.counter += 1
            #print(GameData.counter)
            self.auto_miners()
            if GameData.state not in ('INTRO','LOADGAME'):
                self.backpack_rect = draw_backpack_icon()
                self.statistics_rect = draw_stats_icon()
            self.settings_rect = draw_settings_icon()
            rects = self.draw_scene(GameData.state)

            for self.event in pygame.event.get():
                if self.event.type == pygame.QUIT or self.quitstate:  # should be the only IF, so the game will always close first. i think
                    with open('Autosaved Game.txt', 'w') as file:
                        savestatelist = GameData.totalmined, GameData.shard, GameData.shard, GameData.workers, GameData.minerstr
                        file.write(str(savestatelist))
                    # Quit Pygame
                    pygame.quit()
                    sys.exit()
                    #running = False
                elif self.event.type == pygame.MOUSEBUTTONDOWN and self.event.button == 1:
                    if GameData.state == 'INTRO':
                        self.intro_events(rects)
                        #GameData.counter += 61
                        if GameData.counter>60:
                            if self.settings_rect.collidepoint(self.event.pos):
                                self.change_state('SETTINGS')
                    elif self.settings_rect.collidepoint(self.event.pos):
                        self.change_state('SETTINGS')
                    elif GameData.state not in ('INTRO', 'SETTINGS', 'LOADGAME', 'TUTORIAL','BACKPACK') and self.backpack_rect.collidepoint(self.event.pos):
                        self.change_state('BACKPACK')
                    elif GameData.state not in ('INTRO', 'SETTINGS', 'LOADGAME', 'TUTORIAL','STATISTICS') and self.statistics_rect.collidepoint(self.event.pos):
                        self.change_state('STATISTICS')
                    elif GameData.state == 'BACKPACK' and self.backpack_rect.collidepoint(self.event.pos):
                        GameData.state=GameData.laststate
                    elif GameData.state == 'STATISTICS' and self.statistics_rect.collidepoint(self.event.pos):
                        GameData.state=GameData.laststate
                    elif GameData.state == 'LOADGAME':
                        self.loadgame_events(rects)
                    elif GameData.state == 'SETTINGS':
                        self.settings_page_events(rects)
                    elif GameData.state == 'STATISTICS':
                        self.statistics_events(rects)
                    elif GameData.state == 'BACKPACK':
                        self.backpack_events(rects)
                    elif GameData.state == 'TUTORIAL':
                        self.tutorial_events(rects)
                    elif GameData.state == 'TOWN':
                        self.town_events(rects)
                    elif GameData.state == 'MINELEVEL1':
                        self.mine_level_1_events(rects)
                    elif GameData.state == 'MINERSGUILD':
                        self.miners_guild_events(rects)
                    elif GameData.state == 'TREEBUILDING':
                        self.tree_building_events(rects)


            # Update the display
            pygame.display.flip()
            self.clock.tick(self.FPS)

playgame = SystemHandler()
#pygame.time.wait(1000)

if __name__ == "__main__":
    playgame.play_game()

