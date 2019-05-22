#  ***********
# Klasa populacji rakiet
# Modul zawiera funkcje tworzenia nowej generacji,
# oceniania i krzyzowania

from Application import *
from Rocket import *
from Vector import *

OBSTACLE_LOSE = 0.5 # loses 50% of fitness

class Population(object):

    def __init__(self):
        self.members = []   # list of rockets
        self.best = Rocket()  # member with the highest fitness in population
        self.avarge_fitness = 0
        self.finished = 0
        self.generation = 1
        self.new_gen()
        self.time = datetime.now()
        self.target_size = 40
        self.target = (WIDTH-80, int(HEIGHT/2 - 20))
        self.max_distance = hypot(self.target[0] + self.target_size // 2, self.target[1] + self.target_size // 2)
        self.found_way = []

    def new_gen(self):
        for i in range(POPULATION_SIZE):
            m = Rocket()
            for i in range(WIDTH // CELL_SIZE):
                for j in range(HEIGHT // CELL_SIZE):
                    x = uniform(-1, 1)
                    y = uniform(-1, 1)
                    while y == 0:
                        y = uniform(-1, 1)
                    m.DNA[i].append(x / y)
            self.members.append(m)

    def fitness_function(self):
        best = Rocket()
        for member in self.members:
            d = hypot(self.target[0] - member.p_location.x,
                      self.target[1] - member.p_location.y)
            time = 30
            if member.reached and not member.color == "red":
                time = member.time.seconds
                member.color = "red"
            max_way = hypot(self.target[0] - x_start, self.target[1] - y_start)
            travaled_way = hypot(x_start - member.p_location.x, y_start - member.p_location.y)
            way_points = travaled_way / max_way
            fit_value = (((30 - time) / 30 / 2) + ((self.max_distance - d)/ self.max_distance + way_points)) / 2
            #fit_value = fit_value ** 2
            member.fitness = fit_value
            if member.fitness > best.fitness:
                best = member
            self.avarge_fitness += member.fitness
        self.avarge_fitness /= POPULATION_SIZE
        self.best = best

    def crossover(self, parent1, parent2):
        p = (parent1, parent2)
        child = Rocket()
        b = 0
        if parent2.color == "red" or parent1.color == "red":
            child.color = "blue"
        if parent1.fitness < parent2.fitness:
            b = 1
        #child.DNA = list(p[b].DNA[:(WIDTH//CELL_SIZE//2)])
        #child.DNA += (p[1 - b].DNA[:(WIDTH//CELL_SIZE//2)]).copy()
        first = p[b].DNA[:int(WIDTH//CELL_SIZE//2)]
        second = p[b - 1].DNA[int(WIDTH//CELL_SIZE//2):]
        new = first + second
        child.DNA = new
        return child

    def selection(self):
        matin_pool = []
        for i in range(POPULATION_SIZE):
            member = self.members[i]
            times = int(member.fitness * 100)
            for i in range(times):
                matin_pool.append(member)
        possibilites = len(matin_pool)
        print("Matin pool len",possibilites)
        new_population = []
        for m in range(POPULATION_SIZE):
            a = randint(0, possibilites - 1)
            b = randint(0, possibilites - 1)
            parent1 = matin_pool[a]
            parent2 = matin_pool[b]
            child = self.crossover(parent1, parent2)
            child.mutate()
            new_population.append(child)
        self.members = new_population
        t = datetime.now()
        for new_m in self.members:
            new_m.time = t
        self.finished = 0
