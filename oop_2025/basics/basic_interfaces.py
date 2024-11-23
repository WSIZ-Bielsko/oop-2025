import math
from abc import ABC, abstractmethod
from select import select


# To jest "interfejs"
class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass

    @abstractmethod
    def perimeter(self) -> float:
        pass


# Implement the interface
class Square(Shape):

    def __init__(self, side_length):
        self.side_length = side_length

    def area(self) -> float:
        return self.side_length ** 2

    def perimeter(self) -> float:
        return 4 * self.side_length


class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        return self.radius ** 2

    def perimeter(self) -> float:
        return 2 * self.radius * math.pi


class Triangle(Shape):
    def __init__(self, a, b, c):
        pass

    def area(self) -> float:
        # todo
        pass

    def perimeter(self) -> float:
        # todo
        pass


class Trapezoid(Shape):
    def __init__(self, a: float, b: float, h: float):
        self.h = h
        self.b = b
        self.a = a

    def area(self) -> float:
        return self.h * (self.a + self.b) / 2

    def perimeter(self) -> float:
        c = math.sqrt(self.h ** 2 + ((self.a - self.b) / 2) ** 2)

        # Calculate perimeter
        perimeter = self.a + self.b + 2 * c
        return perimeter


class IBoxBounded(ABC):
    @abstractmethod
    def get_bounding_box(self) -> float:
        pass


class BoundedCircle(IBoxBounded, Circle):

    def get_bounding_box(self) -> float:
        return 0

    def area(self) -> float:
        return self.radius ** 2 * math.pi


# Delegacja

class DelegatingBoundedCircle(IBoxBounded, Circle):

    def __init__(self, radius: float):
        self.circle = Circle(radius)

    def area(self) -> float:
        return self.circle.area()

    def perimeter(self) -> float:
        return self.circle.perimeter()

    def get_bounding_box(self) -> float:
        return 0

if __name__ == '__main__':
    sq = Square(5)
    # print(sq.area())
    # print(sq.perimeter())

    # t = Trapezoid(10, 10, 10)
    # print(t.a)

    c = BoundedCircle(radius=1)
    print(c.get_bounding_box())
    print(c.area())
