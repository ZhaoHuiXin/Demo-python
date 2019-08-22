class Shape:
    def __init__(self, solid):
        self.solid = solid


class Circle(Shape):
    def __init__(self, center, radius, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.center = center
        self.radius = radius

    def intersects(self, shape):
        # delegate to the generic function, ! swapping ! arguments
        return intersects_with_circle(shape, self)


from functools import singledispatch

@singledispatch
def intersects_with_circle(shape, circle):
    raise TypeError("Don't know how to compute intersection of (!r) with (!r)")