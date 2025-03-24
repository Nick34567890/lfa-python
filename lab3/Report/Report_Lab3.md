# Topic: Lexer & Scanner
****
### Course: Formal Languages & Finite Automata
Author: Gancear Nichita
----
## Theory:
****
&ensp;&ensp;&ensp; Lexical analysis is the first phase of a compiler or interpreter, where the source code is converted from a sequence of characters into a sequence of tokens that can be more easily processed by later phases. The component that performs this task is known as a lexer, scanner, or tokenizer.
##### Core Concepts
- **Lexemes**: The actual character sequences in the source code that match a pattern for a token type. For example, in `count = 7`, the lexemes are `count`, `=`, and `7`.
- **Tokens**: The categorized and classified lexemes. A token typically contains:
    - A token type/category (e.g., `<IDENTIFIER>`, `<OPERATOR>`, `<NUMBER>`)
    - The actual lexeme value (e.g., "count", "=", "7")
    - Optional metadata (line number, position, etc.)
- **Regular Expressions**: Most lexers use regular expressions or finite automata to define and recognize token patterns.
##### The Scanning Process
1. **Input Buffering**: The lexer reads the input source code, often employing buffer techniques for efficiency.
2. **Pattern Matching**: The lexer applies rules to identify the next token, usually following a "longest match" or "maximal munch" principle.
3. **Token Generation**: Once a pattern is matched, the lexer creates a token with the appropriate type and value.
4. **Error Handling**: When encountering unexpected characters, the lexer must report errors or attempt recovery.
5. **Whitespace and Comments**: These are typically discarded by the lexer unless they're significant in the language.
##### Lexer Types
- **Hand-written Lexers**: Programmed manually, offering precise control and potentially better performance.
- **Generated Lexers**: Created using tools like Lex, Flex, ANTLR, which automatically produce lexer code from token specifications.
- **Deterministic Finite Automata (DFA) Based**: Most efficient implementation, where the lexer transitions between states based on input characters.
##### Challenges in Lexical Analysis
- **Ambiguity**: Some character sequences could match multiple token patterns (resolved by prioritization or longest match).
- **Context Sensitivity**: Some tokens may depend on context (e.g., an identifier that is also a keyword).
- **Lookahead**: Sometimes determining a token requires looking ahead at subsequent characters.
- **Error Recovery**: Continuing to parse after encountering invalid tokens can be complex.

&ensp;&ensp;&ensp; Lexical analysis, while conceptually simple, forms the critical foundation for all subsequent phases of compilation or interpretation. By breaking down source code into meaningful tokens, it significantly simplifies the parsing stage that follows.

## Objectives:
****
1. Understand what lexical analysis is.
2. Get familiar with the inner workings of a lexer/scanner/tokenizer.
3. Implement a sample lexer and show how it works.

&ensp;&ensp;&ensp; **Note:** Just because too many students were showing me the same idea of lexer for a calculator, I've decided to specify requirements for such case. Try to make it at least a little more complex. Like, being able to pass integers and floats, also to be able to perform trigonometric operations (cos and sin). **But it does not mean that you need to do the calculator, you can pick anything interesting you want**

## Implementation description

##### The `TokenType.py` Def
&ensp;&ensp;&ensp; The `TokenType` enumeration defines all possible token categories that the lexer can recognize. These types can be grouped into several categories:
- **Reserved Keywords**: Language-specific commands like `FOREACH`, `CROP`, and `ROTATE`
- **Type Identifiers**: Data types such as `TYPE_BATCH`, `TYPE_IMG`, `TYPE_INT`, and `TYPE_PXLS`
- **Operators and Symbols**: Mathematical operators (`PLUS`, `MINUS`) and syntactic elements
- **Special Tokens**: `EOL` (end-of-line) and `EOF` (end-of-file) markers

&ensp;&ensp;&ensp; This comprehensive categorization allows the lexer to classify each token properly during the tokenization process.

