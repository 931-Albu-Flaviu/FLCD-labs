class FiniteAutomata:
    '''

    '''
    def __init__(self):
        self.states=[]
        self.alphabet=[]
        self.transitions={}
        self.initialState = None
        self.finalStates = []
        
    def readFromFile(file_name: str):
        states = []
        alphabet = []
        transitions = {}
        initial_state = None
        final_states = []

        with open(file_name, 'r') as file:
            for lineCounter, line in enumerate(file, start=1):
                line: str = line.strip()
                tokens = line.split(";")
                if tokens[0] == "states":
                    states = tokens[1:]
                elif tokens[0] == "alphabet":
                    alphabet = tokens[1:]
                elif tokens[0] == "transitions":
                    for transition in tokens[1:]:
                        transition_tokens = transition.split(",")
                        trans = (transition_tokens[0], transition_tokens[1])
                        if trans in transitions:
                            transitions[trans].append(transition_tokens[2])
                        else:
                            transitions[trans] = [transition_tokens[2]]
                elif tokens[0] == "initialState":
                    initial_state = tokens[1]
                elif tokens[0] == "finalState":
                    final_states = tokens[1:]
        return FiniteAutomata()

    def printStates(self):
        print("Set of states: ", self.states)

    def printAlphabet(self):
        print("FA alphabet: ", self.alphabet)

    def printInitialState(self):
        print("Initial state: ", self.initialState)

    def printFinalStates(self):
        print("Final states: ", self.finalStates)

    def printTransitions(self):
        print("Transitions: ")
        for t in self.transition.keys():
            print("delta({0}, {1}) = {2}".format(t[0], t[1], self.transition[t]))


