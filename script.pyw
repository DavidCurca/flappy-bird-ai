import time
import pyglet
from pyglet import image
from pyglet.window import mouse
from pyglet import clock
from pyglet.gl import *
import numpy as np
from pyglet.window import key
from random import seed
from random import randint
import random
import glob

seed(12345)
txtfiles = [""]*1000
num_files,num_page,total_page = 0,1,0
playerY,game_state,gravity,vel,lift,gen,clk = 450/2, 0, 0.6, 0, 15, 1, 0
gravityBird,velBird,liftBird = [0.8]*21,[0]*21,[15]*21
panSpeed,bestIndex,maxi = 8, 0, 0
colors = [(230, 25, 75, 255), (60, 180, 75, 255), (255, 225, 25, 255), (0, 130, 200, 255),
          (245, 130, 48, 255), (145, 30, 180, 255), (70, 240, 240, 255), (240, 50, 230, 255),
          (210, 245, 60, 255), (250, 190, 190, 255), (0, 128, 128, 255), (230, 190, 255, 255),
          (170, 110, 40, 255), (0, 0, 0, 255), (128, 0, 0, 255), (170, 255, 195, 255),
          (128, 128, 0, 255), (255, 215, 180, 255), (0, 0, 128, 255), (128, 128, 128, 255)]
names = ['Andrew', 'Billy', 'Willy', 'Joel', 'Mary', 'Michael', 'Austin',
         'Harry', 'Jordan', 'Alan', 'John', 'Mark', 'Henry', 'Paul', 'Pete',
         'Nick', 'Sam', 'Tom', 'Phill', 'Dick']
imgs = [image.load('imgs/players/1.png'), image.load('imgs/players/2.png'), image.load('imgs/players/3.png'), image.load('imgs/players/4.png'),
        image.load('imgs/players/5.png'), image.load('imgs/players/6.png'), image.load('imgs/players/7.png'), image.load('imgs/players/8.png'),
        image.load('imgs/players/9.png'), image.load('imgs/players/10.png'), image.load('imgs/players/11.png'), image.load('imgs/players/12.png'),
        image.load('imgs/players/13.png'), image.load('imgs/players/14.png'), image.load('imgs/players/15.png'), image.load('imgs/players/16.png'),
        image.load('imgs/players/17.png'), image.load('imgs/players/18.png'), image.load('imgs/players/19.png'), image.load('imgs/players/20.png')]
statuses = [True]*21
positions = [450/2]*21
scores = [0]*21
life_scores = [0]*21
biases = [[0 for i in range(4)] for j in range(22)]
weights = [[0 for i in range(15)] for j in range(22)]
brainIndex = 0
pipesX = [220, 520, 820, 1020]
pipesV = [0, 0, 0, 0]
menu_pic = image.load('imgs/menu.png')
load_pic = image.load('imgs/load.png')
wait_pic = image.load('imgs/wait.png')
back_pic = image.load('imgs/background.png')
backnn_pic = image.load('imgs/backnn.png')
pipe_pic = image.load('imgs/pipe.png')
player_pic = image.load('imgs/bird.png')
lose_pic = image.load('imgs/lost.png')
cell_pic = image.load('imgs/cell.png')
mini_pic = image.load('imgs/mini.png')
straight = [image.load('imgs/lines/straight/straight25.png'), image.load('imgs/lines/straight/straight25.png'), image.load('imgs/lines/straight/straight50.png'),
            image.load('imgs/lines/straight/straight75.png'), image.load('imgs/lines/straight/straight100.png')]
down = [image.load('imgs/lines/down/down25.png'), image.load('imgs/lines/down/down25.png'), image.load('imgs/lines/down/down50.png'),
            image.load('imgs/lines/down/down75.png'), image.load('imgs/lines/down/down100.png')]
up = [image.load('imgs/lines/up/up25.png'), image.load('imgs/lines/up/up25.png'), image.load('imgs/lines/up/up50.png'),
            image.load('imgs/lines/up/up75.png'), image.load('imgs/lines/up/up100.png')]
