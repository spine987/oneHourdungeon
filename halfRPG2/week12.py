import pygame
import random,sys
from assets import *
from pygame.locals import *

player_x = 4
player_y = 4

MAZE_H = 10; MAZE_W = 10
DUNGEON_W = MAZE_W * 3
DUNGEON_H = MAZE_H * 3

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
    global player_x,player_y
    pygame.init()
    pygame.display.set_caption("生成迷宮")
    screen = pygame.display.set_mode((750,750))
    clock = pygame.time.Clock()

    makeNewDungeon()
    #遊戲迴圈
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            #玩家移動
            key = pygame.key.get_pressed()
            if event.type == KEYDOWN:
                if key[K_LEFT] == True:
                    if player_x > 0 and dungeon[player_y][player_x - 1] == 0:
                        player_x -= 1
                if key[K_RIGHT] == True:
                    if player_x < W*3 and dungeon[player_y][player_x + 1] == 0:
                        player_x += 1
                if key[K_UP] == True:
                    if player_y > 0 and dungeon[player_y - 1][player_x] == 0:
                        player_y -= 1
                if key[K_DOWN] == True:
                    if player_y < H*3 and dungeon[player_y + 1][player_x] == 0:
                        player_y += 1

        #顯示畫面
        W = 25
        H = 25
        for y in range(DUNGEON_H):
            for x in range(DUNGEON_W):
                if dungeon[y][x] == 0:
                    screen.blit(img_floor,[x*W, y*H])
                if dungeon[y][x] == 1:
                    screen.blit(img_wall,[x*W, y*H])
                if player_x == x and player_y == y:
                    screen.blit(img_player[2],[x*W+2, y*H-6])
                           
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()