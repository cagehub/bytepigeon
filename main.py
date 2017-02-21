def pizza_parser(text):
    pizza = [1,1]
    return text

inputfile = open('small.in', 'r')
outputfile = open('small.out', 'w')
text = inputfile.readlines()

pizza = pizza_parser(text)

outputfile.writelines(pizza)
inputfile.close()
outputfile.close()