downsuper = [image.load('imgs/lines/downsuper/downsuper25.png'), image.load('imgs/lines/downsuper/downsuper25.png'), image.load('imgs/lines/downsuper/downsuper50.png'),
            image.load('imgs/lines/downsuper/downsuper75.png'), image.load('imgs/lines/downsuper/downsuper100.png')]
upsuper = [image.load('imgs/lines/upsuper/upsuper25.png'), image.load('imgs/lines/upsuper/upsuper25.png'), image.load('imgs/lines/upsuper/upsuper50.png'),
            image.load('imgs/lines/upsuper/upsuper75.png'), image.load('imgs/lines/upsuper/upsuper100.png')]
score = 0
window_menu = pyglet.window.Window(500, 500, 'flappy bird - menu', fullscreen=False)
window_game = pyglet.window.Window(720,450, 'flappy bird', fullscreen=False)
window_brain = pyglet.window.Window(720, 450, 'flappy bird - brain', fullscreen=False)
window_load = pyglet.window.Window(500, 500, 'flappy bird - load', fullscreen=False)
window_game.set_visible(False)
window_brain.set_visible(False)
window_load.set_visible(False)
window_brain.set_icon(mini_pic)
window_game.set_icon(player_pic)
window_menu.set_icon(player_pic)
window_load.set_icon(player_pic)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

for i in range(4):
    pipesV[i] = randint(10, 140)

for i in range(20):
    for j in range(12):
        weights[i][j] = round(random.uniform(-1, 1), 2)
    for j in range(4):
        biases[i][j] = round(random.uniform(-1, 1), 2)


@window_menu.event
def on_mouse_press(x, y, button, modifiers):
    global game_state
    if button == mouse.LEFT:
        if(x >= 70 and x <= 390 and y >= 300 and y <= 375):
            game_state = 1
            print('Play Yourself')
            window_menu.set_visible(False)
            window_game.set_visible(True)
        elif(x >= 70 and x <= 390 and y >= 200 and y <= 277):
            game_state = 2
            print('Train A.I')
            window_menu.set_visible(False)
            window_game.set_visible(True)
            window_brain.set_visible(True)

@window_game.event
def on_mouse_press(x, y, button, modifiers):
    global game_state,score,pipesX,pipesV
    if button == mouse.LEFT:
        if(game_state == 0):
            if(x >= 175 and x <= 533 and y >= 215 and y <= 320):
                game_state = 1
                score = 0
                pipesX = [520, 820, 1120, 1320]
                pipesV = [0, 0, 0, 0]
                for i in range(4):
                    pipesV[i] = randint(10, 160)
            elif(x >= 175 and x <= 533 and y >= 85 and y <= 175):
                print('Exit')
                window_game.close()
                window_menu.close()
                window_brain.close()

@window_brain.event
def on_mouse_press(x, y, button, modifiers):
    global brainIndex,game_state
    if button == mouse.LEFT:
        if(x >= 520 and x <= 715 and y >= 60 and y <= 100):
            UpdateFiles()
            SaveModel(brainIndex)
        elif(x >= 520 and x <= 715 and y >= 10 and y <= 100):
            window_brain.set_visible(False)
            window_load.set_visible(True)
            game_state = 3

