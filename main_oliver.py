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

    def x2(self):
        return self.x + self.w - 1

    def y2(self):
        return self.y + self.h - 1

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
        return " ".join ([str (self.y), str (self.x), str (self.y2()), str (self.x2()), '\n'])

def in_range (num, min, max):
    return num >= min and num <= max

def pizza_parser(filename):
    pizza = Pizza()
    with open(filename) as f:
        pizza.rows, pizza.cols, pizza.mini, pizza.maxc = map(int, f.readline().split())
        pizza.lines = np.array([list(l.strip()) for l in f])
    return pizza

#def slice_printer(slices):
    #outputfile = open('result.out', 'w')
    #outputfile.write(str(len(slices)) + '\n')
   # for slice in slices:
      #  outputfile.write(slice.to_string())
    #outputfile.close()

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


def getValidNonConflictingSliceFromLocation(x,y, pizza, troubleSlices):
    for y_end in range(y+1,y+getMaxPossibleHeight(pizza.rows,pizza.maxc,y)):
        for x_end in range(x+getMaxPossibleWidth(pizza.cols, pizza.maxc, x)-1, 0, -1): #dont need to do checking on next line if we set range properly here
            if ((y_end - y + 1)*(x_end - x + 1)) <= pizza.maxc and check_valid(pizza.lines[y:y_end + 1, x:x_end + 1], pizza.mini)\
                    and not conflicts_with_troubled(Slice(x, y, y_end - y+ 1,x_end - x + 1), troubleSlices):
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
        if slice.conflicts_with(trouble):
            return True
    return False


def rehabilitate_troublemakers(troubleSlices, y):
    new_troubleSlices = []
    for slice in troubleSlices:
        if (slice.y + slice.h) > y:
            new_troubleSlices.append(slice)

    return new_troubleSlices


def main():
    pizza = pizza_parser('medium.in')
    slices = []
    troubleSlices = []
    area = 0

    x = 0
    y = 0

    while y < pizza.rows:
        troubleSlices = rehabilitate_troublemakers(troubleSlices,y)
        x=0
        print(y)
        while x < pizza.cols:
            found = False
            for size in range(getMaxPossibleWidth(pizza.cols, pizza.maxc, x), 2*pizza.mini - 1, -1):
                if check_valid(pizza.lines[y:y+1,x:x+size], pizza.mini):
                    valid_slice = Slice(x, y, 1, size)
                    if not conflicts_with_troubled(valid_slice, troubleSlices):
                        slices.append(valid_slice)
                        area += valid_slice.area()
                        x += size -1
                        found = True
                        break

            if not found:
                trouble_slice = getValidNonConflictingSliceFromLocation(x,y, pizza, troubleSlices)
                if (trouble_slice != None):
                    troubleSlices.append(trouble_slice)
                    slices.append(trouble_slice)
                    area += trouble_slice.area()
                    x += trouble_slice.w -1
            x += 1
        y += 1


    #should double check if none of the found slices actually conflict...
    print("found:" + str(slices.__len__()))
    #i = 1
    #print("doing validity check")
    #for slice in slices:
        #print("checking:" + str(i))
        #for other in slices:
            #if slice != other and slice.conflicts_with(other):
                #print("u fucked up")
                #break
        #i += 1

    print("final area: " + str(area))
    slice_printer(slices)



main()
