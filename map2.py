import pygame, sys, random
from button import *
from Setting import *

class map2():
    def __init__(self, Surface):
        super().__init__()
        #Thiết lập hình ảnh
        self.Background = pygame.transform.scale(pygame.image.load(f"imgdino/map2/background.png").convert_alpha(), (Width, Height))
        self.dinoImages = []
        for i in range(6):
            self.dinoImages.append(pygame.transform.scale(pygame.image.load(f"imgdino/map2/dino{i}.png").convert_alpha(), (70, 80)))
        self.bossImage = pygame.transform.scale(pygame.image.load(f"imgdino/map2/boss.png").convert_alpha(), (130, 140))
        self.enemyImage = pygame.image.load(f"imgdino/map2/enemy.png").convert_alpha()
        self.bulletImage = pygame.transform.scale(pygame.image.load(f"imgdino/map2/bullet.png").convert_alpha(), (30, 30))
        self.Player = dinosauro_fly(self.dinoImages[0].get_rect(center = (100, 100)), self.bulletImage.get_rect, 5, 20)
        self.Boss = boss_fly(self.bossImage.get_rect(center = (700, 200)), self.enemyImage.get_rect(), 3, 50)
        self.dinoAnimation = 0
       #thiết lập thông tin game
        self.Score = 0
        self.highScore = 0
        self.Block = True
        self.bloodBossFont = pygame.font.Font(typeText, 30)
        self.playerFont = pygame.font.Font(typeText, 15)
        #tạo âm thanh
        Sounds["dinoShoot"] = pygame.mixer.Sound('imgdino/startgame/shoot1.wav')
        Sounds["bossCollide"] = pygame.mixer.Sound('imgdino/startgame/tick.wav')
        #tạo khung hình
        self.Surface = Surface
        self.Clock = pygame.time.Clock()
    
    def set_event(self):
        self.eventPlayer = pygame.USEREVENT
        pygame.time.set_timer(self.eventPlayer, 400)
        self.eventBoss = pygame.USEREVENT + 1
        pygame.time.set_timer(self.eventBoss, 700)
    
    def reset_game(self):
        self.Boss.reset_game()
        self.Player.reset_game()

    def huong_dan(self):
        Background = pygame.image.load("imgdino/startgame/huongdan2.jpg")
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
        buttonSetting = Button(375, 20, 50, 25, "Menu", 10)
        self.huong_dan()
        while(True):
            for Event in pygame.event.get():
                if Event.type == pygame.QUIT:
                    sys.exit()
                elif Event.type == self.eventPlayer:
                    self.Player.resetShoot = True
                    if self.Player.Direction != (0,0):
                        self.dinoAnimation += 1
                        if self.dinoAnimation == len(self.dinoImages):
                            self.dinoAnimation = 0
                    else:
                        self.dinoAnimation = 0
                elif Event.type == self.eventBoss:
                    self.Boss.create_enemy()
            self.Player.update()
            self.Player.numBullet = self.Boss.update(self.Player.numBullet)
            self.Boss.Enemys = self.Player.check_collide(self.Boss.Enemys)
            self.Player.Bullets = self.Boss.check_collide(self.Player.Bullets)
            bloodBossText = self.bloodBossFont.render(f"{self.Boss.Blood}", False, "red")
            bulletText = self.playerFont.render(f"Bullets: {self.Player.numBullet}", False, "purple")
            bloodPlayerText = self.playerFont.render(f"{self.Player.Blood}", False, "purple")
            self.Surface.blit(self.Background, (0,0))
            self.Surface.blit(self.dinoImages[self.dinoAnimation], self.Player.dinoRect)
            for Bullet in self.Player.Bullets:
                self.Surface.blit(self.bulletImage, Bullet)
            self.Surface.blit(self.bossImage, self.Boss.bossRect)
            for Enemy in self.Boss.Enemys:
                self.Surface.blit(self.enemyImage, Enemy.Rect)
            self.Surface.blit(bloodPlayerText, (self.Player.dinoRect.x + 40, self.Player.dinoRect.y - 20))
            self.Surface.blit(bloodBossText, (self.Boss.bossRect.x + 20, self.Boss.bossRect.y - 40))
            self.bgWin = pygame.transform.scale(pygame.image.load('imgdino/map2/background1.png').convert_alpha(), (300, 300))
            self.bgLose = pygame.transform.scale(pygame.image.load('imgdino/map2/background2.png').convert_alpha(), (300, 300))
            self.Surface.blit(bulletText, (40, 20))
            if buttonSetting.buttonEvent(self.Surface):
                if not menu_setting(self.Surface):
                    return False
            if self.Boss.Blood <= 0:
                if self.Score > self.highScore:
                    self.highScore = self.Score
                save_data(1, int(self.highScore), "f")
                checkStatus = announcement(True, self.Score, self.highScore, self.Surface)
                if checkStatus == (True, True):
                    self.reset_game()
                elif checkStatus == (False, False):
                    pygame.time.set_timer(self.eventPlayer, 0)
                    pygame.time.set_timer(self.eventBoss, 0)
                    return False
                else:
                    pygame.time.set_timer(self.eventPlayer, 0)
                    pygame.time.set_timer(self.eventBoss, 0)
                    return True         
            elif self.Player.Blood <= 0:
                if self.Score > self.highScore:
                    self.highScore = self.Score
                save_data(1, int(self.highScore), "f")
                checkStatus = announcement(False, self.Score, self.highScore, self.Surface)
                if checkStatus == (True, True):
                    self.reset_game()
                else:
                    pygame.time.set_timer(self.eventPlayer, 0)
                    pygame.time.set_timer(self.eventBoss, 0)
                    return False
            pygame.display.update()
            self.Clock.tick(60)