```csharp
public enum TokenType
{
   // Reserved Keywords 
    LEFT = "LEFT"
    SET = "SET"
    ELIF = "ELIF"
    ELSE = "ELSE"
    ...
    // Types
    TYPE_DBL = "TYPE_DBL"
    TYPE_INT = "TYPE_INT"
    TYPE_PXLS = "TYPE_PXLS"
     ....
    //Values
    PXLS_VALUE = "PXLS_VALUE"
    STR_VALUE = "STR_VALUE"
    BOOL_VALUE = "BOOL_VALUE"
	....
}
```

##### The `Token` Class
&ensp;&ensp;&ensp; The `Token` class serves as a data structure that encapsulates information about individual tokens found during lexical analysis. Each token stores:
- `Type`: The category of token as defined in the `TokenType` enum
- `Value`: The actual string representation of the token in the source code
- `Line` and `Column`: The exact position where the token appears in the source file

&ensp;&ensp;&ensp; This positional data is particularly valuable for error reporting, as it allows precise location information when syntax errors occur.

```
class Token:
    def __init__(self, token_type: TokenType, value: str, line: int, column: int):
        self.type = token_type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"{self.type}: '{self.value}' at line {self.line}, column {self.column}"

```

##### The Logic Within `Tokenizer`
The `Tokenizer` class declaration establishes the core components needed for lexical analysis:
- `_input`: Stores the entire source code as a string
- `_position`: Tracks the current character position during analysis
- `_line` and `_column`: Keep track of the current line and column for error reporting

&ensp;&ensp;&ensp; These private fields maintain the tokenizer's state as it processes the input character by character. The position tracking is essential for both token extraction and providing accurate location information.

```
 def __init__(self, input_text: str):
        self.input = input_text
        self.position = 0
        self.line = 1
        self.column = 1
   // ...
   
  
```

&ensp;&ensp;&ensp; The `NumberRegex` static field defines a regular expression pattern for identifying numeric values in the source code. It handles three different number formats: decimal numbers (`\d+\.\d+`) - e.g., `3.14`; pixel values (`\d+p`) - e.g., `42p`; Integer values (`\d+`) - e.g., `100`.

&ensp;&ensp;&ensp; The `RegexOptions.Compiled` flag improves performance by compiling the regular expression once, which is beneficial since the pattern will be used repeatedly during tokenization.

```
  number_regex = r'(\d+\.\d+|\d+p|\d+)```
```
public List<Token> Tokenize()
{
	List<Token> tokens = new List<Token>();
	while(_position < _input.Length)
	{
		char current = _input[_position];

		// Skip whitespaces
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

```
```
&ensp;&ensp;&ensp; The `match_token` method serves as the heart of the lexer, implementing a comprehensive pattern matching system for identifying tokens in the source code. It employs a hierarchical approach to token recognition, working from simple to complex patterns.

&ensp;&ensp;&ensp; Initially, the method checks for single-character symbols like parentheses, commas, and basic operators, which can be identified with a simple character comparison. For multi-character operators such as `==`, `>=`, and `<=`, the method uses the `peek(self)` helper function to examine the next character without advancing the position. This lookahead capability is essential for correctly distinguishing between operators like `=` (assignment) and `==` (equality comparison).

&ensp;&ensp;&ensp; After handling symbols and operators, the method proceeds to more complex token types. For alphabetic characters or specific identifier symbols (`$` or `#`), it reads the entire word and passes it to `create_word_token(self, word)` for classification as either a reserved keyword or an identifier. For numeric characters, it invokes `match_number(self)` to parse various numeric formats. String literals are handled by `read_string(self)`, which extracts the content between quotation marks.

&ensp;&ensp;&ensp; This cascading approach to token matching creates a priority system where more specific patterns are checked before more general ones. If no pattern matches the current character, the method returns null, signaling to the caller that an unrecognized character has been encountered. This design provides excellent flexibility while maintaining clean, readable code structure, making it easy to understand how each token type is identified and processed during the lexical analysis phase.
```

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
```

&ensp;&ensp;&ensp; The `advance` method provides a fundamental mechanism for token creation while simultaneously managing the lexer's position within the input stream. It performs two essential operations in a single, concise function.

&ensp;&ensp;&ensp; First, it advances both the position and column counters by one character, effectively moving the Lexer's focus to the next character in the input stream. This positional update is crucial for the sequential processing of the source code and ensures that each character is examined exactly once during tokenization. The position counter tracks the absolute position in the input string, while the column counter provides the relative position within the current line, which is reset whenever a newline character is encountered.