@window_load.event
def on_mouse_press(x, y, button, modifiers):
    global brainIndex,game_state,num_filse,num_page,total_page
    if button == mouse.LEFT:
        if(x >= 25 and x <= 210 and y >= 25 and y <= 70):
            print("Prev")
            if(num_page > 1):
                num_page -= 1
        elif(x >= 290 and x <= 470 and y >= 25 and y <= 70):
            print("Next")
            if(num_page < total_page):
                num_page += 1
        elif(x >= 23 and x <= 472 and y >= 390 and y <= 430):
            LoadNeuralNetwork(txtfiles[(num_page*7-6)])
        elif(x >= 23 and x <= 472 and y >= 335 and y <= 378):
            LoadNeuralNetwork(txtfiles[(num_page*7-6)+1])
        elif(x >= 23 and x <= 472 and y >= 285 and y <= 330):
            LoadNeuralNetwork(txtfiles[(num_page*7-6)+2])
        elif(x >= 23 and x <= 472 and y >= 235 and y <= 280):
            LoadNeuralNetwork(txtfiles[(num_page*7-6)+3])
        elif(x >= 23 and x <= 472 and y >= 185 and y <= 230):
            LoadNeuralNetwork(txtfiles[(num_page*7-6)+4])
        elif(x >= 23 and x <= 472 and y >= 133 and y <= 175):
            LoadNeuralNetwork(txtfiles[(num_page*7-6)+5])
        elif(x >= 23 and x <= 472 and y >= 80 and y <= 125):
            LoadNeuralNetwork(txtfiles[(num_page*7-6)+6])

def ResetGame():
    global gen,brainIndex,bestIndex,maxi,clk
    gen,brainIndex,bestIndex,clk = 0,0,0,0
    for i in range(20):
        positions[i] = 450/2
        life_scores[i] = 0
        scores[i] = 0
    maxi = 0
    biases = [[0 for i in range(4)] for j in range(22)]
    weights = [[0 for i in range(15)] for j in range(22)]
    brainIndex = 0
    pipesX = [220, 520, 820, 1020]
    pipesV = [0, 0, 0, 0]
    for i in range(4):
        pipesV[i] = randint(10, 140)
    gravityBird,velBird,liftBird = [0.8]*21,[0]*21,[15]*21

def LoadNeuralNetwork(file):
    global game_state
    state = 1
    weight_index = -1
    bias_index = -1
    ResetGame()
    model = open("models/" + file)
    for i in range(17):
        try:
            line = model.readline()
            value = float(line)
            if(state == 1):
                weight_index += 1
                for nn in range(20):
                    weights[nn][weight_index] = value
            else:
                bias_index += 1
                for nn in range(20):
                    biases[nn][bias_index] = value
        except:
            state = 2
    window_load.set_visible(False)
    window_brain.set_visible(True)
    game_state = 2

@window_menu.event
def on_draw():
    window_menu.clear()
    menu_pic.blit(0, 0, 0)

@window_load.event
def on_draw():
    global num_page
    window_load.clear()
    load_pic.blit(0,0,0)
    label_file = pyglet.text.Label(txtfiles[(num_page*7-6)],font_name='Times New Roman',font_size=14,color = (0, 0, 0, 255),x = 100, y = 410,anchor_x='center', anchor_y='center'); label_file.draw()
    label_file = pyglet.text.Label(txtfiles[(num_page*7-6)+1],font_name='Times New Roman',font_size=14,color = (0, 0, 0, 255),x = 100, y = 360,anchor_x='center', anchor_y='center'); label_file.draw()
    label_file = pyglet.text.Label(txtfiles[(num_page*7-6)+2],font_name='Times New Roman',font_size=14,color = (0, 0, 0, 255),x = 100, y = 310,anchor_x='center', anchor_y='center'); label_file.draw()
    label_file = pyglet.text.Label(txtfiles[(num_page*7-6)+3],font_name='Times New Roman',font_size=14,color = (0, 0, 0, 255),x = 100, y = 260,anchor_x='center', anchor_y='center'); label_file.draw()
    label_file = pyglet.text.Label(txtfiles[(num_page*7-6)+4],font_name='Times New Roman',font_size=14,color = (0, 0, 0, 255),x = 100, y = 210,anchor_x='center', anchor_y='center'); label_file.draw()
    label_file = pyglet.text.Label(txtfiles[(num_page*7-6)+5],font_name='Times New Roman',font_size=14,color = (0, 0, 0, 255),x = 100, y = 160,anchor_x='center', anchor_y='center'); label_file.draw()
    label_file = pyglet.text.Label(txtfiles[(num_page*7-6)+6],font_name='Times New Roman',font_size=14,color = (0, 0, 0, 255),x = 100, y = 110,anchor_x='center', anchor_y='center'); label_file.draw()

