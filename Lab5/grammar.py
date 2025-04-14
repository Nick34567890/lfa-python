
from typing import List, Set, Union

class Letter:
    EPSILON = 'ε'

    def __init__(self, symbol: str):
        self.symbol = symbol

    def __repr__(self):
        return self.symbol

    def __eq__(self, other):
        return isinstance(other, Letter) and self.symbol == other.symbol

    def __hash__(self):
        return hash(self.symbol)


class DeriveRule:
    def __init__(self, left: Letter, right: Union[List[Letter], str]):
        self.left = left
        if isinstance(right, str) and right == Letter.EPSILON:
            self.right = [Letter(Letter.EPSILON)]
        else:
            self.right = right

    def __repr__(self):
        right_str = ' '.join(str(r) for r in self.right)
        return f"{self.left} → {right_str}"

    def __eq__(self, other):
        return self.left == other.left and self.right == other.right

    def __hash__(self):
        return hash((self.left, tuple(self.right)))


class Grammar:
    def __init__(self, VN: Set[Letter], VT: Set[Letter], P: Set[DeriveRule], S: Letter):
        self.non_terminals = VN
        self.terminals = VT
        self.productions = P
        self.start_symbol = S

    def __repr__(self):
        result = [f"Start symbol: {self.start_symbol}"]
        result.append("Productions:")
        for rule in self.productions:
            result.append(f"  {rule}")
        return '\n'.join(result)
