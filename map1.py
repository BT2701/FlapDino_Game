import pygame, sys, random
from button import *
from Setting import *

# Màn 1 -----------------------------------------------------------------
class map1():
    def __init__(self, Surface):
        super().__init__()
        #thiết lập hình ảnh
        self.Background = pygame.transform.scale(pygame.image.load(f"imgdino\\map1\\background0.png").convert_alpha(), (Width, Height))
        self.floorXPos = 0
        self.Floor = pygame.transform.scale2x(pygame.image.load("imgdino/map1/background3.png").convert())
        self.dinoDown = pygame.image.load('imgdino/map1/dino-fly-down.png')
        self.dinoMid = pygame.image.load('imgdino/map1/dino-fly.png')
        self.dinoUp = pygame.image.load('imgdino/map1/dino-fly-up.png')
        self.dinoList= [self.dinoDown, self.dinoMid, self.dinoUp]
        self.dinoIndex = 0
        self.Dinosaur = self.dinoList[self.dinoIndex]
        self.dinoRect = self.Dinosaur.get_rect(center = (200, 100))
        #Thiết lập trọng lực
        self.Gravity = 0.15
        self.dinoMovement = 0
        #Thiết lập thông tin màn chơi
        self.gameActive = True
        self.Score = 0
        self.highScore = 0
        self.Block = True
        self.gameFont = pygame.font.Font(typeText, 20)
        #tạo ống
        self.pipeSurface = pygame.transform.scale2x(pygame.image.load("imgdino/map1/pipe.png"))
        self.pipeList = []
        self.pipeHeightList =[200, 250, 300]
        #tạo âm thanh
        Sounds["dinoSoundMap1"] = pygame.mixer.Sound('imgdino/map1/sfx_wing.wav')
        Sounds["hitSoundMap1"] = pygame.mixer.Sound('imgdino/map1/sfx_hit.wav')
        Sounds["scoreSoundMap1"] = pygame.mixer.Sound('imgdino/map1/te.wav')
        #tạo khung hình
        self.Surface = Surface
        self.Clock = pygame.time.Clock()

    def set_event(self):
        self.dinoFlap = pygame.USEREVENT + 1
        pygame.time.set_timer(self.dinoFlap, 200)
        self.spawnPipe = pygame.USEREVENT
        pygame.time.set_timer(self.spawnPipe, 300)
    
    def draw_floor(self):
        self.Surface.blit(self.Floor, (self.floorXPos, 380))
        self.Surface.blit(self.Floor, (self.floorXPos + 800, 380))

    def create_pipe(self):
        randomPipePos =random.choice(self.pipeHeightList)
        bottomPipe = self.pipeSurface.get_rect(midtop = (800, randomPipePos))
        topPipe = self.pipeSurface.get_rect(midtop = (800, randomPipePos - 650))
        return bottomPipe, topPipe
    
    def move_pipe(self):
        for Pipe in self.pipeList:
            Pipe.centerx -= 5

    def draw_pipe(self):
        for Pipe in self.pipeList:
            if Pipe.bottom >= 450:
                self.Surface.blit(self.pipeSurface, Pipe)
            else:
                flipPipe=pygame.transform.flip(self.pipeSurface, False, True)
                self.Surface.blit(flipPipe, Pipe)

    #xử lý va chạm
    def check_collision(self):
        for Pipe in self.pipeList:
            if self.dinoRect.colliderect(Pipe):
                Sounds["hitSoundMap1"].play()
                return False
        if self.dinoRect.top <= -75 or self.dinoRect.bottom >= 380:
            return False
        return True

    def rotate_dino(self):
        new_dino= pygame.transform.rotozoom(self.Dinosaur,-self.dinoMovement*3,1)
        return new_dino

    def dino_animation(self):
        self.Dinosaur = self.dinoList[self.dinoIndex]
        self.dinoRect = self.Dinosaur.get_rect(center=(200, self.dinoRect.centery))

    def score_display(self, gameState):
        if gameState=='main game':
            scoreSurface = self.gameFont.render(f'Score: {int(self.Score)}',True,(0,0,0))
            scoreRect= scoreSurface.get_rect(topleft = (10,30))
            self.Surface.blit(scoreSurface,scoreRect)
    
    def update_score(self):
        if self.Score > self.highScore:
            self.highScore = self.Score

    def reset_game(self):
        self.gameActive = True
        self.pipeList.clear()
        self.dinoRect.center = (200,100)
        self.dinoMovement = 0
        self.Score = 0

    def huong_dan(self):
        Background = pygame.image.load("imgdino/startgame/huongdan1.jpg")
        BGRect = Background.get_rect(center = (400, 200))
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
        while True:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_SPACE or  event.key == pygame.K_UP) and self.gameActive:
                        self.dinoMovement =-4
                        Sounds["dinoSoundMap1"].play()
                if event.type== self.spawnPipe:
                    self.pipeList.extend(self.create_pipe())
                if event.type== self.dinoFlap:
                    if self.dinoIndex < 2:
                        self.dinoIndex += 1
                    else:
                        self.dinoIndex = 0
                    self.dino_animation()
            self.Surface.blit(self.Background,(0,0))
            if self.gameActive:
                #dinosaur
                self.dinoMovement += self.Gravity
                rotated_dino = self.rotate_dino()
                self.dinoRect.centery += self.dinoMovement
                self.Surface.blit(rotated_dino,self.dinoRect)
                #xử lý va chạm
                self.gameActive = self.check_collision()
                #pipe
                self.move_pipe()
                self.draw_pipe()
                self.Score += 0.1
                self.score_display('main game')
                if self.Score % 100 == 0 and self.Score != 0:
                    Sounds["scoreSoundMap1"].play()
            elif self.Score > 10:
                self.update_score()
                save_data(0, int(self.highScore), "f")
                checkStatus = announcement(True, self.Score, self.highScore, self.Surface)   
                if checkStatus == (True, True):
                    self.reset_game()
                elif checkStatus == (False, False):
                    pygame.time.set_timer(self.spawnPipe, 0)
                    pygame.time.set_timer(self.dinoFlap, 0)
                    return False
                else:
                    pygame.time.set_timer(self.spawnPipe, 0)
                    pygame.time.set_timer(self.dinoFlap, 0)
                    return True    
            else:
                self.update_score()
                save_data(0, int(self.highScore), "f")
                checkStatus = announcement(False, self.Score, self.highScore, self.Surface)
                if checkStatus == (True, True):
                    self.reset_game()
                else:
                    pygame.time.set_timer(self.spawnPipe, 0)
                    pygame.time.set_timer(self.dinoFlap, 0)
                    return False
            #floor
            self.floorXPos -= 1
            self.draw_floor()
            if self.floorXPos <= -800:
                self.floorXPos = 0
            if buttonSetting.buttonEvent(self.Surface):
                if not menu_setting(self.Surface):
                    return False
            pygame.display.update()
            self.Clock.tick(120)


if __name__ == "__main__":
    pygame.init()
    Screen = pygame.display.set_mode((800,450))
    m = map1(Screen)
    m.run()
