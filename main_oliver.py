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
        outputfile.write(" ".join ([str (slice.x), str (slice.y), ":" ,str (slice.x +slice.w - 1), str (slice.y + slice.h - 1), '\n']))
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

def get_valid_slices(rows, cols, slices, pizza):
    for i in range(pizza.rows - rows):
        for j in range(pizza.cols - cols):
            if check_valid(pizza.lines[i:i+rows][j:j+cols], pizza.mini):
                slices.append(Slice(i, j, rows, cols))


def getValidSliceFromLocation(x,y, pizza):
    for y_end in range(y+1,y+getMaxPossibleHeight(pizza.rows,pizza.maxc,y)):
        for x_end in range(x+getMaxPossibleWidth(pizza.cols, pizza.maxc, x)-1, 0, -1):
            if check_valid(pizza.lines[y:y_end + 1, x:x_end + 1], pizza.mini):
                return Slice(x, y, y_end - y+ 1,x_end - x + 1)
    return None

def getMaxPossibleWidth(cols, max_size, x):
    if cols - x < max_size:
        return cols - x
    else:
        return max_size


def getMaxPossibleHeight(rows, max_size, y):
    if rows - y < max_size:
        return rows - y
    else:
        return max_size

def conflicts_with_troubled(slice, troublemakers):
    for trouble in troublemakers:
        if slice.



def main():
    pizza = pizza_parser('small.in')
    slices = []
    troubleSlices = []

    x = 0
    y = 0

    while y < pizza.rows:
        x=0
        while x < pizza.cols:
            found = False
            for size in range(getMaxPossibleWidth(pizza.cols, pizza.maxc, x), 2*pizza.mini - 1, -1):
                if check_valid(pizza.lines[y:y+1,x:x+size], pizza.mini):
                    valid_slice = Slice(x, y, 1, size)
                    if not conflicts_with_troubled(valid_slice, troubleSlices):
                        slices.append(valid_slice)
                        x += size -1
                        found = True
                        break

            if not found:
                trouble_slice = getValidSliceFromLocation(x,y, pizza)
                if (trouble_slice != None):
                    troubleSlices.append(trouble_slice)
                    slices.append(trouble_slice)
                    x += trouble_slice.w
            x += 1
        y += 1





    slice_printer(slices)



main()
