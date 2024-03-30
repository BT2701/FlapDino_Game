from button import *
from map1 import *
from map2 import *
from map3 import *
from Setting import *
import pygame,sys

class Main():
    #Khởi tạo game
    def __init__(self, Width, Height):
        pygame.init()
        float()

        pygame.display.set_caption('Khủng long bạo túa và những người bạn')
        Sounds["musicgame"] = pygame.mixer.Sound("./imgdino/startgame/musicstartgame.wav")
        Sounds["Click"] = pygame.mixer.Sound('./imgdino/startgame/tap.wav')
        Sounds["winGame"] = pygame.mixer.Sound('./imgdino/startgame/wingame1.wav')
        Sounds["loseGame"] = pygame.mixer.Sound('./imgdino/startgame/losegame1.wav')
        Sounds["musicgame"].set_volume(0.1)
        Sounds["musicgame"].play(loops = -1)
        self.Width, self.Height = Width, Height
        self.Screen = pygame.display.set_mode([Width, Height])
        self.Clock = pygame.time.Clock() 
        self.Background = pygame.transform.scale(pygame.image.load(f"./imgdino/startgame/background.png"), (Width, Height))
        self.T = map1(self.Screen)
        self.Mi = map2(self.Screen)
        self.Ma = map3(self.Screen)
        f = open("data.txt", "r")
        Data = f.readline().split(",")
        self.T.highScore = int(Data[0])
        self.Mi.highScore = int(Data[1])
        self.Ma.highScore = int(Data[2])
        if Data[3] == "f":
            self.T.Block = False
        if Data[4] == "f":
            self.Mi.Block = False
        if Data[5] == "f":
            self.Ma.Block = False
        f.close()
        set_volume(0.3)

    #Màn hình game start
    def start_game(self):
        buttonStartGame = Button(315, 180, 170, 70, "Start game", 15)
        buttonLoadSave = Button(315, 270, 170, 70, "Load save", 15)
        buttonSetting = Button(315, 360, 170, 70, "Setting", 15)
        Title = pygame.transform.scale(pygame.image.load(f"./imgdino/startgame/title.png"), (Width - 200, 200))
        titlePos = Title.get_rect(center = (Width//2, -50))
        while(True):
            self.Screen.blit(self.Background, (0, 0))
            self.Screen.blit(Title, titlePos)
            if titlePos.centery < 100:
                titlePos.centery += 5
                pygame.display.update()
                self.Clock.tick(60)
                continue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            if buttonStartGame.buttonEvent(self.Screen):
                self.video_intro_game()
                self.level_1()
            if buttonSetting.buttonEvent(self.Screen):
                menu_setting(self.Screen)
            if buttonLoadSave.buttonEvent(self.Screen):
                self.load_game()
            pygame.display.update()
            self.Clock.tick(60)
    
#Màn 1
    def level_1(self):
        self.T.Block = False
        self.T.set_event()
        self.T.reset_game()
        if self.T.run():
            self.level_2()
        
# Màn 2
    def level_2(self):
        self.Mi.Block = False
        self.Mi.set_event()
        self.Mi.reset_game()
        if self.Mi.run():
            self.level_3()
#Màn 3
    def level_3(self):
        self.Ma.Block = False
        self.Ma.set_event()
        self.Ma.reset_game()
        if self.Ma.run():
            if random.randint(1,2) == 1:
                self.video_end1_game()
            else:
                self.video_end2_game()

    def video_intro_game(self):
        EVTANI = pygame.USEREVENT + 9
        textHD = pygame.font.Font(typeText, 15).render("Click to continue", False, "black")
        background = pygame.transform.scale(pygame.image.load(f"./imgdino/map1/background0.png"), (self.Width, self.Height))
        closeBG = pygame.transform.scale(pygame.image.load(f"./imgdino/startgame/blackBG.png"), (self.Width, self.Height + 20))
        Dino = []
        girlDino = pygame.transform.scale(pygame.image.load(f"./imgdino/startgame/dinogirl0.png"), (100, 100))
        Boss = pygame.transform.scale(pygame.image.load(f"./imgdino/map3/boss0.png"), (250, 250))
        for i in range(3):
            Dino.append(pygame.transform.scale(pygame.image.load(f"./imgdino/startgame/dino{i}.png"), (100, 100)))
        posDino = pygame.Vector2((self.Width/2 -140,self.Height - 145))
        posCloseBG = pygame.Vector2((0,(self.Height +20)*(-1)))
        posDinoGirl = pygame.Vector2((self.Width/2 ,self.Height - 145))
        posEnemy = pygame.Vector2((self.Width + 100,self.Height - 270))
        with open("SGChat.txt", 'r') as f:
            dataList = f.readlines()
        textList = []
        for s in dataList:
            textList.append(s.strip())
        numText = 0
        aniDino = 0
        Chat = True
        endChat = False
        endIntro = False
        lastChat = False
        closeScreen = False
        while True:
            self.Screen.fill("white")
            self.Screen.blit(background, (0,0))
            if endChat:
                if posEnemy.x < posDinoGirl.x:
                    posEnemy.x += 6
                    posDinoGirl.x += 6
                    lastChat = True
                    if posDinoGirl.x > self.Width:
                        endChat = False
                        endIntro = True
                        pygame.time.set_timer(EVTANI, 100)
                else:
                    posEnemy.x -= 6
            if endIntro:
                posDino.x += 6 
                if posDino.x > self.Width + 100:
                    endIntro = False
                    closeScreen = True
                    pygame.time.set_timer(EVTANI, 0)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if Chat:
                        numText += 1
                        if numText == len(textList) -1:
                            Chat = False
                            endChat = True
                if event.type == EVTANI:
                    aniDino += 1
                    if aniDino == len(Dino):
                        aniDino = 0

            self.Screen.blit(Dino[aniDino], posDino)
            self.Screen.blit(girlDino, posDinoGirl)
            self.Screen.blit(Boss, posEnemy)
            if Chat:
                if numText%2 == 0:
                    Text = pygame.font.Font(typeText, 17).render(textList[numText], False, "black")
                else:
                    Text = pygame.font.Font(typeText, 17).render(textList[numText], False, "DeepPink1")
                rectText = Text.get_rect(center = (self.Width//2, self.Height//2))
                self.Screen.blit(Text, rectText)
                self.Screen.blit(textHD, (self.Width - textHD.get_width(),self.Height - textHD.get_height()))
            if lastChat:
                Text = pygame.font.Font(typeText, 17).render(textList[numText], False, "DeepPink1")
                rectText = Text.get_rect(center = (self.Width//2, self.Height//2))
                self.Screen.blit(Text, rectText)
            if closeScreen:
                posCloseBG.y += 6
                self.Screen.blit(closeBG, posCloseBG)
                if posCloseBG.y > 0:
                    return
            pygame.display.update()
            self.Clock.tick(60)
    
    def video_end1_game(self):
        EVTANI = pygame.USEREVENT + 6
        pygame.time.set_timer(EVTANI, 100)
        EVTRAG = pygame.USEREVENT + 7
        textHD = pygame.font.Font(typeText, 15).render("Click to continue", False, "black")
        buttonEnd = Button(self.Width - 150, self.Height - 100, 100, 50, "End game", 10)
        background = pygame.transform.scale(pygame.image.load(f"./imgdino/map1/background0.png"), (self.Width, self.Height))
        Dino = []
        girlDino = []
        richDino = []
        cryDino = pygame.transform.scale(pygame.image.load(f"./imgdino/startgame/dinocry0.png"), (100, 100))
        for i in range(3):
            richDino.append(pygame.transform.scale(pygame.image.load(f"./imgdino/startgame/richdino{i}.png"), (100, 100)))
        for i in range(3):
            Dino.append(pygame.transform.scale(pygame.image.load(f"./imgdino/startgame/dino{i}.png"), (100, 100)))
        for i in range(3):
            girlDino.append(pygame.transform.scale(pygame.image.load(f"./imgdino/startgame/dinogirl{i}.png"), (100, 100)))
        pos = pygame.Vector2((0,self.Height - 145))
        pos2 = pygame.Vector2((self.Width/2 ,self.Height - 145))
        pos3 = pygame.Vector2((self.Width/2 + 100,self.Height - 145))
        with open("BEChat.txt", 'r') as f:
            dataList = f.readlines()
        textList = []
        for s in dataList:
            textList.append(s.strip())
        numText = 0
        animationDino = 0
        animationRichDino = 0
        animationGirlDino = 0
        checkChat = False
        checkEndChat = False
        while True:
            self.Screen.fill("white")
            if pos.x < pos2.x - 200:
                pos.x += 2
            else:
                if not checkEndChat:
                    checkChat = True
                    pygame.time.set_timer(EVTANI, 0)
                    animationDino = 0 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == EVTANI:
                    animationDino += 1
                    if animationDino == len(Dino):
                        animationDino = 0
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if checkChat:
                        numText += 1
                        if numText == len(textList):
                            checkChat = False
                            checkEndChat = True
                            pygame.time.set_timer(EVTRAG, 100)
                if event.type == EVTRAG:
                    animationRichDino += 1
                    if animationRichDino == len(Dino):
                        animationRichDino = 0
                    animationGirlDino += 1
                    if animationGirlDino == len(Dino):
                        animationGirlDino = 0
            self.Screen.blit(background, (0,0))
            self.Screen.blit(Dino[animationDino], pos)
            self.Screen.blit(girlDino[animationGirlDino], pos2)
            self.Screen.blit(richDino[animationRichDino], pos3)
            if checkChat:
                if numText%2 == 0:
                    Text = pygame.font.Font(typeText, 17).render(textList[numText], False, "black")
                else:
                    Text = pygame.font.Font(typeText, 17).render(textList[numText], False, "DeepPink1")
                rectText = Text.get_rect(center = (self.Width//2, self.Height//2))
                self.Screen.blit(Text, rectText)
                self.Screen.blit(textHD, (self.Width - textHD.get_width(),self.Height - textHD.get_height()))
            if checkEndChat:
                    if pos2.x > -100:
                        pos2.x -= 2
                    if pos3.x > -100:
                        pos3.x -= 2
                    else:
                        self.Screen.blit(cryDino, pos)
                        if buttonEnd.buttonEvent(self.Screen):
                            pygame.time.set_timer(EVTANI, 0)
                            pygame.time.set_timer(EVTRAG, 0)
                            return
            pygame.display.update()
            self.Clock.tick(60)
    
    def video_end2_game(self):
        EVTANI = pygame.USEREVENT + 6
        pygame.time.set_timer(EVTANI, 100)
        nameFile = "HEChat.txt"
        textHD = pygame.font.Font(typeText, 15).render("Click to continue", False, "black")
        buttonEnd = Button(self.Width - 150, self.Height - 100, 100, 50, "End game", 10)
        background = pygame.transform.scale(pygame.image.load(f"./imgdino/map1/background0.png"), (self.Width, self.Height))
        Dino = []
        girlDino = pygame.transform.scale(pygame.image.load(f"./imgdino/startgame/dinogirl0.png"), (100, 100))
        Heart = pygame.image.load(f"imgdino/startgame/h2.png")
        for i in range(3):
            Dino.append(pygame.transform.scale(pygame.image.load(f"./imgdino/startgame/dino{i}.png"), (100, 100)))
        pos = pygame.Vector2((0,self.Height - 145))
        pos2 = pygame.Vector2((self.Width/2 ,self.Height - 145))
        posHeart =  pygame.Vector2((self.Width//2 - 27, self.Height - 145))
        with open(nameFile, 'r') as f:
            dataList = f.readlines()
        textList = []
        for s in dataList:
            textList.append(s.strip())
        numText = 0
        animationDino = 0
        checkChat = False
        checkEndChat = False
        while True:
            self.Screen.fill("white")
            if pos.x < pos2.x - 200:
                pos.x += 2
            else:
                if not checkEndChat:
                    checkChat = True
                    pygame.time.set_timer(EVTANI, 0)
                    animationDino = 0 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == EVTANI:
                    animationDino += 1
                    if animationDino == len(Dino):
                        animationDino = 0
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not checkChat:
                        continue
                    numText += 1
                    if numText == len(textList):
                        checkChat = False
                        checkEndChat = True
            self.Screen.blit(background, (0,0))
            self.Screen.blit(Dino[animationDino], pos)
            self.Screen.blit(girlDino, pos2)
            if checkChat:
                if numText%2 == 0:
                    Text = pygame.font.Font(typeText, 17).render(textList[numText], False, "black")
                else:
                    Text = pygame.font.Font(typeText, 17).render(textList[numText], False, "DeepPink1")
                rectText = Text.get_rect(center = (self.Width//2, self.Height//2))
                self.Screen.blit(Text, rectText)
                self.Screen.blit(textHD, (self.Width - textHD.get_width(),self.Height - textHD.get_height()))
            if checkEndChat:
                if pos.x < pos2.x - 90:
                    pos.x += 2
                else:
                    pygame.time.set_timer(EVTANI, 0)
                    animationDino = 0 
                    if posHeart.y > -20:
                        posHeart.y -= 2
                    else:
                        posHeart.y = self.Height - 145
                    if buttonEnd.buttonEvent(self.Screen):
                        pygame.time.set_timer(EVTANI, 0)
                        return
                    self.Screen.blit(Heart, posHeart)
            pygame.display.update()
            self.Clock.tick(60)

    def load_game(self):
        Maps = []
        checkMap = [False, False, False]
        mapRect = [] 
        lvText = []
        lvRect = []
        buttonReturn = Button(20, 20, 100, 30, "Return", 10)
        chainImage = pygame.transform.scale(pygame.image.load(f"./imgdino/startgame/chain.png"), (200, 200))
        for i in range(3):
            Maps.append(pygame.transform.scale(pygame.image.load(f"./imgdino/startgame/level{i + 1}.png"), (200, 200)))
            mapRect.append(Maps[i].get_rect(topleft = (50+ i*50 + i *200, 125)))
            lvText.append(pygame.font.Font(typeText, 20).render(f"Level {i + 1}", True, ("black")))
            lvRect.append(lvText[i].get_rect(topleft = (80+ i*50 + i *200, 350)))
        if self.T.Block:
            checkMap[0] = True
        if self.Mi.Block:
            checkMap[1] = True
        if self.Ma.Block:
            checkMap[2] = True
        while(True):
            mousePos = pygame.mouse.get_pos() 
            self.Screen.fill("white")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            for i in range(len(Maps)):
                self.Screen.blit(Maps[i], mapRect[i])
                self.Screen.blit(lvText[i], lvRect[i])
                if checkMap[i]:
                    self.Screen.blit(chainImage, mapRect[i])
                else:
                    if mapRect[i].collidepoint(mousePos):
                        if pygame.mouse.get_pressed(num_buttons = 3)[0]:
                            Sounds["Click"].play()
                            if i == 0:
                               self.level_1()
                               return
                            elif i == 1:
                               self.level_2()
                               return
                            else:
                               self.level_3()
                               return
            if buttonReturn.buttonEvent(self.Screen):
                return
            pygame.display.update()
            self.Clock.tick(60)
            
# Hàm main để chạy chương trình
if __name__ == '__main__':
    game = Main(800, 450)
    game.start_game()