from abc import ABC, abstractmethod


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
    def __init__(self, radius):
        pass

class Triangle(Shape):
    def __init__(self, a, b, c):
        pass



if __name__ == '__main__':
    sq = Square(5)
    print(sq.area())
    print(sq.perimeter())