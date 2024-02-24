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
counter = 0 #play time

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
    center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))  # gets rect of the text shape, placed centered at a location
state = 'INTRO'
promptnumber = -1
shard = 50
sshard = 0
mouseclick = 0
minerstr = 1
str_up = 0

#Player Inventory
player_inventory = []

#Game Text
nextbuttontext = 'Next'
tuttext = ['Welcome to the Mines of Esswun!','Click the icon to mine, and gain rocks', 'Your loot is shown here',
           'and when your work is done, ', 'return to town here!']
minerswelcome = ['Welcome to the Miner\'s Guild!','Spend your shards to upgrade your mining skill']
str_upgrade_text = ['Click power +1!', 'Not enough shards!']

#Pre-Determined Locations For Repeat Items
Text_Location_Center = (WINDOW_WIDTH/2,WINDOW_HEIGHT-150)
Text_Location_Left = (160,WINDOW_HEIGHT-110)
Text_Location_Right = (WINDOW_WIDTH-150,WINDOW_HEIGHT-110)
tuttext_locations = [Text_Location_Center,
                     Text_Location_Center,
                     Text_Location_Left,
                     Text_Location_Center,
                     Text_Location_Right]

#Next Button
def draw_next_button():
    nexttext_font = pygame.font.Font(None, 40)
    nextbuttonstring = nexttext_font.render(str(nextbuttontext), True, WHITE)  # rendering text as object/image
    nextbuttontext_rect = nextbuttonstring.get_rect(
        center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50))  # gets rect of the text shape, placed centered at a location
    nextbuttontext_rect.inflate_ip(nextbuttontext_rect.width*1.2,nextbuttontext_rect.height*1.2)
    newtextspot = nextbuttonstring.get_rect(center = nextbuttontext_rect.center)
    pygame.draw.rect(screen, RED, nextbuttontext_rect) #draw red rect
    screen.blit(nextbuttonstring, newtextspot) #draw next text
    return nextbuttontext_rect

homepath=r'C:\Users\Kyle\Pictures\PyGame Assets'
workpath=r'C:\Users\kcwalina\Documents\PyGameLocalAssets'
laptop=r'C:\Users\kcwalina\Documents\PyGame-Project'
path=laptop

#Background Images
quainttownimage = pygame.image.load(path+r'\QuaintTownSquare.png')
level1minesceneimage = pygame.image.load(path+r'\RockyMineLevel1.png')
minersguildimage = pygame.image.load(path+r'\MinersGuildInterior.png')

#Icon Images
towniconimage = pygame.image.load(path+r'\TownIcon.png')
level1minesceneimageicon = pygame.image.load(path+r'\RockyMineLevel1.png')
glowingrockiconimage = pygame.image.load(path+r'\GlowingRockIcon.png')
minersguildiconimage = pygame.image.load(path+r'\MinersGuildLogo.png')
strength_up_icon = pygame.image.load(path+r'\StrengthUpImage.png')

