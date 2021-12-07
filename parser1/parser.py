from typing import Literal

from domain.LanguageSymbols import *
from parser1.grammar import Grammar


class ParserRecursiveDescendant:

    grammar: Grammar
    state: Literal["q", "b", "f", "e"]

    def __init__(self, grammar):
        self.grammar = grammar
        self.work=[]
        self.input=[]
        self.state="q"
        self.debug = False
        self.index=0
        self.tree = []

        self.symbol=symbols
        self.words=[]
        self.iteration=0

    def printParserStep(self, step):
        print("~~~~~~~~~~~~")
        print(step)
        print("iteration: ", self.iteration)
        self.iteration += 1
        print(self.state)
        print(self.index)
        string = ""
        for i in self.work:
            if type(i) != tuple:
                string += "\"" + list(self.tokenCodes.keys())[list(self.tokenCodes.values()).index(int(i))] + "\" , "
            else:
                string += str(i) + ", "
        print(string)
        string = ""
        for i in self.input:
            try:
                string += "\"" + list(self.tokenCodes.keys())[list(self.tokenCodes.values()).index(int(i))] + "\" , "
            except:
                string += str(i) + ", "
        print(string)
        string = ""
        for i in self.words:
            if type(i) != tuple:
                string += "\"" + list(self.tokenCodes.keys())[list(self.tokenCodes.values()).index(int(i))] + "\" , "
            else:
                string += str(i) + ", "
        print(string)

    def expand(self):
        #when top of input nonTerminal
        nonTerminal = self.input.pop(0)
        self.work.append((nonTerminal, 0))
        # this probably should not be all the time 0 but we will see
        a = list(self.grammar.getProductions()[nonTerminal])[0]
        self.input = a.split(" ") + self.input
        if self.debug:
            self.printParserStep("expand")


    def advance(self):
        #when top of input terminal
        self.work.append(self.input.pop(0))
        self.index += 1
        if self.debug:
            self.printParserStep("advance")

    def momentaryInsuccess(self):
        #WHEN: head of input stack is a terminal ≠ current symbol from input
        self.state = "b"
        if self.debug:
            self.printParserStep("mom insuccess")

    def back(self):
        #when state is "b" we restore the input
        #restauration of the input if is not okk
        self.input = [self.work.pop()] + self.input
        self.index -= 1
        if self.debug:
            self.printParserStep("back")


    def success(self):
        self.state = "f"
        self.index += 1
        if self.debug:
            self.printParserStep("success")


    def anotherTry(self):
        if self.index == 0 and self.work[len(self.work) - 1][0] == self.grammar.getStartingSymbol():
            self.state="e"
            return

        (currentNonTerm, nonTermIndex) = self.work.pop()
        currentNonTermProductions = self.grammar.getProductions()[currentNonTerm]

        if len(currentNonTermProductions) - 1 > nonTermIndex:
            self.state = "q"
            self.work.append((currentNonTerm, nonTermIndex + 1))

            #remove previos production and add current production
            for i in currentNonTermProductions[nonTermIndex]:
                self.input.pop(0)
            aux = currentNonTermProductions[nonTermIndex + 1]
            self.input = aux + self.input

        else:
            for i in currentNonTermProductions[nonTermIndex]:
                self.input.pop(0)
            self.input = [currentNonTerm] + self.input

    def checkWordLength(self, w):
        if len(w) > self.index:
            return self.input[0] == w[self.index]
        return False

    def parse_tree(self,work):
        father=-1

        for index in range(0, len(work)):
            if type(work[index]) == tuple:
                self.tree.append(Node(work[index][0]))
                self.tree[index].production = work[index][1]
            else:
                self.tree.append(Node(work[index]))

        for index in range(0, len(work)):
            if type(work[index]) == tuple:
                self.tree[index].father = father
                father = index
                lengthProduction = len(self.grammar.getProductions()[work[index][0]][work[index][1]])
                vectorIndex = []
                # [1, 2, 3, 4] we will add some offsets according to the corresponding production size in order to match the indexes
                # [1, 2, 9, 21]
                for i in range(1, lengthProduction + 1):
                    vectorIndex.append(index + i)
                for i in range(0, lengthProduction):
                    if self.tree[vectorIndex[i]].production != -1:  # if it is a nonTerminal, compute offset
                        offset = self.getProductionOffset(vectorIndex[i])
                        for j in range(i + 1, lengthProduction):
                            vectorIndex[j] += offset
                for i in range(0, lengthProduction - 1):
                    self.tree[vectorIndex[i]].sibling = vectorIndex[i + 1]

            else:
                self.tree[index].father = father
                father = -1



    def getProductionOffset(self, index):
        production = self.grammar.getProductions()[self.work[index][0]][self.work[index][1]]
        lengthOfProduction = len(production)
        offset = lengthOfProduction
        for i in range(1, lengthOfProduction + 1):
            if type(self.work[index + i]) == tuple:
                offset += self.getProductionOffset(index + i)
        return offset


    def run(self,w):
        self.words=w
        self.state="q"
        self.index=0
        self.work=[]
        self.input=[self.grammar.getStartingSymbol()]
        while self.state !="f" and self.state!="e":
            if self.state=="q":
                if len(self.input) == 0 and self.index == len(self.words):
                    self.success()
                else:
                    if self.input[0] in self.grammar.getNonTerminals():
                        self.expand()
                    elif self.input[0] in self.grammar.getTerminals() and self.checkWordLength(self.words):
                        self.advance()
                # we have a momentary insuccess
                    else:
                        self.momentaryInsuccess()
            elif self.state=="b":
                # back
                if self.work[len(self.work) - 1] in self.grammar.getTerminals():
                    self.back()
                # anotherTry
                else:
                    self.anotherTry()

        if self.state == "e":
            print("ERROR")
        else:
            print("Sequence accepted")
            print(self.work, self.input, self.index)

    def write_tree_to_file(self, filename):
        file = open(filename, "w")
        file.write("index | value | father | sibling\n")

        for index in range(0, len(self.work)):
            file.write(str(index) + " " + str(self.tree[index]) + "\n")
            print(index, " ", str(self.tree[index]))

        file.close()

class Node:
    # this is a node in the parse tree, an arbitrary tree using the father sibling representation
    # all nodes are connected with only 2 links - the father and the right sibling
    # these nodes will be stored in a python list
    def __init__(self, value):
        self.father = -1
        self.sibling = -1
        self.value = value
        self.production = -1

    def __str__(self):
        return str(self.value) + " " + str(self.father) + " " + str(self.sibling)




