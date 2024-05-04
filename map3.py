import pygame, sys, random
from button import *
from Setting import *

class map3():
    def __init__(self, Surface):
        super().__init__()
        #Thiết lập hình ảnh
        self.Background = pygame.transform.scale(pygame.image.load(f"imgdino/map3/background0.png"), (Width, Height))
        self.dinoImages = []
        for i in range(4):
            self.dinoImages.append(pygame.transform.scale(pygame.image.load(f"imgdino/map3/dino{i}.png"), (70, 73)))
        self.bossImages = []
        for i in range(3):
            self.bossImages.append(pygame.transform.scale(pygame.image.load(f"imgdino/map3/boss{i}.png"), (300, 300)))
        self.enemyImage = pygame.transform.scale(pygame.image.load(f"imgdino/map3/enemy.png"), (90, 50))
        self.bulletImage = pygame.image.load(f"imgdino/map3/bullet1.png")
        self.dinoAnimation = 0
        self.bossAnimation = 0
        #Tạo 2 đối tượng chính của màn chơi
        self.Player = dino_swim(self.dinoImages[0].get_rect(), 5, 1)
        self.Boss = boss_octopus(self.bossImages[0].get_rect(center = (1000, 250)), 3, 30)
        #thiết lập thông tin game
        self.Score = 0
        self.highScore = 0
        self.Block = True
        self.bossVisible = False
        self.bloodBossFont = pygame.font.Font(typeText, 30)
        self.playerFont = pygame.font.Font(typeText, 15)
        #tạo âm thanh
        Sounds["dinoShoot2"] = pygame.mixer.Sound('imgdino/startgame/shoot1.wav')
        Sounds["bossHit"] = pygame.mixer.Sound("imgdino/startgame/hitboss.wav")
        Sounds["ItemSound"] = pygame.mixer.Sound("imgdino/startgame/Item.wav")
        #tạo khung hình
        self.Surface = Surface
        self.Clock = pygame.time.Clock()
        
    def set_event(self):
        self.eventPlayer = pygame.USEREVENT
        pygame.time.set_timer(self.eventPlayer, 400)
        self.eventBoss = pygame.USEREVENT + 1
        pygame.time.set_timer(self.eventBoss, 1000)
    
    def reset_game(self):
        self.Score = 0
        self.bossVisible = False
        self.enemyImage = pygame.transform.scale(pygame.image.load(f"imgdino/map3/enemy.png"), (90, 50))
        self.Boss.reset_game()
        self.Player.reset_game()

    def huong_dan(self):
        Background = pygame.image.load("imgdino/startgame/huongdan3.jpg")
        BGRect = Background.get_rect(center = (400, 220))
        buttonOK = Button(350, 400, 70, 30, "OK!", 15)
        while True:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    sys.exit()
            self.Surface.fill("white")
            self.Surface.blit(Background, BGRect)
            if buttonOK.buttonEvent(self.Surface):
                return
            pygame.display.update()
            self.Clock.tick(60)

    def run(self):
        checkLose = False
        buttonSetting = Button(375, 20, 50, 25, "Menu", 10)
        self.huong_dan()
        while(True):
            for Event in pygame.event.get():
                if Event.type == pygame.QUIT:
                    sys.exit()
                elif Event.type == self.eventPlayer:
                    self.dinoAnimation += 1
                    if self.dinoAnimation == len(self.dinoImages):
                        self.dinoAnimation = 0
                    self.bossAnimation += 1
                    if self.bossAnimation == len(self.bossImages):
                        self.bossAnimation = 0
                elif Event.type == self.eventBoss:
                    self.Boss.create_enemy()
                elif Event.type == pygame.KEYDOWN:
                    if Event.key == pygame.K_e:
                        if self.Player.numBullet > 0:
                            Sounds["dinoShoot2"].play()
                            self.Player.create_bullet()
                            self.Player.numBullet -= 1
                    elif Event.key == pygame.K_SPACE:
                        self.Player.jumpHeight = -5
            self.Boss.Blood = self.Player.update(self.Boss.hitBox, self.Boss.Blood)
            if self.bossVisible:
                core, checkLose = self.Boss.update2(self.Player.hitBox)
                self.Score += core
            else:
                core, checkLose = self.Boss.update1(self.Player.hitBox)
                self.Score += core
            bloodBoss = self.bloodBossFont.render(f"{self.Boss.Blood}", False, "red")
            scoreText = self.playerFont.render(f"Score: {self.Score}", False, "black")
            bulletText = self.playerFont.render(f"Bullets: {self.Player.numBullet}", False, "Black")
            self.Surface.blit(self.Background, (0,0))
            self.Surface.blit(self.dinoImages[self.dinoAnimation], self.Player.dinoRect)
            for Bullet in self.Player.Bullets:
                self.Surface.blit(self.bulletImage, Bullet)
            self.Surface.blit(self.bossImages[self.bossAnimation], self.Boss.bossRect)
            for Enemy in self.Boss.Enemys:
                if Enemy.width == 40:
                    self.Surface.blit(self.itemImage, Enemy)
                else:
                    self.Surface.blit(self.enemyImage, Enemy)
            self.Surface.blit(bloodBoss, (self.Boss.bossRect.centerx, self.Boss.bossRect.y - 20))
            self.Surface.blit(scoreText, (Width//2 - scoreText.get_width()//2, 50))
            self.Surface.blit(bulletText, (40, 20))
            if buttonSetting.buttonEvent(self.Surface):
                if not menu_setting(self.Surface):
                    return False
            pygame.display.update()
            if self.Boss.Blood <= 0:
                if self.Score > self.highScore:
                    self.highScore = self.Score
                save_data(2, int(self.highScore), "f")
                checkStatus = announcement(True, self.Score, self.highScore, self.Surface)
                if checkStatus == (True, True):
                    self.reset_game()
                    continue
                elif checkStatus == (False, False):
                    pygame.time.set_timer(self.eventPlayer, 0)
                    pygame.time.set_timer(self.eventBoss, 0)
                    return False
                else:
                    pygame.time.set_timer(self.eventPlayer, 0)
                    pygame.time.set_timer(self.eventBoss, 0)
                    return True     
            elif checkLose:
                if self.Score > self.highScore:
                    self.highScore = self.Score
                save_data(2, int(self.highScore), "f")
                checkStatus = announcement(False, self.Score, self.highScore, self.Surface)
                if checkStatus == (True, True):
                    self.reset_game()
                    checkLose = False
                    continue
                else:
                    pygame.time.set_timer(self.eventPlayer, 0)
                    pygame.time.set_timer(self.eventBoss, 0)
                    return False
            if self.Score  % 15 == 0 and self.Score != 0:
                Sounds["ItemSound"].play()
                self.Score += 1
                self.Player.numBullet += 7
            if  not self.bossVisible:
                if self.Score > 17:
                    self.bossVisible = True
                    self.Boss.Enemys.clear()
                    self.enemyImage = pygame.transform.scale(pygame.image.load(f"imgdino/map3/bullet0.png"), (90, 50))
            self.Clock.tick(60)

class dino_swim():
    def __init__(self, dinoRect, jumpHeight, Blood):
        #tạo thuộc tính cho khủng long
        self.Blood = Blood
        self.jumpHeight = jumpHeight
        self.dinoRect = dinoRect 
        self.hitBox = pygame.Rect(0,0, dinoRect.width - 50, dinoRect.height - 50)
        #tạo thuộc tính mảng viên đạn
        self.Bullets = []
        self.numBullet = 0
        #tạo trọng lực của khủng long
        self.Gravity = 0.3
    
    def update(self, bossRect, bossBlood):
        self.jumpHeight += self.Gravity
        self.dinoRect.centery += self.jumpHeight
        if self.dinoRect.y < 50:
            self.dinoRect.y = 50
        elif self.dinoRect.y >= 390:
            self.dinoRect.y = 390
        self.hitBox.center = self.dinoRect.center
        for Bullet in self.Bullets:
            if Bullet.colliderect(bossRect):
                Sounds["bossHit"].play()
                bossBlood -= 10
                self.Bullets.remove(Bullet)
            elif Bullet.x > Width:
                self.Bullets.remove(Bullet)
            else:
                Bullet.x += 7
        return bossBlood
    
    def reset_game(self):
        self.Blood = 1
        self.Bullets.clear()
        self.numBullet = 0
        self.dinoRect.topleft = (0, 0)

    def create_bullet(self):
        Bullet = pygame.Rect(850, random.randint(70, 370), 50, 20)
        Bullet.center = self.dinoRect.center
        self.Bullets.append(Bullet) 
    
class boss_octopus():
    def __init__(self, bossRect, Speed, Blood):
        self.Speed = Speed
        self.bossRect = bossRect
        self.Enemys = []
        self.Blood = Blood
        self.hitBox = pygame.Rect(bossRect.x + 150, bossRect.y, 600, 190)   
    
    def update2(self, dinoRect):
        if self.bossRect.centerx > 700:
            self.bossRect.centerx -= 5
            self.hitBox.centerx -= 5
        for Enemy in self.Enemys:
            Enemy.x -= 5
            if Enemy.colliderect(dinoRect):
                return 0, True
            elif Enemy.x < -50:
                self.Enemys.remove(Enemy)
                return 1, False
        return 0, False
    
    def update1(self, dinoRect):
        for Enemy in self.Enemys:
            if Enemy.colliderect(dinoRect):
                return 0, True
            Enemy.x -= 5
            if Enemy.x < -50:
                self.Enemys.remove(Enemy)
                return 1, False
        return 0, False
    
    def create_enemy(self):
        Enemy = pygame.Rect(850, random.randint(70, 370), 70, 73)
        self.Enemys.append(Enemy)      
    
    def reset_game(self):
        self.bossRect.centerx = 1000
        self.hitBox.x = self.bossRect.x + 150
        self.Blood = 30
        self.Enemys.clear()

if __name__ == "__main__":
    pygame.init()
    Screen = pygame.display.set_mode((800,450))
    t = map3(Screen)
    t.run()