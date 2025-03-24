# Token.py
from TokenType import TokenType

class Token:
    def __init__(self, token_type: TokenType, value: str, line: int, column: int):
        self.type = token_type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"{self.type}: '{self.value}' at line {self.line}, column {self.column}"
