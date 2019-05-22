# Program generujacy populacje rakiet ktore docieraja do wyznaczonego celu
#
# Program korzysta z algorytmu genetycznego
# **** Grzegorz Jarzabek ****
# *** 13.12.2018 ***

WIDTH = 1100
HEIGHT = 700
CELL_SIZE = 10

POPULATION_SIZE = 360

PROPORTION = [8, 0, 18, 25, 9, 20, 0, 25, 8, 0]
sum_x = 0
sum_y = 0
for i in range(0, 10, 2):
    sum_x += PROPORTION[i]
    sum_y += PROPORTION[i+1]


from tkinter import *
from random import randint, uniform
from math import atan, acos, tan, cos, sin, degrees, pi, fabs, hypot
from datetime import *
from Population import *


class App(Tk):

    def __init__(self):
        super().__init__()
        self.minsize(width=WIDTH, height=HEIGHT)
        self.maxsize(width=WIDTH, height=HEIGHT)
        self.title("Smart Rockets")
        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT, bg="white")
        self.cells = [[0 for j in range(HEIGHT)] for i in range(WIDTH)]
        self.canvas.pack()
        self.rockets = Population()
        self.create_target()
        self.gen_info = self.canvas.create_text((WIDTH / 2 - 15, 15), text=f"Generation: {self.rockets.generation}",
                                                font=("Arial", 20), fill="black")
        self.parameters_info = []
        self.draw_info()
        #self.create_obstacle()
       # self.create_obstacle2()


    def create_target(self):
        self.canvas.create_rectangle(self.rockets.target[0], self.rockets.target[1],
                                     self.rockets.target[0] + self.rockets.target_size,
                                     self.rockets.target[1] + self.rockets.target_size,
                                     fill="#504D4D", outline="")
        for i in range(self.rockets.target_size):
            for j in range(self.rockets.target_size):
                self.cells[self.rockets.target[0] + i][self.rockets.target[1] + j] = 1

    def create_obstacle(self):
        x1 = int(WIDTH/2)
        x2 = x1 + 10
        y1 = int(HEIGHT/5 * 2)
        y2 = y1*2
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="#504D4D", outline="")
        for i in range(x2-x1+1):
            for j in range(y2-y1+1):
                self.cells[x1 + i][y1 + j] = 2

    def create_obstacle2(self):
        x1 = int(WIDTH/7*5)
        x2 = x1 + 10
        y1 = int(HEIGHT/5)
        y2 = y1*2
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="#504D4D", outline="")
        for i in range(x2-x1+1):
            for j in range(y2-y1+1):
                self.cells[x1 + i][y1 + j] = 2


    def draw_info(self):
        for i in self.parameters_info:
            self.canvas.delete(i)
        self.parameters_info = []
        id1 = self.canvas.create_text((WIDTH-110, 20), text=f"Mutation rate: {Rocket.MUTATION_RATE*100}%",
                                                    font=("Arial", 10), fill="black")
        id2 = self.canvas.create_text((WIDTH-110, 35), text=f"Best fitness: {self.rockets.best.fitness}",
                                                    font=("Arial", 10), fill="black")
        id3 = self.canvas.create_text((WIDTH - 110, 50), text=f"Avarge fitness: {self.rockets.avarge_fitness}",
                                font=("Arial", 10), fill="black")
        id4 = self.canvas.create_text((WIDTH - 110, 65), text=f"Population: {POPULATION_SIZE}",
                                      font=("Arial", 10), fill="black")
        self.parameters_info.append(id1)
        self.parameters_info.append(id2)
        self.parameters_info.append(id3)
        self.parameters_info.append(id4)


    def proceed(self):
        for r in self.rockets.members:
            if not r.hit_obstacle:
                self.canvas.delete(r.id)
                r.update(self.canvas, self.rockets, self.cells)
                r.id = self.canvas.create_polygon(r.p_layout, fill=r.color, outline="")

        duration = datetime.now() - self.rockets.time
        duration = duration.seconds
        if self.rockets.finished < POPULATION_SIZE and duration < 30:
            self.after(15, self.proceed)
        else:
            for r in self.rockets.members:
                self.canvas.delete(r.id)
            self.rockets.fitness_function()
            self.rockets.selection()
            self.rockets.generation += 1
            self.canvas.delete(self.gen_info)
            self.rockets.time = datetime.now()
            self.draw_info()
            self.gen_info = self.canvas.create_text((WIDTH / 2 - 15, 15), text=f"Generation: {self.rockets.generation}",
                                                    font=("Arial", 20), fill="black")
            self.after(15, self.proceed)


if __name__ == '__main__':
    a = App()
    a.proceed()
    a.mainloop()