class dinosauro_fly():
    def __init__(self, dinoRect, bulletRect, Speed, Blood):
        #tạo thuộc tính cho khủng long
        self.Blood = Blood
        self.Speed = Speed
        self.Direction = pygame.math.Vector2()
        self.dinoRect = dinoRect 
        self.hitBox = dinoRect
        self.hitBox.width -= 30
        self.hitBox.height -= 30
        self.resetShoot = False
        #tạo thuộc tính mảng viên đạn
        self.Bullets = []
        self.bulletRect = bulletRect
        self.numBullet = 0
        self.checkShoot = False

    def move(self):
        Keys = pygame.key.get_pressed()
        #kiểm tra phím lên xuống
        if Keys[pygame.K_UP]:
            self.Direction.y = -1
        elif Keys[pygame.K_DOWN]:
            self.Direction.y = 1
        else:
            self.Direction.y = 0
        #kiểm tra phím trái, phải
        if Keys[pygame.K_RIGHT]:
            self.Direction.x = 1
        elif Keys[pygame.K_LEFT]:
            self.Direction.x = -1
        else: 
            self.Direction.x = 0 
        #kiểm tra phím k 
        if Keys[pygame.K_z]:
            self.checkShoot = True 
        #Thay đổi vị trí rect
        self.dinoRect.center += self.Direction * self.Speed
        self.hitBox.center = self.dinoRect.center
    
    def update(self):
        self.move()
        for Bullet in self.Bullets:
            if Bullet.x > Width:
                self.Bullets.remove(Bullet)
            else:
                Bullet.x += 5
        # giới hạn phạm vi di chuyển của khủng long
        # chiều dọc:
        if self.dinoRect.y < 5:
            self.dinoRect.y = 5
        elif self.dinoRect.y >= 370:
            self.dinoRect.y = 370
        # chiều ngang: đến nữa màn hình bên trái
        if self.dinoRect.x < 0:
            self.dinoRect.x = 0
        elif self.dinoRect.x >= 400:
            self.dinoRect.x = 400 
        #xử lý khủng long bắn đạn 
        if self.checkShoot and self.numBullet > 0 and self.resetShoot:
            self.Bullets.append(self.bulletRect(center = self.dinoRect.center)) 
            Sounds["dinoShoot"].play()
            self.numBullet -= 1
            self.resetShoot = False
            self.checkShoot = False
        else:
            self.checkShoot = False

    def check_collide(self, Enemys):
        for Enemy in Enemys:
            if self.hitBox.colliderect(Enemy.Rect):
                self.Blood -= 5
                Enemys.remove(Enemy)            
        return Enemys

    def reset_game(self):
        self.Blood = 20
        self.Bullets.clear()
        self.numBullet = 0
        self.dinoRect.center = (100, 100)

class boss_fly():
    def __init__(self, bossRect, enemyRect, Speed, Blood):
        self.Speed = Speed
        self.bossRect = bossRect
        self.enemyRect = enemyRect
        self.Enemys = []
        self.Blood = Blood
        self.hitBox = self.bossRect
        self.hitBox.width -= 40
        self.hitBox.height -= 40
    
    def move(self):
        if self.bossRect.y < 0 or self.bossRect.y > 230:
            self.Speed *= (-1)   
        self.bossRect.y += self.Speed 
    
    def update(self, numBullet):
        self.move()
        for Enemy in self.Enemys:
            Enemy.Rect.centerx -= Enemy.Speed
            Enemy.Rect.centery += Enemy.ranY
            if Enemy.Rect.centerx < 0:
                self.Enemys.remove(Enemy)
                numBullet += 1
            elif Enemy.Rect.centery < 0 or Enemy.Rect.centery > 450: 
                self.Enemys.remove(Enemy)
        if numBullet > 5:
            numBullet = 5
        return numBullet
    
    def create_enemy(self):
        e = enemy(self.bossRect.centerx, self.bossRect.centery,3)
        self.Enemys.append(e) 

    def check_collide(self, Bullets):
        for Bullet in Bullets:
            if self.bossRect.colliderect(Bullet):
                self.Blood -= 10
                Sounds["bossCollide"].play()
                Bullets.remove(Bullet)            
        return Bullets

    def reset_game(self):
        self.Blood = 50
        self.Enemys.clear()
        self.bossRect.center = (700, 200)

class enemy():
    def __init__(self, PosX, PosY, Speed):
        self.Speed = Speed
        self.Rect = pygame.Rect(PosX, PosY, 50, 53)
        self.ranY = random.choice((1,-1)) * random.randint(0, 1)

if __name__ == "__main__":
    pygame.init()
    Screen = pygame.display.set_mode((Width, Height))
    t = map2(Screen)
    t.run()
