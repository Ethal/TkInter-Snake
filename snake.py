#!/usr/bin/python
# -*- encoding: utf-8 -*-

import random
import string

try:
    import tkinter
except ImportError:
    import Tkinter as tkinter

FOOD_COLOR = ('yellow','yellow')


class Application:
    TITLE = 'Snake'
    SIZE = 300, 300
    MOVE = 10
    SNAKE_SIZE = 7

    # initialize parameters of this class && parameters of Tk() class
    def __init__(self, master):
        self.master = master

        self.head = None
        self.head_position = None
        # segment : Snake body
        self.segments = []
        self.segment_positions = []
        self.food = None
        self.food_position = None
        self.direction = None
        self.moved = True

        self.running = False
        # below : initialize the specific parameter of Tk() class
        self.init()

    def init(self):
        self.master.title(self.TITLE)

        self.canvas = tkinter.Canvas(self.master)
        self.canvas.grid(sticky=tkinter.NSEW)

        self.start_button = tkinter.Button(self.master, text='Start', command=self.on_start)
        self.start_button.grid(sticky=tkinter.EW)

        self.master.bind('<Up>', self.on_up) #w
        self.master.bind('<Left>', self.on_left) #a
        self.master.bind('<Down>', self.on_down) #s
        self.master.bind('<Right>', self.on_right) #d
        self.master.bind('p', self.on_pause) #pause

        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.master.resizable(width=False, height=False)
        self.master.geometry('%dx%d' % self.SIZE)

    def on_start(self):
        self.reset()
        if self.running:
            self.running = False
            self.start_button.configure(text='Start')
        else:
            self.running = True
            self.start_button.configure(text='Stop')
            self.start()

    def reset(self):
        #self.segments.clear() # Not work with python 2.7
        self.segments = [] # to be check on python 3.x
        #self.segment_positions.clear() # Not work with python 2.7
        self.segment_positions = [] # to be check on python 3.x
        self.canvas.delete(tkinter.ALL)

    def start(self):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        self.canvas.create_rectangle(10, 10, width-10, height-10)
        self.direction = random.choice('wasd')
        
        x = round(width // 2, -1)
        y = round(height // 2, -1)

        head_position = [x,y,x+self.SNAKE_SIZE,y+self.SNAKE_SIZE]
        self.head = self.canvas.create_oval(tuple(head_position), fill='green')
        self.head_position = head_position

        self.spawn_food()
        self.tick()

    def spawn_food(self):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        positions = [tuple(self.head_position), self.food_position] + self.segment_positions

        x = round(random.randint(20, width-20), -1)
        y = round(random.randint(20, height-20), -1)
        position = (x, y,x+self.SNAKE_SIZE,y+self.SNAKE_SIZE)
        while position in positions:
            x = round(random.randint(20, width-20), -1)
            y = round(random.randint(20, height-20), -1)
            position = (round(random.randint(20, width-20), -1), round(random.randint(20, height-20), -1))

        color = random.choice(FOOD_COLOR)
        self.food = self.canvas.create_rectangle(tuple(position),fill=color)
        self.food_position = position

    def tick(self):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        previous_head_position = tuple(self.head_position)

        if self.direction == 'w':
            self.head_position[1] -= self.MOVE
            self.head_position[3] -= self.MOVE
        elif self.direction == 'a':
            self.head_position[0] -= self.MOVE
            self.head_position[2] -= self.MOVE
        elif self.direction == 's':
            self.head_position[1] += self.MOVE
            self.head_position[3] += self.MOVE
        elif self.direction == 'd':
            self.head_position[0] += self.MOVE
            self.head_position[2] += self.MOVE

        head_position = tuple(self.head_position)
        if (self.head_position[0] < 10 or self.head_position[0] >= width-10 or
            self.head_position[1] < 10 or self.head_position[1] >= height-10 or
            any(segment_position == head_position for segment_position in self.segment_positions)):
            self.game_over()
            return

        if head_position == self.food_position:
            self.canvas.coords(self.food, previous_head_position)
            self.segments.append(self.food)
            self.segment_positions.append(previous_head_position)
            self.spawn_food()

        if self.segments:
            previous_position = previous_head_position
            for index, (segment, position) in enumerate(zip(self.segments, self.segment_positions)):
                self.canvas.coords(segment, previous_position)
                self.segment_positions[index] = previous_position
                previous_position = position

        self.canvas.coords(self.head, head_position)

        if self.running and self.moved:
            self.canvas.after(150, self.tick)

    def game_over(self):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        self.running = False
        self.start_button.configure(text='Start')
        score = len(self.segments) * 10
        self.canvas.create_text((round(width // 2, -1), round(height // 2, -1)), text='Game Over! Your score was: %d' % score)

    def on_up(self, event):
        if self.moved and not self.direction == 's':
            self.direction = 'w'

    def on_down(self, event):
        if self.moved and not self.direction == 'w':
            self.direction = 's'

    def on_left(self, event):
        if self.moved and not self.direction == 'd':
            self.direction = 'a'

    def on_right(self, event):
        if self.moved and not self.direction == 'a':
            self.direction = 'd'

    def on_pause(self, event):
        if self.moved:
            self.moved = False
        else:
            self.moved = True
            self.tick()



def main():
    root = tkinter.Tk()
    Application(root)
    root.mainloop()


if __name__ == '__main__':
    main()
