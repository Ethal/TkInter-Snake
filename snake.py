#!/usr/bin/python
# -*- encoding: utf-8 -*-

import random

try:
    import tkinter
except ImportError:
    import Tkinter as tkinter

import os.path

FOOD_COLOR = ('yellow', 'yellow')


class Application:
    """ Application. """
    TITLE = 'Snake'
    SIZE = 400, 400
    BORDER = 10
    MOVE = 10
    SNAKE_SIZE = 7

    # initialize parameters of this class && parameters of Tk() class
    def __init__(self, master):
        """ Init. """
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
        # scores
        self.scores = tkinter.StringVar()
        self.highscore = 0

        self.running = False
        # below : initialize the specific parameter of Tk() class
        self.init()

    def init(self):
        """ Init the game."""
        self.master.title(self.TITLE)

        self.canvas = tkinter.Canvas(self.master)
        self.canvas.grid(sticky=tkinter.NSEW)

        self.start_button = tkinter.Button(self.master, text='Start', command=self.on_start)
        self.start_button.grid(row=1, sticky=tkinter.EW)

        # scores
        self.high_scores()
        self.scores.set(('Score: %d High Score: %d' % (len(self.segments)*10, self.highscore)))
        self.score_label = tkinter.Label(self.master, textvariable=self.scores)
        self.score_label.grid(row=2, sticky=tkinter.EW)

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
        """ Start Button Pressed."""
        self.reset()
        if self.running:
            self.running = False
            self.start_button.configure(text='Start')
        else:
            self.running = True
            self.start_button.configure(text='Stop')
            self.start()

    def reset(self):
        """ reset the game """
        self.segments = []
        self.segment_positions = []
        self.canvas.delete(tkinter.ALL)

    def start(self):
        """ Start game. """
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        self.canvas.create_rectangle(self.BORDER, self.BORDER, width-self.BORDER, height-self.BORDER)
        self.direction = random.choice('wasd')

        # scores
        self.high_scores()
        self.scores.set(('Score: %d High Score: %d' % (len(self.segments)*10, self.highscore)))

        pos_x = round(width // 2, -1)
        pos_y = round(height // 2, -1)

        head_position = [pos_x, pos_y, pos_x+self.SNAKE_SIZE, pos_y+self.SNAKE_SIZE]
        self.head = self.canvas.create_oval(tuple(head_position), fill='green')
        self.head_position = head_position

        self.spawn_food()
        self.tick()

    def spawn_food(self):
        """Draw the food."""
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        positions = [tuple(self.head_position), self.food_position] + self.segment_positions

        pos_x = round(random.randint(20, width-20), -1)
        pos_y = round(random.randint(20, height-20), -1)
        position = (pos_x, pos_y, pos_x+self.SNAKE_SIZE, pos_y+self.SNAKE_SIZE)
        while position in positions:
            pos_x = round(random.randint(20, width-20), -1)
            pos_y = round(random.randint(20, height-20), -1)
            position = (round(random.randint(20, width-20), -1), round(random.randint(20, height-20), -1))

        color = random.choice(FOOD_COLOR)
        self.food = self.canvas.create_rectangle(tuple(position), fill=color)
        self.food_position = position

    def tick(self):
        """Draw the snake."""
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
        if (self.head_position[0] < self.BORDER or self.head_position[0] >= width-self.BORDER or
            self.head_position[1] < self.BORDER or self.head_position[1] >= height-self.BORDER or
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
            # scores
            if (len(self.segments)*10) > self.highscore:
                self.highscore = len(self.segments)*10

            self.scores.set(('Score: %d High Score: %d'% (len(self.segments)*10, self.highscore)))
            self.canvas.after(150, self.tick)

    def game_over(self):
        """ Game over."""
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        # scores
        self.high_scores()

        self.running = False
        self.start_button.configure(text='Start')
        score = len(self.segments) * 10
        if score >= self.highscore:
            self.canvas.create_text((round(width // 2, -1), round(height // 2, -1)), text='Game Over! Great, You have the High score : %d' % score)
        else:
            self.canvas.create_text((round(width // 2, -1), round(height // 2, -1)), text='Game Over! Your score is: %d' % score)

    def high_scores(self):
        """ Get and Save the High score to the file score.txt"""
        filename = 'score.txt'
        if os.path.isfile(filename):
            ofile = open(filename, 'r')
            score = ofile.read()
            if len(score) != 0:
                self.highscore = int(score)
            ofile.close()

        if (len(self.segments)*10) >= self.highscore:
            wfile = open(filename, 'w')
            score = ('%d' % (len(self.segments)*10))
            wfile.write(score)
            wfile.close()

    def on_up(self, event):
        """ Arrow key up pressed."""
        if self.moved and not self.direction == 's':
            self.direction = 'w'

    def on_down(self, event):
        """ Arrow key down pressed."""
        if self.moved and not self.direction == 'w':
            self.direction = 's'

    def on_left(self, event):
        """ Arrow key left pressed."""
        if self.moved and not self.direction == 'd':
            self.direction = 'a'

    def on_right(self, event):
        """ Arrow key right pressed."""
        if self.moved and not self.direction == 'a':
            self.direction = 'd'

    def on_pause(self, event):
        """ P (Pause) key pressed."""
        if self.moved:
            self.moved = False
        else:
            self.moved = True
            self.tick()



def main():
    """ start application."""
    root = tkinter.Tk()
    Application(root)
    root.mainloop()


if __name__ == '__main__':
    main()
