import pygame
import sys
import random
#from intro_scene import *

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
towniconimage = pygame.transform.scale(towniconimage, (90, 90))

level1minesceneimageicon = pygame.image.load('RockyMineLevel1.png')
level1minesceneimageicon = pygame.transform.scale(level1minesceneimageicon, (90, 90))

glowingrockicon = pygame.image.load('GlowingRockIcon.png')
glowingrockicon = pygame.transform.scale(glowingrockicon, (120, 120))

minersguildicon = pygame.image.load('MinersGuildLogo.png')
minersguildicon = pygame.transform.scale(minersguildicon, (90, 90))

strength_up_icon = pygame.image.load('StrengthUpImage.png')
strength_up_icon = pygame.transform.scale(strength_up_icon, (120, 120))

hire_worker_icon = pygame.image.load('HireWorkerIcon.png')
hire_worker_icon = pygame.transform.scale(hire_worker_icon, (120, 120))

def game_timer():
    global counter
    counter += 1
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
    return icon_rect
#Make shard
def make_click_shard():
    global shard, sshard
    shard+=(minerstr/2)
    sshard_chance = random.randint(1,300)
    if sshard_chance >= (300-minerstr):
        if minerstr < 10:
            sshard += 1
    if minerstr >= 15:
            sshard += 2
def auto_miners():
    global shard, sshard
    if workers >= 1:
        shard += workers/60
        sshard_chance = random.randint(1, 3000)
        if sshard_chance >= (3000-(workers)):
            sshard += 1
def get_cost():
    global minerstr, workers
    cost_texts={}
    minerstrcost = int(minerstr*25)
    workercost = int(workers*1.75)+5
    cost_texts['str_upgrade_text'] = ['Click power +1!', 'Not enough shards! (Costs ' + str(minerstrcost) + ')']
    cost_texts['worker_hired_text'] = ['Worker speed increased!', 'Not enough Special Shards! (Costs ' + str(workercost) + ')']
    return minerstrcost, workercost,cost_texts
cost_texts=get_cost()[2]

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
    global glowingrockicon
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
def change_state(new_state):
    global state
    state = new_state
def draw_scene(sceneinput): #argument passed through is State
    if sceneinput == 'INTRO':
        return intro_rects_and_images() #these return rect dicts where each item should be a rect. draw_scene is equal to versatile rects now
    if sceneinput == 'TUTORIAL':
        return tutorial_rects_and_images()
    if sceneinput == 'MINELEVEL1':
        return mine_level_1_rects_and_images()
    if sceneinput == 'TOWN':
        return town_rects_and_images()
    if sceneinput == 'MINERSGUILD':
        return miners_guild_rects_and_images()
def intro_rects_and_images():
    rects={}
    get_text_box(newgametext[0],40,(WINDOW_WIDTH-400,WINDOW_HEIGHT-300), RED) #tuple of 4, with 3 rects: 2 for draw, 1 for collide
    rects['new_game_rect'] = get_text_box(newgametext[1],40, (WINDOW_WIDTH-600,WINDOW_HEIGHT-200), BLUE)
    rects['load_game_rect'] = get_text_box(newgametext[2],40, (WINDOW_WIDTH-250,WINDOW_HEIGHT-200), BLUE)
    screen.blit(introstring, introtext_rect)  # blits the rendered text onto the rectangle that is at a location

    #functions for other scene elements can go here, and isolate the rects for collide function
    return rects
def intro_events(rects):
    global shard, sshard, workers, minerstr
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
def tutorial_rects_and_images(): #where basically everything is drawn and established
    rects={}
    draw_background(level1minesceneimage)
    if promptnumber < len(tuttext):
        get_text_box(tuttext[promptnumber],35,tuttext_locations[promptnumber], RED)
    draw_shardicon()
    draw_location_icon(towniconimage)
    draw_mainclicktarget()
    rects['next_button']=draw_next_button()
    return rects
def tutorial_events(rects):
    if rects['next_button'].collidepoint(event.pos):
        increment_number()
        if promptnumber >= len(tuttext):
            change_state('MINELEVEL1')