# Drawing scene backgrounds
def draw_background(locationimage):
    background_image = pygame.transform.scale(locationimage, (WINDOW_HEIGHT,WINDOW_HEIGHT))
    background_rect = background_image.get_rect(center=(WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
    screen.blit(background_image,background_rect)

#Drawing location icons
def draw_location_icon(locationiconimage):
    return_icon_image = pygame.transform.scale(locationiconimage,(90,90))
    screen.blit(return_icon_image,set_stage_icon_rects()[0])

def draw_screen_icons(locationiconimage):
    if state == 'TUTORIAL':
        draw_location_icon(locationiconimage)
    if state == 'CAVELEVEL1':
        draw_location_icon(locationiconimage)
    if state == 'TOWN':
        townlocation_icon_image = pygame.transform.scale(minersguildiconimage, (90, 90))
        screen.blit(townlocation_icon_image, set_stage_icon_rects()[1])
        draw_location_icon(locationiconimage)
    if state == 'MINERSGUILD':
        minerslocation_icon_image = pygame.transform.scale(strength_up_icon, (120, 120))
        screen.blit(minerslocation_icon_image, set_stage_icon_rects()[2])
        draw_location_icon(locationiconimage)
    else:pass


def draw_intro():
    if state == 'INTRO':
        screen.blit(introstring, introtext_rect)  # blits the rendered text onto the rectangle that is at a location
        draw_next_button()

#Make shard
def make_click_shard(shard,sshard):
    shard+=minerstr
    sshard_chance = random.randint(1,100)
    if sshard_chance == 99:
        sshard += 1
    return shard, sshard

def draw_shardicon():
    #Shards
    shard_font = pygame.font.Font(None, 30)
    shard_string = 'Shards: '+ str(shard)
    shard_text = shard_font.render(shard_string, True, WHITE)
    shardrect = shard_text.get_rect(center=(60,550))
    screen.blit(shard_text,shardrect)

    #Special Shards
    sshard_font = pygame.font.Font(None, 30)
    sshard_string = 'Special Shards: '+ str(sshard)
    sshard_text = sshard_font.render(sshard_string, True, WHITE)
    sshardrect = sshard_text.get_rect(center=(95,580))
    screen.blit(sshard_text,sshardrect)

def draw_mainclicktarget():
    glowingrockicon = pygame.transform.scale(glowingrockiconimage, (120, 120))
    glowingrockicon_rect = glowingrockicon.get_rect(center=(400,300))
    screen.blit(glowingrockicon, glowingrockicon_rect)
    return glowingrockicon_rect

def draw_text_box(drawntext,fontsize,textlocation):
    boxtext = drawntext
    boxtextfont = pygame.font.Font(None,fontsize)
    renderedtext = boxtextfont.render(str(boxtext),True,WHITE)
    renderedrect = renderedtext.get_rect(center=textlocation) #width/2, height/2 ie.
    renderedrect.inflate_ip(renderedrect.width,renderedrect.height)
    newrenderedrect = renderedtext.get_rect(center = renderedrect.center)
    screen.blit(renderedtext,newrenderedrect)

### SCENES
def draw_tutorial():
    if state == 'TUTORIAL':
        draw_background(level1minesceneimage)
        if promptnumber < len(tuttext):
            draw_text_box(tuttext[promptnumber],35,tuttext_locations[promptnumber])
        draw_next_button()
        #draw_location_icon(towniconimage)
        draw_shardicon()
        draw_screen_icons(towniconimage)
        draw_mainclicktarget()

def draw_cavelevel1():
    if state == 'CAVELEVEL1':
        draw_background(level1minesceneimage)
        draw_shardicon()
        draw_mainclicktarget()
        draw_screen_icons(towniconimage)
        #draw_location_icon(towniconimage)

def draw_town():
    if state == 'TOWN':
        draw_background(quainttownimage)
        draw_shardicon()
        draw_screen_icons(level1minesceneimageicon)
        #draw_location_icon(level1minesceneimageicon)

def draw_miners_guild():
    if state == 'MINERSGUILD':
        draw_background(minersguildimage)
        draw_shardicon()
        draw_screen_icons(towniconimage)
        #draw_location_icon(towniconimage)
        draw_text_box(minerswelcome[0], 30, Text_Location_Center)
        draw_text_box(minerswelcome[1], 30, (400,500))
        #draw_location_icon(towniconimage)
        if str_up == 1:
            draw_text_box(str_upgrade_text[0], 30, (400, 250))
        if str_up == 2:
            draw_text_box(str_upgrade_text[1], 30, (400, 250))


# Stage Icon Rect.
def set_stage_icon_rects():
    icon_rect = pygame.Rect((WINDOW_WIDTH-95,WINDOW_HEIGHT-95),(90,90)) #location, size
    icon_rect = pygame.draw.rect(screen,CLEAR,icon_rect) #draw it

    if state == 'TOWN':
        minersguild_rect = pygame.Rect((WINDOW_WIDTH-300,WINDOW_HEIGHT-300),(90,90)) #location, size
    else: minersguild_rect = None

    if state == 'MINERSGUILD':
        minersguild_str_up_rect = pygame.Rect((WINDOW_WIDTH-450,WINDOW_HEIGHT-300),(120,120)) #location, size
    else: minersguild_str_up_rect = None

    return icon_rect, minersguild_rect, minersguild_str_up_rect

# Game loop
running = True
while running:
    # Event handling
    clock.tick(FPS)
    counter += 1 #total frame number
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #should be the only IF, so the game will always close first. i think
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #mouse_pos = pygame.mouse.get_pos()
            if draw_next_button().collidepoint(event.pos):
                if state == 'INTRO':
                    state = 'TUTORIAL'
                promptnumber += 1
                if promptnumber >= len(tuttext) and state == 'TUTORIAL':
                    state = 'CAVELEVEL1'
            elif draw_mainclicktarget().collidepoint(event.pos) and (state == 'TUTORIAL' or state == 'CAVELEVEL1'):
                shard, sshard = make_click_shard(shard,sshard)
            elif set_stage_icon_rects()[0].collidepoint(event.pos):
                if state == 'CAVELEVEL1' or state == 'MINERSGUILD':
                    state = 'TOWN'
                    #print('caught')
                elif state == 'TOWN':
                    state = 'CAVELEVEL1'
            elif set_stage_icon_rects()[1] is not None:
                if set_stage_icon_rects()[1].collidepoint(event.pos) and state == 'TOWN':
                    state = 'MINERSGUILD'
            elif set_stage_icon_rects()[2] is not None:
                if set_stage_icon_rects()[2].collidepoint(event.pos) and state == 'MINERSGUILD':
                    if shard >= 50:
                        shard -= 50
                        minerstr += 1
                        str_up = 1 # (1 for yes, generate success text)
                    else:
                        str_up = 2 # (2 for no)

    # Clear the screen
    screen.fill(CLEAR) # Passively fills all blank space. Catch-all just in case

    draw_intro()
    draw_tutorial()
    draw_cavelevel1()
    draw_town()
    draw_miners_guild()
    #draw_screen_icons()

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