@window_menu.event
def on_close():
    quit()

@window_load.event
def on_close():
    quit()

@window_game.event
def on_close():
    quit()

@window_brain.event
def on_close():
    quit()


@window_game.event
def on_key_press(symbol, modifiers):
    if symbol == 32:
        if(game_state == 1):
            Jump()
        
def Jump():
   global playerY,vel,lift
   vel = -10

def JumpBird(i):
    velBird[i] = -10

def UpdateFiles():
    global num_files,total_page
    index = 0
    for file in glob.glob("models/*.txt"):
        index += 1
        result = ""
        number_string = ""
        number_int = 0
        can_copy = False
        for char in file:
            if(can_copy == True):
                result += char
                if(char >= '0' and char <= '9'):
                    number_string += char
            elif(can_copy == False and char == '\\'):
                can_copy = True
        txtfiles[index] = result
        for i in range(len(number_string)):
            number_int *= 10
            number_int += int(number_string[i-len(number_string)])
        if(number_int > num_files):
            num_files = number_int+1
    total_page = index/7
    if(index%7 != 0):
        total_page += 1
    total_page = int(total_page)

def SaveModel(index):
    global num_files
    f = open("models/model_" + str(num_files) + ".txt", "w")
    for i in range(12):
        f.write(str(round(weights[index][i], 2)) + "\n")
    f.write("\n")
    for i in range(4):
        f.write(str(round(biases[index][i], 2)) + "\n")
    f.close()
    print("Save Model")
    num_files += 1

def Sigmoid(x):
    return 1/(1 + np.exp(-x))

def CalculateNeuralNetwork(index):
    positionOfBird = 450-int(positions[index])
    topPipe = int(260+pipesV[CelMaiApropiat()])
    bottomPipe = int((260+pipesV[CelMaiApropiat()]-35)-90)
    hL    = [0]*4
    hL[0] = reLU((Encode(positionOfBird)*weights[index][0])+(Encode(topPipe)*weights[index][3])+(Encode(bottomPipe)*weights[index][6])+biases[index][0])
    hL[1] = reLU((Encode(positionOfBird)*weights[index][1])+(Encode(topPipe)*weights[index][4])+(Encode(bottomPipe)*weights[index][7])+biases[index][1])
    hL[2] = reLU((Encode(positionOfBird)*weights[index][2])+(Encode(topPipe)*weights[index][5])+(Encode(bottomPipe)*weights[index][8])+biases[index][2])
    G = (hL[0]*weights[index][9]) + (hL[1]*weights[index][10]) + (hL[2]*weights[index][11]) + biases[index][3]
    G = Sigmoid(G)
    return round(G, 2)

def reLU(x):
    if(x < 0):
        return 0
    return x

def Encode(x):
    return x/450

def GetIndex(weight):
    if(weight < 0.25):
        return 0
    elif(weight < 0.50):
        return 1
    elif(weight < 0.75):
        return 2
    else:
        return 3

