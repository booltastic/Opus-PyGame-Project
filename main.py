import pygame
import os
import sys
import random
#from intro_scene import *

# Initialize Pygame
pygame.init()
pygame.mixer.init()

#You are hired to mine this mysterious shard. There's some sort of value you're unaware of. You get better, and start to
# recruit your own miners. Over time, the mine depletes. But you can venture further...

class systemhandler:
    def __init__(self):
        # Set up the display
        screen_res = 'small'
        if screen_res == 'medium':
            self.WINDOW_WIDTH, self.WINDOW_HEIGHT = 1200, 900
            self.fontscale = int(1.75)
        elif screen_res == 'large':
            self.WINDOW_WIDTH, self.WINDOW_HEIGHT = 1600, 1200
            self.fontscale = int(2.5)
        else:
            self.WINDOW_WIDTH, self.WINDOW_HEIGHT = 800, 600
            self.fontscale = int(1)
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Practice Clicker Game")
        self.clock = pygame.time.Clock()
        self.FPS = 30
        self.timecounter = 0
        self.counter = 0  # play time
        self.thirdFPS = 0
        self.timer = 0
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
        self.workercost = 0
        self.workers = 0
        self.worker_hired = 0
        self.workerlimit = 10
        self.savestatelist = [self.totalmined, self.shard, self.sshard, self.workers, self.minerstr]

        # Player Inventory
        player_inventory = []

        # Game Text
        self.tuttext = ['Welcome to the Mines of Esswun, kid!', 'We need you to mine these blue shards.',"Don't ask questions. Just mine!",
                   'Your loot is shown here',
                   'and when your work is done, ', 'return to town here!']

        # Pre-Determined Locations For Repeat Items
        self.Text_Location_Center = (self.WINDOW_WIDTH*0.5 , self.WINDOW_HEIGHT*0.73)
        self.Text_Location_Left = (self.WINDOW_WIDTH*0.22, self.WINDOW_HEIGHT*0.7)
        self.Text_Location_Right = (self.WINDOW_WIDTH*0.78, self.WINDOW_HEIGHT*0.76)
        self.tuttext_locations = [self.Text_Location_Center,
                             self.Text_Location_Center,
                             self.Text_Location_Center,
                             self.Text_Location_Left,
                             self.Text_Location_Center,
                             self.Text_Location_Right]
        self.screen_center = (self.WINDOW_WIDTH//2, self.WINDOW_HEIGHT//2)
        self.mini_icon = (self.WINDOW_HEIGHT*0.1,self.WINDOW_HEIGHT*0.1)
        self.small_icon = (self.WINDOW_HEIGHT*0.15,self.WINDOW_HEIGHT*0.15)
        self.medium_icon = (self.WINDOW_HEIGHT*0.2,self.WINDOW_HEIGHT*0.2)
        self.large_icon = ((self.WINDOW_HEIGHT*0.5,self.WINDOW_HEIGHT*0.5))

        # Background Images
        self.introimage = pygame.image.load('IntroScreen.jpeg')
        self.quainttownimage = pygame.image.load('QuaintTownSquare.png')
        self.level1minesceneimage = pygame.image.load('RockyMineLevel1.png')
        self.minersguildimage = pygame.image.load('MinersGuildInterior.png')
        self.loadgamescreenimage = pygame.image.load('LoadGameScreen.jpg')

        # Icon Images
        def load_img(imagefile, size):
            imageicon = pygame.image.load(imagefile)
            imageicon = pygame.transform.scale(imageicon, (size))
            return imageicon

        self.towniconimage = load_img('TownIcon.png',self.small_icon)
        self.treebuildingicon = load_img('TreeBuilding.png', self.medium_icon)
        self.level1minesceneimageicon = load_img('RockyMineLevel1.png', self.medium_icon)
        self.glowingrockicon = load_img('IsolatedGlowingRockIcon.png', self.small_icon)
        self.glowingrockicon2 = load_img('DarkenedIsolatedGlowingRockIcon.png', self.small_icon)
        self.minersguildicon = load_img('MinersGuildLogo.png', self.medium_icon)
        self.strength_up_icon = load_img('StrengthUpImage.png', self.medium_icon)
        self.darkenedstrength_up_icon = load_img('DarkenedStrengthUpImage.png', self.medium_icon)
        self.hire_worker_icon = load_img('HireWorkerIcon.png', self.medium_icon)
        self.darkenedhire_worker_icon = load_img('DarkenedHireWorkerIcon.png', self.medium_icon)
        self.ShopRobotMiner_icon = load_img('ShopRobotMiner.jpg', self.medium_icon)
        self.DarkenedShopRobotMiner_icon = load_img('DarkenedShopRobotMiner.jpg', self.medium_icon)
        self.background_glow_icon1 = load_img('GlowingLight.png', self.large_icon)
        self.background_glow_icon2 = load_img('GlowingLight - Rotated1.png', self.large_icon)
        self.background_glow_icon3 = load_img('GlowingLight - Rotated2.png', self.large_icon)
        self.settings_icon = load_img('SettingsIcon2.png',self.mini_icon)
        self.mouse_clicked = pygame.mouse.get_pressed()[0]  # check once for happy mouse status function
        self.mouse_pos = pygame.mouse.get_pos()

        def get_mouse_status():
            self.mouse_clicked = pygame.mouse.get_pressed()[0] #continuously is checking each frame
            self.mouse_pos = pygame.mouse.get_pos()

        def darken_on_click(rect, icon, darkenedicon):
            if self.mouse_clicked and rect.collidepoint(self.mouse_pos):
                self.screen.blit(darkenedicon, rect)
            else:
                self.screen.blit(icon, rect)

        def game_timer():
            self.counter += 1

        # Drawing scene backgrounds
        def draw_background(locationimage):
            background_image = pygame.transform.scale(locationimage, (self.WINDOW_HEIGHT, self.WINDOW_HEIGHT))
            background_rect = background_image.get_rect(center=(self.WINDOW_WIDTH / 2, self.WINDOW_HEIGHT / 2))
            self.screen.blit(background_image, background_rect)

        #Draw settings icon
        def draw_settings_icon():
            if self.counter>60:
                settings_rect = self.settings_icon.get_rect(center=(self.WINDOW_WIDTH * 0.95, self.WINDOW_HEIGHT * 0.065))
                self.screen.blit(self.settings_icon, settings_rect)
                return settings_rect

        # Next Button
        def draw_next_button():
            nextbuttontext = 'Next'
            nexttext_font = pygame.font.Font(None, 40*self.fontscale)
            nextbuttonstring = nexttext_font.render(str(nextbuttontext), True, self.WHITE)  # rendering text as object/image
            nextbutton_rect = nextbuttonstring.get_rect(
                center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT*0.92))  # gets rect of the text shape, placed at a location
            nextbutton_rect = nextbutton_rect.inflate(nextbutton_rect.width * 1.2,
                                                      nextbutton_rect.height * 1.2)  # inflated to clickable size
            buttontextspot = nextbuttonstring.get_rect(center=nextbutton_rect.center)
            pygame.draw.rect(self.screen, self.BLUE, nextbutton_rect)  # draw rect
            self.screen.blit(nextbuttonstring, buttontextspot)  # draw next text
            return nextbutton_rect

        def draw_back_button():
            backbuttontext = 'Back'
            nexttext_font = pygame.font.Font(None, 40*self.fontscale)
            nextbuttonstring = nexttext_font.render(str(backbuttontext), True, self.WHITE)  # rendering text as object/image
            nextbutton_rect = nextbuttonstring.get_rect(
                center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT*0.92))  # gets rect of the text shape, placed at a location
            nextbutton_rect = nextbutton_rect.inflate(nextbutton_rect.width * 1.2,
                                                      nextbutton_rect.height * 1.2)  # inflated to clickable size
            buttontextspot = nextbuttonstring.get_rect(center=nextbutton_rect.center)
            pygame.draw.rect(self.screen, self.BLUE, nextbutton_rect)  # draw rect
            self.screen.blit(nextbuttonstring, buttontextspot)  # draw next text
            return nextbutton_rect

        # Drawing location icons
        def draw_location_icon(locationiconimage):
            icon_rect = pygame.Rect((self.WINDOW_WIDTH*0.8822, self.WINDOW_HEIGHT*0.843), (self.small_icon))  # location, size
            pygame.draw.rect(self.screen, self.CLEAR, icon_rect)  # draw it. currently drawn off screen (beside background)
            return_icon_image = pygame.transform.scale(locationiconimage, (self.small_icon))
            self.screen.blit(return_icon_image, icon_rect)
            return icon_rect

        # Make shard
        def make_click_shard():
            self.shard += (self.minerstr / 2)
            self.totalmined += (self.minerstr / 2)
            sshard_chance = random.randint(1, 300)
            if sshard_chance >= (300 - self.minerstr):
                if self.minerstr < 10:
                    self.sshard += 1
                if self.minerstr >= 15:
                    self.sshard += 2

        def auto_miners():
            if self.workers >= 1:
                self.shard += self.workers / 60
                self.totalmined += self.workers / 60
                sshard_chance = random.randint(1, 3000)
                if sshard_chance >= (3000 - (self.workers)):
                    self.sshard += 1

        def get_cost():
            cost_texts = {}
            #self.minerstrcost = int(self.minerstr * 25)
            self.minerstrcost = int(25 * (2**(1/5))**(self.minerstr-1))
            #self.workercost = int(self.workers * 1.75) + 5
            self.workercost = int(5*(5**(1/3))**(self.workers-1))
            cost_texts['str_upgrade_text'] = ['Mining Strength +1!', 'Not enough Shards!']
            cost_texts['worker_hired_text'] = ['New worker recruited!',
                                               'Not enough Special Shards!', 'Worker limit reached (Current limit '+str(self.workerlimit) + ')']
            return cost_texts

        def draw_shardicon():
            # Shards
            totalmined_string = 'Total Shards Mined: ' + str(int(self.totalmined))
            get_text_box(totalmined_string, 35*self.fontscale, (self.WINDOW_WIDTH*0.0175, self.WINDOW_HEIGHT*0.05), self.OPAQUEBLACK, 'left', 1)

            shard_string = 'Shards: ' + str(int(self.shard))
            get_text_box(shard_string, 35*self.fontscale, (self.WINDOW_WIDTH*0.0175, self.WINDOW_HEIGHT*0.8), self.OPAQUEBLACK, 'left',0.1)

            # Special Shards
            sshard_string = 'Special Shards: ' + str(int(self.sshard))
            get_text_box(sshard_string, 35*self.fontscale, (self.WINDOW_WIDTH*0.0175, self.WINDOW_HEIGHT*0.85), self.OPAQUEBLACK, 'left',0.1)

            # Workers
            worker_string = 'Workers: ' + str(int(self.workers))
            get_text_box(worker_string, 35*self.fontscale, (self.WINDOW_WIDTH*0.0175, self.WINDOW_HEIGHT*0.9), self.OPAQUEBLACK, 'left',0.1)

            # Mining Strength
            minestr_string = 'Mining Strength: ' + str(int(self.minerstr))
            get_text_box(minestr_string, 35*self.fontscale, (self.WINDOW_WIDTH*0.0175, self.WINDOW_HEIGHT*0.95), self.OPAQUEBLACK, 'left',0.1)

        def draw_mainclicktarget():
            get_mouse_status()
            timer = int(self.counter/3)
            for i in range(0,1):
                if timer % 3 == i:
                    glowing_background_rect = self.background_glow_icon1.get_rect(center=self.screen_center)
                    self.screen.blit(self.background_glow_icon1, glowing_background_rect)
            for i in range(1,2):
                if timer % 3 == i:
                    glowing_background_rect = self.background_glow_icon2.get_rect(center=self.screen_center)
                    self.screen.blit(self.background_glow_icon2, glowing_background_rect)
            for i in range(2,3):
                if timer % 3 == i:
                    glowing_background_rect = self.background_glow_icon3.get_rect(center=self.screen_center)
                    self.screen.blit(self.background_glow_icon3, glowing_background_rect)

            glowingrockicon_rect = self.glowingrockicon.get_rect(center=self.screen_center)
            darken_on_click(glowingrockicon_rect, self.glowingrockicon, self.glowingrockicon2)

            return glowingrockicon_rect

        def get_text_box(drawntext, fontsize, textlocation, color, alignment='center',vertboxscale=float(1), horiboxscale=float(0.15)):  # made for rects loops
            boxtext = drawntext
            boxtextfont = pygame.font.Font(None, fontsize)
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
        def change_state(new_state):
            if self.state != 'LOADGAME' and self.state != 'SETTINGS':
                self.laststate = self.state
            self.state = new_state

        def draw_scene(sceneinput):  # argument passed through is State
            if sceneinput == 'INTRO':
                return intro_rects_and_images()  # these return rect dicts where each item should be a rect. draw_scene is equal to versatile rects now
            if sceneinput == 'LOADGAME':
                return loadgame_rects_and_images()
            if sceneinput == 'SETTINGS':
                return settings_page()
            if sceneinput == 'TUTORIAL':
                return tutorial_rects_and_images()
            if sceneinput == 'MINELEVEL1':
                return mine_level_1_rects_and_images()
            if sceneinput == 'TOWN':
                return town_rects_and_images()
            if sceneinput == 'MINERSGUILD':
                return miners_guild_rects_and_images()

        def intro_rects_and_images():
            rects = {}
            introstring = 'Welcome to Mine.Cafe!'
            newgametext = ['New Game', 'Load Game']
            timer = int(self.counter)
            background_image = pygame.transform.scale(self.introimage, (self.WINDOW_HEIGHT, self.WINDOW_HEIGHT))
            if timer < 60:
                HEIGHT = self.WINDOW_HEIGHT*(1.5-(timer/60)) #blit exactly off screen. at 0.5, it will be centered. want it to take 60 frames.
            else:
                HEIGHT = self.WINDOW_HEIGHT/2
            background_rect = background_image.get_rect(center=(self.WINDOW_WIDTH / 2, HEIGHT))
            self.screen.blit(background_image, background_rect)
            if timer > 60:
                get_text_box(introstring,50*self.fontscale,(self.WINDOW_WIDTH/2, self.WINDOW_HEIGHT*0.23), self.OPAQUERED)
                rects['new_game_rect'] = get_text_box(newgametext[0], 50*self.fontscale, (self.WINDOW_WIDTH*0.35, self.WINDOW_HEIGHT*0.53), self.BLUE)
                rects['load_game_rect'] = get_text_box(newgametext[1], 50*self.fontscale, (self.WINDOW_WIDTH*0.65, self.WINDOW_HEIGHT*0.53), self.BLUE)
            return rects

        def intro_events(rects):
            if self.counter>60:
                if rects['new_game_rect'].collidepoint(event.pos):
                    #self.savestatelist=[0,0,0,0,1]
                    change_state('TUTORIAL')
                if rects['load_game_rect'].collidepoint(event.pos):
                    change_state('LOADGAME')

        def settings_page():
            draw_background(self.loadgamescreenimage)
            rects={}
            rects['save_game_rect']=get_text_box('Save Game', 40 * self.fontscale,
                         (self.WINDOW_WIDTH / 2, self.WINDOW_HEIGHT * 0.3),
                         self.OPAQUERED)
            rects['load_game_rect']=get_text_box('Load Game', 40 * self.fontscale,
                         (self.WINDOW_WIDTH / 2, self.WINDOW_HEIGHT * 0.5),
                         self.OPAQUERED)
            rects['back_button'] = draw_back_button()
            if self.saveprogress == False:
                get_text_box('Brooo cmon you just started XD', 40 * self.fontscale,
                             (self.WINDOW_WIDTH / 2, self.WINDOW_HEIGHT * 0.8),
                             self.OPAQUERED)
                self.gamesavesuccessful = False
            if self.gamesavesuccessful == True:
                get_text_box('Game saved successfully', 40 * self.fontscale,
                             (self.WINDOW_WIDTH / 2, self.WINDOW_HEIGHT * 0.8),
                             self.OPAQUERED)
                self.saveprogress = True
            return rects

        def settings_page_events(rects):
            if rects['load_game_rect'].collidepoint(event.pos):
                self.saveprogress = True
                self.gamesavesuccessful = False
                change_state('LOADGAME')
            if rects['save_game_rect'].collidepoint(event.pos):
                savestatelist = self.totalmined, self.shard, self.sshard, self.workers, self.minerstr
                if savestatelist == (0, 0, 0, 0, 1):
                    self.saveprogress = False
                else:
                    with open('gamesave.txt', 'w') as file:
                        file.write(str(savestatelist))
                    self.gamesavesuccessful = True
            if rects['back_button'].collidepoint(event.pos):
                self.saveprogress = True
                self.gamesavesuccessful = False
                self.state=self.laststate

        def loadgame_rects_and_images():
            draw_background(self.loadgamescreenimage)
            rects={}
            rects['back_button'] = draw_back_button()
            files_with_string = []
            for file in os.listdir():
                if 'gamesave' in file or 'autosave' in file:  # Check if the file is a text file
                    files_with_string.append(file)
            numberoffiles = len(files_with_string)
            if numberoffiles>0:
                for savefile in files_with_string:
                    rects[savefile]=get_text_box(savefile, 40 * self.fontscale, (self.WINDOW_WIDTH / 2, self.WINDOW_HEIGHT * (0.3+(int(files_with_string.index(savefile))*0.2))),
                         self.OPAQUERED)
            else:
                get_text_box('No save files found!', 40 * self.fontscale,
                             (self.WINDOW_WIDTH / 2, self.WINDOW_HEIGHT * 0.3),
                              self.OPAQUERED)
            return rects

        def loadgame_events(rects):
            for file in rects:
                if rects[file].collidepoint(event.pos) and 'back_button' not in file:
                    with open(file, 'r') as savefile:
                        content = savefile.read().split('(')[1]
                        content = content.split(')')[0]
                        content = content.split(', ')
                        if len(content) == 0:
                            pass
                        self.totalmined, self.shard, self.sshard, self.workers, self.minerstr = float(content[0]), float(content[1]), float(
                            content[2]), float(
                            content[3]), float(content[4])
                        change_state('TOWN')
            if rects['back_button'].collidepoint(event.pos):
                self.saveprogress = True
                self.gamesavesuccessful = False
                if self.laststate == 'INTRO':
                    self.state = 'INTRO'
                else:
                    self.state = 'SETTINGS'

        def tutorial_rects_and_images():  # where basically everything is drawn and established
            rects = {}
            draw_background(self.level1minesceneimage)
            draw_shardicon()
            draw_mainclicktarget()
            if self.promptnumber < len(self.tuttext):
                get_text_box(self.tuttext[self.promptnumber], 40*self.fontscale, self.tuttext_locations[self.promptnumber], self.OPAQUERED)
            draw_location_icon(self.towniconimage)
            rects['next_button'] = draw_next_button()
            return rects

        def tutorial_events(rects):
            if rects['next_button'].collidepoint(event.pos):
                increment_number()
                if self.promptnumber >= len(self.tuttext):
                    change_state('MINELEVEL1')

        def mine_level_1_rects_and_images():
            rects = {}
            draw_background(self.level1minesceneimage)
            draw_shardicon()
            rects['mainclicktarget'] = draw_mainclicktarget()
            rects['corner_location_icon'] = draw_location_icon(self.towniconimage)
            return rects

        def mine_level_1_events(rects):
            if rects['corner_location_icon'].collidepoint(event.pos):
                change_state('TOWN')
            if rects['mainclicktarget'].collidepoint(event.pos):
                make_click_shard()

        def town_rects_and_images():
            rects = {}
            draw_background(self.quainttownimage)
            draw_shardicon()
            rects['minersguild_rect'] = pygame.Rect((self.WINDOW_WIDTH*0.59, self.WINDOW_HEIGHT*0.34),
                                                    (self.medium_icon))  # location, size
            self.screen.blit(self.minersguildicon, rects['minersguild_rect'])

            rects['level1mine_rect'] = pygame.Rect((self.WINDOW_WIDTH*0.43, self.WINDOW_HEIGHT*0.65),
                                                    (self.medium_icon))  # location, size
            self.screen.blit(self.level1minesceneimageicon, rects['level1mine_rect'])

            rects['treebuilding_rect'] = pygame.Rect((self.WINDOW_WIDTH*0.266, self.WINDOW_HEIGHT*0.34),
                                                    (self.medium_icon))  # location, size
            self.screen.blit(self.treebuildingicon, rects['treebuilding_rect'])

            town_text = ['Back to the mines',"Miner's Guild", 'Strange Tree Building']
            get_text_box(town_text[0], 30 * self.fontscale,
                         (self.WINDOW_WIDTH * 0.5, self.WINDOW_HEIGHT * 0.89), self.OPAQUERED)
            get_text_box(town_text[1], 30 * self.fontscale,
                         (self.WINDOW_WIDTH * 0.66, self.WINDOW_HEIGHT * 0.58), self.OPAQUERED)
            get_text_box(town_text[2], 30 * self.fontscale,
                         (self.WINDOW_WIDTH * 0.34, self.WINDOW_HEIGHT * 0.58), self.OPAQUERED)
            return rects

        def town_events(rects):
            if rects['level1mine_rect'].collidepoint(event.pos):
                change_state('MINELEVEL1')
            if rects['minersguild_rect'].collidepoint(event.pos):
                change_state('MINERSGUILD')

        def miners_guild_rects_and_images():
            self.mouse_clicked = pygame.mouse.get_pressed()[0] #continuously is checking each frame
            self.mouse_pos = pygame.mouse.get_pos()
            rects = {}
            cost_texts = get_cost()  # just running get_cost and reading values
            draw_background(self.minersguildimage)
            draw_shardicon()

            #Rects
            rects['corner_location_icon'] = draw_location_icon(self.towniconimage)
            rects['ShopRobotMiner_rect'] = pygame.Rect((self.WINDOW_WIDTH*0.2, self.WINDOW_HEIGHT*0.3),
                                                    self.medium_icon)
            rects['str_up_rect'] = pygame.Rect((self.WINDOW_WIDTH*0.435, self.WINDOW_HEIGHT*0.3), self.medium_icon)  # location, size
            rects['hire_worker_rect'] = pygame.Rect((self.WINDOW_WIDTH*0.68, self.WINDOW_HEIGHT*0.3),
                                                    self.medium_icon)  # location, size
            #Text
            minerswelcome = ['Welcome to the Miner\'s Guild!', 'Spend your shards to upgrade your mining skill']
            descripts = ['Cute little robot guy','Increase amount of shards mined per click (Costs '+ str(self.minerstrcost)+' Shards)','Hire worker for passive Shard mining (Costs '+str(self.workercost)+' Special Shards)']
            get_text_box(minerswelcome[0], 30*self.fontscale, (self.WINDOW_WIDTH*0.5,self.WINDOW_HEIGHT*0.635), self.OPAQUERED, horiboxscale=0.09)
            get_text_box(minerswelcome[1], 30*self.fontscale, (self.WINDOW_WIDTH*0.5,self.WINDOW_HEIGHT*0.72), self.OPAQUERED, horiboxscale=0.09)
            if rects['ShopRobotMiner_rect'].collidepoint(self.mouse_pos):
                get_text_box(descripts[0], 30 * self.fontscale, (self.WINDOW_WIDTH * 0.5, self.WINDOW_HEIGHT * 0.55),
                         self.OPAQUERED, horiboxscale=0.09)
            if rects['str_up_rect'].collidepoint(self.mouse_pos):
                get_text_box(descripts[1], 30 * self.fontscale, (self.WINDOW_WIDTH * 0.5, self.WINDOW_HEIGHT * 0.55),
                             self.OPAQUERED, horiboxscale=0.09)
            if rects['hire_worker_rect'].collidepoint(self.mouse_pos):
                get_text_box(descripts[2], 30 * self.fontscale, (self.WINDOW_WIDTH * 0.5, self.WINDOW_HEIGHT * 0.55),
                             self.OPAQUERED, horiboxscale=0.09)

            #Blits
            darken_on_click(rects['str_up_rect'], self.strength_up_icon, self.darkenedstrength_up_icon)
            darken_on_click(rects['hire_worker_rect'], self.hire_worker_icon, self.darkenedhire_worker_icon)
            darken_on_click(rects['ShopRobotMiner_rect'], self.ShopRobotMiner_icon, self.DarkenedShopRobotMiner_icon)

            if self.str_up == 1:
                get_text_box(cost_texts['str_upgrade_text'][0], 30*self.fontscale, (self.WINDOW_WIDTH*0.5,self.WINDOW_HEIGHT*0.25), self.OPAQUERED)
                self.timer += 1
                self.worker_hired = 0
                if self.timer >= 90:
                    self.str_up, self.timer = 0, 0
            elif self.str_up == 2:
                get_text_box(cost_texts['str_upgrade_text'][1], 30*self.fontscale, (self.WINDOW_WIDTH*0.5,self.WINDOW_HEIGHT*0.25), self.OPAQUERED)
                self.timer += 1
                if self.timer >= 90:
                    self.str_up, self.timer = 0, 0
            if self.worker_hired == 1:
                get_text_box(cost_texts['worker_hired_text'][0], 30*self.fontscale, (self.WINDOW_WIDTH*0.5,self.WINDOW_HEIGHT*0.25), self.OPAQUERED)
                self.timer += 1
                self.str_up = 0
                if self.timer >= 90:
                    self.worker_hired, self.timer = 0, 0
            elif self.worker_hired == 2:
                get_text_box(cost_texts['worker_hired_text'][1], 30*self.fontscale, (self.WINDOW_WIDTH*0.5,self.WINDOW_HEIGHT*0.25), self.OPAQUERED)
                self.timer += 1
                self.str_up = 0
                if self.timer >= 90:
                    self.worker_hired, self.timer = 0, 0
            elif self.worker_hired == 3:
                get_text_box(cost_texts['worker_hired_text'][2], 30 * self.fontscale,
                             (self.WINDOW_WIDTH * 0.5, self.WINDOW_HEIGHT * 0.25), self.OPAQUERED)
                self.timer += 1
                self.str_up = 0
                if self.timer >= 90:
                    self.worker_hired, self.timer = 0, 0
            return rects

        def miners_guild_events(rects):
            if rects['str_up_rect'].collidepoint(event.pos):
                self.timer = 0
                self.worker_hired = 0
                if self.shard >= self.minerstrcost:
                    self.shard -= self.minerstrcost
                    self.minerstr += 1
                    self.str_up = 1  # (1 for yes, generate success text)
                else:
                    self.str_up = 2  # (2 for no)

            if rects['hire_worker_rect'].collidepoint(event.pos):
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
            if rects['corner_location_icon'].collidepoint(event.pos):
                change_state('TOWN')
                self.str_up = 0
                self.worker_hired = 0

        def increment_number():
            self.promptnumber += 1

        rects = draw_scene('INTRO')
        settings_rect = draw_settings_icon()
        # Game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # should be the only IF, so the game will always close first. i think
                    with open('autosave.txt', 'w') as file:
                        savestatelist = self.totalmined, self.shard, self.sshard, self.workers, self.minerstr
                        file.write(str(savestatelist))
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state == 'INTRO':
                        intro_events(rects)
                        if self.counter>60:
                            if settings_rect.collidepoint(event.pos):
                                change_state('SETTINGS')
                    elif settings_rect.collidepoint(event.pos):
                        change_state('SETTINGS')
                    elif self.state == 'LOADGAME':
                        loadgame_events(rects)
                    elif self.state == 'SETTINGS':
                        settings_page_events(rects)
                    elif self.state == 'TUTORIAL':
                        tutorial_events(rects)
                    elif self.state == 'TOWN':
                        town_events(rects)
                    elif self.state == 'MINELEVEL1':
                        mine_level_1_events(rects)
                    elif self.state == 'MINERSGUILD':
                        miners_guild_events(rects)
            # Clear the screen
            self.screen.fill(self.BLACK)  # Passively fills all blank space. Catch-all just in case

            # Event handling
            game_timer()  # total frame number
            rects = draw_scene(self.state)
            settings_rect=draw_settings_icon()
            auto_miners()

            # Update the display
            pygame.display.flip()
            self.clock.tick(self.FPS)

playgame = systemhandler()
# Quit Pygame
pygame.quit()
sys.exit()