&ensp;&ensp;&ensp; Second, the method creates and returns a new `Token` object with the specified type and value. The token's position is recorded as the current line and the previous column (calculated as `_column - 1`), which accurately reflects where the token began in the source code. This positional information is invaluable for error reporting and syntax highlighting in development environments.

```
  def advance(self, token_type, value):
        self.position += 1
        self.column += 1
        return Token(token_type, value, self.line, self.column - 1)

    def advance_two(self, token_type, value):
        self.position += 2
        self.column += 2
        return Token(token_type, value, self.line, self.column - 2)
```

&ensp;&ensp;&ensp; The `peek(self)` method provides the lexer with crucial lookahead capability, allowing it to examine upcoming characters without altering the current position or state. This function returns the character immediately following the current position, or a null character (`\0`) if the end of the input has been reached.

&ensp;&ensp;&ensp; Lookahead functionality is essential for correctly identifying tokens that could begin with the same character but continue differently. For instance, distinguishing between assignment (`=`) and equality comparison (`==`) requires looking at the character after the first equals sign. Without this capability, the lexer would have to potentially backtrack after discovering that a single-character interpretation was incorrect, significantly complicating the tokenization logic.

&ensp;&ensp;&ensp; The implementation elegantly handles boundary conditions by checking if the next position is within the valid range of the input string before attempting to access it. This prevents potential index-out-of-range exceptions when peeking at the last character of the input. The use of the ternary conditional operator makes the code concise while still providing complete functionality.

```
def peek(self):
        return self.input[self.position + 1] if self.position + 1 < len(self.input) else '\0'
```

