reservedWords = []
separators = []
operators = []
symbols=[]


def readFile():
    with open('Token.in', 'r') as f:
        f.readline()
        for i in range(11):
            separator = f.readline().strip()
            if separator == "<space>":
                separator = " "
            separators.append(separator)
        for i in range(13):
            operators.append(f.readline().strip())
        for i in range(13):
            reservedWords.append(f.readline().strip())
