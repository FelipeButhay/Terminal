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

FPS = .05
SX, SY = 228, 38
GX, GY = 114, 38

class Snake:
    def __init__(self) -> None:
        self.sprite = "#"
        self.direction = (1, 0)
        self.direction_s = (1, 0)
        self.body = [(1,1), (2,1), (3,1)]
        self.apple = False
        self.head = self.body[-1]
        
    def move(self):
        self.body.append((self.body[-1][0] + self.direction[0], self.body[-1][1] + self.direction[1]))
        if not self.apple:
            self.body.pop(0)
        else:
            self.apple = False
        self.head = self.body[-1]
        
    def illegal(self):
        if len(self.body) > len(set(self.body)):
            return True

        if self.head[0] >= GX or self.head[0] < 0 or self.head[1] >= GY or self.head[1] < 0:
            return True
        
        return False
    
class Apple:
    def __init__(self):
        self.sprite = "O"
        self.exist = False
        self.pos = None
        
    def spawn(self, body):
        self.exist = True
        while True:
            self.pos = random.randint(0, GX-1), random.randint(1, GY-1)
            if not self.pos in body:
                break
            
snake = Snake()
apple = Apple()
            
n = 0
while True:
    n += 1 
    key = detect_keypress()
    if key:
        if key == bytes("w", "utf-8") and snake.direction_s != ( 0, 1):    #cuando toco el espacio salta el pajerito
            snake.direction = ( 0,-1)
            print(snake.direction)
        if key == bytes("a", "utf-8") and snake.direction_s != ( 1, 0):    #cuando toco el espacio salta el pajerito
            snake.direction = (-1, 0)
            print(snake.direction)
        if key == bytes("s", "utf-8") and snake.direction_s != ( 0,-1):    #cuando toco el espacio salta el pajerito
            snake.direction = ( 0, 1)
            print(snake.direction)
        if key == bytes("d", "utf-8") and snake.direction_s != (-1, 0):    #cuando toco el espacio salta el pajerito
            snake.direction = ( 1, 0)
            print(snake.direction)
            
        if key == bytes("\x1b", "utf-8"): # cuando toco el esc se termina el juego uwu
            print(f"SALISTE DEL JUEGO")
            break
        
    if n%40:
        snake.move()
        snake.direction_s = snake.direction
        if apple.pos in snake.body:
            snake.apple = True
            apple.exist = False
            apple.pos = None
        if snake.illegal():
            print("PERDISTE EL JUEGO")
            break
        
        if not apple.exist:
            apple.spawn(snake.body)
        
        clear()
        screen = [["|", *[" " for x in range(SX)], "|"] for y in range(SY)]
        
        screen[1 + apple.pos[1]][1 + apple.pos[0]*2] = apple.sprite
        # for x in [(0,1), (0,-1), (1,0), (-1,0)]:
        #     screen[1 + apple.pos[1]*2 + x[1]][1 + apple.pos[0]*2 + x[0]] = apple.sprite
            
        for x in snake.body:
            screen[1 + x[1]][1 + x[0]*2] = snake.sprite
            
        print("-"*230)
        for y in screen:
            y = "".join(y)
            print(y)
        print("-"*230)
        
    time.sleep(FPS)