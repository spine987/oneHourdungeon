import pygame,random,sys
from assets import *
from character import *
from pygame.locals import *

FPS = 60
tmr = 0

MAZE_H = 10; MAZE_W = 10
DUNGEON_W = MAZE_W * 3
DUNGEON_H = MAZE_H * 3

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)

BLINK = [(224,255,255), (224,255,255), (224,255,255), (192,240,255), (192,240,255), (192,240,255),\
         (128,224,255), (128,224,255), (128,224,255), (64,192,255), (64,192,255), (64,192,255),\
         (128,224,255), (128,224,255), (128,224,255), (192,240,255), (192,240,255), (192,240,255),]

player = Player()
enemy = Monster()

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

def init_message():
    global messageList
    messageList = [""]*10

def append_message(message):
    for i in range(-10,-1,1):
        messageList[i] = messageList[i+1]
    messageList[-1] = message

def delete_message():
    if messageList[-1] != "":
        for i in range(-10,0,1):
            if messageList[i] != "":
                messageList[i] = ""
                break

def draw_text(screen, text, x, y, font, color):
    surface = font.render(text,True,BLACK)
    screen.blit(surface,[x+1, y+2])

    surface = font.render(text,True,color)
    screen.blit(surface, [x,y])

def draw_Battle(screen, font):
    bg_x = 0
    bg_y = 0

    #搖晃畫面
    if enemy.eff > 0:
        enemy.eff = enemy.eff - 1
        bg_x = random.randint(-20,20)
        bg_y = random.randint(-10,10)

    screen.blit(img_battleBg, [bg_x, bg_y])
    if enemy.blink % 5 == 0:
        screen.blit(enemy.img, [enemy.x, enemy.y + enemy.step])
    if enemy.blink > 0:
        enemy.blink = enemy.blink - 1
    for i in range(10):
        draw_text(screen, messageList[i], 600, 100+i*50, font, WHITE)

def output_BattleCommand(screen, font):
    COMMAND = ["[A]ttack","[P]otion","[B]lze gem","[R]un"]
    for i in range(4):
        color = WHITE
        if btl_cmd == i: color = BLINK[tmr%18]
        draw_text(screen, COMMAND[i], 20, 360+60*i, font, color)

def input_BattleCommand(key):
    global btl_cmd
    enter = False
    #指令輸入
    if key[K_UP]   and tmr % 6 == 0 and btl_cmd > 0: btl_cmd -= 1
    if key[K_DOWN] and tmr % 6 == 0 and btl_cmd < 3: btl_cmd += 1
    if key[K_z]: enter = True
    return enter

def ifMonsterEncounter():
    global gameMode,tmr,floor
    if random.randint(0,1000) > 900:
        init_message()
        enemy.init(floor)
        gameMode = 1
        tmr = 0

def draw_bar(screen, x, y, width, height, hp, maxhp):
    pygame.draw.rect(screen, WHITE, [x-2, y-2, width + 4, height + 4])
    pygame.draw.rect(screen, BLACK, [x, y, width, height])
    if hp > 0:
        pygame.draw.rect(screen, RED, [x, y, width*hp/maxhp, height])

