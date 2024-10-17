from config import *
import os

def load_img(imagefile, size):
    imageicon = pygame.image.load('Assets/'+imagefile)
    imageicon = pygame.transform.scale(imageicon, (size))
    return imageicon

class Sprite:
    def __init__(self, sprite_dir):
        self.dir_frame_list = os.listdir(sprite_dir)
        self.animation_len = len(self.dir_frame_list)
        self.is_animating = False
        self.current_frame = 0
        self.img_frame_list = []
        for frame in self.dir_frame_list:
            self.img_frame_list.append(pygame.image.load(os.path.join(sprite_dir,frame)))

    def stop_animate_Sprite(self):
        if self.is_animating:
            self.is_animating = False

    def start_animate_Sprite(self):
        if self.is_animating == False:
            self.is_animating = True

    def animate_Sprite(self):
        if self.is_animating and self.current_frame<self.animation_len:
            self.sprite_animation = self.img_frame_list[int(self.current_frame)]
            print(self.sprite_animation)
            self.current_frame+=0.1
        else:
            self.current_frame=0
            self.sprite_animation = self.img_frame_list[0]
        return self.sprite_animation

robo_boss_sprite = Sprite(r'Assets\RoboDance Animation')

introimage = pygame.image.load(r'Assets/'+'IntroScreen.jpeg')
quainttownimage = pygame.image.load(r'Assets/'+'QuaintTownSquare.png')
level1minesceneimage = pygame.image.load(r'Assets/'+'RockyMineLevel1.png')
minersguildimage = pygame.image.load(r'Assets/'+'MinersGuildInterior.png')
loadgamescreenimage = pygame.image.load(r'Assets/'+'LoadGameScreen.jpg')
backpackscreenimage = pygame.image.load(r'Assets/'+'Backpack_Background_Image.jpg')
stats_page_image = pygame.image.load(r'Assets/'+'Statistic_Background_Image.jpg')
treebuildingscene = pygame.image.load(r'Assets/'+'TreeBuilding.png')
roboworkshopbackground = pygame.image.load(r'Assets/'+'RoboWorkshop.jpg')

towniconimage = load_img('TownIcon.png', small_icon)
treebuildingicon = load_img('TreeBuilding.png', medium_icon)
level1minesceneimageicon = load_img('RockyMineLevel1.png', medium_icon)
glowingrockicon = load_img('IsolatedGlowingRockIcon.png', small_icon)
glowingrockicon2 = load_img('DarkenedIsolatedGlowingRockIcon.png', small_icon)
minersguildicon = load_img('MinersGuildLogo.png', medium_icon)
strength_up_icon = load_img('StrengthUpImage.png', medium_icon)
darkenedstrength_up_icon = load_img('DarkenedStrengthUpImage.png', medium_icon)
hire_worker_icon = load_img('HireWorkerIcon.png', medium_icon)
darkenedhire_worker_icon = load_img('DarkenedHireWorkerIcon.png', medium_icon)
DarkenedShopRobotMiner_icon = load_img('DarkenedShopRobotMiner.jpg', medium_icon)
background_glow_icon1 = load_img('GlowingLight.png', large_icon)
background_glow_icon2 = load_img('GlowingLight - Rotated1.png', large_icon)
background_glow_icon3 = load_img('GlowingLight - Rotated2.png', large_icon)
settings_icon = load_img('SettingsIcon2.png', mini_icon)
stats_icon = load_img('StatisticIcon.jpg', small_icon)
backpack_icon = load_img('BackpackImage.jpg', small_icon)

# Characters
robot_boss_image = load_img('RobotBossImage.jpg', small_icon)
ShopRobotMiner_icon = load_img('ShopRobotMiner.jpg', medium_icon)
SmallBasicDemon_icon = load_img('SmallBasicDemon.jpg', small_icon)