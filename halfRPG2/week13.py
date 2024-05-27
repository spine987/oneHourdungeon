import pygame,random,sys
from assets import *
from character import *
from pygame.locals import *

FPS = 60

MAZE_H = 10; MAZE_W = 10
DUNGEON_W = MAZE_W * 3
DUNGEON_H = MAZE_H * 3

player = Player()

def makeNewDungeon():
    global maze, dungeon

    #初始化路徑圖 & 地下城
    maze = [[0]*MAZE_W for i in range(MAZE_H)]
    dungeon = [[1]*DUNGEON_W for i in range(DUNGEON_H)]
    #使路徑圖外圍變為牆壁
    for x in range(MAZE_W):
        maze[0][x] = 1
        maze[-1][x] = 1
    for y in range(MAZE_H):
        maze[y][0] = 1
        maze[y][-1] = 1
    #使路徑圖生成柱子 & 牆壁
    XP = [-1 ,1 ,0 ,0]
    YP = [0 ,0 ,1,-1]
    for y in range(2,MAZE_H-2,2):
        for x in range(2,MAZE_W-2,2):
            maze[y][x] = 1
            d = random.randint(0,3)
            if x > 2:
                d = random.randint(1,3)
            maze[y + YP[d]][x + XP[d]] = 1
    #透過路徑圖生成地下城
    for y in range(MAZE_H):
        for x in range(MAZE_W):
            dx = x*3+1
            dy = y*3+1
            if maze[y][x] == 0:
                dungeon[dy][dx] = 0
                #道路有兩成的機率生成房間
                if random.randint(1,100) <= 20:
                    for i in range(-1,2):
                        for j in range(-1,2):
                            dungeon[dy+i][dx+j] = 0
                else:
                    if maze[y][x-1] == 0:
                        dungeon[dy][dx-1] = 0
                    if maze[y][x+1] == 0:
                        dungeon[dy][dx+1] = 0
                    if maze[y-1][x] == 0:
                        dungeon[dy-1][dx] = 0
                    if maze[y+1][x] == 0:
                        dungeon[dy+1][dx] = 0

def main():
    pygame.init()
    pygame.display.set_caption("攝影機跟隨玩家")
    screen = pygame.display.set_mode((880,720))
    clock = pygame.time.Clock()

    makeNewDungeon()

    walkCooldown = 0
    changeActCooldown = 0
    #遊戲迴圈
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            key = pygame.key.get_pressed()
            #玩家移動
            if event.type == KEYDOWN:
                if walkCooldown <= 0:
                    if key[K_LEFT] == True:
                        if player.x > 0 and dungeon[player.y][player.x
                                                             - 1] == 0:
                            walkCooldown = 8
                            player.x -= 1
                            if changeActCooldown <= 0 : 
                                player.act = 4 if player.act != 4 else 5
                                changeActCooldown = 9
                        else:
                            player.act = 4
                                    
                    if key[K_RIGHT] == True:
                        if player.x < W*3 and dungeon[player.y][player.x
                                                               + 1] == 0:
                            walkCooldown = 8
                            player.x = player.x + 1
                            if changeActCooldown <= 0 : 
                                player.act = 6 if player.act != 6 else 7
                                changeActCooldown = 9
                        else:
                            player.act = 6

                    if key[K_UP] == True:
                        if player.y > 0 and dungeon[player.y - 1][player.x
                                                                  ] == 0:
                            walkCooldown = 8
                            player.y -= 1 
                            if changeActCooldown <= 0 : 
                                player.act = 0 if player.act != 0 else 1
                                changeActCooldown = 9
                        else:
                            player.act = 0

                    if key[K_DOWN] == True:
                        if player.y < H*3 and dungeon[player.y + 1][player.x
                                                                     ] == 0:
                            walkCooldown = 8
                            player.y += 1
                            if changeActCooldown <= 0 : 
                                player.act = 2 if player.act != 2 else 3
                                changeActCooldown = 9
                        else:
                            player.act = 2
        
        #計算冷卻時間
        if changeActCooldown > 0:
            changeActCooldown -= 1

        if walkCooldown > 0:
            walkCooldown -= 1

        #顯示畫面
        for y in range(-10,11):
                for x in range(-13,14):
                    W = 48
                    H = 48
                    try:
                        if dungeon[player.y + y][player.x + x] == 0:
                            screen.blit(img_floor,[W*(x+5),H*(y+5)])
                        elif dungeon[player.y + y][player.x + x] == 1:
                            screen.blit(img_wall,[W*(x+5),H*(y+5)])
                    except:
                        screen.blit(img_wall,[W*(x+5),H*(y+5)])
                    if x == 0 and y == 0:
                        screen.blit(img_player[player.act],[W*(x+5)+7,H*(y+5)-7])
                           
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()