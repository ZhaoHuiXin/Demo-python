from functools import singledispatch
class Shape:
    def __init__(self, solid):
        self.solid = solid

class Circle(Shape):
    def __init__(self, center, radius, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.center = center
        self.radius = radius

    # def draw(self):
    #     print("\u25CF" if self.solid else "\u25A1")


class Parallelogram(Shape):
    def __init__(self, pa, pb, pc, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pa = pa
        self.pb = pb
        self.pc = pc

    # def draw(self):
    #     print("\u2580" if self.solid else "\u2581")


class Triangle(Shape):
    def __init__(self, pa, pb, pc, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pa = pa
        self.pb = pb
        self.pc = pc

    # def draw(self):
    #     print("\u2582" if self.solid else "\u2583")

@singledispatch
def draw(shape):
    print("Type error!")

@draw.register(Circle)
def _(shape):
    print("\u25CF" if shape.solid else "\u25A1")

@draw.register(Parallelogram)
def _(shape):
    print("\u2580" if shape.solid else "\u2581")

@draw.register(Triangle)
def _(shape):
    print("\u2582" if shape.solid else "\u2583")

def main():
    circle = Circle(center=(0, 0), radius=5, solid=True)
    draw(circle)
    # draw(shape=circle) # TypeError: draw requires at least 1 positional argument

if __name__ == '__main__':
    main()