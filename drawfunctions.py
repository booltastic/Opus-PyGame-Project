import pygame
from config import *
from images import *
from gamedata import *

def draw_inventory():
    shard_string = 'Shards: ' + str(int(GameData.shard))
    get_text_box(shard_string, 35, (WINDOW_WIDTH * 0.5, WINDOW_HEIGHT * 0.5), BLACK, 'center', 1)

    # Special Shards
    sshard_string = 'Special Shards: ' + str(int(GameData.sshard))
    get_text_box(sshard_string, 35, (WINDOW_WIDTH * 0.5, WINDOW_HEIGHT * 0.6), BLACK, 'center', 1)


def draw_statistics():
    # Shards
    totalmined_string = 'Total Shards Mined: ' + str(int(GameData.totalmined))
    get_text_box(totalmined_string, 35, (WINDOW_WIDTH * 0.5, WINDOW_HEIGHT * 0.4), BLACK, 'center', 1)

    # # Workers
    worker_string = 'Workers: ' + str(int(GameData.workers))
    get_text_box(worker_string, 35, (WINDOW_WIDTH * 0.5, WINDOW_HEIGHT * 0.5), BLACK, 'center', 1)
    #
    # # Mining Strength
    minestr_string = 'Mining Strength: ' + str(int(GameData.minerstr))
    get_text_box(minestr_string, 35, (WINDOW_WIDTH * 0.5, WINDOW_HEIGHT * 0.6), BLACK, 'center', 1)

def draw_mainclicktarget():
    get_mouse_status()
    timer = int(GameData.counter / 3)
    for i in range(0, 1):
        if timer % 3 == i:
            glowing_background_rect = background_glow_icon1.get_rect(center=screen_center)
            screen.blit(background_glow_icon1, glowing_background_rect)
    for i in range(1, 2):
        if timer % 3 == i:
            glowing_background_rect = background_glow_icon2.get_rect(center=screen_center)
            screen.blit(background_glow_icon2, glowing_background_rect)
    for i in range(2, 3):
        if timer % 3 == i:
            glowing_background_rect = background_glow_icon3.get_rect(center=screen_center)
            screen.blit(background_glow_icon3, glowing_background_rect)

    glowingrockicon_rect = glowingrockicon.get_rect(center=screen_center)
    darken_on_click(glowingrockicon_rect, glowingrockicon, glowingrockicon2)

    return glowingrockicon_rect


def get_text_box(drawntext, fontsize, textlocation, color, alignment='center', vertboxscale=float(1),
                 horiboxscale=float(0.15)):  # made for rects loops
    boxtext = drawntext
    boxtextfont = pygame.font.Font(None, int(fontsize * (fontscale)))
    renderedtext = boxtextfont.render(str(boxtext), True, WHITE)  # renders text image
    if alignment == 'left':
        colliderect = renderedtext.get_rect(
            midleft=textlocation)  # create rect the size of the text at chosen location. sets ratio of size, and where we want the center
    else:
        colliderect = renderedtext.get_rect(
            center=textlocation)
    colliderect = colliderect.inflate(colliderect.width * horiboxscale,
                                      colliderect.height * vertboxscale)  # inflate that rect in place to twice its size, this is what gets clicked
    # pygame.draw.rect(self.screen, color,
    #                  colliderect)  # draws the rect renderedrect, this cannot be passed to collidepoint though (just drawing it)
    renderedtextrect = renderedtext.get_rect(
        center=colliderect.center)  # this rect is creating a text sized rect and placing it at the center of the big rect, so its already centered.
    surface = pygame.Surface(colliderect.size, pygame.SRCALPHA)
    pygame.draw.rect(surface, color,
                     surface.get_rect())
    screen.blit(surface, colliderect)
    screen.blit(renderedtext, renderedtextrect)
    return colliderect  # if applicable. only used if you need to click it

def draw_background(locationimage):
    background_image = pygame.transform.scale(locationimage, (WINDOW_HEIGHT, WINDOW_HEIGHT))
    background_rect = background_image.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
    screen.blit(background_image, background_rect)

#Draw settings icon
def draw_settings_icon():
    if GameData.counter>60:
        settings_rect = settings_icon.get_rect(center=(WINDOW_WIDTH * 0.937, WINDOW_HEIGHT * 0.065))
        screen.blit(settings_icon, settings_rect)
        return settings_rect

# Next Button
def draw_button(buttontext, buttonheight=0.95):
    text_font = pygame.font.Font(None, int(40*fontscale))
    buttonstring = text_font.render(str(buttontext), True, WHITE)  # rendering text as object/image
    button_rect = buttonstring.get_rect(
        center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT*buttonheight))  # gets rect of the text shape, placed at a location
    button_rect = button_rect.inflate(button_rect.width * 1.2,button_rect.height * 1.2)  # inflated to clickable size
    buttontextspot = buttonstring.get_rect(center=button_rect.center)
    pygame.draw.rect(screen, BLUE, button_rect)  # draw rect
    screen.blit(buttonstring, buttontextspot)  # draw next text
    return button_rect

def draw_next_button():
    button_rect=draw_button('Next')
    return button_rect

def draw_fight_button():
    button_rect=draw_button('Fight',0.85)
    return button_rect

def draw_back_button():
    button_rect=draw_button('Back')
    return button_rect

# Drawing location icons
def draw_location_icon(locationiconimage):
    icon_rect = pygame.Rect((WINDOW_WIDTH*0.8822, WINDOW_HEIGHT*0.843), (small_icon))  # location, size
    return_icon_image = pygame.transform.scale(locationiconimage, (small_icon))
    screen.blit(return_icon_image, icon_rect)
    return icon_rect

def draw_speaker_icon(speakerimage):
    speaker_rect = pygame.Rect((WINDOW_WIDTH * 0.22, WINDOW_HEIGHT * 0.68),
                                (small_icon))  # location, size
    speaker_icon_image = pygame.transform.scale(speakerimage, (small_icon))
    screen.blit(speaker_icon_image, speaker_rect)

def draw_backpack_icon():
    #if state not in ('INTRO', 'SETTINGS', 'LOADGAME'):
    backpack_rect = pygame.Rect((WINDOW_WIDTH * 0.006, WINDOW_HEIGHT * 0.68),(small_icon))  # location, size
    backpack_icon_image = pygame.transform.scale(backpack_icon, (small_icon))
    screen.blit(backpack_icon_image, backpack_rect)
    return backpack_rect

def draw_stats_icon():
    # if state not in ('INTRO', 'SETTINGS', 'LOADGAME'):
    statistics_rect = pygame.Rect((WINDOW_WIDTH * 0.006, WINDOW_HEIGHT * 0.84),
                            (small_icon))  # location, size
    statistics_icon_image = pygame.transform.scale(stats_icon, (small_icon))
    screen.blit(statistics_icon_image, statistics_rect)
    return statistics_rect

def get_mouse_status():
    mouse_clicked = pygame.mouse.get_pressed()[0] #continuously is checking each frame
    mouse_pos = pygame.mouse.get_pos()
    return mouse_clicked, mouse_pos

def darken_on_click( rect, icon, darkenedicon):
    mouse_clicked,mouse_pos=get_mouse_status()
    if mouse_clicked and rect.collidepoint(mouse_pos):
        screen.blit(darkenedicon, rect)
    else:
        screen.blit(icon, rect)