def DrawNeuralNetwork(index):
    global clk
    result = CalculateNeuralNetwork(index)
    if(clk%5 == 0 and result >= 0.50):
        JumpBird(index)
    cell_pic.blit(150, 140, 0)
    cell_pic.blit(150, 240, 0)
    cell_pic.blit(150, 345, 0)
    cell_pic.blit(300, 140, 0)
    cell_pic.blit(300, 240, 0)
    cell_pic.blit(300, 340, 0)
    cell_pic.blit(450, 240, 0)

    straight[GetIndex(weights[index][0])].blit(225, 340, 0)
    straight[GetIndex(weights[index][4])].blit(225, 240, 0)
    straight[GetIndex(weights[index][8])].blit(225, 140, 0)
    straight[GetIndex(weights[index][10])].blit(375, 240, 0)
    
    down[GetIndex(weights[index][1])].blit(225, 295, 0)
    down[GetIndex(weights[index][5])].blit(225, 195, 0)
    down[GetIndex(weights[index][9])].blit(375, 295, 0)
    
    downsuper[GetIndex(weights[index][2])].blit(225, 195, 0)
    
    up[GetIndex(weights[index][3])].blit(225, 282, 0)
    up[GetIndex(weights[index][7])].blit(225, 182, 0)
    up[GetIndex(weights[index][11])].blit(375, 182, 0)
    
    upsuper[GetIndex(weights[index][6])].blit(225, 190, 0)
    label_position = pyglet.text.Label(str(450-int(positions[index])),font_name='Times New Roman',font_size=14,color = (0, 0, 0, 255),x = 195, y = 390,anchor_x='center', anchor_y='center');label_position.draw()
    label_position = pyglet.text.Label(str(int(260+pipesV[CelMaiApropiat()])),font_name='Times New Roman',font_size=14,color = (0, 0, 0, 255),x = 195, y = 285,anchor_x='center', anchor_y='center'); label_position.draw()
    label_position = pyglet.text.Label(str(int((260+pipesV[CelMaiApropiat()]-35)-90)),font_name='Times New Roman',font_size=14,color = (0, 0, 0, 255),x = 195, y = 180,anchor_x='center', anchor_y='center');label_position.draw()
    #label_bias = pyglet.text.Label(str(biases[index][0]),font_name='Times New Roman',font_size=14,color = (0, 0, 0, 255),x = 345, y = 380,anchor_x='center', anchor_y='center'); label_bias.draw()
    #label_bias = pyglet.text.Label(str(biases[index][1]),font_name='Times New Roman',font_size=14,color = (0, 0, 0, 255),x = 345, y = 280,anchor_x='center', anchor_y='center'); label_bias.draw()
    #label_bias = pyglet.text.Label(str(biases[index][2]),font_name='Times New Roman',font_size=14,color = (0, 0, 0, 255),x = 345, y = 180,anchor_x='center', anchor_y='center'); label_bias.draw()
    label_result = pyglet.text.Label(str(result),font_name='Times New Roman',font_size=14,color = (0, 0, 0, 255),x = 495, y = 285,anchor_x='center', anchor_y='center'); label_result.draw()

def CelMaiApropiat():
    mini = 10000000
    index = 0
    for i in range(4):
        if(mini > pipesX[i]):
            mini = pipesX[i]
            index = i
    return index

@window_brain.event
def on_draw():
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    global brainIndex,clk,maxi,bestIndex
    if(game_state == 2):
        window_brain.clear()
        backnn_pic.blit(0,0,0)
        status = "Alive"
        status_color = (0, 255, 0, 255)
        if(statuses[brainIndex] == False):
            status = "Dead"
            status_color = (255, 0, 0, 255)
        label_name = pyglet.text.Label(names[brainIndex],font_name='Times New Roman',font_size=16,color = colors[brainIndex],x = 150, y = 85,anchor_x='center', anchor_y='center')
        label_status = pyglet.text.Label(status,font_name='Times New Roman',font_size=16,color = status_color,x = 155,y = 50,anchor_x='center', anchor_y='center')
        label_score = pyglet.text.Label(str(life_scores[brainIndex]),font_name='Times New Roman',font_size=16,color = (0, 0, 0, 255),x = 120 ,y = 20,anchor_x='center', anchor_y='center')
        life_scores[brainIndex] += 1
        if(life_scores[brainIndex] > maxi):
            maxi = life_scores[brainIndex]
            bestIndex = brainIndex
        label_name.draw()
        label_status.draw()
        label_score.draw()
        DrawNeuralNetwork(brainIndex)

