import pygame
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
        self.text_font = pygame.font.Font(None, 50*self.fontscale)
        self.introstring = 'Welcome to Mine.Cafe!'
        self.introstring = self.text_font.render(str(self.introstring), True, self.WHITE)  # rendering text as object/image
        self.introtext_rect = self.introstring.get_rect(
            center=(self.WINDOW_WIDTH // 2,
                    ((self.WINDOW_HEIGHT // 2) - self.WINDOW_HEIGHT/6)))  # gets rect of the text shape, placed centered at a location
        self.state = 'INTRO'
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

        # Player Inventory
        player_inventory = []

        # Game Text
        self.nextbuttontext = 'Next'
        self.tuttext = ['Welcome to the Mines of Esswun, kid!', 'We need you to mine these blue shards.',"Don't ask questions. Just mine!",
                   'Your loot is shown here',
                   'and when your work is done, ', 'return to town here!']
        self.minerswelcome = ['Welcome to the Miner\'s Guild!', 'Spend your shards to upgrade your mining skill']
        self.newgametext = ['Load saved game?', 'New Game', 'Load Game']

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
        self.small_icon = (self.WINDOW_HEIGHT*0.15,self.WINDOW_HEIGHT*0.15)
        self.medium_icon = (self.WINDOW_HEIGHT*0.2,self.WINDOW_HEIGHT*0.2)
        self.large_icon = ((self.WINDOW_HEIGHT*0.5,self.WINDOW_HEIGHT*0.5))

        # Background Images
        self.quainttownimage = pygame.image.load('QuaintTownSquare.png')
        self.level1minesceneimage = pygame.image.load('RockyMineLevel1.png')
        self.minersguildimage = pygame.image.load('MinersGuildInterior.png')

        # Icon Images
        self.towniconimage = pygame.image.load('TownIcon.png')
        self.towniconimage = pygame.transform.scale(self.towniconimage, (self.small_icon))

        self.treebuildingicon = pygame.image.load('TreeBuilding.png')
        self.treebuildingicon = pygame.transform.scale(self.treebuildingicon, (self.small_icon))

        self.level1minesceneimageicon = pygame.image.load('RockyMineLevel1.png')
        self.level1minesceneimageicon = pygame.transform.scale(self.level1minesceneimageicon, (self.small_icon))

        self.glowingrockicon = pygame.image.load('IsolatedGlowingRockIcon.png')
        self.glowingrockicon = pygame.transform.scale(self.glowingrockicon, (self.medium_icon))

        self.glowingrockicon2 = pygame.image.load('DarkenedIsolatedGlowingRockIcon.png')
        self.glowingrockicon2 = pygame.transform.scale(self.glowingrockicon2, (self.medium_icon))

        self.background_glow_icon1 = pygame.image.load('GlowingLight.png')
        self.background_glow_icon1 = pygame.transform.scale(self.background_glow_icon1, (self.large_icon))
        self.background_glow_icon2 = pygame.image.load('GlowingLight - Rotated1.png')
        self.background_glow_icon2 = pygame.transform.scale(self.background_glow_icon2, (self.large_icon))
        self.background_glow_icon3 = pygame.image.load('GlowingLight - Rotated2.png')
        self.background_glow_icon3 = pygame.transform.scale(self.background_glow_icon3, (self.large_icon))

        self.minersguildicon = pygame.image.load('MinersGuildLogo.png')
        self.minersguildicon = pygame.transform.scale(self.minersguildicon, (self.small_icon))

        self.strength_up_icon = pygame.image.load('StrengthUpImage.png')
        self.strength_up_icon = pygame.transform.scale(self.strength_up_icon, (self.medium_icon))

        self.hire_worker_icon = pygame.image.load('HireWorkerIcon.png')
        self.hire_worker_icon = pygame.transform.scale(self.hire_worker_icon, (self.medium_icon))

        self.ShopRobotMiner_icon = pygame.image.load('ShopRobotMiner.jpg')
        self.ShopRobotMiner_icon = pygame.transform.scale(self.ShopRobotMiner_icon, (self.medium_icon))

        def game_timer():
            self.counter += 1
            self.thirdFPS += 1/3

        # Drawing scene backgrounds
        def draw_background(locationimage):
            background_image = pygame.transform.scale(locationimage, (self.WINDOW_HEIGHT, self.WINDOW_HEIGHT))
            background_rect = background_image.get_rect(center=(self.WINDOW_WIDTH / 2, self.WINDOW_HEIGHT / 2))
            self.screen.blit(background_image, background_rect)

        # Next Button
        def draw_next_button():
            nexttext_font = pygame.font.Font(None, 40*self.fontscale)
            nextbuttonstring = nexttext_font.render(str(self.nextbuttontext), True, self.WHITE)  # rendering text as object/image
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
            self.minerstrcost = int(self.minerstr * 25)
            self.workercost = int(self.workers * 1.75) + 5
            cost_texts['str_upgrade_text'] = ['Mining Strength +1!', 'Not enough shards! (Costs ' + str(self.minerstrcost) + ')']
            cost_texts['worker_hired_text'] = ['Worker speed increased!',
                                               'Not enough Special Shards! (Costs ' + str(self.workercost) + ')', 'Worker limit reached (Current limit '+str(self.workerlimit) + ')']
            return cost_texts

        def draw_shardicon():
            # Shards
            totalmined_string = 'Total Shards Mined: ' + str(int(self.totalmined))
            get_text_box(totalmined_string, 35*self.fontscale, (self.WINDOW_WIDTH*0.0175, self.WINDOW_HEIGHT*0.05), self.OPAQUEBLACK, 'left', 1)

            shard_string = 'Shards: ' + str(int(self.shard))
            get_text_box(shard_string, 35*self.fontscale, (self.WINDOW_WIDTH*0.0175, self.WINDOW_HEIGHT*0.8), self.OPAQUEBLACK, 'left',0)

            # Special Shards
            sshard_string = 'Special Shards: ' + str(int(self.sshard))
            get_text_box(sshard_string, 35*self.fontscale, (self.WINDOW_WIDTH*0.0175, self.WINDOW_HEIGHT*0.85), self.OPAQUEBLACK, 'left',0)

            # Workers
            worker_string = 'Workers: ' + str(int(self.workers))
            get_text_box(worker_string, 35*self.fontscale, (self.WINDOW_WIDTH*0.0175, self.WINDOW_HEIGHT*0.9), self.OPAQUEBLACK, 'left',0)

            # Mining Strength
            minestr_string = 'Mining Strength: ' + str(int(self.minerstr))
            get_text_box(minestr_string, 35*self.fontscale, (self.WINDOW_WIDTH*0.0175, self.WINDOW_HEIGHT*0.95), self.OPAQUEBLACK, 'left',0)

        def draw_mainclicktarget():
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

            mouse_clicked = pygame.mouse.get_pressed()[0]
            mouse_pos = pygame.mouse.get_pos()

            glowingrockicon_rect = self.glowingrockicon.get_rect(center=self.screen_center)
            if mouse_clicked and glowingrockicon_rect.collidepoint(mouse_pos):
                self.screen.blit(self.glowingrockicon2, glowingrockicon_rect)
            else:
                self.screen.blit(self.glowingrockicon, glowingrockicon_rect)
            return glowingrockicon_rect

        def get_text_box(drawntext, fontsize, textlocation, color, alignment='center',boxscale=float(1)):  # made for rects loops
            boxtext = drawntext
            boxtextfont = pygame.font.Font(None, fontsize)
            renderedtext = boxtextfont.render(str(boxtext), True, self.WHITE)  # renders text image
            if alignment == 'left':
                colliderect = renderedtext.get_rect(
                    midleft=textlocation)  # create rect the size of the text at chosen location. sets ratio of size, and where we want the center
            else:
                colliderect = renderedtext.get_rect(
                    center=textlocation)
            colliderect = colliderect.inflate(colliderect.width * 0.15,
                                              colliderect.height*boxscale)  # inflate that rect in place to twice its size, this is what gets clicked
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
            self.state = new_state

        def draw_scene(sceneinput):  # argument passed through is State
            if sceneinput == 'INTRO':
                return intro_rects_and_images()  # these return rect dicts where each item should be a rect. draw_scene is equal to versatile rects now
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
            get_text_box(self.newgametext[0], 40*self.fontscale, (self.WINDOW_WIDTH/2, self.WINDOW_HEIGHT*0.5),
                         self.RED)  # tuple of 4, with 3 rects: 2 for draw, 1 for collide
            rects['new_game_rect'] = get_text_box(self.newgametext[1], 40*self.fontscale, (self.WINDOW_WIDTH*0.25, self.WINDOW_HEIGHT*0.65), self.BLUE)
            rects['load_game_rect'] = get_text_box(self.newgametext[2], 40*self.fontscale, (self.WINDOW_WIDTH*0.75, self.WINDOW_HEIGHT*0.65), self.BLUE)
            self.screen.blit(self.introstring, self.introtext_rect)  # blits the rendered text onto the rectangle that is at a location
            # functions for other scene elements can go here, and isolate the rects for collide function
            return rects

        def intro_events(rects):
            if rects['new_game_rect'].collidepoint(event.pos):
                change_state('TUTORIAL')
            elif rects['load_game_rect'] is not None:
                if rects['load_game_rect'].collidepoint(event.pos):
                    try:
                        with open('savestate.txt', 'r') as file:
                            content = file.read().split('(')[1]
                            content = content.split(')')[0]
                            content = content.split(', ')
                            if len(content) == 0:
                                pass
                            self.totalmined, self.shard, self.sshard, self.workers, self.minerstr = float(content[0]), float(content[1]), float(
                                content[2]), float(
                                content[3]), float(content[4])
                            change_state('TOWN')
                    except FileNotFoundError:
                        pass

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

            #rects['corner_location_icon'] = draw_location_icon(self.quainttownimage)
            rects['minersguild_rect'] = pygame.Rect((self.WINDOW_WIDTH*0.6, self.WINDOW_HEIGHT*0.4),
                                                    (self.small_icon))  # location, size
            self.screen.blit(self.minersguildicon, rects['minersguild_rect'])

            rects['level1mine_rect'] = pygame.Rect((self.WINDOW_WIDTH*0.45, self.WINDOW_HEIGHT*0.65),
                                                    (self.small_icon))  # location, size
            self.screen.blit(self.level1minesceneimageicon, rects['level1mine_rect'])

            rects['treebuilding_rect'] = pygame.Rect((self.WINDOW_WIDTH*0.3, self.WINDOW_HEIGHT*0.4),
                                                    (self.small_icon))  # location, size
            self.screen.blit(self.treebuildingicon, rects['treebuilding_rect'])

            town_text = ['Back to the mines',"Miner's Guild", 'Strange Tree Building']
            get_text_box(town_text[0], 30 * self.fontscale,
                         (self.WINDOW_WIDTH * 0.5, self.WINDOW_HEIGHT * 0.85), self.OPAQUERED)
            get_text_box(town_text[1], 30 * self.fontscale,
                         (self.WINDOW_WIDTH * 0.65, self.WINDOW_HEIGHT * 0.6), self.OPAQUERED)
            get_text_box(town_text[2], 30 * self.fontscale,
                         (self.WINDOW_WIDTH * 0.34, self.WINDOW_HEIGHT * 0.6), self.OPAQUERED)
            return rects

        def town_events(rects):
            if rects['level1mine_rect'].collidepoint(event.pos):
                change_state('MINELEVEL1')
            if rects['minersguild_rect'].collidepoint(event.pos):
                change_state('MINERSGUILD')

        def miners_guild_rects_and_images():
            rects = {}
            cost_texts = get_cost()  # just running get_cost and reading values
            draw_background(self.minersguildimage)
            draw_shardicon()
            rects['corner_location_icon'] = draw_location_icon(self.towniconimage)

            get_text_box(self.minerswelcome[0], 30*self.fontscale, (self.WINDOW_WIDTH*0.5,self.WINDOW_HEIGHT*0.55), self.OPAQUERED)
            get_text_box(self.minerswelcome[1], 30*self.fontscale, (self.WINDOW_WIDTH*0.5,self.WINDOW_HEIGHT*0.65), self.OPAQUERED)

            rects['str_up_rect'] = pygame.Rect((self.WINDOW_WIDTH*0.44, self.WINDOW_HEIGHT*0.3), self.medium_icon)  # location, size
            self.screen.blit(self.strength_up_icon, rects['str_up_rect'])

            rects['hire_worker_rect'] = pygame.Rect((self.WINDOW_WIDTH*0.68, self.WINDOW_HEIGHT*0.3),
                                                    self.medium_icon)  # location, size
            self.screen.blit(self.hire_worker_icon, rects['hire_worker_rect'])

            rects['ShopRobotMiner_rect'] = pygame.Rect((self.WINDOW_WIDTH*0.2, self.WINDOW_HEIGHT*0.3),
                                                    self.medium_icon)
            self.screen.blit(self.ShopRobotMiner_icon, rects['ShopRobotMiner_rect'])

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
        # Game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # should be the only IF, so the game will always close first. i think
                    with open('savestate.txt', 'w') as file:
                        savestatelist = self.totalmined, self.shard, self.sshard, self.workers, self.minerstr
                        file.write(str(savestatelist))
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state == 'INTRO':
                        intro_events(rects)
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
            auto_miners()

            # Update the display
            pygame.display.flip()
            self.clock.tick(self.FPS)

playgame = systemhandler()
# Quit Pygame
pygame.quit()
sys.exit()