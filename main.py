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
        pizza.lines = [l for l in f]
    return pizza

pizza = pizza_parser('small.in')

#outputfile = open('small.out', 'w')
#outputfile.writelines(pizza)
#outputfile.close()