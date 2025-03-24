# Tokenizer.py
import re
from Token import Token
from TokenType import TokenType

class Tokenizer:
    def __init__(self, input_text: str):
        self.input = input_text
        self.position = 0
        self.line = 1
        self.column = 1

    # Regex patterns for tokenizing
    number_regex = r'(\d+\.\d+|\d+p|\d+)'

    def tokenize(self):
        tokens = []

        while self.position < len(self.input):
            current = self.input[self.position]

            if current in ('\n', '\r'):
                self.handle_newline(current)
                continue

            # Skip over whitespaces (spaces, tabs, etc.)
            if current in (' ', '\t'):
                self.skip_whitespace()
                continue

            token = self.match_token()
            if token:
                tokens.append(token)
            else:
                raise Exception(f"Unexpected character '{current}' at line {self.line}, column {self.column}")

        tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return tokens

    def skip_whitespace(self):
        # Skip over any whitespace characters
        while self.position < len(self.input) and self.input[self.position] in (' ', '\t'):
            self.position += 1
            self.column += 1

    def handle_newline(self, current):
        if current == '\n':
            self.line += 1
            self.column = 1
        elif current == '\r':
            if self.position + 1 < len(self.input) and self.input[self.position + 1] == '\n':
                self.position += 1
            self.line += 1
            self.column = 1
        self.position += 1

    def match_token(self):
        current = self.input[self.position]

        if current == ')':
            return self.advance(TokenType.CLOSE_P, ")")
        if current == '(':
            return self.advance(TokenType.OPEN_P, "(")
        if current == ',':
            return self.advance(TokenType.COMMA, ",")
        if current == '}':
            return self.advance(TokenType.CLOSE_BLOCK, "}")
        if current == '{':
            return self.advance(TokenType.OPEN_BLOCK, "{")
        if current == ';':
            return self.advance(TokenType.EOL, ";")
        if current == '/':
            return self.advance(TokenType.DIVIDE, "/")
        if current == '*':
            return self.advance(TokenType.MULTIPLY, "*")
        if current == '+':
            return self.advance(TokenType.PLUS, "+")
        if current == '-':
            return self.advance(TokenType.MINUS, "-")

        if current == '=':
            if self.peek() == '=':
                return self.advance_two(TokenType.EQUAL, "==")
            return self.advance(TokenType.ASSIGN, "=")

        if current == '>':
            if self.peek() == '=':
                return self.advance_two(TokenType.GREATER_EQUAL, ">=")
            return self.advance(TokenType.GREATER, ">")

        if current == '<':
            if self.peek() == '=':
                return self.advance_two(TokenType.SMALLER_EQUAL, "<=")
            return self.advance(TokenType.SMALLER, "<")

        if current == '!':
            if self.peek() == '=':
                return self.advance_two(TokenType.NOT_EQUAL, "!=")
            return None

        if current.isalpha() or current in ('$','#'):
            word = self.read_word()
            return self.create_word_token(word)

        if current.isdigit():
            return self.match_number()

        if current == '"':
            return self.read_string()

        return None

    def advance(self, token_type, value):
        self.position += 1
        self.column += 1
        return Token(token_type, value, self.line, self.column - 1)

    def advance_two(self, token_type, value):
        self.position += 2
        self.column += 2
        return Token(token_type, value, self.line, self.column - 2)

    def peek(self):
        return self.input[self.position + 1] if self.position + 1 < len(self.input) else '\0'

    def read_word(self):
        start = self.position
        while self.position < len(self.input) and (self.input[self.position].isalnum() or self.input[self.position] in ('$', '#')):
            self.position += 1
            self.column += 1
        return self.input[start:self.position]

    def create_word_token(self, word):
        # This function maps words to token types
        if word.upper() in TokenType.__members__:
            return Token(TokenType[word.upper()], word, self.line, self.column - len(word))
        if word.startswith('$') or word.startswith('#'):
            return Token(TokenType.VAR_IDENTIFIER, word, self.line, self.column - len(word))
        raise Exception(f"Unexpected word '{word}' at line {self.line}, column {self.column - len(word)}")

    def match_number(self):
        match = re.match(self.number_regex, self.input[self.position:])
        if match:
            value = match.group(0)
            self.position += len(value)
            self.column += len(value)
            if value.endswith('p'):
                return Token(TokenType.PXLS_VALUE, value, self.line, self.column - len(value))
            if '.' in value:
                return Token(TokenType.DBL_VALUE, value, self.line, self.column - len(value))
            return Token(TokenType.INT_VALUE, value, self.line, self.column - len(value))
        return None

    def read_string(self):
        self.position += 1
        self.column += 1
        start = self.position
        while self.position < len(self.input) and self.input[self.position] != '"':
            self.position += 1
            self.column += 1
        value = self.input[start:self.position]
        self.position += 1
        self.column += 1
        return Token(TokenType.STR_VALUE, f'"{value}"', self.line, self.column - len(value) - 2)
