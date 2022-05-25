from tkinter import *
import time
import random

tk = Tk()
tk.title('Game')
tk.resizable(0, 0)
tk.wm_attributes('-topmost', 1)
canvas = Canvas(tk, width=500, height=500, highlightthickness=0)
canvas.pack()
tk.update()

N = 50

class Ball: 
    def __init__(self, canvas, paddle,block, score, color):
        self.canvas = canvas
        self.paddle = paddle
        self.blocks = block
        self.score = score
        self.id = canvas.create_oval(10,10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 100)
        # задаём список возможных направлений для старта
        starts = [-2, -1, 1, 2] 
        random.shuffle(starts)
        self.x = starts[0]
        # в самом начале он всегда падает вниз, поэтому уменьшаем значение по оси y
        self.y = -2
        # шарик узнаёт свою высоту и ширину
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        # свойство, которое отвечает за то, достиг шарик дна или нет. Пока не достиг, значение будет False
        self.hit_bottom = False

    # обрабатываем касание платформы
    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                return True
        return False

    def hit_block(self, pos):
        global N
        for i in range(N):
            if self.blocks[i].visible!= False:
                block_pos = self.canvas.coords(self.blocks[i].id)
                if pos[0] <= block_pos[2] and pos[2] >= block_pos[0]:
                    if pos[1] <= block_pos[3] and pos[3] >= block_pos[1]:
                        self.score.hit()
                        self.blocks[i].visible = False
                        return True
        return False

    # метод, который отвечает за движение шарика
    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        # если шарик падает сверху  
        if pos[1] <= 0:
            self.y = 2
        # если шарик правым нижним углом коснулся дна
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
            # выводим сообщение и количество очков
            canvas.create_text(250, 120, text='Game Over', font=('Courier', 30), fill='red')
        # если было касание платформы
        if self.hit_paddle(pos) == True:
            self.y = -2
        if self.hit_block(pos) == True:
            #del self.block
            self.y = 2
        # если коснулись левой стенки
        if pos[0] <= 0:
            self.x = 2
        # если коснулись правой стенки
        if pos[2] >= self.canvas_width:
            self.x = -2
            
class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas 
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        # задаём список возможных стартовых положений платформы
        start_1 = [40, 60, 90, 120, 150, 180, 200]
        random.shuffle(start_1)
        self.starting_point_x = start_1[0]
        self.canvas.move(self.id, self.starting_point_x, 400)
        # пока платформа никуда не движется, поэтому изменений по оси х нет
        self.x = 0
        # платформа узнаёт свою ширину
        self.canvas_width = self.canvas.winfo_width()
        # задаём обработчик нажатий
        # если нажата стрелка вправо — выполняется метод turn_right()
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        # если стрелка влево — turn_left()
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all("<KeyRelease>", self.stop)
        # пока платформа не двигается, поэтому ждём
        self.started = False
        # как только игрок нажмёт Enter — всё стартует
        self.canvas.bind_all('<KeyPress-Return>', self.start_game)

    # движение 
    def turn_right(self, event):
        self.x = 2
    def turn_left(self, event):
        self.x = -2
    def stop(self, event):    
        self.x = 0
    # игра начинается
    def start_game(self, event):
        self.started = True

    # метод, который отвечает за движение платформы
    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        # если мы упёрлись
        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x = 0

class Block:
    def __init__(self, canvas, x, y, color):
        self.score = 0
        self.canvas = canvas
        self.id = canvas.create_rectangle(x, y, x+50, y+10, fill=color)
        self.visible = True

    def draw(self):
        if self.visible == False:
            canvas.itemconfigure(self.id, state='hidden')


class Score:
    def __init__(self, canvas, color):
        self.score = 0
        self.canvas = canvas
        self.id = canvas.create_text(450, 450, text=self.score, font=('Courier', 15), fill=color)

    # обрабатываем касание платформы
    def hit(self):
        self.score += 1 
        self.canvas.itemconfig(self.id, text=self.score)

        
score = Score(canvas, 'green')
paddle = Paddle(canvas, 'White')
block=[]
for i in range(N):
    for j in range(N//10):
        block.append(Block(canvas, 1+50*i, 1+10*j, 'grey'))
ball = Ball(canvas, paddle,block, score, 'red')
while not ball.hit_bottom:
    if paddle.started == True:
        ball.draw()
        paddle.draw()
        for i in range(N):
            block[i].draw()
    if score.score == N:
        canvas.create_text(250, 120, text='You Win', font=('Courier', 30), fill='red')
        self.hit_bottom = True
    # обновляем наше игровое поле, чтобы всё, что нужно, закончило рисоваться
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)
time.sleep(3)
