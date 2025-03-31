from lab4.regex_node import RegexNodeType

class RegexTreePrinter:
    @staticmethod
    def print_tree(node, depth=0):
        indent = ' ' * (depth * 2)

        if node.type == RegexNodeType.LITERAL:
            print(f"{indent}Literal: '{node.value}'")
        elif node.type == RegexNodeType.ALTERNATION:
            print(f"{indent}Alternation:")
            for child in node.children:
                RegexTreePrinter.print_tree(child, depth + 1)
        elif node.type == RegexNodeType.CONCATENATION:
            print(f"{indent}Concatenation:")
            for child in node.children:
                RegexTreePrinter.print_tree(child, depth + 1)
        elif node.type == RegexNodeType.REPETITION:
            rep_info = f"{node.min_repeat} to " + ("∞" if node.max_repeat == -1 else str(node.max_repeat))
            print(f"{indent}Repetition ({rep_info}):")
            for child in node.children:
                RegexTreePrinter.print_tree(child, depth + 1)
