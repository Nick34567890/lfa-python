'''
Variant 15:
VN={S, A, B},
VT={a, b, c},
P={
    S → aS
    S → bS
    S → cA
    A → aB
    B → aB
    B → bB
    B → c
}

'''




import random

class Grammar:
    def __init__(self, non_terminals, terminals, productions, start_symbol):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.productions = productions
        self.start_symbol = start_symbol

    # Generates a valid string from the grammar
    def generate_string(self):
        return self._generate_string_from_symbol(self.start_symbol)

    # Helper function to recursively generate a string from a non-terminal symbol
    def _generate_string_from_symbol(self, symbol):
        if symbol in self.terminals:
            return symbol

        # Get possible productions for the non-terminal
        production_options = self.productions.get(symbol, [])
        if not production_options:
            return ""  #no found (error case)

        # Randomly pick a production and expand recursively
        production = random.choice(production_options)
        result = []
        for char in production:
            result.append(self._generate_string_from_symbol(char))
        return "".join(result)

    # Converts the Grammar object into a FiniteAutomaton object
    def to_finite_automaton(self):
        # Convert production rules to states and transitions for the Finite Automaton
        #Exmaple set
        states = set(['q0', 'q1', 'q2'])
        alphabet = self.terminals
        transition_function = {
            'q0': {'a': 'q1', 'b': 'q1', 'c': 'q2'},
            'q1': {'a': 'q1', 'b': 'q1', 'c': 'q2'},
            'q2': {'a': 'q1', 'b': 'q1', 'c': 'q2'}
        }
        start_state = 'q0'
        accepting_states = {'q2'}

        return FiniteAutomaton(states, alphabet, transition_function, start_state, accepting_states)


class FiniteAutomaton:
    def __init__(self, states, alphabet, transition_function, start_state, accepting_states):
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.start_state = start_state
        self.accepting_states = accepting_states

    # Check if a given input string is accepted by the automaton
    def string_belongs_to_language(self, input_string):
        current_state = self.start_state

        for symbol in input_string:
            if symbol not in self.alphabet:
                return False
            if current_state in self.transition_function and symbol in self.transition_function[current_state]:
                current_state = self.transition_function[current_state][symbol]
            else:
                return False

        return current_state in self.accepting_states


def main():
    # Define the grammar for Variant 15
    non_terminals = {'S', 'A', 'B'}
    terminals = {'a', 'b', 'c'}
    productions = {
        'S': ['aS', 'bS', 'cA'],
        'A': ['aB'],
        'B': ['aB', 'bB', 'c']
    }
    start_symbol = 'S'

    grammar = Grammar(non_terminals, terminals, productions, start_symbol)

    # Generate 5 valid strings from the grammar
    print("Generated strings:")
    generated_strings = [grammar.generate_string() for _ in range(5)]
    for string in generated_strings:
        print(string)

    # Convert the grammar to a finite automaton
    automaton = grammar.to_finite_automaton()

    # Check if generated strings are accepted by the automaton
    print("\nString acceptance check:")
    for s in generated_strings:
        print(f"String '{s}' accepted: {automaton.string_belongs_to_language(s)}")


    while(True):
        print("\nEnter a string to check against the FA rules: ")
        inputS = input("String: ").lower()
        if(inputS.lower() == "exit"):
            break
        print(f"String '{inputS}' accepted: {automaton.string_belongs_to_language(inputS)}")

if __name__ == "__main__":
    main()
