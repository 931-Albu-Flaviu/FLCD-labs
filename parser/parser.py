from typing import Literal

from domain.LanguageSymbols import *
from parser.grammar import Grammar


class ParserRecursiveDescendant:

    grammar: Grammar
    state: Literal["q", "b", "f", "e"]

    def __init__(self, grammar):
        self.grammar = grammar
        self.work=[]
        self.input=[]
        self.state="q"
        self.index=0
        self.symbol=symbols
        self.word=[]

    def expand(self):
        #when top of input nonTerminal
        nonTerminal = self.input.pop(0)
        self.work.append((nonTerminal, 0))
        # this probably should not be all the time 0 but we will see
        a = list(self.grammar.getProductions()[nonTerminal])[0]
        self.input = a.split(" ") + self.input


    def advance(self):
        #when top of input terminal
        self.work.append(self.input.pop(0))
        self.index += 1

    def momentaryInsuccess(self):
        #WHEN: head of input stack is a terminal ≠ current symbol from input
        self.state = "b"

    def back(self):
        #when state is "b" we restore the input
        #restauration of the input if is not okk
        self.input = [self.work.pop()] + self.input
        self.index -= 1


    def success(self):
        self.state = "f"
        self.index += 1

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



