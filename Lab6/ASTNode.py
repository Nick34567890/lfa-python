# Define ASTNode class
class ASTNode:
    def __init__(self, node_type, value):
        self.node_type = node_type
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def print(self, prefix, is_tail):
        print(f"{prefix}{'└── ' if is_tail else '├── '}{self.node_type}({self.value})")
        for i in range(len(self.children)):
            self.children[i].print(prefix + ('    ' if is_tail else '│   '), i == len(self.children) - 1)