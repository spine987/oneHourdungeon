import pygame
import os
pygame.init()

img_battleBg = pygame.image.load(os.path.join("halfRPG","img","btlbg.png"))
img_effect = pygame.image.load(os.path.join("halfRPG","img","effect_a.png"))
img_title = pygame.image.load(os.path.join("halfRPG","img","title.png"))
img_para = pygame.image.load(os.path.join("halfRPG","img","parameter.png"))
img_dark = pygame.image.load(os.path.join("halfRPG","img","dark.png"))
img_victory = pygame.image.load(os.path.join("halfRPG","img","victory.png"))

img_effectBOrg = pygame.image.load(os.path.join("halfRPG","img","effect_b.png"))
img_wallOrg = pygame.image.load(os.path.join("halfRPG","img","wall.png"))
img_floorOrg = pygame.image.load(os.path.join("halfRPG","img","floor.png"))
img_playerOrg = [pygame.image.load(os.path.join("halfRPG","img",f"mychr{i}.png")) for i in range(0,9)]
img_boxOrg = pygame.image.load(os.path.join("halfRPG","img","tbox.png"))
img_stairOrg = pygame.image.load(os.path.join("halfRPG","img","stairs.png"))
img_cocoonOrg = pygame.image.load(os.path.join("halfRPG","img","cocoon.png"))

img_player = [pygame.transform.scale(img_playerOrg[i],(30,50)) for i in range(9)]
img_wall = pygame.transform.scale(img_wallOrg,(48,48))
img_floor = pygame.transform.scale(img_floorOrg,(48,48))
img_box = pygame.transform.scale(img_boxOrg,(48,48))
img_stair = pygame.transform.scale(img_stairOrg,(48,48))
img_cocoon =  pygame.transform.scale(img_cocoonOrg,(48,48))

#SE
se = [
    pygame.mixer.Sound(os.path.join("halfRPG","sound","ohd_se_attack.ogg")),
    pygame.mixer.Sound(os.path.join("halfRPG","sound","ohd_se_blaze.ogg")),
    pygame.mixer.Sound(os.path.join("halfRPG","sound","ohd_se_potion.ogg")),
    pygame.mixer.Sound(os.path.join("halfRPG","sound","ohd_jin_gameover.ogg")),
    pygame.mixer.Sound(os.path.join("halfRPG","sound","ohd_jin_levup.ogg")),
    pygame.mixer.Sound(os.path.join("halfRPG","sound","ohd_jin_win.ogg")),
    pygame.mixer.Sound(os.path.join("halfRPG","sound","ohd_se_open.ogg")),
    pygame.mixer.Sound(os.path.join("halfRPG","sound","ohd_se_stair.ogg")),
]

for i in range(len(se)):
    se[i].set_volume(1.8)