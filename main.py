import numpy as np

class Pizza:
    def __init__(self):
        self.lines = []
        self.rows = 0
        self.cols = 0
        self.mini = 0
        self.maxc = 0

    def isValidSlice(self, slice):
        if(slice.h == 0 or slice.w == 0)
            return False
        if(slice.h * slice.w > self.maxc):
            return False
        #if() check if all tomatoes potatoes

        return True


class Slice:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.h = 0
        self.w = 0

def pizza_parser(filename):
    pizza = Pizza()
    with open(filename) as f:
        pizza.rows, pizza.cols, pizza.mini, pizza.maxc = map(int, f.readline().split())
        pizza.lines = np.array([list(l.strip()) for l in f])
    return pizza

pizza = pizza_parser('small.in')


#outputfile = open('small.out', 'w')
#outputfile.writelines(pizza)
#outputfile.close()