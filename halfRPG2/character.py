import pygame,random,os

class Player():
    def __init__(self,lv=1,maxexp=30,exp=0,maxhp=100,atk=10,x=4,y=4,act=2,food=100,potion=0,blazegem=0):
        self.lv = lv
        self.maxexp = maxexp
        self.exp = exp
        self.maxhp = maxhp
        self.hp = maxhp
        self.atk = atk
        self.x = x
        self.y = y
        self.act = act
        self.food = food
        self.potion = potion
        self.blazegem = blazegem

    def init(self,lv=1,maxexp=20,exp=0,maxhp=100,atk=10,x=4,y=4,act=2,food=100,potion=0,blazegem=0):
        self.lv = lv
        self.maxexp = maxexp
        self.exp = exp
        self.maxhp = maxhp
        self.hp = maxhp
        self.atk = atk
        self.x = x
        self.y = y
        self.act = act
        self.food = food
        self.potion = potion
        self.blazegem = blazegem

    def levelUp(self):
        self.lv += 1
        self.exp = 0
        self.maxexp += self.lv * 5
        self.maxhp += self.lv * 5
        self.hp = self.maxhp
        self.atk += self.lv

class Monster():
    def __init__(self,lv=0,img=1):
        self.lv = lv
        self.exp = self.lv * 5 + 15
        self.maxhp = self.lv * 10 + 20
        self.hp = self.maxhp
        self.atk = self.lv * 5 + 7
        self.img = pygame.image.load(os.path.join("halfRPG","img",f"enemy{img}.png"))
        self.x = 440 - self.img.get_width() / 2
        self.y = 560 - self.img.get_height()
        self.step = 0
        self.blink = 0
        self.eff = 0

    def init(self,floor):
        self.lv = max(1,random.randint(floor-1,floor+1))
        self.exp = self.lv * 5 + 15
        self.maxhp = self.lv * 10 + 20
        self.hp = self.maxhp
        self.atk = self.lv * 5 + 7
        self.img = pygame.image.load(os.path.join("halfRPG","img",f"enemy{min(floor,random.randint(1,floor+1))}.png"))
        self.x = 440 - self.img.get_width() / 2
        self.y = 560 - self.img.get_height()
        self.step = 0
        self.blink = 0
        self.eff = 0
        self.isboss = False

    def boss(self,floor):
        self.lv = floor + 2 
        self.exp = self.lv * 5 + 15
        self.maxhp = self.lv * 10 + 200
        self.hp = self.maxhp
        self.atk = self.lv * 3
        self.img = pygame.image.load(os.path.join("halfRPG","img","enemy9.png"))
        self.x = 440 - self.img.get_width() / 2
        self.y = 560 - self.img.get_height()
        self.step = 0
        self.blink = 0
        self.eff = 0
        self.isBoss = True
