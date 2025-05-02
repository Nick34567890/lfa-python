from Files.Lexer import Lexer
from Files.Parser import Parser


# Main function to interact with the user
def main():
    input_text = input("Enter operation: ")
    lexer = Lexer(input_text)
    tokens = lexer.tokenize()

    parser = Parser(tokens)

    try:
        ast = parser.parse()
        ast.print("", True)
    except RuntimeError as e:
        print("Invalid expression:", e)

if __name__ == "__main__":
    main()
