from grammar import Grammar, DeriveRule, Letter

def get_grammar_15():
    S, A, B, C, D = map(Letter, ["S", "A", "B", "C", "D"])
    a, b = map(Letter, ["a", "b"])

    VN = {S, A, B, C, D}
    VT = {a, b}

    P = {
        DeriveRule(S, [A, C]),
        DeriveRule(S, [B, A]),
        DeriveRule(S, [B]),
        DeriveRule(S, [a, A]),
        DeriveRule(A, [Letter.EPSILON]),
        DeriveRule(A, [a, S]),
        DeriveRule(A, [A, B, a, b]),
        DeriveRule(B, [a]),
        DeriveRule(B, [b, S]),
        DeriveRule(C, [a, b, C]),
        DeriveRule(D, [A, B]),
    }

    return Grammar(VN, VT, P, S)
