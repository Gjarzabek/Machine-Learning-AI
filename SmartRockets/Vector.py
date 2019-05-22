#   Definicja klasy Vector


class Vector(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __truediv__(self, other):
        if other != 0:
            return Vector(self.x / other, self.y / other)
        else:
            return self

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def set(self):
        return Vector(self.x, self.y)

    def len(self):
        return (self.x**2 + self.y**2) ** (0.5)

    def norm(self):
        if self.len() != 0:
            return Vector(self.x / self.len(), self.y / self.len())
        else:
            return self
