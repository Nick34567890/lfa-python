# File: intermediate_normalization_test.py
from Lab5.VariantGrammarToNormalize import get_grammar_12
from Lab5.cnf_engine import CNFengine


def test_s_normalization():
    grammar = get_grammar_12()
    cnf = CNFengine(grammar)
    cnf.resolve_starting_symbol()

    assert cnf.has_s_on_right(grammar.start_symbol, grammar.productions)

    cnf_grammar = cnf.get_grammar()
    assert not cnf.has_s_on_right(cnf_grammar.start_symbol, cnf_grammar.productions)

if __name__ == "__main__":
    test_s_normalization()
    print("test_s_normalization passed.")
