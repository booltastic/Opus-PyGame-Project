

screen_res = 'small'
if screen_res == 'medium':
    WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 900
    fontscale = 1
elif screen_res == 'large':
    WINDOW_WIDTH, WINDOW_HEIGHT = 1600, 1200
    fontscale = 2.5
else:
    WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
    fontscale = 0.7

mini_icon = (WINDOW_HEIGHT * 0.1, WINDOW_HEIGHT * 0.1)
small_icon = (WINDOW_HEIGHT * 0.15, WINDOW_HEIGHT * 0.15)
medium_icon = (WINDOW_HEIGHT * 0.2, WINDOW_HEIGHT * 0.2)
large_icon = (WINDOW_HEIGHT * 0.5, WINDOW_HEIGHT * 0.5)

# Pre-Determined Locations For Repeat Items
Text_Location_TalkCenter = (WINDOW_WIDTH * 0.35, WINDOW_HEIGHT * 0.755)
Text_Location_Center = (WINDOW_WIDTH*0.5 , WINDOW_HEIGHT*0.7)
Text_Location_Left = (WINDOW_WIDTH*0.22, WINDOW_HEIGHT*0.7)
Text_Location_Right = (WINDOW_WIDTH*0.78, WINDOW_HEIGHT*0.76)
screen_center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)