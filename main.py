import numpy as np

class Pizza:
    def __init__(self):
        self.lines = []
        self.rows = 0
        self.cols = 0
        self.mini = 0
        self.maxc = 0

class Slice:
    def __init__(self, X, Y, H, W):
        self.x = X
        self.y = Y
        self.h = H
        self.w = W

    def area(self):
        return self.h * self.w

def pizza_parser(filename):
    pizza = Pizza()
    with open(filename) as f:
        pizza.rows, pizza.cols, pizza.mini, pizza.maxc = map(int, f.readline().split())
        pizza.lines = np.array([list(l.strip()) for l in f])
    return pizza

def slice_printer(slices):
    print 'selected area ' + str(selected_area(slices))
    outputfile = open('result.out', 'w')
    outputfile.write(str(len(slices)) + '\n')
    for slice in slices:
        outputfile.write(" ".join ([str (slice.y), str (slice.x), str (slice.y +slice.h), str (slice.x + slice.w), '\n']))
    outputfile.close()

def selected_area (slices):
    return sum ([s.area() for s in slices])

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

def get_valid_slices(rows, cols, slices, pizza):
    for i in range(pizza.rows - rows):
        for j in range(pizza.cols - cols):
            if check_valid(pizza.lines[i:i+rows][j:j+cols], pizza.mini):
                slices.append(Slice(i, j, rows, cols))

def main():
    pizza = pizza_parser('medium.in')
    slices = []
    for rows in range(1, pizza.rows):
        for cols in range(1, pizza.cols):
            cells = rows * cols
            if cells <= pizza.maxc:
                get_valid_slices(rows, cols, slices, pizza)
    slice_printer(slices)

main()