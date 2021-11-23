from typing import Set, Dict, List


class Grammar:
    non_terminals : Set[str]
    terminals : Set[str]
    productions: Dict[str,List[str]]
    starting_symbol: str


    def __init__(self,non_terminals,terminals, productions,starting_symbol):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.productions = productions
        self.starting_symbol = starting_symbol

    @staticmethod
    def parseFile(self, filename):
        with open(filename, "r") as file:
            with open(filename, "r") as file:
                non_terminals = set([nt.strip() for nt in file.readline().strip().split(',')])
                terminals = set([nt.strip() for nt in file.readline().strip().split(',')])
                starting_symbol = file.readline().strip()
                productions = {}
                for line in file:
                    symbol, rules = [el.strip() for el in line.strip().split('->')]
                    rules = set([rule.strip() for rule in rules.split('|')])
                    # validation
                    for rule in rules:
                        for res in rule.split(' '):
                            if res not in terminals and res not in non_terminals:
                                raise SyntaxError(
                                    "Rule element not present in either terminals or non terminals element:" + res)
                    # if no error add to productions
                    productions[symbol] = rules
                return Grammar(non_terminals, terminals, productions, starting_symbol)

    def getNonTerminals(self):
        return self.non_terminals

    def getTerminals(self):
        return self.terminals

    def getProductions(self):
        return self.productions

    def getStartingSymbol(self):
        return self.starting_symbol


