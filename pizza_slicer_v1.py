import numpy as np
import random

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
        #print str (self.area()), self.to_string()

    def x2(self):
        return self.x + self.h - 1

    def y2(self):
        return self.y + self.w - 1

    def area(self):
        return self.h * self.w

    def conflicts_with(self, other):
        other_x_overlaps_self = in_range(other.x, self.x, self.x2()) or in_range(other.x2(), self.x, self.x2())
        other_y_overlaps_self = in_range(other.y, self.y, self.y2()) or in_range(other.y2(), self.y, self.y2())

        self_x_overlaps_other = in_range(self.x, other.x, other.x2()) or in_range(self.x2(), other.x, other.x2())
        self_y_overlaps_other = in_range(self.y, other.y, other.y2()) or in_range(self.y2(), other.y, other.y2())

        # TODO: double check this
        if other_x_overlaps_self and other_y_overlaps_self:
            return True

        if self_x_overlaps_other and self_y_overlaps_other:
            return True

        return False

    def to_string(self):
        return " ".join ([str (self.x), str (self.y), str (self.x2()), str (self.y2()), '\n'])

def in_range (num, min, max):
    return num >= min and num <= max

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
        outputfile.write(slice.to_string())
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
    for i in range(pizza.rows - rows + 1):
        for j in range(pizza.cols - cols + 1):
            if check_valid(np.array(pizza.lines)[i:i+rows,j:j+cols], pizza.mini):
                #print np.array(pizza.lines)[i:i+rows, j:j+cols]
                slices.append(Slice(i, j, rows, cols))

def remove_conflicts(all_slices, selected_slice):
    new_slices = []
    for s in all_slices:
        if not selected_slice.conflicts_with (s):
            new_slices.append(s)
    return new_slices

def select_slices_random(all_slices):
    selected_slices = []

    while all_slices:
        print "remaining slices:" + str(len(all_slices))
        selected_pos = random.choice(range(0, len (all_slices)))
        selected_slice = all_slices[selected_pos]
        selected_slices.append(selected_slice)
        all_slices.pop(selected_pos)
        all_slices = remove_conflicts (all_slices, selected_slice)

    print "Random pick selected " + str(len(selected_slices)) + " slices with area " + \
          str(selected_area(selected_slices))

    return selected_slices

def main():
    # dont try with bigger ones
    pizza = pizza_parser('small.in')
    slices = []
    print pizza.rows, pizza.cols
    for rows in range(1, pizza.rows):
        for cols in range(1, pizza.cols):
            cells = rows * cols
            if cells <= pizza.maxc and cells >= 2 * pizza.mini:
                get_valid_slices(rows, cols, slices, pizza)
                print cells, len(slices)

    random_slices = select_slices_random (slices)

    slice_printer(random_slices)
    #slice_printer(slices)

main()