from typing import List, Dict, Tuple


class FiniteAutomaton:
    states: List[str]
    alphabet: List[str]
    transitions: Dict[Tuple[str, str], List[str]]
    initial_state: str
    final_states: List[str]

    def __init__(self, states: List[str], alphabet: List[str], transitions: Dict[Tuple[str, str], List[str]],
                 initial_state: str, final_states: List[str]):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states

    @staticmethod
    def readFromFile(file_name: str):
        states = []
        alphabet = []
        transitions = {}
        initial_state = None
        final_states = []

        with open(file_name, 'r') as file:
            for lineCounter, line in enumerate(file, start=1):
                line: str = line.strip()
                tokens = line.split(" ")
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
        return FiniteAutomaton(states, alphabet, transitions, initial_state, final_states)

    def printStates(self):
        print("Set of states: ", self.states)

    def printAlphabet(self):
        print("FA alphabet: ", self.alphabet)

    def printInitialState(self):
        print("Initial state: ", self.initial_state)

    def printFinalStates(self):
        print("Final states: ", self.final_states)

    def printTransitions(self):
        print("Transitions: ")
        for t in self.transitions.keys():
            print("delta({0}, {1}) = {2}".format(t[0], t[1], self.transitions[t]))

    def checkSequence(self, sequence) -> bool:
        if not self.Dfa():
            raise ArithmeticError("FiniteAutomaton is not a DFA")
        current_state = self.initial_state

        while sequence != "":
            transition_key = (current_state, sequence[0])

            if transition_key in self.transitions.keys():
                current_state = self.transitions[transition_key][0]
                sequence = sequence[1:]

            else:
                return False

        return current_state in self.final_states

    def Dfa(self) -> bool:
        for k in self.transitions.keys():
            if len(self.transitions[k]) > 1:
                return False
        return True


if __name__ == "__main__":
    automata = FiniteAutomaton.readFromFile("fa.in")
    automata.printStates()
    automata.printAlphabet()
    automata.printInitialState()
    automata.printFinalStates()
    automata.printTransitions()
    print("65", automata.checkSequence("65"))
    print("12a", automata.checkSequence("12a"))
    print("0", automata.checkSequence("0"))