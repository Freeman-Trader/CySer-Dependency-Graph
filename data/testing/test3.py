import numpy.random as banana
from binascii import hexlify as hexy

X = 10
ba = banana.rand(X)
print(ba)


class B:
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def b1(self):
        print(f"({self.p1}, {self.p2}, {self.p3}")


Y = 10 * 10


class C:
    constant_var = 'EXTRA STUFF'
    
    def __init__(self, point, new_point):
        self.point = point
        self.new_point = new_point
        print("Recorded points = ", point, new_point)
        
    def c1(self):
        return "This is c1" + self.constant_var

    def c2(self, s):
        return hexy(self.c1().encode()).decode()


Y = Y // 2
ba = banana.rand(Y)
print("Some random thing: ", ba)
