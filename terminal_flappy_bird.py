import msvcrt
import time
import os
import random

def detect_keypress():
    key = None
    if msvcrt.kbhit(): 
        key = msvcrt.getch()
    return key

def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")  

G = .5
FPS = .2

class Pipe:
    def __init__(self, gap) -> None:
        self.gap = gap
        self.v = -1.5
        
        self.grid = [["[][][]" for x in range(gap)], ["[][][]" for x in range(30-gap)]]
        self.pos = [[223, 0], [223, gap + 10]]
        self.size = (6, gap), (6, 30-gap)
        
    def move(self) -> None:
        self.pos[0][0] += self.v
        self.pos[1][0] += self.v
        
class Bird:
    def __init__(self) -> None:
        self.v = 0
        self.pos = [30, 10]
        self.grid = ["### ",
                     "#O#>",
                     "### ",]
        self.size = (4, 3)
    
    def move(self) -> None:
        self.v += G*FPS 
        self.pos[1] += self.v*FPS
        if self.pos[1] > 40-self.size[1]:
            self.pos[1] = 40-self.size[1]
        if self.pos[1] < 0:
            self.pos[1] = 0
        
bird = Bird()

n = 69
f = 0
pipes = []
while True:
    n += 1
    
    key = detect_keypress()
    if key:
        if key == bytes(" ", "utf-8"):    #cuando toco el espacio salta el pajerito
            bird.v = -3
        if key == bytes("\x1b", "utf-8"): # cuando toco el esc se termina el juego uwu
            print(f"SALISTE DEL JUEGO, PUNTAJE FINAL: {f}")
            break
        
    bird.move()
        
    if n == 70:
        pipes.append(Pipe(random.randint(3, 27)))
        n = 0
        
    for p in pipes[:]:
        p.move()
        if p.pos[0][0] < 0:
            pipes.remove(p)
            f += 1
        
    clear()
    
    cs = ""
    for y in range(40):
        c = [" " for x in range(230)]
        if int(bird.pos[1]) <= y and y < int(bird.pos[1]) + bird.size[1]:
            for xx, x in enumerate(bird.grid[y-int(bird.pos[1])]):
                c[bird.pos[0]+xx] = x
                
        for p in pipes:
            if p.pos[0][1] <= y and y < p.pos[0][1] + p.size[0][1]:
                for xx, x in enumerate(p.grid[0][y-p.pos[0][1]]):
                    c[int(p.pos[0][0])+xx] = x
                    
            if p.pos[1][1] <= y and y < p.pos[1][1] + p.size[1][1]:
                for xx, x in enumerate(p.grid[1][y-p.pos[1][1]]) :
                    c[int(p.pos[1][0])+xx] = x
        
        c = "".join(c)
        cs += c
        print(c)
        
    if cs.count("#") < 8:
        print(f"PERDISTE DEL JUEGO, PUNTAJE FINAL: {f}")
        break
        
    time.sleep(FPS)