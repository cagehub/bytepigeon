def pizza_parser(inputfile):
    with inputfile as f:
        first_line = f.readline()

    return first_line

inputfile = open('small.in', 'r')
outputfile = open('small.out', 'w')

pizza = pizza_parser(inputfile)

outputfile.writelines(pizza)
inputfile.close()
outputfile.close()