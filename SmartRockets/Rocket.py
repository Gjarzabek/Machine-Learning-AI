# *****************************
# Modul zawierajacy definicje klasy Rakiety

from Application import *
from Vector import *

def index_to_coordinates(i, j):
    return (i * CELL_SIZE, j * CELL_SIZE)

def coordinates_to_index(x, y):
    return (int(x / CELL_SIZE), int(y / CELL_SIZE))

x_start = sum_x / 5 + 15
y_start = sum_y / 5 + 38

class Rocket(object):

    MAX_VEL = 8
    MAX_FORCE = 2
    MUTATION_RATE = 0.02

    def __init__(self):
        self.DNA = [[] for i in range(int(WIDTH/CELL_SIZE))]
        self.fitness = 0
        #self.target = Vector(0, 0)
        self.steering = Vector(0, 0)
        self.desire_velocity = Vector(0 , 0)
        self.p_location = Vector(sum_x / 5 + 15, sum_y / 5 + HEIGHT//2)
        self.p_layout = PROPORTION
        self.velocity = Vector(0, 0)
        self.max_force = Rocket.MAX_FORCE
        self.acceleration = Vector(0, 0)
        self.forces = Vector(0, 0)
        self.id = 0
        self.hit_obstacle = False
        self.reached = False
        self.hit_wall = False
        self.time = datetime.now()
        self.color = "black"

    def mutate(self):
        mutation = Rocket.MUTATION_RATE
        for i in range(WIDTH // CELL_SIZE):
            for j in range(4, HEIGHT // CELL_SIZE):
                if mutation >= uniform(0, 1):
                    x = uniform(-1, 1)
                    y = uniform(-1, 1)
                    while x == 0:
                        x = uniform(-1, 1)
                    self.DNA[i][j] = (y / x)

    def acc_force_reset(self):
        self.acceleration.x = 0
        self.acceleration.y = 0
        self.forces.x = 0
        self.forces.y = 0

    def apply_force(self, v: Vector):
        if not self.hit_obstacle:
            self.forces += v

    def obstacle_collision(self, cells):
        in_tab = (int(self.p_location.x), int(self.p_location.y))
        if self.p_location.x > WIDTH or self.p_location.y < 0 or self.p_location.x < 0 or self.p_location.y > HEIGHT:
            self.velocity = Vector(0, 0)
            self.hit_obstacle = True
        elif cells[in_tab[0]][in_tab[1]] == 2:
            self.velocity = Vector(0, 0)
            self.hit_obstacle = True
            self.hit_wall = True
        elif cells[in_tab[0]][in_tab[1]] == 1:
            self.velocity = Vector(0, 0)
            self.hit_obstacle = True
            self.reached = True
            self.time = datetime.now() - self.time

    def set_desire(self):
        cell = coordinates_to_index(self.p_location.x, self.p_location.y)
        a = self.DNA[ cell[0] ][ cell[1] ]      # wspolcznynnik kierunku aktualnej porzadanej predkosci
        if a < 0:
            alfa = atan(a) + pi
        else:
            alfa = atan(a)
        if self.velocity.x != 0:
            b = self.velocity.y / self.velocity.x
        else:
            b = self.velocity.y * 10000000
        if b < 0:
            beta = atan(b) + pi
        else:
            beta = atan(b)
        gamma = fabs(alfa - beta)
        if alfa < beta:
            gamma = pi - gamma
        right = True
        if gamma == pi/2:
            if uniform(0,1) > 0.5:
                right = False
        elif gamma > pi/2:
            right = False
            gamma = pi - gamma
        self.desire_velocity = self.turn(right, a, b)
        self.desire_velocity = self.desire_velocity.norm()
        self.desire_velocity *= Rocket.MAX_VEL

    # funkcja decyduje czy w aktualnej klatce rakieta ma skrecic w lewo czy w prawo
    # zwraca wektor predkosci
    # right - zwrot skretu, a - mozliwy kierunek skretu, b - aktualny kierunek
    def turn(self, right, a, b):
        if a > 0:
            if b > 0:
                if self.velocity.y > 0:
                     return Vector(1, a)
                else:
                    return Vector(-1, -a)
            else:
                if self.velocity.y > 0:
                    if right:
                        return Vector(-1, -a)
                    else:
                        return Vector(1, a)
                else:
                    if right:
                        return Vector(1, a)
                    else:
                        return Vector(-1, -a)
        else:
            if b < 0:
                if self.velocity.y > 0:
                    return Vector(-1, -a)
                else:
                    return Vector(1, a)
            else:
                if self.velocity.y > 0:
                    if right:
                        return Vector(-1, -a)
                    else:
                        return Vector(1, a)
                else:
                    if right:
                        return Vector(1, a)
                    else:
                        return Vector(-1, -a)


    def set_steering(self):
        self.steering = self.desire_velocity - self.velocity
        if self.steering.len() > self.max_force:
            self.steering = self.steering.norm() * self.max_force

    def update(self, canvas, population, cells):
        self.apply_force(self.steering)
        self.acceleration += self.forces
        self.velocity += self.acceleration
        if self.velocity.len() > Rocket.MAX_VEL:
            self.velocity = self.velocity.norm() * Rocket.MAX_VEL
        self.rotate()
        self.obstacle_collision(cells)
        if not self.hit_obstacle:
            self.set_desire()
            self.set_steering()
        else:
            population.finished += 1
        self.p_location += self.velocity
        for x in range(0, 10, 2):
            self.p_layout[x] += self.p_location.x
            self.p_layout[x+1] += self.p_location.y
        self.acc_force_reset()

    def side(self, current, change):
        if current.x != 0:
            a = current.y / current.x
        else:
            a = current.y * 1000000
        if a > 0:
            if current.x > 0:
                if change.y <  a * change.x:
                    return True
            else:
                if change.y > a * change.x:
                    return True
        else:
            if current.x < 0:
                if change.y > a * change.x:
                    return True
            else:
                if change.y < a * change.x:
                    return True

    def rotate(self):
        sumx = 0
        sumy = 0
        for i in range(0, 10, 2):
            sumx += self.p_layout[i]
            sumy += self.p_layout[i + 1]
        center = (sumx / 5, sumy / 5)
        f_cent = Vector(self.p_layout[0] - center[0], self.p_layout[1] - center[1])
        front = f_cent.set()
        v = self.velocity.set()
        left = self.side(front, v)
        if v.len() != 0 and front.len() != 0:
            cos_alfa = (v.x * front.x + v.y * front.y) / (v.len() * front.len())
            if cos_alfa > 1:
                cos_alfa = 1
            if cos_alfa < -1:
                cos_alfa = -1
        else:
            cos_alfa = 1
        alfa = acos(cos_alfa)
        if left:
            alfa = -alfa
        for i in range(0, 10, 2):
            f_cent = Vector(self.p_layout[i] - center[0], self.p_layout[i + 1] - center[1])
            v = Vector(f_cent.x * cos(alfa) - f_cent.y * sin(alfa), f_cent.x * sin(alfa) + f_cent.y * cos(alfa) )
            self.p_layout[i] = v.x
            self.p_layout[i + 1] = v.y
