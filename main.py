import numpy as np

class Pizza:
    def __init__(self):
        self.lines = []
        self.rows = 0
        self.cols = 0
        self.mini = 0
        self.maxc = 0

    def isValidSlice(self, slice):
        if(slice.h == 0 or slice.w == 0):
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

    def __init__(self, X, Y, H, W):
        self.x = X
        self.y = Y
        self.h = H
        self.w = W

def pizza_parser(filename):
    pizza = Pizza()
    with open(filename) as f:
        pizza.rows, pizza.cols, pizza.mini, pizza.maxc = map(int, f.readline().split())
        pizza.lines = np.array([list(l.strip()) for l in f])
    return pizza

def slice_printer(slices):
    outputfile = open('result.out', 'w')
    outputfile.write(str(len(slices)) + '\n')
    for slice in slices:
        outputfile.write(" ".join ([str (slice.y), str (slice.x), str (slice.y +slice.h), str (slice.x + slice.w), '\n']))
    outputfile.close()

def check_valid(slice, min_required):
    m_count = 0
    t_count = 0
    for line in slice:
        for cell in line:
            if cell == 'M':
                m_count += 1
            elif cell == 'T':
                t_count += 1

            if m_count >= min_required and t_count >= min_required:
                return True
    return False

pizza = pizza_parser('small.in')

a = pizza.maxc / 2
for i in range(pizza.rows - a):
    for j in range(pizza.cols - a):
        is_valid = check_valid(pizza.lines[i:i+a][j:j+a], pizza.mini)
        print "{},{} {}".format(i, j, is_valid)

slices = []
#slices.append(Slice(0, 0, 2, 1))
#slices.append(Slice(3, 2, 1, 2))
slice_printer(slices)

#outputfile = open('small.out', 'w')
#outputfile.writelines(pizza)
#outputfile.close()