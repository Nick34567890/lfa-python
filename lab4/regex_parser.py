from lab4.regex_node import RegexNode, RegexNodeType


class RegexParser:
    def parse_regex(self, pattern):
        position = 0
        ast, _ = self.parse_expression(pattern, position)
        return ast

    def parse_expression(self, pattern, position):
        concat_node = RegexNode(RegexNodeType.CONCATENATION)

        while position < len(pattern):
            current_char = pattern[position]

            if current_char == ')':  # Closing parenthesis indicates end of group
                return concat_node, position  # Return the current concatenation node and position

            if current_char == '|':  # Alternation (|) symbol
                position += 1
                alternation_node = RegexNode(RegexNodeType.ALTERNATION)
                alternation_node.children.append(concat_node)
                next_node, position = self.parse_expression(pattern, position)  # Handle alternation
                alternation_node.children.append(next_node)
                return alternation_node, position  # Return the alternation node and updated position

            term_node, position = self.parse_term(pattern, position)
            concat_node.children.append(term_node)

        return concat_node, position

    def parse_term(self, pattern, position):
        current_char = pattern[position]
        base_node = None

        if current_char == '(':  # Handle subexpressions with '('
            position += 1  # Skip '('
            base_node, position = self.parse_expression(pattern, position)  # Parse inner expression

            if position < len(pattern) and pattern[position] == ')':
                position += 1  # Skip closing ')'
            else:
                raise ValueError("Expected closing parenthesis ')'")

        else:  # Handle literal characters
            base_node = RegexNode(RegexNodeType.LITERAL)
            base_node.value = current_char
            position += 1

        # Handle repetition operators +, *, ?, {n,m}
        if position < len(pattern):
            next_char = pattern[position]
            if next_char == '+':
                position += 1
                return self.create_repetition_node(base_node, 1, -1), position  # 1 or more repetitions
            elif next_char == '*':
                position += 1
                return self.create_repetition_node(base_node, 0, -1), position  # 0 or more repetitions
            elif next_char == '?':
                position += 1
                return self.create_repetition_node(base_node, 0, 1), position  # 0 or 1 repetitions
            elif next_char == '{':
                position += 1  # Skip '{'
                min_repeat, max_repeat, position = self.parse_repeat_range(pattern, position)
                return self.create_repetition_node(base_node, min_repeat, max_repeat), position

        return base_node, position

    def parse_repeat_range(self, pattern, position):
        min_repeat = 0
        max_repeat = 0

        # Read the minimum repeat value
        while position < len(pattern) and pattern[position].isdigit():
            min_repeat = min_repeat * 10 + int(pattern[position])
            position += 1

        if position < len(pattern) and pattern[position] == ',':
            position += 1  # Skip the comma
            # Read the maximum repeat value
            while position < len(pattern) and pattern[position].isdigit():
                max_repeat = max_repeat * 10 + int(pattern[position])
                position += 1

        if position < len(pattern) and pattern[position] == '}':
            position += 1
        else:
            raise ValueError("Expected closing '}' for repetition range")

        # Handle case where max_repeat is not provided
        if max_repeat == 0:
            max_repeat = -1  # Means unlimited repetitions

        return min_repeat, max_repeat, position

    def create_repetition_node(self, base_node, min_repeat, max_repeat):
        repetition_node = RegexNode(RegexNodeType.REPETITION)
        repetition_node.min_repeat = min_repeat
        repetition_node.max_repeat = max_repeat
        repetition_node.children.append(base_node)
        return repetition_node
