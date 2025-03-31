# regex_node.py
class RegexNodeType:
    LITERAL = 'Literal'
    ALTERNATION = 'Alternation'
    CONCATENATION = 'Concatenation'
    REPETITION = 'Repetition'


class RegexNode:
    def __init__(self, node_type):
        self.type = node_type
        self.value = ""
        self.children = []
        self.min_repeat = 0
        self.max_repeat = 0
