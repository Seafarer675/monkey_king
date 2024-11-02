import os                       #載入os模組
import pygame                   #載入pygame模組
from pygame.time import Clock   #從pygame.time載入Clock
import random                   #載入random模組

pygame.init()#遊戲初始化
clock = pygame.time.Clock()     #pygame內建函氏
WIDTH = 600                     #設定視窗寬度
HIGH = 700                      #設定視窗高度
run = True                      #預設run為True使遊戲運行
fps = 60                        #幀數設為60
white = (255,255,255)           #白色的RGB代碼
Black = (0,0,0)                 #黑色的RGB代碼

pygame.display.set_caption("Monkey King")    #更改遊戲名稱
#創建視窗
screen = pygame.display.set_mode((WIDTH,HIGH))
#載入圖片
#os.path可直接抓取python的所在位置，加上.join("資料夾","圖片檔名")
player_img = pygame.image.load(os.path.join("img","monkeyking.png")).convert()  #孫悟空的圖片
rock_img = pygame.image.load(os.path.join("img","pig.png")).convert()           #豬八戒的圖片
bump_ing = pygame.image.load(os.path.join("img","people.png")).convert()        #唐三藏的圖片

#新增三藏
def new_bump():
    bump =Bump()
    all_sprites.add(bump)
    bumps.add(bump)

#記分板
font_name = pygame.font.match_font("arial")
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.centerx , text_rect.top = x, y
    surf.blit(text_surface, text_rect)

#血條
def draw_health(surf, hp, x, y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HIGHT = 10
    fill = (hp/100)*BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HIGHT)
    pygame.draw.rect(surf, (0, 255, 0), fill_rect)
    pygame.draw.rect(surf, white, outline_rect, 2)

#初始化界面
def draw_init():
    draw_text(screen, "Monkey King", 64, WIDTH/2, HIGH/4)
    draw_text(screen, "a:move to the left", 22, WIDTH/2, HIGH/2.5)
    draw_text(screen, "d:move to the right", 22, WIDTH/2, HIGH/2.2)
    draw_text(screen, "Colliding with Zhu Bajie scores 1 point.", 22, WIDTH/2, HIGH/1.7)
    draw_text(screen, "Colliding with Tang Sanzang results in a deduction of 20% health.", 22, WIDTH/2, HIGH/1.6)
    draw_text(screen, "The initial health value is 100.", 22, WIDTH/2, HIGH/1.5)
    draw_text(screen, "Press any button to start", 18, WIDTH/2, HIGH*3/4)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(fps)                     
        for event in pygame.event.get():    
            if event.type == pygame.QUIT:   
                pygame.quit()
            elif event.type == pygame.KEYUP:
                waiting = False

#結束介面
def draw_end():
    draw_text(screen, "Game Over", 64, WIDTH/2, HIGH/4)
    draw_text(screen, "Click the mouse to back to init", 22, WIDTH/2, HIGH/2.5)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(fps)                     
        for event in pygame.event.get():    
            if event.type == pygame.QUIT:   
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                waiting = False

class Player(pygame.sprite.Sprite):     #建立一個類別去繼承內建的sprite類別
    def __init__(self):                 #初始化實體屬性
        pygame.sprite.Sprite.__init__(self) #call內建的sprite初始函式
        self.image = pygame.transform.scale(player_img, (50,38)) #調整圖片大小
        self.image.set_colorkey(Black)      #將圖片底部的黑色部分透明化
        self.rect = self.image.get_rect()   #定位圖片
        self.radius = 19                    #圖片圓的直徑
        self.rect.centerx = WIDTH/2         #將初始位置設在中間
        self.rect.bottom = HIGH -10         #將高度固定於底部
        self.speedx = 20                    #控制移動速度
        self.health = 100                       #血條
        
    def update(self):                   #建立update函式
        key_pressed = pygame.key.get_pressed()  #檢測鍵盤上的案件有無被按壓
        if key_pressed[pygame.K_d]:         #右移條件句
            self.rect.x += self.speedx      #以speedx的速度向右移
        if key_pressed[pygame.K_a]:         #左移條件句
            self.rect.x -= self.speedx      #以speedx的速度向左移
        if self.rect.right > WIDTH:             #設定控制邊界
            self.rect.right = WIDTH             #重制其出發點
        if self.rect.left < 0:                  #設定控制邊界
            self.rect.left = 0                  #重制其出發點
        
class Rock(pygame.sprite.Sprite):     #建立一個類別去繼承內建的sprite類別
    def __init__(self):                 #初始化實體屬性
        pygame.sprite.Sprite.__init__(self) #call內建的sprite初始函式
        self.image = pygame.transform.scale(rock_img, (100,70))
        self.image.set_colorkey(Black)                      #將圖片底部的黑色部分透明化
        self.rect = self.image.get_rect()   #定位圖片
        self.radius = 37                    #圖片圓的直徑
        self.rect.x = random.randrange(0,WIDTH - self.rect.width)    #random的randrange函氏會回傳兩個數字之間的隨機一個
        self.rect.y = random.randrange(-100,-40)                #random的randrange函氏會回傳兩個數字之間的隨機一個
        self.speedy = random.randrange(2,10)                    #控制y軸移動速度
        self.speedx = random.randrange(-3,3)                    #控制x移動速度
    def update(self):                   #建立update函式
       self.rect.y += self.speedy       #y座標為移動的
       self.rect.x += self.speedx       #x座標為移動的
       if self.rect.top > HIGH or self.rect.left > WIDTH or self.rect.right < 0:    #若圖片超出邊界
            self.rect.x = random.randrange(0,WIDTH - self.rect.width)    #random的ranfrange函氏會回傳兩個數字之間的隨機一個
            self.rect.y = random.randrange(-100,-40)                #random的ranfrange函氏會回傳兩個數字之間的隨機一個
            self.speedy = random.randrange(2,10)                    #控制y移動速度
            self.speedx = random.randrange(-3,3)                    #控制x移動速度

