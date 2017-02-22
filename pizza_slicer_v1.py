import random

import numpy as np


class Pizza:
    def __init__(self):
        self.lines = []
        self.rows = 0
        self.cols = 0
        self.mini = 0
        self.maxc = 0


class Slice:
    def __init__(self, r1, c1, r2, c2):
        self.r1 = r1
        self.r2 = r2
        self.c1 = c1
        self.c2 = c2
        # print str (self.area()), self.to_string()

    def height(self):
        return self.r2 - self.r1 + 1

    def width(self):
        return self.c2 - self.c1 + 1

    def area(self):
        return self.height() * self.width()

    def x2(self):
        return self.x + self.h - 1

    def y2(self):
        return self.y + self.w - 1

    def conflicts_with(self, other):
        return not (self.r2 < other.r1 or self.r1 > other.r2 or self.c2 < other.c1 or self.c1 > other.c2)

    def to_string(self):
        return " ".join([str(self.r1), str(self.c1), str(self.r2), str(self.c2), '\n'])


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


def selected_area(slices):
    return sum([s.area() for s in slices])


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
            if check_valid(pizza.lines[i:i + rows, j:j + cols], pizza.mini):
                #print pizza.lines[i:i+rows, j:j+cols]
                slices.append(Slice(i, j, i + rows - 1, j + cols - 1))


def remove_conflicts(all_slices, selected_slice):
    #new_slices = []
    for s in all_slices:
        #if not selected_slice.conflicts_with(s):
        #    new_slices.append(s)
        if selected_slice.conflicts_with(s):
            all_slices.pop(s)
    return all_slices


def select_slices_random(all_slices):
    selected_slices = []

    while all_slices:
        print "remaining slices:" + str(len(all_slices))
        selected_pos = random.choice(range(0, len(all_slices)))
        selected_slice = all_slices[selected_pos]
        selected_slices.append(selected_slice)
        all_slices.pop(selected_pos)
        all_slices = remove_conflicts(all_slices, selected_slice)

    print "Random pick selected " + str(len(selected_slices)) + " slices with area " + \
          str(selected_area(selected_slices))

    return selected_slices

def select_slices_random_dict(slices):
    print "initializing slice map"
    slice_map = dict(zip(range(len(slices)), slices))

    print "initializing conflict map"
    conflict_map = dict.fromkeys(range(len(slices)))
    for key in conflict_map:
        conflict_map[key] = []

    #for key in conflict_map:
    #    print "conflict:", str (key), ":", str (conflict_map[key])

    print "building conflict map"
    for key1 in slice_map:
        slice1 = slice_map[key1]
        print "Adding conflicts for", str(key1)
        for key2 in range(key1, len(slice_map)):
            slice2 = slice_map[key2]
            if slice1.conflicts_with(slice2):
                conflict_map[key1].append(key2)
                conflict_map[key2].append(key1)

    print "Picking slices"
    selected_slices = []
    while slice_map:
        print "remaining slices:" + str(len(slice_map))
        selected_slice = random.choice(slice_map.keys())
        selected_slices.append(slice_map[selected_slice])

        slice_map.pop(selected_slice)
        for c in conflict_map[selected_slice]:
            if c in slice_map:
                slice_map.pop(c)

    print "Random pick selected " + str(len(selected_slices)) + " slices with area " + \
          str(selected_area(selected_slices))

    return selected_slices


def main():
    # dont try with bigger ones
    pizza = pizza_parser('medium.in')
    slices = []

    print pizza.rows, pizza.cols
    for rows in range(1, pizza.rows):
        for cols in range(1, pizza.cols):
            cells = rows * cols
            if cells <= pizza.maxc and cells >= 2 * pizza.mini:
                get_valid_slices(rows, cols, slices, pizza)
                print cells, len(slices)

    random_slices = select_slices_random_dict(slices)

    slice_printer(random_slices)

main()
