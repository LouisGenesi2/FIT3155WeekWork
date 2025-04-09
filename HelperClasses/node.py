from .CharTable import CharTable
class Edge:
    def __init__(self, value, dest):
        self.value = value
        self.dest = dest

class Node:
    def __init__(self, is_leaf: bool, value: str):
        self.is_leaf = is_leaf
        self.value = value

class CharNode(Node):
    """ Tree implemented with CharTable as children for O(1) lookup
        of children
    """
    def __init(self, is_leaf: bool, value: str):
        super().__init__(is_leaf=is_leaf, value=value)
        self.array = CharTable()

class BinaryNode(Node):
    def __init__(self, is_leaf: bool, value: str):
        super().__init__(is_leaf=is_leaf, value=value)
        self.left = None
        self.right = None
    
    def set_left_edge(self, dest):
        self.left = dest
    
    def set_right_edge(self, dest):
        self.right = dest
    
    def get_left_edge(self):
        return self.left
    
    def get_right_edge(self):
        return self.right
    
    def get_value(self):
        return self.value

    def is_leaf(self):
        return self.is_leaf