def main():
    global gameMode
    global screen,font,clock,floor,tmr
    global btl_cmd

    pygame.init()
    pygame.display.set_caption("戰鬥場景")
    font = pygame.font.Font(None,30) 
    screen = pygame.display.set_mode((880,720))
    clock = pygame.time.Clock()

    floor = 1
    gameMode = 0
    btl_cmd = 0

    init_message()
    makeNewDungeon()

    walkCooldown = 0
    changeActCooldown = 0
    #遊戲迴圈
    while True:
        tmr += 1
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        key = pygame.key.get_pressed()
        #非戰鬥狀態
        if gameMode == 0:
            #玩家移動
            if event.type == KEYDOWN:
                if walkCooldown <= 0:
                    if key[K_LEFT] == True:
                        if player.x > 0 and dungeon[player.y][player.x - 1] == 0:
                            ifMonsterEncounter()
                            walkCooldown = 8
                            player.x -= 1
                            if changeActCooldown <= 0 : 
                                player.act = 4 if player.act != 4 else 5
                                changeActCooldown = 9
                        else:
                            player.act = 4
                                    
                    if key[K_RIGHT] == True:
                        if player.x < W*3 and dungeon[player.y][player.x + 1] == 0:
                            ifMonsterEncounter()
                            walkCooldown = 8
                            player.x = player.x + 1
                            if changeActCooldown <= 0 : 
                                player.act = 6 if player.act != 6 else 7
                                changeActCooldown = 9
                        else:
                            player.act = 6

                    if key[K_UP] == True:
                        if player.y > 0 and dungeon[player.y - 1][player.x] == 0:
                            ifMonsterEncounter()
                            walkCooldown = 8
                            player.y -= 1 
                            if changeActCooldown <= 0 : 
                                player.act = 0 if player.act != 0 else 1
                                changeActCooldown = 9
                        else:
                            player.act = 0

                    if key[K_DOWN] == True:
                        if player.y < H*3 and dungeon[player.y + 1][player.x] == 0:
                            ifMonsterEncounter()
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

        #進入戰鬥
        elif gameMode > 0:
            if gameMode != 1 or tmr >= 1.4*FPS:
                draw_Battle(screen, font)
                draw_bar(screen, 360, 580, 200, 10, enemy.hp, enemy.maxhp)
            
            #過場特效
            if gameMode == 1:

                if 0*FPS <= tmr and tmr <= 0.5*FPS:
                    height = 24 * tmr
                    pygame.draw.rect(screen, BLACK, [0, 0, 880, height])
                    pygame.draw.rect(screen, BLACK, [0, 720 - height, 880, height])

                if 0.8*FPS <= tmr and tmr <= 1.6*FPS:
                    height = 720 - 6.8*tmr
                    pygame.draw.rect(screen, BLACK, [0, 0, 880, height])
                    pygame.draw.rect(screen, BLACK, [0, 720 - height, 880, height])

                if tmr == 2*FPS:
                    append_message("Encounter")
                    gameMode = 2
                    tmr = 0

            #玩家的回合
            elif gameMode == 2:
                if tmr == 1*FPS:
                    append_message("Your Turn")
                if tmr >= 1.2*FPS:
                    output_BattleCommand(screen, font)
                if tmr >= 1.3*FPS and input_BattleCommand(key) == True:
                    if btl_cmd == 0:
                        gameMode = 3
                        tmr = 0
                    if btl_cmd == 1 and player.potion > 0 :
                        gameMode = 7
                        tmr = 0
                    if btl_cmd == 2 and player.blazegem > 0:
                        gameMode = 8
                        tmr = 0
                    if btl_cmd == 3:
                        gameMode = 9
                        tmr = 0
            
            #玩家攻擊
            elif gameMode == 3:
                if tmr == 1*FPS:
                    append_message("You Attack!")
                if tmr >= 1.3*FPS and tmr <= 1.45*FPS:
                    screen.blit(img_effect, [850-tmr*6, -200+tmr*6])
                if tmr == 2*FPS:
                    enemy.blink = 15
                    damage = random.randint(int(player.atk * 0.6), int(player.atk * 1.4))
                    append_message(f"make {damage} damage!")
                    enemy.hp = enemy.hp - damage
                if tmr == 2.5*FPS:
                    if enemy.hp <= 0:
                        gameMode = 4
                    else:
                        gameMode = 5
                    tmr =  0

            #怪物死亡
            elif gameMode == 4:
                if tmr == 1*FPS: 
                    append_message("You Win!")  
                if tmr == 3*FPS:
                    gameMode = 0
                    init_message()
                    tmr = 0

            #怪物的回合 & 怪物攻擊
            elif gameMode == 5:
                if tmr == 1*FPS:
                    append_message("Enemy Turn")
                if tmr == 2*FPS:
                    append_message("Enemy Attack!")
                    enemy.step = 30
                if tmr == 2.5*FPS:
                    damage = random.randint(int(enemy.atk * 0.6), int(enemy.atk * 1.4))
                    append_message(f"make {damage} damage!")
                    player.hp = max(player.hp - damage, 0)
                    enemy.eff = 5
                    enemy.step = 0
                if tmr == 3*FPS:
                    if player.hp <= 0:
                        gameMode = 6
                    else:
                        gameMode = 2
                    tmr = 0

            #玩家死亡
            elif gameMode == 6:
                if tmr == 1*FPS: 
                    append_message("You Lose!")
                if tmr == 2.5*FPS:
                    gameMode = -1
                    init_message()
                    tmr = 0

            #回復藥水
            elif gameMode == 7:
                if tmr == 1*FPS:
                    append_message("Use Potion!")
                    player.potion -= 1
                if tmr == 1.8*FPS:
                    player.hp = int(min(player.hp + 0.5*player.maxhp, player.maxhp))
                if tmr == 2.5*FPS:
                    gameMode = 5
                    tmr =  0

            #火焰寶石
            elif gameMode == 8:
                if tmr == 1*FPS:
                    append_message("Use BlazeGem!")
                    player.blazegem -= 1
                if tmr >= 1.3*FPS and tmr <= 1.8*FPS:
                    img_effectB = pygame.transform.rotozoom(img_effectBOrg, 30*tmr*5/FPS, (12-tmr*5/FPS)/8)
                    img_effectB = pygame.transform.scale(img_effectB,[350,350])
                    X = 440 - img_effectB.get_width() / 2
                    Y = 390 - img_effectB.get_height() / 2
                    screen.blit(img_effectB, [X, Y])
                if tmr == 2*FPS:
                    enemy.blink = 15
                    damage = random.randint(int(player.atk * 2.3), int(player.atk * 3))
                    append_message(f"make {damage} damage!")
                    enemy.hp = enemy.hp - damage
                if tmr == 2.5*FPS:
                    if enemy.hp <= 0:
                        gameMode = 4
                    else:
                        gameMode = 5
                    tmr =  0

            #玩家逃跑
            elif gameMode == 9:
                if tmr == 0.5*FPS:
                    append_message("You Run!")
                if tmr == 1.5*FPS: 
                    append_message(". . . . . . .")
                if tmr == 2.5*FPS:
                    append_message(". . . . . ")
                if tmr == 3.5*FPS:
                    append_message(". . .")
                if tmr == 4.5*FPS:
                    if random.randint(0,100) <= 30:
                        append_message("Failed")
                    else:
                        append_message("Success")
                        gameMode = 10
                        tmr = 0
                if tmr == 5.5*FPS:
                    gameMode = 5
                    tmr = 0

            #玩家逃跑成功        
            elif gameMode == 10:
                if tmr == 1*FPS:
                    gameMode = 0
                    init_message()
                    tmr = 0

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()