def mine_level_1_rects_and_images():
    rects={}
    draw_background(level1minesceneimage)
    draw_shardicon()
    rects['mainclicktarget']=draw_mainclicktarget()
    rects['corner_location_icon']=draw_location_icon(towniconimage)
    return rects
def mine_level_1_events(rects):
    if rects['corner_location_icon'].collidepoint(event.pos):
        change_state('TOWN')
    if rects['mainclicktarget'].collidepoint(event.pos):
        make_click_shard()
def town_rects_and_images():
    rects={}
    draw_background(quainttownimage)
    draw_shardicon()
    rects['corner_location_icon']=draw_location_icon(level1minesceneimageicon)
    rects['minersguild_rect'] = pygame.Rect((WINDOW_WIDTH - 300, WINDOW_HEIGHT - 300), (90, 90))  # location, size
    screen.blit(minersguildicon, rects['minersguild_rect'])
    return rects
def town_events(rects):
    if rects['corner_location_icon'].collidepoint(event.pos):
        change_state('MINELEVEL1')
    if rects['minersguild_rect'].collidepoint(event.pos):
        change_state('MINERSGUILD')
def miners_guild_rects_and_images():
    global shard, sshard, timer, worker_hired, workers, minerstr, str_up
    rects={}
    draw_background(minersguildimage)
    draw_shardicon()
    rects['corner_location_icon']=draw_location_icon(towniconimage)

    get_text_box(minerswelcome[0], 30, Text_Location_Center, RED)
    get_text_box(minerswelcome[1], 30, (400, 500), RED)

    rects['str_up_rect'] = pygame.Rect((WINDOW_WIDTH - 450, WINDOW_HEIGHT - 300), (120, 120))  # location, size
    screen.blit(strength_up_icon, rects['str_up_rect'])
    rects['hire_worker_rect'] = pygame.Rect((WINDOW_WIDTH - 250, WINDOW_HEIGHT - 300), (120, 120))  # location, size
    screen.blit(hire_worker_icon, rects['hire_worker_rect'])

    if str_up == 1:
        get_text_box(cost_texts['str_upgrade_text'][0], 30, (400, 250),RED)
        timer += 1
        worker_hired=0
        if timer >= 90:
            str_up, timer = 0, 0
    elif str_up == 2:
        get_text_box(cost_texts['str_upgrade_text'][1], 30, (400, 250),RED)
        timer += 1
        if timer >= 90:
            str_up, timer = 0, 0
    if worker_hired == 1:
        get_text_box(cost_texts['worker_hired_text'][0], 30, (400, 250),RED)
        timer += 1
        str_up = 0
        if timer >= 90:
            worker_hired, timer = 0, 0
    elif worker_hired == 2:
        get_text_box(cost_texts['worker_hired_text'][1], 30, (400, 250),RED)
        timer += 1
        str_up = 0
        if timer >= 90:
            worker_hired, timer = 0, 0
    return rects
def miners_guild_events(rects):
    global shard, sshard, timer, worker_hired, workers, minerstr, str_up
    if rects['str_up_rect'].collidepoint(event.pos):
        timer = 0
        worker_hired = 0
        if shard >= get_cost()[0]:
            shard -= get_cost()[0]
            minerstr += 1
            str_up = 1 # (1 for yes, generate success text)
        else:
            str_up = 2 # (2 for no)

    if rects['hire_worker_rect'].collidepoint(event.pos):
        timer = 0
        str_up = 0

        if sshard >= get_cost()[1]:
            sshard -= get_cost()[1]
            worker_hired = 1
            workers += 1
        else:
            worker_hired = 2
    if rects['corner_location_icon'].collidepoint(event.pos):
        change_state('TOWN')
        str_up = 0
        worker_hired = 0

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
            elif state == 'TOWN':
                town_events(rects)
            elif state == 'MINELEVEL1':
                mine_level_1_events(rects)
            elif state == 'MINERSGUILD':
                miners_guild_events(rects)
    # Clear the screen
    screen.fill(CLEAR) # Passively fills all blank space. Catch-all just in case

    # Event handling
    game_timer() #total frame number
    rects=draw_scene(state)
    auto_miners()

    # Update the display
    pygame.display.flip()
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()