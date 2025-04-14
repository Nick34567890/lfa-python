from Lab5.VariantGrammarToNormalize import get_grammar_15
from Lab5.cnf_engine import CNFengine

def print_grammar_details(grammar):
    V_N = grammar.non_terminals
    V_T = grammar.terminals
    S = grammar.start_symbol
    P = grammar.productions

    print("V_N :", [str(x) for x in V_N])
    print("V_T:", [str(x) for x in V_T])
    print("S: ", str(S))
    print("P:[")
    prod_map = {}
    for rule in P:
        lhs = rule.left
        rhs = rule.right
        if lhs not in prod_map:
            prod_map[lhs] = []
        prod_map[lhs].append(rhs)
    for lhs, rhss in prod_map.items():
        rhs_str = " | ".join([" ".join(str(symbol) for symbol in rhs) if rhs else "ε" for rhs in rhss])
        print(f"  {str(lhs)} → {rhs_str}")
    print("]")

def print_initial_grammar(grammar):
    print("\033[96mInitial grammar:\033[0m")
    print_grammar_details(grammar)

def print_productions(cnf_engine):
    grammar = cnf_engine.get_grammar()
    print("\nProductions:")
    print_grammar_details(grammar)

def test_normalization():
    grammar = get_grammar_15()
    cnf_engine = CNFengine(grammar)
    cnf_engine.normalize()
    print_productions(cnf_engine)

def test_with_reasoning():
    grammar = get_grammar_15()

    # Step 0: Print initial grammar in styled format
    print_initial_grammar(grammar)
    print("\n" + "-" * 50)

    cnf_engine = CNFengine(grammar)

    # Step 1: Resolve starting symbol
    print("\033[93mStep 1: Grammar after resolving S rule:\033[0m")
    cnf_engine.resolve_starting_symbol()
    print_grammar_details(cnf_engine.get_grammar())
    print("\n" + "-" * 50)

    # Step 2: Remove inaccessible rules
    print("\033[96mStep 2: Grammar after removing inaccessible rules:\033[0m")
    cnf_engine.remove_inaccessible()
    print_grammar_details(cnf_engine.get_grammar())
    print("\n" + "-" * 50)

    # Step 3: Eliminate epsilon transitions
    print("\033[95mStep 3: Grammar after eliminating epsilon transitions:\033[0m")
    cnf_engine.eliminate_epsilon_transitions()
    print_grammar_details(cnf_engine.get_grammar())
    print("\n" + "-" * 50)

    # Step 4: Eliminate renamings
    print("\033[94mStep 4: Grammar after eliminating renamings:\033[0m")
    cnf_engine.eliminate_renamings()
    print_grammar_details(cnf_engine.get_grammar())
    print("\n" + "-" * 50)

    # Step 5: Shorten productions
    print("\033[93mStep 5: Grammar after shortening productions:\033[0m")
    cnf_engine.replace_long_productions()
    print_grammar_details(cnf_engine.get_grammar())
    print("\n" + "-" * 50)

    # Step 6: Replace terminals with intermediate rules
    print("\033[95mStep 6: Grammar after replacing terminals with intermediate rules:\033[0m")
    cnf_engine.replace_terminals_with_intermediate()
    print_grammar_details(cnf_engine.get_grammar())
    print("\n" + "-" * 50)

    # Step 7: Remove repetitions
    print("\033[92mStep 7: Grammar after removing repetitions:\033[0m")
    cnf_engine.remove_repetitions()
    print_grammar_details(cnf_engine.get_grammar())
    print("\n" + "=" * 50)

if __name__ == "__main__":
    test_normalization()
    test_with_reasoning()