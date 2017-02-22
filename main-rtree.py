import numpy as np
import rtree

class Pizza:
    def __init__(self):
        self.lines = []
        self.rows = 0
        self.cols = 0
        self.mini = 0
        self.maxc = 0

class Slice:
    def __init__(self, R, C, H, W):
        self.r = R
        self.c = C
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
        outputfile.write(" ".join ([str (slice.r), str (slice.c), str (slice.r +slice.h), str (slice.c + slice.w), '\n']))
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

def get_valid_slices(rows, cols, pizza):
    for i in range(pizza.rows - rows):
        for j in range(pizza.cols - cols):
            if check_valid(pizza.lines[i:i+rows,j:j+cols], pizza.mini):
                left = j
                bottom = i
                right = j + cols - 0.000001
                top = i + rows - 0.00001
                intersections = idx.intersection((left, bottom, right, top))
                found = False
                for _ in intersections:
                    found = True
                    break

                if not found:
                    output[i:i+rows,j:j+cols] = len(slices)
                    idx.insert(len(slices), (left, bottom, right, top))
                    slices.append(Slice(i, j, rows, cols))
                    break

pizza = pizza_parser('small.in')
lines = pizza.lines
idx = rtree.index.Index()
slices = []
output = np.copy(pizza.lines)

for rows in range(1, pizza.rows):
    for cols in range(1, pizza.cols):
        cells = rows * cols
        if cells <= pizza.maxc:
            get_valid_slices(rows, cols, pizza)

slice_printer(slices)
