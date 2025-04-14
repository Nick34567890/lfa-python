from grammar import Grammar, DeriveRule, Letter

class CNFengine:
    def __init__(self, grammar: Grammar):
        self.grammar = grammar

    def normalize(self):
        self.resolve_starting_symbol()
        self.remove_inaccessible()
        self.eliminate_epsilon_transitions()
        self.eliminate_renamings()
        self.replace_long_productions()
        self.replace_terminals_with_intermediate()
        self.remove_repetitions()

    def resolve_starting_symbol(self):
        # Add a new start symbol S0 → S if S appears on right-hand side
        if self.has_s_on_right(self.grammar.start_symbol, self.grammar.productions):
            new_start = Letter("S0")
            new_rule = DeriveRule(new_start, [self.grammar.start_symbol])
            self.grammar.productions.add(new_rule)
            self.grammar.non_terminals.add(new_start)
            self.grammar.start_symbol = new_start

    def has_s_on_right(self, s, productions):
        for rule in productions:
            if s in rule.right:
                return True
        return False

    def remove_inaccessible(self):
        accessible = set()
        queue = [self.grammar.start_symbol]

        while queue:
            current = queue.pop()
            if current not in accessible:
                accessible.add(current)
                for rule in self.grammar.productions:
                    if rule.left == current:
                        for symbol in rule.right:
                            if symbol in self.grammar.non_terminals:
                                queue.append(symbol)

        self.grammar.productions = {
            rule for rule in self.grammar.productions if rule.left in accessible
        }
        self.grammar.non_terminals = {
            nt for nt in self.grammar.non_terminals if nt in accessible
        }

    def eliminate_epsilon_transitions(self):
        nullable = set()
        for rule in self.grammar.productions:
            if rule.right == []:
                nullable.add(rule.left)

        changed = True
        while changed:
            changed = False
            for rule in self.grammar.productions:
                if all(sym in nullable for sym in rule.right) and rule.left not in nullable:
                    nullable.add(rule.left)
                    changed = True

        new_productions = set()
        for rule in self.grammar.productions:
            right = rule.right
            n = len(right)
            indexes = [i for i, sym in enumerate(right) if sym in nullable]
            for i in range(1 << len(indexes)):
                if i == 0:
                    continue
                temp = right[:]
                for j, idx in enumerate(indexes):
                    if (i >> j) & 1:
                        temp[idx] = None
                new_right = [s for s in temp if s is not None]
                new_productions.add(DeriveRule(rule.left, new_right))
        self.grammar.productions.update(new_productions)
        self.grammar.productions = {
            rule for rule in self.grammar.productions if rule.right != []
        }

    def eliminate_renamings(self):
        unit_pairs = {(rule.left, rule.right[0])
                      for rule in self.grammar.productions
                      if len(rule.right) == 1 and rule.right[0] in self.grammar.non_terminals}

        changed = True
        while changed:
            changed = False
            new_pairs = unit_pairs.copy()
            for (a, b) in unit_pairs:
                for (c, d) in unit_pairs:
                    if b == c and (a, d) not in new_pairs:
                        new_pairs.add((a, d))
                        changed = True
            unit_pairs = new_pairs

        new_productions = set()
        for (a, b) in unit_pairs:
            for rule in self.grammar.productions:
                if rule.left == b and (len(rule.right) != 1 or rule.right[0] not in self.grammar.non_terminals):
                    new_productions.add(DeriveRule(a, rule.right))

        self.grammar.productions = {
            rule for rule in self.grammar.productions
            if not (len(rule.right) == 1 and rule.right[0] in self.grammar.non_terminals)
        }
        self.grammar.productions.update(new_productions)

    def replace_long_productions(self):
        new_productions = set()
        counter = 1

        for rule in self.grammar.productions:
            if len(rule.right) <= 2:
                new_productions.add(rule)
            else:
                left = rule.left
                right = rule.right
                while len(right) > 2:
                    new_var = Letter(f"X{counter}")
                    counter += 1
                    self.grammar.non_terminals.add(new_var)
                    new_productions.add(DeriveRule(left, [right[0], new_var]))
                    left = new_var
                    right = right[1:]
                new_productions.add(DeriveRule(left, right))

        self.grammar.productions = new_productions

    def replace_terminals_with_intermediate(self):
        new_productions = set()  # Temporary set to hold new productions
        terminal_map = {}
        counter = 1

        for rule in self.grammar.productions:
            new_right = []
            for sym in rule.right:
                if sym in self.grammar.terminals and len(rule.right) > 1:
                    if sym not in terminal_map:
                        new_var = Letter(f"T{counter}")
                        counter += 1
                        terminal_map[sym] = new_var
                        self.grammar.non_terminals.add(new_var)
                        new_productions.add(DeriveRule(new_var, [sym]))  # Add intermediate terminal rule
                    new_right.append(terminal_map[sym])  # Replace terminal with intermediate symbol
                else:
                    new_right.append(sym)  # Keep non-terminal or terminal unchanged
            new_productions.add(DeriveRule(rule.left, new_right))

        self.grammar.productions = new_productions  # Now update after iteration

    def remove_repetitions(self):
        self.grammar.productions = set(self.grammar.productions)

    def get_grammar(self):
        return self.grammar

    def __repr__(self):
        return str(self.grammar)
