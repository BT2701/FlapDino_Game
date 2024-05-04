
Width, Height = 800, 450
typeText = "imgdino/startgame/PressStart2P-Regular.ttf"
Sounds = {}

def save_data(localData = 0, Data1 = 0, Data2 = "t"):
    f = open("data.txt", mode='r')
    r = f.readline().split(",")
    r[localData] = str(Data1)
    r[localData + 3] = Data2
    s = r[0] + "," + r[1] + "," + r[2] + "," + r[3] + "," + r[4] + "," + r[5]
    f.close()
    f = open("data.txt", mode='w')
    f.write(s)
    f.close()