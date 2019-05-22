# implementacja algorytmu A*
# plik glowny(main)
i = 0

from tkinter import *
from bisect import *
from random import *

rows        = 50
columns     = 60
size        = 15
PROBABILITY = 0.2
PROB2       = 0.3

# biale to nie ruszone
# zielone w liscie do sprawdzenia
# czerwone w liscie sprawdzonych
# niebieskie wybrane na aktualna najlepsza droge

colors_n_nums = {-1: "black", 0: "white", 1: "red", 2: "green", 3: "blue"}


class Node(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = colors_n_nums[0]
        self.f_score = 0
        self.g_score = 1000
        self.neighbours = []    # lista edge'y
        self.came_from = None

    def __lt__(self, other):
        return self.f_score > other.f_score

class Window(Tk):

    def __init__(self, start, end):
        super().__init__()
        self.title("A* Path winding")
        self.minsize(width=columns*size, height=rows*size)
        self.maxsize(width=columns*size, height=rows*size)
        self.canvas = Canvas(self, width=columns*size, height=rows*size)
        self.canvas.pack()
        self.pool = []
        self.tup_start = start
        self.tup_end = end
        # zmienne potrzebne do dzialania algorytmu A*
        self.koniec = False
        self.x1 = self.tup_start[0]
        self.y1 = self.tup_start[1]
        self.x2 = self.tup_end[0]
        self.y2 = self.tup_end[1]
        self.path = []
        self.akt = 1

        # tworzenie wierzcholkow
        for k in range(columns):
            j = 0
            self.pool.append([Node(k, j)])
            j += 1
            while j < rows:
                self.pool[k].append(Node(k, j))
                j += 1


        # tworzenie krawedzi
        for k in range(columns):
            for j in range(rows):
                c = self.pool[k][j]
                if k > 0:
                    c.neighbours.append(self.pool[k-1][j])
                    if j < rows - 1:
                        c.neighbours.append(self.pool[k - 1][j + 1])
                    if j > 0:
                        c.neighbours.append(self.pool[k - 1][j - 1])
                if j > 0:
                    c.neighbours.append(self.pool[k][j-1])
                if k < columns-1:
                    c.neighbours.append(self.pool[k+1][j])
                    if j < rows - 1:
                        c.neighbours.append(self.pool[k + 1][j + 1])
                    if j > 0:
                        c.neighbours.append(self.pool[k + 1][j - 1])
                if j < rows-1:
                    c.neighbours.append(self.pool[k][j+1])

        self.do_sprawdzenia = [self.pool[self.x1][self.y1]]
        # bisect.insort(a, 3)
        #lista.sort(key=lambda x: x[1])
        #def __cmp__(self, other):
        #return self.f_score - other.f_score

    def path_refactor(self, node):
        for i in self.path:
            self.canvas.delete(i)
        self.path = []
        while node.came_from != None:
            akt = node.came_from
            id = self.canvas.create_rectangle(akt.x * size, akt.y * size, (akt.x + 1) * size, (akt.y + 1) * size,
                                              fill=colors_n_nums[3], outline="")
            node = akt
            self.path.append(id)

    @staticmethod
    def dist(one, two):
        return ((two.x - one.x)**2 + (two.y - one.y)**2) ** 0.5

    @staticmethod
    def heuristic(one,two):
        return Window.dist(one, two)

    def walls(self):
        for i in range(columns):
            for j in range(rows):
                if uniform(0,1) <= (PROBABILITY):
                    self.pool[i][j].color = colors_n_nums[-1]
        self.pool[0][0].color = colors_n_nums[0]
        self.pool[columns-1][rows-1].color = colors_n_nums[0]

    def walls2(self):
        r = int(PROB2 * rows * columns)
        for i in range(r):
            x = randint(0,columns-1)
            y = randint(0,rows-1)
            self.pool[x][y].color = colors_n_nums[-1]
        self.pool[0][0].color = colors_n_nums[0]
        self.pool[columns-1][rows-1].color = colors_n_nums[0]


    def background(self):
        for i in range(columns):
            for j in range(rows):
                self.canvas.create_rectangle(i * size, j * size, (i + 1) * size, (j + 1) * size,
                                                 fill=self.pool[i][j].color, outline="")

    def draw_canv(self):
        if not self.koniec:
            if (len(self.do_sprawdzenia)) != 0:
                akt = self.do_sprawdzenia.pop()
                self.akt = akt
                #self.path_refactor(self.akt)
                if akt.x == self.x2 and akt.y == self.y2:
                    akt.color = colors_n_nums[2]
                    self.koniec = True  # znalazlem droge
                akt.color = colors_n_nums[2]
                self.canvas.create_rectangle(akt.x * size, akt.y * size, (akt.x + 1) * size, (akt.y + 1) * size,
                                             fill=akt.color, outline="")
                #for i in self.do_sprawdzenia:
                #    print(i.f_score,end=' ')
                #print('\n')
                for neig in akt.neighbours:
                    if neig.color != colors_n_nums[2] and neig.color != colors_n_nums[-1]:
                        temporary_g = akt.g_score + Window.dist(akt, neig)
                        new_way = False
                        if neig.color != colors_n_nums[1]:  # jeszcze tu nie bylem
                            neig.color = colors_n_nums[1]
                            self.canvas.create_rectangle(neig.x * size, neig.y * size, (neig.x + 1) * size, (neig.y + 1) * size,
                                                         fill=neig.color, outline="")
                            neig.g_score = temporary_g
                            neig.f_score = neig.g_score + Window.heuristic(neig, self.pool[self.x2][self.y2])
                            insort(self.do_sprawdzenia, neig)
                            new_way = True
                        elif neig.g_score > temporary_g:
                            neig.g_score = temporary_g
                            neig.f_score = neig.g_score + Window.heuristic(neig, self.pool[self.x2][self.y2])
                            new_way = True
                        if new_way:
                            neig.came_from = akt
            else:
                self.koniec = True

            self.after(2, self.draw_canv)
        else:
            self.path_refactor(self.akt)
        #for i in range(columns):
        #    for j in range(rows):
        #        self.canvas.create_rectangle(i*size, j*size, (i+1)*size, (j+1)*size, fill=self.pool[i][j].color, outline="")


w = Window((0, 0), (columns-1, rows-1))
w.walls2()
w.walls()
w.background()
w.draw_canv()
w.mainloop()
