from lab4.regex_node import RegexNodeType

class RegexGenerator:
    def __init__(self, regex_parser, repetition_limit=5):
        self.repetition_limit = repetition_limit
        self.regex_parser = regex_parser

    def generate_valid_combinations(self, pattern, max_combinations=40):
        root_node = self.regex_parser.parse_regex(pattern)
        results = self.generate_combinations_from_node(root_node)

        # Limit the number of combinations generated
        return results[:max_combinations]

    def generate_combinations_from_node(self, node):
        results = []

        if node.type == RegexNodeType.LITERAL:
            results.append(node.value)

        elif node.type == RegexNodeType.ALTERNATION:
            for child in node.children:
                results.extend(self.generate_combinations_from_node(child))

        elif node.type == RegexNodeType.CONCATENATION:
            results.append("")
            for child in node.children:
                child_combos = self.generate_combinations_from_node(child)
                new_results = []
                for existing_result in results:
                    for child_combo in child_combos:
                        new_results.append(existing_result + child_combo)
                results = new_results

        elif node.type == RegexNodeType.REPETITION:
            base_results = self.generate_combinations_from_node(node.children[0])
            results.append("")  # For empty case like * or ?

            if node.min_repeat == 0 and node.max_repeat == 1:  # ? (0 or 1)
                results.extend(base_results)
            elif node.min_repeat == 1 and node.max_repeat == -1:  # + (1 or more)
                for count in range(1, self.repetition_limit + 1):
                    combinations = self.generate_repetitions(base_results, count)
                    results.extend(combinations)
                results.pop(0)  # Remove empty case for + operator
            elif node.min_repeat == 0 and node.max_repeat == -1:  # * (0 or more)
                for count in range(1, self.repetition_limit + 1):
                    combinations = self.generate_repetitions(base_results, count)
                    results.extend(combinations)
            else:  # {n} or {n,m}
                max_repeat = self.repetition_limit if node.max_repeat == -1 else min(node.max_repeat, self.repetition_limit)
                for count in range(node.min_repeat, max_repeat + 1):
                    combinations = self.generate_repetitions(base_results, count)
                    results.extend(combinations)
                if node.min_repeat > 0:
                    results.pop(0)  # Remove empty case for {n,m} where n > 0

        return results

    def generate_repetitions(self, base_strings, count):
        if count == 0:
            return [""]
        if count == 1:
            return base_strings[:]

        result = []
        sub_results = self.generate_repetitions(base_strings, count - 1)
        for sub_result in sub_results:
            for base_str in base_strings:
                result.append(sub_result + base_str)

        return result
