# TokenType.py
from enum import Enum

class TokenType(Enum):
    # Reserved Keywords
    BATCH = "BATCH"
    FOREACH = "FOREACH"
    FSIZE = "FSIZE"
    FNAME = "FNAME"
    FHEIGHT = "FHEIGHT"
    FWIDTH = "FWIDTH"
    METADATA = "METADATA"
    RIGHT = "RIGHT"
    LEFT = "LEFT"
    SET = "SET"
    ELIF = "ELIF"
    ELSE = "ELSE"
    IF = "IF"
    SHARPEN = "SHARPEN"
    NEGATIVE = "NEGATIVE"
    BW = "BW"
    SEPIA = "SEPIA"
    CROP = "CROP"
    ROTATE = "ROTATE"
    IMG = "IMG"
    IN = "IN"
    INT = "INT"
    DOUBLE = "DOUBLE"

    # Types
    TYPE_BATCH = "TYPE_BATCH"
    TYPE_IMG = "TYPE_IMG"
    TYPE_STR = "TYPE_STR"
    TYPE_BOOL = "TYPE_BOOL"
    TYPE_DBL = "TYPE_DBL"
    TYPE_INT = "TYPE_INT"
    TYPE_PXLS = "TYPE_PXLS"

    # Values
    PXLS_VALUE = "PXLS_VALUE"
    STR_VALUE = "STR_VALUE"
    BOOL_VALUE = "BOOL_VALUE"
    DBL_VALUE = "DBL_VALUE"
    INT_VALUE = "INT_VALUE"

    # Identifier
    VAR_IDENTIFIER = "VAR_IDENTIFIER"

    # Symbols
    CLOSE_P = "CLOSE_P"
    OPEN_P = "OPEN_P"
    COMMA = "COMMA"
    NOT_EQUAL = "NOT_EQUAL"
    EQUAL = "EQUAL"
    SMALLER = "SMALLER"
    GREATER = "GREATER"
    SMALLER_EQUAL = "SMALLER_EQUAL"
    GREATER_EQUAL = "GREATER_EQUAL"
    ASSIGN = "ASSIGN"
    CLOSE_BLOCK = "CLOSE_BLOCK"
    OPEN_BLOCK = "OPEN_BLOCK"
    DIVIDE = "DIVIDE"
    MULTIPLY = "MULTIPLY"
    MINUS = "MINUS"
    PLUS = "PLUS"

    # SPECIAL
    EOL = "EOL"
    EOF = "EOF"
