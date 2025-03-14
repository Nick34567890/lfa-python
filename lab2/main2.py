'''
Variant 15
Q = {q0,q1,q2,q3},
∑ = {a,b,c},
F = {q3},
δ(q0,a) = q0,
δ(q1,b) = q2,
δ(q0,a) = q1,
δ(q2,a) = q2,
δ(q2,b) = q3,
δ(q2,c) = q0.
'''


from collections import defaultdict, deque
import matplotlib.pyplot as plt

class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions  # {(state, symbol): [next_states]}
        self.start_state = start_state
        self.final_states = final_states

    def is_deterministic(self):
        """Check if the automaton is deterministic (DFA)."""
        for key, next_states in self.transitions.items():
            if len(next_states) > 1:
                return False
        return True

    def to_regular_grammar(self):
        """Convert FA to Regular Grammar."""
        rules = defaultdict(list)

        for (state, symbol), next_states in self.transitions.items():
            for next_state in next_states:
                rules[state].append(f"{symbol}{next_state}")

        # Add ε (epsilon) production for final states
        for final_state in self.final_states:
            rules[final_state].append("ε")

        return dict(rules)

    def classify_grammar(self):
        """Classify grammar based on Chomsky hierarchy."""
        # Since we're using finite automata, it must be Type 3 (Regular Grammar)
        return "Type 3 (Regular Grammar)"

    def convert_ndfa_to_dfa(self):
        """Convert NDFA to DFA using subset construction."""
        dfa_transitions = {}
        start = frozenset([self.start_state])
        queue = deque([start])
        visited = {start}

        while queue:
            current = queue.popleft()

            for symbol in self.alphabet:
                next_states = set()

                for state in current:
                    next_states.update(self.transitions.get((state, symbol), []))

                next_states_frozen = frozenset(next_states)

                if next_states:
                    dfa_transitions[(current, symbol)] = next_states_frozen
                    if next_states_frozen not in visited:
                        visited.add(next_states_frozen)
                        queue.append(next_states_frozen)

        # Determine final states for DFA
        dfa_final_states = {state for state in visited if any(s in self.final_states for s in state)}

        return FiniteAutomaton(visited, self.alphabet, dfa_transitions, start, dfa_final_states)

    def visualize(self):
        """Visualize the FA using matplotlib."""
        plt.figure(figsize=(8, 6))
        pos = {state: (i*2, 0) for i, state in enumerate(self.states)}

        # Plot states
        for state in self.states:
            x, y = pos[state]
            color = 'red' if state in self.final_states else 'white'
            circle = plt.Circle((x, y), 0.5, color=color, ec='black', zorder=2)
            plt.gca().add_patch(circle)
            plt.text(x, y, state, fontsize=12, ha='center', va='center', zorder=3)

        # Plot transitions
        for (state, symbol), next_states in self.transitions.items():
            for next_state in next_states:
                x1, y1 = pos[state]
                x2, y2 = pos[next_state]

                plt.arrow(x1, y1, x2 - x1 - 0.5, y2 - y1,
                          length_includes_head=True, head_width=0.2, fc='blue', ec='blue')
                mid_x = (x1 + x2) / 2
                mid_y = (y1 + y2) / 2
                plt.text(mid_x, mid_y + 0.2, symbol, color='blue', fontsize=10)

        # Starting state arrow
        start_x, start_y = pos[self.start_state]
        plt.arrow(start_x - 1, start_y, 0.8, 0, length_includes_head=True, head_width=0.2, fc='green', ec='green')
        plt.text(start_x - 1.5, start_y, "start", color='green', fontsize=10)

        plt.axis('equal')
        plt.axis('off')
        plt.title("Finite Automaton Visualization")
        plt.show()


# Variant 15 Definition
states = {'q0', 'q1', 'q2', 'q3'}
alphabet = {'a', 'b', 'c'}
transitions = {
    ('q0', 'a'): ['q0', 'q1'],
    ('q1', 'b'): ['q2'],
    ('q2', 'a'): ['q2'],
    ('q2', 'b'): ['q3'],
    ('q2', 'c'): ['q0']
}
start_state = 'q0'
final_states = {'q3'}

# Instantiate FA
fa = FiniteAutomaton(states, alphabet, transitions, start_state, final_states)

# Check if DFA
is_dfa = fa.is_deterministic()
print(f"Is the FA deterministic? {'Yes' if is_dfa else 'No'}")

# Convert to Regular Grammar
regular_grammar = fa.to_regular_grammar()
print("\nRegular Grammar Production Rules:")
for state, productions in regular_grammar.items():
    for prod in productions:
        print(f"{state} -> {prod}")

# Grammar classification
grammar_type = fa.classify_grammar()
print(f"\nGrammar Type: {grammar_type}")

# Convert NDFA to DFA if necessary
if not is_dfa:
    dfa = fa.convert_ndfa_to_dfa()
    print("\nConverted DFA Transitions:")
    for (state_set, symbol), next_state_set in dfa.transitions.items():
        current = ','.join(state_set)
        next_state = ','.join(next_state_set)
        print(f"({current}, {symbol}) -> {next_state}")

# Visualize the FA
fa.visualize()

