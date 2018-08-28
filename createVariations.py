def slimVariations():
    temp = []
    with open('variations.txt', 'r') as rfile:
        with open('varNew.txt', 'w') as wfile:
            for line in rfile:
                temp.append(line)
            temp.sort()
            for i in temp:
                wfile.namewrite(i)


def getVariations(state):
    tempstr = ''
    state = state.lower()
    temp = [state]
    j = 0
    for i in state:
        if (j < len(state) - 1):
            tempstr += i
            temp.append(tempstr)
        j += 1

    splitState = state.split(' ')
    if (len(splitState) > 1):
        temp.append("{}{}".format(splitState[0][0], splitState[1][0]))
        temp.append("{}{}".format(splitState[0].strip(' '), splitState[1].strip(' ')))
    return temp
    

def variations():
    with open('locations.csv', 'r') as locFile:
        with open('citystate.txt', 'w') as varFile:
            for line in locFile:
                lineSplit = line.split(',')
                arr = []
                varFile.write("'{}, {}',".format(lineSplit[1], lineSplit[2]))
                
    # slimVariations()

def main():
    variations()


if __name__ == '__main__':
    main()
