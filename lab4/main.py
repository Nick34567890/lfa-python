from lab4.regex_generator import RegexGenerator
from lab4.regex_parser import RegexParser
from lab4.regex_tree_printer import RegexTreePrinter
import re

def main():
    patterns = [
        "(a|b)(c|d)E+G?",
        "P(Q|R|S)T(UV|W|X)*Z+",
        "1(0|1)*2(3|4){5}36"
    ]

    regex_parser = RegexParser()
    regex_generator = RegexGenerator(regex_parser)

    for i, pattern in enumerate(patterns):
        print("REGEX GENERATOR:")
        print("-------------------------")
        print(f"Pattern {i + 1}: {pattern}")

        valid_combinations = regex_generator.generate_valid_combinations(pattern)
        print(f"Generated valid combinations:")
        for combo in valid_combinations:
            print(f" - {combo}")

        print(f"All combinations valid: {all(re.match(f'^{pattern}$', combo) for combo in valid_combinations)}")
        print(f"Total amount of generated symbols: {len(valid_combinations)}")

        print("\nProcessing sequence for pattern {i + 1}:")
        root_node = regex_parser.parse_regex(pattern)
        RegexTreePrinter.print_tree(root_node)
        print("\n")


if __name__ == "__main__":
    main()
