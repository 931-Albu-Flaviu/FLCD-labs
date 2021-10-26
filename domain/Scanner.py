import re

from domain.LanguageSymbols import *


class Scanner:

    def __init__(self) -> None:
        self.cases = ["=+", "<+", ">+", "<=+", ">=+", "==+", "!=+", "=-", "<-", ">-", "<=-", ">=-", "==-", "!=-"]

    def getStringToken(self, line, index):
        token = ''
        quotes = 0

        while index < len(line) and quotes < 2:
            if line[index] == '"':
                quotes += 1
            token += line[index]
            index += 1

        return token, index

    def getCharToken(self, line, index):
        token = ''
        quotes = 0

        while index < len(line) and quotes < 2:
            if line[index] == '\'':
                quotes += 1
            token += line[index]
            index += 1

        return token, index
    #if i find a ' i just searh for the other one and return the string that is between them

    def isPartOfOperator(self, char):
        for op in operators:
            if char in op:
                return True
        return False

    def getOperatorToken(self, line, index):
        token = ''

        while index < len(line) and self.isPartOfOperator(line[index]):
            token += line[index]
            index += 1

        return token, index

    def isIdentifier(self, token):
        return re.match(r'^[a-z]([a-zA-Z]|[0-9])*$', token) is not None
    #trebuie sa inceapa cu litera mica dupa poate fi urmat de a-zA-Z sau 0-9 de mai multe ori

    def isConstant(self, token):
        return re.match(r'^(0|([+-]?[1-9][0-9]*)|([+-]?[0-9]\.[0-9]+))$|^\".\"$|^\".*\"$|^\'[a-zA-Z0-9]\'$', token) is not None
    #
    '''
    the tokenizer goes charachter by char on every line and checks
    if the curretn char is a part of oerator, separator or begins a string 
    or is an identifier and after that appends the token to a list which will be returned
    '''
    def tokenize(self, line):
        token = ''
        index = 0
        tokens = []
        while index < len(line):
            if self.isPartOfOperator(line[index]):
                if token:
                    tokens.append(token)
                token, index = self.getOperatorToken(line, index)
                tokens.append(token)
                token = ''  # reset token

            elif line[index] == '"':
                if token:
                    tokens.append(token)
                token, index = self.getStringToken(line, index)
                tokens.append(token)
                token = ''  # reset token
            elif line[index] == '\'':
                if token:
                    tokens.append(token)
                token, index = self.getCharToken(line, index)
                tokens.append(token)
                token = ''  # reset token


            elif line[index] in separators:
                if token:
                    tokens.append(token)
                token, index = line[index], index + 1
                tokens.append(token)
                token = ''  # reset token

            else:
                token += line[index]
                index += 1
        if token:
            tokens.append(token)
        return tokens