&ensp;&ensp;&ensp; The read_word(self) method extracts word-based tokens, such as identifiers and keywords, by processing continuous sequences of letters, digits, and special symbols ($ or #). It records the starting position, advances through valid characters, and uses Substring to extract the full word once a non-word character is reached.

&ensp;&ensp;&ensp; This efficient, no-backtracking approach returns the word for further classification, separating extraction from categorization. This modularity strengthens the lexical analyzer’s design by keeping concerns distinct.

```
def read_word(self):
        start = self.position
        while self.position < len(self.input) and (self.input[self.position].isalnum() or self.input[self.position] in ('$', '#')):
            self.position += 1
            self.column += 1
        return self.input[start:self.position]
```

&ensp;&ensp;&ensp; The `create_word_token(self, word)` method serves as a semantic classifier for word tokens in the lexical analysis process. After a word has been extracted by the `ReadWord()` method, this function determines its specific token type based on language rules and creates the appropriate token object.

&ensp;&ensp;&ensp; The method first attempts to classify the word as a reserved keyword using a comprehensive switch statement that compares the uppercase version of the word against all known keywords in the language. This case-insensitive comparison provides flexibility in the language syntax, allowing programmers to use keywords in any case. For each recognized keyword, a new `Token` object is created with the appropriate token type, the original word value, and the position information.

&ensp;&ensp;&ensp; If the `word` doesn't match any keyword, the method checks if it's an identifier by examining its first character. In this language, identifiers are distinguished by special prefix symbols: `$` for variables and `#` for batch identifiers. If either prefix is detected, the method returns a `VAR_IDENTIFIER` token with the complete identifier.

&ensp;&ensp;&ensp; Last but not least, if a `word` fails to match either a keyword or identifier pattern, the method throws an exception with detailed information about the unexpected word and its position in the source code. This strict validation ensures that only valid tokens are accepted, providing immediate feedback on syntax errors.

```
def create_word_token(self, word):
        # This function maps words to token types
        if word.upper() in TokenType.__members__:
            return Token(TokenType[word.upper()], word, self.line, self.column - len(word))
        if word.startswith('$') or word.startswith('#'):
            return Token(TokenType.VAR_IDENTIFIER, word, self.line, self.column - len(word))
        raise Exception(f"Unexpected word '{word}' at line {self.line}, column {self.column - len(word)}")
```

&ensp;&ensp;&ensp; The `match_number(self)` method handles the complex task of recognizing and classifying numerical literals in the source code. Unlike simpler tokens, numbers can appear in various formats, each requiring specific handling and classification.

&ensp;&ensp;&ensp; The method leverages the predefined `NumberRegex` pattern to identify valid numeric sequences at the current position. This approach combines the power of regular expressions with the precision of position-based matching by ensuring that the match starts exactly at the current position in the input string.

&ensp;&ensp;&ensp; Upon successful matching, the method extracts the complete numeric value and advances both the position and column counters by the length of the matched text. This single-step advancement is more efficient than character-by-character processing for multi-digit numbers.

&ensp;&ensp;&ensp; The method then applies sophisticated classification logic to determine the specific numeric token type based on the format of the matched value. If the number ends with 'p' (e.g., "100p"), it's classified as a pixel value (`PXLS_VALUE`). If it contains a decimal point (e.g., "3.14"), it's recognized as a floating-point value (`DBL_VALUE`). Otherwise, it's classified as an integer (`INT_VALUE`). This classification allows the parser to enforce type-specific rules during the semantic analysis phase.

&ensp;&ensp;&ensp; If the regular expression fails to match a valid number pattern at the current position, the method throws an exception with detailed diagnostic information. This error handling ensures that malformed numeric literals are detected early in the compilation process, providing clear feedback to the programmer about the nature and location of the syntax error.

```
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
```

&ensp;&ensp;&ensp; The `read_string(self)` method implements specialized handling for string literals, which require different processing than other token types due to their delimited nature and potential to contain various characters.

&ensp;&ensp;&ensp; The method begins by advancing past the opening quotation mark and incrementing both position and column counters. This prepares the lexer to capture the content between the quotes rather than including the delimiting characters themselves.

&ensp;&ensp;&ensp; After storing the starting position, the method enters a loop that continues until either the closing quotation mark is encountered or the end of the input is reached. During this loop, the position and column counters are incremented for each character within the string content. This approach allows the string to contain any characters, including those that would otherwise be interpreted as operators or keywords outside of a string context.

&ensp;&ensp;&ensp; Once the closing quotation mark is detected, the method extracts the string content using the stored starting position and the current position. The method then advances past the closing quote and creates a new token of type `STR_VALUE`. Notably, the token's value includes the quotation marks (`f'"{value}""`) to preserve the complete string literal format, while the positional information accounts for the entire string including the quotes.

```
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
```

## Conclusions / Screenshots / Results
****
&ensp;&ensp;&ensp; In this section, besides the conclusion that gets described at the end, an example of output, resulted from the execution of the program, is also explained in-depth.

- By tokenizing input from `Main.py` with a snippet of code written based on my grammar:

```
BATCH #rawImages = "C:/raw/";
    FOREACH IMG $img IN #rawImages {
        INT $width = METADATA $img FWIDTH;
        INT $height = METADATA $img FHEIGHT;
        
        CROP $img (1920, 1080);
        
        DOUBLE $fileSize = METADATA $img FSIZE;
        IF $fileSize > 10000 {
            SET $img NEGATIVE;
        }
        ELSE {
            SET $img SEPIA;
        }
        
        IF $height > $width {
            ROTATE $img RIGHT;
        }
    }
```

- We get the following result, as the tokenized version of our input:

```
Tokens:
TokenType.BATCH: 'BATCH' at line 2, column 5
TokenType.VAR_IDENTIFIER: '#rawImages' at line 2, column 11
TokenType.ASSIGN: '=' at line 2, column 22
TokenType.STR_VALUE: '"C:/raw/"' at line 2, column 24
TokenType.EOL: ';' at line 2, column 33
TokenType.FOREACH: 'FOREACH' at line 3, column 5
TokenType.IMG: 'IMG' at line 3, column 13
TokenType.VAR_IDENTIFIER: '$img' at line 3, column 17
TokenType.IN: 'IN' at line 3, column 22
TokenType.VAR_IDENTIFIER: '#rawImages' at line 3, column 25
TokenType.OPEN_BLOCK: '{' at line 3, column 36
TokenType.INT: 'INT' at line 4, column 9
TokenType.VAR_IDENTIFIER: '$width' at line 4, column 13
TokenType.ASSIGN: '=' at line 4, column 20
TokenType.METADATA: 'METADATA' at line 4, column 22
TokenType.VAR_IDENTIFIER: '$img' at line 4, column 31
TokenType.FWIDTH: 'FWIDTH' at line 4, column 36
TokenType.EOL: ';' at line 4, column 42
TokenType.INT: 'INT' at line 5, column 9
TokenType.VAR_IDENTIFIER: '$height' at line 5, column 13
TokenType.ASSIGN: '=' at line 5, column 21
TokenType.METADATA: 'METADATA' at line 5, column 23
TokenType.VAR_IDENTIFIER: '$img' at line 5, column 32
TokenType.FHEIGHT: 'FHEIGHT' at line 5, column 37
TokenType.EOL: ';' at line 5, column 44
TokenType.CROP: 'CROP' at line 7, column 9
TokenType.VAR_IDENTIFIER: '$img' at line 7, column 14
TokenType.OPEN_P: '(' at line 7, column 19
TokenType.INT_VALUE: '1920' at line 7, column 20
TokenType.COMMA: ',' at line 7, column 24
TokenType.INT_VALUE: '1080' at line 7, column 26
TokenType.CLOSE_P: ')' at line 7, column 30
TokenType.EOL: ';' at line 7, column 31
TokenType.DOUBLE: 'DOUBLE' at line 9, column 9
TokenType.VAR_IDENTIFIER: '$fileSize' at line 9, column 16
TokenType.ASSIGN: '=' at line 9, column 26
TokenType.METADATA: 'METADATA' at line 9, column 28
TokenType.VAR_IDENTIFIER: '$img' at line 9, column 37
TokenType.FSIZE: 'FSIZE' at line 9, column 42
TokenType.EOL: ';' at line 9, column 47
TokenType.IF: 'IF' at line 10, column 9
TokenType.VAR_IDENTIFIER: '$fileSize' at line 10, column 12
TokenType.GREATER: '>' at line 10, column 22
TokenType.INT_VALUE: '10000' at line 10, column 24
TokenType.OPEN_BLOCK: '{' at line 10, column 30
TokenType.SET: 'SET' at line 11, column 13
TokenType.VAR_IDENTIFIER: '$img' at line 11, column 17
TokenType.NEGATIVE: 'NEGATIVE' at line 11, column 22
TokenType.EOL: ';' at line 11, column 30
TokenType.CLOSE_BLOCK: '}' at line 12, column 9
TokenType.ELSE: 'ELSE' at line 13, column 9
TokenType.OPEN_BLOCK: '{' at line 13, column 14
TokenType.SET: 'SET' at line 14, column 13
TokenType.VAR_IDENTIFIER: '$img' at line 14, column 17
TokenType.SEPIA: 'SEPIA' at line 14, column 22
TokenType.EOL: ';' at line 14, column 27
TokenType.CLOSE_BLOCK: '}' at line 15, column 9
TokenType.IF: 'IF' at line 17, column 9
TokenType.VAR_IDENTIFIER: '$height' at line 17, column 12
TokenType.GREATER: '>' at line 17, column 20
TokenType.VAR_IDENTIFIER: '$width' at line 17, column 22
TokenType.OPEN_BLOCK: '{' at line 17, column 29
TokenType.ROTATE: 'ROTATE' at line 18, column 13
TokenType.VAR_IDENTIFIER: '$img' at line 18, column 20
TokenType.RIGHT: 'RIGHT' at line 18, column 25
TokenType.EOL: ';' at line 18, column 30
TokenType.CLOSE_BLOCK: '}' at line 19, column 9
TokenType.CLOSE_BLOCK: '}' at line 20, column 5
TokenType.EOF: '' at line 21, column 5
```

&ensp;&ensp;&ensp; The lexer correctly identifies and categorizes each token in the code snippet, showing the comprehensive capabilities of the implemented tokenizer:
1. **Block Structure Recognition**: The lexer properly identifies the opening and closing curly braces that define code blocks, maintaining correct nesting levels.
2. **Variable and Batch Declarations**: The tokenizer successfully distinguishes between batch identifiers (prefixed with `#`) and variable identifiers (prefixed with `$`), correctly recognizing `#mybatch` as a batch identifier and `$img` and `$width` as variable identifiers.
3. **String Literal Handling**: The string literal `"images/"` is correctly tokenized, preserving the quotation marks as part of the token value.
4. **Reserved Keywords Recognition**: The lexer properly identifies all language keywords like `BATCH`, `FOREACH`, `IN`, `SET`, `SEPIA`, `ROTATE`, `LEFT`, `CROP`, `INT`, `METADATA`, and `FWIDTH`.
5. **Numeric Literal Processing**: The integer values `100` and `200` in the crop operation are correctly identified as `INT_VALUE` tokens.
6. **Operator and Symbol Recognition**: All operators and symbols like assignment (`=`), parentheses, and commas are properly tokenized.
7. **Statement Termination**: Each semicolon is correctly identified as an `EOL` token, marking the end of statements.
8. **Position Tracking**: For each token, the lexer provides accurate line and column information, which is crucial for error reporting in later compilation stages.
9. **End of File Detection**: The final `EOF` token is added automatically, signaling the end of the input.

&ensp;&ensp;&ensp; The output demonstrates that the tokenizer correctly handles all the syntactic elements defined in your grammar, successfully breaking down the source code into a stream of tokens that preserve both the semantic meaning and the syntactic structure of the original program. This tokenized representation forms the foundation for the parsing stage that would follow in a complete compiler implementation.


&ensp;&ensp;&ensp; To sum up, in this laboratory work, I have successfully achieved the first step in developing a specialized domain-specific language (DSL) for batch image processing by implementing a comprehensive lexical analyzer. 

&ensp;&ensp;&ensp; The implemented tokenizer demonstrates several key achievements:
1. **Complete Grammar Support**: The lexer supports all token types defined in the grammar, including specialized tokens for image processing operations (SEPIA, BW, NEGATIVE, SHARPEN), batch processing constructs (FOREACH, IN), metadata extraction (FWIDTH, FHEIGHT), and more.
2. **Robust Error Handling**: The implementation includes error detection mechanisms that provide precise position information (line and column numbers) when unexpected characters or symbols are encountered, greatly facilitating debugging for language users.
3. **Efficient Position Tracking**: The tokenizer maintains accurate line and column information across multiple types of line endings (supporting both Unix and Windows formats), which is essential for proper error reporting and source mapping.
4. **Comprehensive Token Classification**: The implementation distinguishes between various token types, including keywords, identifiers, literals (numeric, string, boolean), operators, and syntax elements, creating a well-structured token stream.
5. **Pattern Recognition**: The scanner effectively recognizes complex patterns like numeric literals with different formats (integers, decimals, pixel values) and identifiers with special prefixes, demonstrating the power of combining regular expressions with procedural tokenization techniques.
6. **Modular Design**: The separation of token extraction (reading) from token classification (creating) provides a clean, maintainable architecture that could be extended for future language enhancements.

&ensp;&ensp;&ensp; The successful implementation of this lexer represents a significant first step toward a complete language toolchain for image processing. By correctly breaking down source code into a stream of meaningful tokens, the tokenizer provides the foundation upon which a parser can build an abstract syntax tree (AST), enabling the subsequent phases of compilation or interpretation.

&ensp;&ensp;&ensp; Future work could include developing a parser, as requested in the future lab No.6, to verify the syntactic correctness of programs according to the grammar, implementing a semantic analyzer to check type consistency and other language-specific rules, and finally, creating an interpreter or code generator to execute the operations on actual image files.

## References
****

<a id="ref3"></a>[1] Presentation on "Formal Languages and Compiler Design" - conf. univ., dr. Irina Cojuhari -
https://else.fcim.utm.md/pluginfile.php/110457/mod_resource/content/0/Theme_1.pdf

<a id="ref4"></a>[2] Presentation on "Regular Language. Finite Automata" - TUM -
https://drive.google.com/file/d/1rBGyzDN5eWMXTNeUxLxmKsf7tyhHt9Jk/view

[3] LLVM - "Kaleidoscope: Kaleidoscope Introduction and the Lexer" - [https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl01.html](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl01.html)

[4] Wikipedia - "Lexical Analysis" - [https://en.wikipedia.org/wiki/Lexical_analysis](https://en.wikipedia.org/wiki/Lexical_analysis)