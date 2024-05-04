import pygame, sys
from Setting import *
class Button():
    #Khởi tạo button
    def __init__(self, X, Y, Width, Height, Text, sizeText):
        self.backGround = []
        self.X = X
        self.Y = Y
        self.Width = Width
        self.Height = Height
        self.Text = Text 
        self.Rect = pygame.Rect(self.X, self.Y, self.Width, self.Height)
        self.surFace = pygame.font.Font(f'imgdino\\startgame\\PressStart2P-Regular.ttf', sizeText).render(self.Text, True, ("black"))
        if Text == "":
            if get_volume():
                self.backGround.append(pygame.transform.scale(pygame.image.load(f"imgdino/startgame/buttonvolume0.png"), (self.Width, self.Height)))
            else:
                self.backGround.append(pygame.transform.scale(pygame.image.load(f"imgdino/startgame/buttonvolume1.png"), (self.Width, self.Height)))
        else:
            self.backGround.append(pygame.transform.scale(pygame.image.load(f"imgdino/startgame/button0.png"), (self.Width, self.Height)))
            self.backGround.append(pygame.transform.scale(pygame.image.load(f"imgdino/startgame/button1.png"), (self.Width, self.Height)))

    #Xử lý va chạm với con trỏ 
    def buttonEvent(self, Screen):
        mousePos = pygame.mouse.get_pos() 
        if self.Rect.collidepoint(mousePos):
            if self.Text == "":
                Screen.blit(self.backGround[0], (self.X, self.Y))
            else:
                Screen.blit(self.backGround[1], (self.X, self.Y))
            if pygame.mouse.get_pressed(num_buttons = 3)[0]:
                Sounds["Click"].play()
                if self.Text == "":
                    if not get_volume():
                        set_volume(0.3)
                        self.backGround[0] = pygame.transform.scale(pygame.image.load(f"imgdino/startgame/buttonvolume0.png"), (self.Width, self.Height))
                    else:
                        set_volume(0)
                        self.backGround[0] = pygame.transform.scale(pygame.image.load(f"imgdino/startgame/buttonvolume1.png"), (self.Width, self.Height))
                pygame.time.wait(100)
                return True
        else:
            Screen.blit(self.backGround[0], (self.X, self.Y))
        pos = [self.X + self.Width/2 - self.surFace.get_width()//2, self.Y + self.Height/2 - self.surFace.get_height()//2]
        Screen.blit(self.surFace, pos)
        return False

def menu_setting(Surface):
        Clock = pygame.time.Clock()
        Status = True
        buttonExit = Button(740, 20, 50, 50, "X", 35)
        buttonVolume= Button(350, 175, 100, 100, "",0)
        buttonReturn = Button(320, 350, 160, 50, "Main menu", 15)
        Title = pygame.font.Font('imgdino/startgame/PressStart2P-Regular.ttf', 30).render("Setting", False, "yellow")
        posTitle = [800//2 - Title.get_width()//2, 50]
        while(Status):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            pygame.draw.rect(Surface, "gray", (25, 25, 750, 400), 0, 50)
            Surface.blit(Title, posTitle)
            if buttonExit.buttonEvent(Surface):
                return True
            buttonVolume.buttonEvent(Surface)
            if buttonReturn.buttonEvent(Surface):
                return False
            pygame.display.update()
            Clock.tick(60)

def announcement(checkWin, Score, highScore, Screen):
        Background = None
        if checkWin:
            Background = pygame.transform.scale(pygame.image.load(f"imgdino/startgame/background1.png"), (200, 200))
            Sounds["winGame"].play()
        else:
            Sounds["loseGame"].play()
            Background = pygame.transform.scale(pygame.image.load(f"imgdino/startgame/background2.png"), (200, 200))
        Clock = pygame.time.Clock()
        Replay = Button(50, 200, 100, 50, "Replay", 15)
        Exit = Button(650, 200, 100, 50, "Exit", 15)
        Next = Button(305, 370, 190, 50, "Next level", 15)
        scoreText = pygame.font.Font(typeText, 20).render(f"Scrore: {int(Score)}", False, "black")
        highScoreText = pygame.font.Font(typeText, 20).render(f"High scrore: {int(highScore)}", False, "yellow")
        backgroundRect = pygame.Rect(295, 25, 210, 400)
        while(True):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            if backgroundRect.width < 750:
                backgroundRect.x -= 10
                backgroundRect.width += 20
                pygame.draw.rect(Screen, "gray", backgroundRect, 0, 50)
                pygame.display.update()
                Clock.tick(60)
                continue
            pygame.draw.rect(Screen, "gray", (25, 25, 750, 400), 0, 50)
            if Replay.buttonEvent(Screen):
                return True, True
            if Exit.buttonEvent(Screen):
                return False, False
            if checkWin:
                if Next.buttonEvent(Screen):
                    return False, True
            Screen.blit(scoreText, scoreText.get_rect(center = (150, 70)))
            Screen.blit(highScoreText, highScoreText.get_rect(center = (600, 70)))
            Screen.blit(Background, Background.get_rect(center = (400, 250)))
            pygame.display.update()
            Clock.tick(10)

def set_volume(value):
    for Sound in Sounds:
            if Sound == "winGame" or Sound == "loseGame":
                Sounds[Sound].set_volume(value/2)
                continue
            Sounds[Sound].set_volume(value)

def get_volume():
    if Sounds["Click"].get_volume() == 0:
        return False
    return True