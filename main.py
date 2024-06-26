import pygame,random,sys
from assets import *
from character import *
from pygame.locals import *

FPS = 60
tmr = 0

MAZE_H = 22; MAZE_W = 22
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
    itemChoice = [0,0,0,0,1]
    TXP = [1, 1, -1, -1]
    TYP = [-1, 1, -1, 1]
    for y in range(MAZE_H):
        for x in range(MAZE_W):
            dx = x*3+1
            dy = y*3+1
            if maze[y][x] == 0:
                dungeon[dy][dx] = 0
                if random.randint(1,100) <= 20:
                    item = random.choice(itemChoice)
                    #房間有兩成的機率生成寶箱
                    if item == 0:
                        for i in range(-1,2):
                            for j in range(-1,2):
                                dungeon[dy+i][dx+j] = 0
                    elif item == 1:
                        for i in range(-1,2):
                            for j in range(-1,2):
                                dungeon[dy+i][dx+j] = 0
                        d = random.randint(0,3)
                        dungeon[dy+TYP[d]][dx+TXP[d]] = 2
                else:
                    if maze[y][x-1] == 0:
                        dungeon[dy][dx-1] = 0
                    if maze[y][x+1] == 0:
                        dungeon[dy][dx+1] = 0
                    if maze[y-1][x] == 0:
                        dungeon[dy-1][dx] = 0
                    if maze[y+1][x] == 0:
                        dungeon[dy+1][dx] = 0

    #生成樓梯 & 蛋
    while True:
        dx = random.randint(int(MAZE_W*3*0.2), int(MAZE_W*3*0.8))
        dy = random.randint(int(MAZE_H*3*0.3), int(MAZE_H*3*0.8))
        if dungeon[dy][dx] == 0:
            for i in range(-1,2):
                for j in range(-1,2):
                    dungeon[dy+i][dx+j] = 0
                    if floor < 5:
                        dungeon[dy][dx] = 3
                    else:
                        dungeon[dy][dx] = 4
            break

def init_message():
    global messageList, messageColor
    messageList = [""]*10
    messageColor = [WHITE]*10

def append_message(message, color=WHITE):
    global messageList, messageColor
    for i in range(-10,-1,1):
        messageList[i] = messageList[i+1]
        messageColor[i] = messageColor[i+1]
    messageList[-1] = message
    messageColor[-1] = color

def delete_message():
    if messageList[-1] != "":
        for i in range(-10,0,1):
            if messageList[i] != "":
                messageList[i] = ""
                messageColor[i] = WHITE
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
        draw_text(screen, messageList[i], 600, 100+i*50, font, messageColor[i])
    draw_para(screen, font)

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
    if random.randint(0,1000) > 994:
        init_message()
        enemy.init(floor)
        gameMode = 1
        tmr = 0

def draw_bar(screen, x, y, width, height, hp, maxhp):
    pygame.draw.rect(screen, WHITE, [x-10, y-2, width + 4, height + 4])
    pygame.draw.rect(screen, BLACK, [x-8, y, width, height])
    if hp > 0:
        pygame.draw.rect(screen, RED, [x-8, y, width*hp/maxhp, height])

def get_boxItem():
    global gameMode, tmr
    d  = random.choice([0,0,0,1,1,2,2,3,3,3])
    se[6].play()
    if d == 0:
        append_message("The chest is empty...")
    if d == 1:
        player.potion += 1
        append_message("Get 1 potion!")
    if d == 2:
        player.blazegem += 1
        append_message("Get 1 blaze gem!")
    if d == 3:
        player.food = min(player.food + 35, 100)
        append_message("Get 35 food!")

def draw_para(screen, font, X=30, Y=600):
    global tmr
    screen.blit(img_para, [X,Y])
    color = WHITE
    if player.hp < 10 and tmr % 10 == 0:color = RED
    draw_text(screen, f"{player.hp}/{player.maxhp}",X+128,Y+6,font,color)
    draw_text(screen,str(player.atk),X+128,Y+33,font,WHITE)
    color = WHITE
    if player.food < 10 and tmr % 10 == 0:color = RED
    draw_text(screen,str(player.food),X+128, Y+60, font, color)
    draw_text(screen,str(player.potion),X+266, Y+6, font, WHITE)
    draw_text(screen,str(player.blazegem),X+266,Y+33,font,WHITE)