@window_game.event
def on_draw():
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    global game_state,clk,brainIndex,maxi,bestIndex,gen
    window_game.clear()
    label = pyglet.text.Label('Score: ' + str(score),
                          font_name='Times New Roman',
                          font_size=20,
                          x=50, y=430,
                          anchor_x='center', anchor_y='center')
    if(game_state == 1):
        back_pic.blit(0, 0, 0)
        global playerY,vel,gravity,pipesX
        vel = vel+gravity
        vel = vel*0.9
        playerY = playerY+vel
        if(playerY >= 430):
            playerY = 430
            vel = 0
        elif(playerY <= 70):
            playerY = 70
            vel = 0
        player_pic.blit(20, 450-playerY, 0)
        for i in range(4):
            pipe_pic.blit(pipesX[i],-300+pipesV[i], 0)
            pipe_pic.blit(pipesX[i], 280+pipesV[i], 0)
            pipesX[i] = pipesX[i]-2
        updatePipes()
        CheckCollision(playerY, 1)
        #print(str(280+pipesV[0]-35) + ", " + str((280+pipesV[0]-35)-115) + ": " + str(500-playerY))
        #player_pic.blit(20, 260+pipesV[CelMaiApropiat()], 0)
        #player_pic.blit(20, (260+pipesV[CelMaiApropiat()]-35)-90, 0)
        label.draw()
    elif(game_state == 0):
        lose_pic.blit(0, 0, 0)
    elif(game_state == 2):
        clk = clk+1
        back_pic.blit(0, 0, 0)
        for i in range(4):
            pipe_pic.blit(pipesX[i],-300+pipesV[i], 0)
            pipe_pic.blit(pipesX[i], 280+pipesV[i], 0)
            pipesX[i] = pipesX[i]-5
        imgs[brainIndex].blit(20, 450-positions[brainIndex], 0)
        AddGravity()
        updatePipes()
        label = pyglet.text.Label('Score: ' + str(scores[brainIndex]),font_name='Times New Roman',font_size=20,x=50, y=430,anchor_x='center', anchor_y='center'); label.draw()
        label = pyglet.text.Label('Gen: ' + str(gen),font_name='Times New Roman',font_size=20,x=40, y=400,anchor_x='center', anchor_y='center'); label.draw()
        if(CheckCollision(positions[brainIndex], 2) == True):
            if(brainIndex == 19):
                gen += 1
                print("Update Brains")
                print("Clone NN. number: " + str(bestIndex))
                CloneNeuralNetwork(bestIndex)
                brainIndex = 0
                for i in range(20):
                    life_scores[i] = 0
                    scores[i] = 0
                maxi = 0
            else:
                brainIndex += 1
                positions[brainIndex] = 225
                pipesX = [220, 520, 820, 1020]
        UpdateFiles()
    elif(game_state == 3):
        wait_pic.blit(0, 0, 0)

def CloneNeuralNetwork(index):
    for i in range(20):
        for j in range(12):
            weights[i][j] = weights[index][j]
        for j in range(4):
            biases[i][j] = biases[index][j]
    for i in range(20):
        nr_schimbare = 0
        for j in range(12):
            #change weights
            coin = random.uniform(-1, 1)
            if(coin > 0.5):
                weights[i][j] += random.uniform(-0.5, 0.5)
        for j in range(4):
            #change biases
            coin = random.uniform(-1, 1)
            if(coin > 0.5):
                biases[i][j] += random.uniform(-0.5, 0.5)
def AddGravity():
    for i in range(20):
        velBird[i] = velBird[i]+gravityBird[i]
        velBird[i] = velBird[i]*0.9
        positions[i] = positions[i]+velBird[i]
        if(positions[i] >= 430):
            positions[i] = 430
            velBird[i] = 0
        elif(positions[i] <= 70):
            positions[i] = 70
            velBird[i] = 0

def updatePipes():
    global pipesX,score,brainIndex
    for i in range(4):
        if(pipesX[i] <= -40):
            pipesX[i] = 1020
            pipesV[i] = randint(10, 140)
            score = score+1
            scores[brainIndex] += 1

def CheckCollision(birdY, g):
    global game_state
    for i in range(4):
        if(pipesX[i] <= 70):
            if(not (450-birdY <= 260+pipesV[CelMaiApropiat()] and 450-birdY >= (260+pipesV[CelMaiApropiat()]-35)-90)):
                if(g == 1):
                    game_state = 0;
                return True
    return False

def update(self):
    global game_state
    
pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.app.run()
#don't bully me, im 11
