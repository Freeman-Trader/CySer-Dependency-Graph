from data.test3 import B, C


class A:

    def __init__(self, starting_multiple):
        self.starting_multiple = starting_multiple

    def a1(self, p1, p2, p3):
        point = B(p1, p2, p3)

        def aa1(pt):
            x = pt.p1 + d(self.starting_multiple, 1)
            y = pt.p2 + d(self.starting_multiple, 2)
            z = pt.p3 + d(self.starting_multiple, 3)
            return p1, p2, p3

        new_point = aa1(point)
        return C(point, new_point)


import time

meaning_of_life = 42
print(f"The answer to the ultimate question of life, the universe, and everything is...")
time.sleep(3)
print(meaning_of_life, "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


def d(p1, p2):
    return p1 + p2
