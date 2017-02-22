import numpy as np
import time

class Pizza:
    def __init__(self):
        self.lines = []
        self.rows = 0
        self.cols = 0
        self.mini = 0
        self.maxc = 0

def pizza_parser(filename):
    pizza = Pizza()
    with open(filename) as f:
        pizza.rows, pizza.cols, pizza.mini, pizza.maxc = map(int, f.readline().split())
        pizza.lines = np.array([list(l.strip()) for l in f])
    return pizza

def slice_printer(slices, filename):
    with open(filename, 'w') as f:
        f.write(str(len(slices)) + '\n')
        for s in slices:
            r1 = s[0]
            c1 = s[1]
            r2 = r1 + s[2] - 1
            c2 = c1 + s[3] - 1
            f.write("{} {} {} {}\n".format(r1, c1, r2, c2))

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

def has_overlap(r, c, rows, cols):
    return np.any(output[r:r+rows, c:c+cols])

def get_valid_slices(rows, cols, pizza):
    for i in range(pizza.rows - rows + 1):
        for j in range(pizza.cols - cols + 1):
            if check_valid(pizza.lines[i:i+rows,j:j+cols], pizza.mini) and not has_overlap(i, j, rows, cols):
                slices.append((i, j, rows, cols))
                output[i:i+rows, j:j+cols] = 1

pizza = pizza_parser('example.in')
lines = pizza.lines
slices = []
output = np.zeros((pizza.rows, pizza.cols), dtype=np.int8)

t0 = time.time()

for rows in reversed(range(1, min(pizza.rows, pizza.maxc + 1))):
    print str(rows)
    for cols in reversed(range(1, min(pizza.cols, pizza.maxc + 1))):
        cells = rows * cols
        if cells <= pizza.maxc and cells >= 2 * pizza.mini:
            get_valid_slices(rows, cols, pizza)

print "{} out of {}".format(np.sum(output), pizza.rows * pizza.cols)
print "total time {}".format(time.time() - t0)

slice_printer(slices, 'example.out')