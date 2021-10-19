class ProgramInternalForm:
    def __init__(self):
        self.pif = []

    def add(self, token, st_position):
        self.pif.append((token, st_position))

    def __str__(self):
        return str(self.pif)