class Bump(pygame.sprite.Sprite):     #建立一個類別去繼承內建的sprite類別
    def __init__(self):                 #初始化實體屬性
        pygame.sprite.Sprite.__init__(self) #call內建的sprite初始函式
        self.image = pygame.transform.scale(bump_ing, (100,70))  #調整圖片大小   
        self.image.set_colorkey(Black)              #將圖片底部的黑色部分透明化
        self.rect = self.image.get_rect()   #定位圖片
        self.radius = 37                    #圖片圓的直徑
        self.rect.x = random.randrange(0,WIDTH - self.rect.width)    #random的ranfrange函氏會回傳兩個數字之間的隨機一個
        self.rect.y = random.randrange(-100,-40)                #random的ranfrange函氏會回傳兩個數字之間的隨機一個
        self.speedy = random.randrange(2,10)                    #控制y軸移動速度
        self.speedx = random.randrange(-3,3)                    #控制x軸移動速度
    def update(self):                   #建立update函式
       self.rect.y += self.speedy   #y座標為移動的
       self.rect.x += self.speedx   #x座標為移動的
       if self.rect.top > HIGH or self.rect.left > WIDTH or self.rect.right < 0:    #若圖片超出邊界
            self.rect.x = random.randrange(0,WIDTH - self.rect.width)    #random的ranfrange函氏會回傳兩個數字之間的隨機一個
            self.rect.y = random.randrange(-100,-40)                #random的ranfrange函氏會回傳兩個數字之間的隨機一個
            self.speedy = random.randrange(2,10)                    #控制y軸移動速度
            self.speedx = random.randrange(-3,3)                    #控制x軸移動速度

all_sprites = pygame.sprite.Group()     #創建一個所有sprite的群組
rocks = pygame.sprite.Group()           #創建一個八戒的群組
bumps = pygame.sprite.Group()           #創建一個三藏的群組
player = Player()                       #創建玩家
all_sprites.add(player)                 #將player sprite物件加入群組

for i in range(8):                      #以迴圈控制八戒數量
    rock = Rock()                       #創建八戒
    all_sprites.add(rock)               #將八戒加到sprite的群組
    rocks.add(rock)                     #將八戒加到八戒的群組
for i in range(5):                      #以迴圈控制三藏的群組
    new_bump()

#遊戲迴圈
show_init = True
score = 0                               #一開始分數等於零
while run:
    #遊戲初始化介面
    if show_init:
        draw_init()
        show_init = False

    clock.tick(fps)                     #控制幀數的函氏
    #取得輸入
    for event in pygame.event.get():    #取得輸入的函氏
        if event.type == pygame.QUIT:   #若pygame.QUIT被執行了
            run = False                 #run = False此時遊戲將被關閉
    #更新遊戲
    all_sprites.update()                #更新遊戲狀況的函氏
    '''判斷兩圖片有無碰撞，及碰撞後何者會消失 True = 留著 False = 消失
    因圖片原為矩形 碰撞判斷模糊 故以pygame.sprite.collide_circle函示將其變為以圓形方式加強碰撞判斷'''
    attack = pygame.sprite.spritecollide(player,rocks,True,pygame.sprite.collide_circle) 
    for i in attack:                    #撞擊迴圈
        score += 1                      #分數加一
        r = Rock()                      #因八戒被悟空撞擊後消失，所以要再創建八戒，使其不斷出現
        all_sprites.add(r)              #將八戒加到sprite的群組
        rocks.add(r)                    #將八戒加到八戒的群組
    hit = pygame.sprite.spritecollide(player,bumps,True,pygame.sprite.collide_circle)  
    for i in hit:
        new_bump()                      #新增三藏 因三藏被悟空撞擊後消失，所以要再創建三藏，使其不斷出現
        player.health -= 20             #撞擊到三藏會扣20滴的血 血量初始值為100
        if player.health <= 0:          #若血量為零
            draw_end()                  #遊戲結束 跳出結束介面 選擇要關閉遊戲 或是回到主畫面
            score = 0                   #分數重置
            show_init = True            #若選擇回到主畫面，主畫面跳出
            player.health = 100         #血量重置
            
    #畫面顯示
    screen.fill((0,0,0))        #將畫面填滿黑色
    all_sprites.draw(screen)    #將所有sprite顯示於螢幕上
    draw_text(screen, str(score), 50, WIDTH/2, 10) #將分數顯示於螢幕上
    draw_health(screen, player.health, 5, 10)      #將血量顯示於螢幕上
    pygame.display.update()       
pygame.quit()                   #遊戲結束
