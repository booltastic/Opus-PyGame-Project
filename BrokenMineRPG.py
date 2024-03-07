import pygame
import sys
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Set up the display
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Practice Clicker Game")
clock = pygame.time.Clock()
FPS = 30
timecounter = 0
counter = 0 #play time
timer = 0


#Set Colors
CLEAR = (0,0,0,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
LIBLUE=(0,128,255)

#Global Variables
titlestring = 'The Clicker Game'
text_font = pygame.font.Font(None, 50)
introstring = 'Welcome to Mine.Cafe!'
introstring = text_font.render(str(introstring), True, WHITE)  # rendering text as object/image
introtext_rect = introstring.get_rect(
    center=(WINDOW_WIDTH // 2, ((WINDOW_HEIGHT // 2)-100))) # gets rect of the text shape, placed centered at a location
state = 'INTRO'
promptnumber = 0
shard = 0
sshard = 0
mouseclick = 0
minerstr = 1
str_up = 0
workers = 0
worker_hired = 0

def get_cost():
    minerstrcost = int(minerstr*25)
    workercost= int(workers*1.75)+5
    str_upgrade_text = ['Click power +1!', 'Not enough shards! (Costs ' + str(minerstrcost) + ')']
    worker_hired_text = ['Worker speed increased!', 'Not enough Special Shards! (Costs ' + str(workercost) + ')']
    return minerstrcost, workercost,str_upgrade_text,worker_hired_text
costs_and_texts=get_cost()

#Player Inventory
player_inventory = []

#Game Text
nextbuttontext = 'Next'
tuttext = ['Welcome to the Mines of Esswun!','Click the icon to mine, and gain rocks', 'Your loot is shown here',
           'and when your work is done, ', 'return to town here!']
minerswelcome = ['Welcome to the Miner\'s Guild!','Spend your shards to upgrade your mining skill']
newgametext = ['Load saved game?','New Game','Load Game']

#Pre-Determined Locations For Repeat Items
Text_Location_Center = (WINDOW_WIDTH/2,WINDOW_HEIGHT-150)
Text_Location_Left = (160,WINDOW_HEIGHT-110)
Text_Location_Right = (WINDOW_WIDTH-150,WINDOW_HEIGHT-110)
tuttext_locations = [Text_Location_Center,
                     Text_Location_Center,
                     Text_Location_Left,
                     Text_Location_Center,
                     Text_Location_Right]

#Background Images
quainttownimage = pygame.image.load('QuaintTownSquare.png')
level1minesceneimage = pygame.image.load('RockyMineLevel1.png')
minersguildimage = pygame.image.load('MinersGuildInterior.png')

#Icon Images
towniconimage = pygame.image.load('TownIcon.png')
level1minesceneimageicon = pygame.image.load('RockyMineLevel1.png')
glowingrockiconimage = pygame.image.load('GlowingRockIcon.png')
minersguildiconimage = pygame.image.load('MinersGuildLogo.png')
strength_up_icon = pygame.image.load('StrengthUpImage.png')
hire_worker_icon = pygame.image.load('HireWorkerIcon.png')

def game_timer(counter):
    counter += 1
    return counter

# Drawing scene backgrounds
def draw_background(locationimage):
    background_image = pygame.transform.scale(locationimage, (WINDOW_HEIGHT,WINDOW_HEIGHT))
    background_rect = background_image.get_rect(center=(WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
    screen.blit(background_image,background_rect)

#Next Button
def draw_next_button():
    nexttext_font = pygame.font.Font(None, 40)
    nextbuttonstring = nexttext_font.render(str(nextbuttontext), True, WHITE)  # rendering text as object/image
    nextbutton_rect = nextbuttonstring.get_rect(
        center=(WINDOW_WIDTH // 2 , WINDOW_HEIGHT - 50))  # gets rect of the text shape, placed at a location
    nextbutton_rect = nextbutton_rect.inflate(nextbutton_rect.width*1.2,nextbutton_rect.height*1.2) #inflated to clickable size
    buttontextspot = nextbuttonstring.get_rect(center = nextbutton_rect.center)
    pygame.draw.rect(screen, BLUE, nextbutton_rect) #draw rect
    screen.blit(nextbuttonstring, buttontextspot) #draw next text
    return nextbutton_rect

#Drawing location icons
def draw_location_icon(locationiconimage):
    icon_rect = pygame.Rect((WINDOW_WIDTH-95,WINDOW_HEIGHT-95),(90,90)) #location, size
    pygame.draw.rect(screen,CLEAR,icon_rect) #draw it. currently drawn off screen (beside background)
    return_icon_image = pygame.transform.scale(locationiconimage,(90,90))
    screen.blit(return_icon_image,icon_rect)

# def draw_screen_icons(locationiconimage):
#     if state == 'TUTORIAL':
#         draw_location_icon(locationiconimage)
#     if state == 'CAVELEVEL1':
#         draw_location_icon(locationiconimage)
#     if state == 'TOWN':
#         townlocation_icon_image = pygame.transform.scale(minersguildiconimage, (90, 90))
#         screen.blit(townlocation_icon_image, set_stage_icon_rects()[1])
#         draw_location_icon(locationiconimage)
#
#     if state == 'MINERSGUILD':
#         strength_up_icon_image = pygame.transform.scale(strength_up_icon, (120, 120))
#         screen.blit(strength_up_icon_image, set_stage_icon_rects()[2])
#
#         hire_worker_icon_image = pygame.transform.scale(hire_worker_icon, (120, 120))
#         screen.blit(hire_worker_icon_image, set_stage_icon_rects()[3])
#
#         draw_location_icon(locationiconimage)
#     else:pass

#Make shard
def make_click_shard(shard,sshard):
    shard+=(minerstr/2)
    sshard_chance = random.randint(1,300)
    if sshard_chance >= (300-minerstr):
        if minerstr < 10:
            sshard += 1
    if minerstr >= 15:
            sshard += 2
    return shard, sshard

def auto_miners(shard,sshard,workers):
    if workers >= 1:
        shard += workers/30
        sshard_chance = random.randint(1, 3000)
        if sshard_chance >= (3000-(workers)):
            sshard += 1
    return shard, sshard

def draw_shardicon():
    #Shards
    shard_font = pygame.font.Font(None, 30)
    shard_string = 'Shards: '+ str(int(shard))
    shard_text = shard_font.render(shard_string, True, WHITE)
    shardrect = shard_text.get_rect(center=(60,550))
    screen.blit(shard_text,shardrect)

    #Special Shards
    sshard_font = pygame.font.Font(None, 30)
    sshard_string = 'Special Shards: '+ str(int(sshard))
    sshard_text = sshard_font.render(sshard_string, True, WHITE)
    sshardrect = sshard_text.get_rect(center=(95,580))
    screen.blit(sshard_text,sshardrect)

def draw_mainclicktarget():
    glowingrockicon = pygame.transform.scale(glowingrockiconimage, (120, 120))
    glowingrockicon_rect = glowingrockicon.get_rect(center=(400,300))
    screen.blit(glowingrockicon, glowingrockicon_rect)
    return glowingrockicon_rect

def get_text_box(drawntext,fontsize,textlocation,color): #made for rects loops
    boxtext = drawntext
    boxtextfont = pygame.font.Font(None,fontsize)
    renderedtext = boxtextfont.render(str(boxtext),True,WHITE) #renders text image
    colliderect = renderedtext.get_rect(center=textlocation) # create rect the size of the text at chosen location. sets ratio of size, and where we want the center
    colliderect = colliderect.inflate(colliderect.width*0.15,colliderect.height) # inflate that rect in place to twice its size, this is what gets clicked
    pygame.draw.rect(screen, color, colliderect) # draws the rect renderedrect, this cannot be passed to collidepoint though (just drawing it)
    renderedtextrect = renderedtext.get_rect(center = colliderect.center) # this rect is creating a text sized rect and placing it at the center of the big rect, so its already centered. used for collide and blit. if blit
    screen.blit(renderedtext,renderedtextrect)
    return colliderect #if applicable. only used if you need to click it


### SCENES ###

def draw_scene(sceneinput): #argument passed through is State
    if sceneinput == 'INTRO':
        return intro_rects_and_images() #these return rect dicts where each item should be a rect. draw_scene is equal to versatile rects now
    if sceneinput == 'TUTORIAL':
        return tutorial_rects_and_images()

# def set_events(sceneinput):
#     if sceneinput == 'INTRO':
#         intro_events(sceneinput)
#     if sceneinput == 'TUTORIAL':
#         tutorial_events(sceneinput)
def intro_rects_and_images():
    rects={}
    rects['new_game_prompt_rect'] = get_text_box(newgametext[0],40,(WINDOW_WIDTH-400,WINDOW_HEIGHT-300), RED) #tuple of 4, with 3 rects: 2 for draw, 1 for collide
    rects['new_game_rect'] = get_text_box(newgametext[1],40, (WINDOW_WIDTH-600,WINDOW_HEIGHT-200), RED)
    rects['load_game_rect'] = get_text_box(newgametext[2],40, (WINDOW_WIDTH-250,WINDOW_HEIGHT-200), RED)
    screen.blit(introstring, introtext_rect)  # blits the rendered text onto the rectangle that is at a location

    #functions for other scene elements can go here, and isolate the rects for collide function
    return rects

def change_state(new_state):
    global state
    state = new_state

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
                    shard, sshard, workers, minerstr = float(content[0]), float(content[1]), float(content[2]), float(
                        content[3])
                    change_state('TOWN')
            except FileNotFoundError:
                pass

def tutorial_rects_and_images():
    rects={}
    rects['screenbackground']=draw_background(level1minesceneimage)
    rects['returnicon'] = pygame.transform.scale(towniconimage, (90, 90))
    if promptnumber < len(tuttext):
        get_text_box(tuttext[promptnumber],35,tuttext_locations[promptnumber], RED)
    rects['shardicon']=draw_shardicon()
    rects['mainclicktarget']=draw_mainclicktarget()
    rects['next_button']=draw_next_button()
    rects['corner_location_icon']=draw_location_icon(towniconimage)
    return rects

# def draw_tutorial():
#     if state == 'TUTORIAL':
#
#         draw_background(level1minesceneimage)
#         draw_shardicon()
#         draw_mainclicktarget()
#         draw_location_icon(towniconimage)
#         draw_next_button()

def tutorial_events(rects):
    if rects['next_button'].collidepoint(event.pos):
        increment_number()
        if promptnumber >= len(tuttext):
            change_state('CAVELEVEL1')

def increment_number():
    global promptnumber
    promptnumber += 1

rects=draw_scene('INTRO')

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #should be the only IF, so the game will always close first. i think
            with open('savestate.txt','w') as file:
                savestatelist = shard,sshard,workers,minerstr
                file.write(str(savestatelist))
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if state == 'INTRO':
                intro_events(rects)
            elif state == 'TUTORIAL':
                tutorial_events(rects)
            # elif draw_mainclicktarget().collidepoint(event.pos) and (state == 'TUTORIAL' or state == 'CAVELEVEL1'):
            #     shard, sshard = make_click_shard(shard,sshard)
            #
            # if stage_rects[0].collidepoint(event.pos):
            #     if state == 'CAVELEVEL1' or state == 'MINERSGUILD':
            #         state = 'TOWN'
            #     elif state == 'TOWN':
            #         state = 'CAVELEVEL1'
            # elif stage_rects[1] is not None:
            #     if stage_rects[1].collidepoint(event.pos) and state == 'TOWN':
            #         state = 'MINERSGUILD'
            # elif stage_rects[2] is not None:
            #     if stage_rects[2].collidepoint(event.pos) and state == 'MINERSGUILD':
            #         timer = 0
            #         worker_hired = 0
            #         if shard >= get_cost()[0]:
            #             shard -= get_cost()[0]
            #             minerstr += 1
            #             str_up = 1 # (1 for yes, generate success text)
            #         else:
            #             str_up = 2 # (2 for no)
            # elif stage_rects[3] is not None: #elif only runs where everything preceding it (until first if) is False
            #     if stage_rects[3].collidepoint(event.pos) and state == 'MINERSGUILD':
            #         timer = 0
            #         str_up = 0
            #         if sshard >= get_cost()[1]:
            #             sshard -= get_cost()[1]
            #             worker_hired = 1
            #             workers += 1
            #         else:
            #             worker_hired = 2
            #print(workers)

    # Clear the screen
    screen.fill(CLEAR) # Passively fills all blank space. Catch-all just in case

    # Event handling
    #stage_rects = set_stage_icon_rects()
    counter = game_timer(counter) #total frame number

    rects=draw_scene(state)
    # str_up, counter, timer, worker_hired = draw_miners_guild(str_up,counter,timer, worker_hired)
    # shard,sshard=auto_miners(shard,sshard,workers)
    #print(worker_hired)
    # Update the display
    pygame.display.flip()
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()

# def draw_cavelevel1():
#     if state == 'CAVELEVEL1':
#         draw_background(level1minesceneimage)
#         draw_shardicon()
#         draw_mainclicktarget()
#         draw_screen_icons(towniconimage)
#
# def draw_town():
#     if state == 'TOWN':
#         draw_background(quainttownimage)
#         draw_shardicon()
#         draw_screen_icons(level1minesceneimageicon)
#
# def draw_miners_guild(str_up,counter,timer, worker_hired):
#     if state == 'MINERSGUILD':
#         draw_background(minersguildimage)
#         draw_shardicon()
#         draw_screen_icons(towniconimage)
#
#         costs_and_texts = get_cost()
#
#         if str_up == 1:
#             draw_text_box(costs_and_texts[2][0], 30, (400, 250),RED)
#             timer += 1
#             worker_hired=0
#             if timer >= 90:
#                 str_up, timer = 0, 0
#         elif str_up == 2:
#             draw_text_box(costs_and_texts[2][1], 30, (400, 250),RED)
#             timer += 1
#             if timer >= 90:
#                 str_up, timer = 0, 0
#         if worker_hired == 1:
#             draw_text_box(costs_and_texts[3][0], 30, (400, 250),RED)
#             timer += 1
#             str_up = 0
#             if timer >= 90:
#                 worker_hired, timer = 0, 0
#         elif worker_hired == 2:
#             draw_text_box(costs_and_texts[3][1], 30, (400, 250),RED)
#             timer += 1
#             str_up = 0
#             if timer >= 90:
#                 worker_hired, timer = 0, 0
#     return str_up, counter, timer, worker_hired
#
# def town_rects():
#     if state == 'TOWN':
#         minersguild_rect = pygame.Rect((WINDOW_WIDTH-300,WINDOW_HEIGHT-300),(90,90)) #location, size
#         return minersguild_rect
#
# def miners_guild_rects():
#     get_text_box(minerswelcome[0], 30, Text_Location_Center, RED)
#     get_text_box(minerswelcome[1], 30, (400, 500), RED)
#     minersguild_str_up_rect = pygame.Rect((WINDOW_WIDTH - 450, WINDOW_HEIGHT - 300), (120, 120))  # location, size
#     hire_worker_icon_rect = pygame.Rect((WINDOW_WIDTH - 250, WINDOW_HEIGHT - 300), (120, 120))  # location, size
#     return minersguild_str_up_rect, hire_worker_icon_rect