def main():
    global gameMode
    global screen,font,clock,floor,tmr
    global btl_cmd, messageColor

    pygame.init()
    pygame.display.set_caption("one hour dungeon")
    font = pygame.font.Font(None,30) 
    screen = pygame.display.set_mode((880,720))
    clock = pygame.time.Clock()

    floor = 1
    gameMode = -1
    isGameover = False
    isVictory = False
    btl_cmd = 0

    init_message()
    makeNewDungeon()

    global changeActCooldown, foodCooldown, hungryCooldown
    walkCooldown = 0
    disCooldown = 0
    foodCooldown = 0
    hungryCooldown = 0
    changeActCooldown = 0
    #遊戲迴圈
    while True:
        tmr += 1
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        key = pygame.key.get_pressed()

        #遊戲標題
        if gameMode == -1:
            if not isGameover and not isVictory and tmr == 1:
                pygame.mixer.music.load(os.path.join("halfRPG","sound","ohd_bgm_title.ogg"))
                pygame.mixer.music.play(-1)
            else:
                isGameover = False
            screen.fill(BLACK)
            if not isVictory:
                screen.blit(img_title, [40,60])
            else:
                screen.blit(img_victory, [40,60])
            draw_text(screen, "Press space key", 363, 560, font, BLINK[tmr%18])
            if key[K_SPACE] == 1:
                isVictory = False
                floor = 1
                makeNewDungeon()
                player.init()
                init_message()
                #設定初始玩家位置
                while True:
                    dx = random.randint(4, MAZE_W*3-4)
                    dy = random.randint(4, MAZE_H*3-4)
                    if dungeon[dy][dx] == 0:
                        player.x = dx
                        player.y = dy
                        break
                gameMode = 0
                tmr = 0
                pygame.mixer.music.load(os.path.join("halfRPG","sound","ohd_bgm_field.ogg"))
                pygame.mixer.music.play(-1)
                
                
        #非戰鬥狀態
        if gameMode == 0:
            #玩家移動
            if event.type == KEYDOWN:
                if walkCooldown <= 0:

                    def doCooldown(act1, act2):
                        global foodCooldown, changeActCooldown, hungryCooldown, player
                        if changeActCooldown <= 0 : 
                                player.act = act1 if player.act != act1 else act2
                                changeActCooldown = 9
                        if player.food > 0 and foodCooldown <= 0 :
                                player.food -= 1
                                foodCooldown = 35

                        if player.food == 0 and hungryCooldown <= 0:
                            player.hp = max(player.hp - int(player.maxhp/50),1)
                            hungryCooldown = 45

                    if key[K_LEFT] == True:
                        if player.x > 0 and dungeon[player.y][player.x - 1] == 0 or dungeon[player.y][player.x - 1] == 3:
                            ifMonsterEncounter()
                            walkCooldown = 8
                            player.x -= 1
                            doCooldown(4, 5)
                        else:
                            player.act = 4
                                    
                    if key[K_RIGHT] == True:
                        if player.x < W*3 and dungeon[player.y][player.x + 1] == 0 or dungeon[player.y][player.x + 1] == 3:
                            ifMonsterEncounter()
                            walkCooldown = 8
                            player.x = player.x + 1
                            doCooldown(6, 7)
                        else:
                            player.act = 6

                    if key[K_UP] == True:
                        if player.y > 0 and dungeon[player.y - 1][player.x] == 0 or dungeon[player.y - 1][player.x] == 3:
                            ifMonsterEncounter()
                            walkCooldown = 8
                            player.y -= 1 
                            doCooldown(0, 1)
                        else:
                            player.act = 0

                    if key[K_DOWN] == True:
                        if player.y < H*3 and dungeon[player.y + 1][player.x] == 0 or dungeon[player.y + 1][player.x] == 3:
                            ifMonsterEncounter()
                            walkCooldown = 8
                            player.y += 1
                            doCooldown(2, 3)

                        else:
                            player.act = 2

            #寶箱
            if key[K_z] == True:
                if (player.act == 4 or player.act == 5) and dungeon[player.y][player.x - 1] == 2: 
                    dungeon[player.y][player.x - 1] = 0 
                    get_boxItem()
                    disCooldown = 320

                if (player.act == 6 or player.act == 7) and dungeon[player.y][player.x + 1] == 2: 
                    dungeon[player.y][player.x + 1] = 0 
                    get_boxItem()
                    disCooldown = 320

                if (player.act == 0 or player.act == 1) and dungeon[player.y - 1][player.x] == 2: 
                    dungeon[player.y - 1][player.x] = 0 
                    get_boxItem()
                    disCooldown += 320

                if (player.act == 2 or player.act == 3) and dungeon[player.y + 1][player.x] == 2: 
                    dungeon[player.y + 1][player.x] = 0 
                    get_boxItem()
                    disCooldown = 320

            #樓梯
            if dungeon[player.y][player.x] == 3:
                se[7].play()
                disCooldown = 320
                floor += 1
                makeNewDungeon()
                if floor != 5:
                    append_message(f"welcome to the floor {floor}!")
                else:
                    append_message("welcome to the final floor!")
                #重設玩家位置
                while True:
                    dx = random.randint(4, MAZE_W*3-4)
                    dy = random.randint(4, MAZE_H*3-4)
                    if dungeon[dy][dx] == 0:
                        player.x = dx
                        player.y = dy
                        break

            #魔王
            def bossBattle():
                global gameMode, tmr
                init_message()
                enemy.boss(floor)
                gameMode = 11
                tmr = 0

            if key[K_z] == True:
                if (player.act == 4 or player.act == 5) and dungeon[player.y][player.x - 1] == 4:
                    bossBattle()

                if (player.act == 6 or player.act == 7) and dungeon[player.y][player.x + 1] == 4: 
                    bossBattle()

                if (player.act == 0 or player.act == 1) and dungeon[player.y - 1][player.x] == 4: 
                    bossBattle()

                if (player.act == 2 or player.act == 3) and dungeon[player.y + 1][player.x] == 4: 
                    bossBattle()

            #計算冷卻時間
            if foodCooldown > 0:
                foodCooldown -= 1

            if hungryCooldown > 0:
                hungryCooldown -= 1

            if changeActCooldown > 0:
                changeActCooldown -= 1

            if walkCooldown > 0:
                walkCooldown -= 1

            #玩家視角
            for y in range(-10,11):
                for x in range(-13,14):
                    W = 48
                    H = 48
                    try:
                        if dungeon[player.y + y][player.x + x] == 0:
                            screen.blit(img_floor,[W*(x+8),H*(y+6)])
                        elif dungeon[player.y + y][player.x + x] == 1:
                            screen.blit(img_wall,[W*(x+8),H*(y+6)])
                        elif dungeon[player.y + y][player.x + x] == 2:
                            screen.blit(img_box, [W*(x+8),H*(y+6)])
                        elif dungeon[player.y + y][player.x + x] == 3:
                            screen.blit(img_stair, [W*(x+8),H*(y+6)])
                        elif dungeon[player.y + y][player.x + x] == 4:
                            screen.blit(img_cocoon, [W*(x+8),H*(y+6)])

                    except:
                        screen.blit(img_wall,[W*(x+8),H*(y+6)])
                    if x == 0 and y == 0:
                        screen.blit(img_player[player.act],[W*(x+8)+7,H*(y+6)-7])

            #陰影效果
            screen.blit(img_dark, [0, 0])

            #玩家數值
            draw_para(screen, font,X=10,Y=10)

            #顯示訊息
            for i in range(10):
                draw_text(screen, messageList[i], 600, 100+i*50, font, messageColor[i])

            if disCooldown == 0:
                delete_message()
                disCooldown = 90

            if disCooldown > 0:
                disCooldown -= 1

        #進入戰鬥
        elif gameMode > 0:
            if gameMode != 1 or tmr >= 1.4*FPS:
                se[4].stop()
                draw_Battle(screen, font)
                draw_bar(screen, 360, 580, 200, 10, enemy.hp, enemy.maxhp)
            
            #過場特效
            if gameMode == 1:
                if tmr == 0.1*FPS:
                    pygame.mixer.music.pause()

                if 0*FPS <= tmr and tmr <= 0.5*FPS:
                    height = 24 * tmr
                    pygame.draw.rect(screen, BLACK, [0, 0, 880, height])
                    pygame.draw.rect(screen, BLACK, [0, 720 - height, 880, height])

                if 0.8*FPS <= tmr and tmr <= 1.6*FPS:
                    height = 720 - 6.8*tmr
                    pygame.draw.rect(screen, BLACK, [0, 0, 880, height])
                    pygame.draw.rect(screen, BLACK, [0, 720 - height, 880, height])
                
                if tmr == 1.8*FPS:
                    pygame.mixer.music.load(os.path.join("halfRPG","sound","ohd_bgm_battle.ogg"))
                    pygame.mixer.music.play(-1)

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
                    se[0].play()
                    enemy.hp = enemy.hp - damage
                if tmr == 2.5*FPS:
                    if enemy.hp <= 0:
                        gameMode = 4
                    else:
                        gameMode = 5
                    tmr =  0

            #怪物死亡
            elif gameMode == 4 and not enemy.isboss :
                if tmr == 1*FPS: 
                    GetEXP = True
                    append_message("You Win!")
                    se[5].play()
                    pygame.mixer.music.stop()
                if tmr == 1.5*FPS and GetEXP == True:
                    append_message(f"Get {enemy.exp} Exp!")
                    player.exp += enemy.exp
                    GetEXP = False 
                if tmr == 2.5*FPS:
                    if player.exp >= player.maxexp:
                        append_message("Level Up!")
                        se[4].play()
                        player.levelUp()
                        tmr = 1.1*FPS 
                if tmr == 3*FPS:
                    gameMode = 0
                    init_message()
                    tmr = 0
                    pygame.mixer.music.load(os.path.join("halfRPG","sound","ohd_bgm_field.ogg"))
                    pygame.mixer.music.play(-1)

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
                    se[0].play()
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
                    append_message("You Lose!",RED)
                    pygame.mixer.music.stop()
                    se[3].play()
                    isGameover = True
                if tmr == 7*FPS:
                    gameMode = -1
                    init_message()
                    tmr = 0

            #回復藥水
            elif gameMode == 7:
                if tmr == 0.5*FPS:
                    append_message("Use Potion!")
                    se[2].play()
                    player.potion -= 1
                if tmr == 1.3*FPS:
                    player.hp = int(min(player.hp + 0.5*player.maxhp, player.maxhp))
                if tmr == 2*FPS:
                    gameMode = 5
                    tmr =  0

            #火焰寶石
            elif gameMode == 8:
                if tmr == 0.5*FPS:
                    append_message("Use BlazeGem!")
                    se[1].play()
                    player.blazegem -= 1
                if tmr >= 0.8*FPS and tmr <= 1.3*FPS:
                    img_effectB = pygame.transform.rotozoom(img_effectBOrg, 30*tmr*5/FPS, (12-tmr*5/FPS)/8)
                    img_effectB = pygame.transform.scale(img_effectB,[350,350])
                    X = 440 - img_effectB.get_width() / 2
                    Y = 390 - img_effectB.get_height() / 2
                    screen.blit(img_effectB, [X, Y])
                if tmr == 1.5*FPS:
                    enemy.blink = 15
                    damage = random.randint(int(player.atk * 2.3), int(player.atk * 3))
                    append_message(f"make {damage} damage!")
                    enemy.hp = enemy.hp - damage
                if tmr == 2*FPS:
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
                    pygame.mixer.music.load(os.path.join("halfRPG","sound","ohd_bgm_field.ogg"))
                    pygame.mixer.music.play(-1)

            #過場特效(魔王版本)
            elif gameMode == 11:
                if tmr == 0.1*FPS:
                    pygame.mixer.music.pause()

                if 0*FPS <= tmr and tmr <= 0.5*FPS:
                    height = 24 * tmr
                    pygame.draw.rect(screen, BLACK, [0, 0, 880, height])
                    pygame.draw.rect(screen, BLACK, [0, 720 - height, 880, height])

                if 0.8*FPS <= tmr and tmr <= 1.6*FPS:
                    height = 720 - 6.8*tmr
                    pygame.draw.rect(screen, BLACK, [0, 0, 880, height])
                    pygame.draw.rect(screen, BLACK, [0, 720 - height, 880, height])

                if tmr == 1.8*FPS:
                    pygame.mixer.music.load(os.path.join("halfRPG","sound","ohd_bgm_boss.ogg"))
                    pygame.mixer.music.play(-1)

                if tmr == 2*FPS:
                    append_message("I Hate The World!!!", RED)
                    gameMode = 2
                    tmr = 0

            #魔王死亡
            elif gameMode == 4 and enemy.isBoss :
                if tmr == 1*FPS: 
                    isVictory = True
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(os.path.join("halfRPG","sound","ohd_bgm_victory.ogg"))
                    pygame.mixer.music.play(-1)
                    append_message("THE BOSS iS DEAD!")
                if tmr == 2.5*FPS:
                    append_message("YOU SAVE THE WORLD!!")
                if tmr == 5.2*FPS:
                    gameMode = -1
                    tmr = 0


        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
