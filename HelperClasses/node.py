from .CharTable import CharTable
from .GlobalInt import GlobalInt

class UkkonenEdge:
    def __init__(self, value: tuple[int, GlobalInt|int], dest):
        self.value = value
        self.dest = dest

    def _update_end_value(self, value: int):
        old_end_value = 
        self.value = (self.value[0], value)

    def _change_dest(self, new_dest: 'CharNode') -> 'CharNode':
        """ Returns old destination
        """
        old_dest = self.dest
        self.dest = new_dest
        return old_dest

    def stultify_end(self, end_value: int):
        if isinstance(self.value[1], GlobalInt):
            self.value[1] = end_value
        else:
            raise AssertionError("Only GlobalInt end should be stultified")
        
    def insert_internal_node(self, insert_at: int, new_node: 'CharNode') -> 'CharNode':
        self._update_end_value(insert_at)
        return self._change_dest(new_node)

class UkkonenTree:
    def __init__(self):
        self.root: 'CharNode' = CharNode()
        self.global_int = 0
        self.active_node = self.root
        self.pending: 'CharNode'|None = None
        self.remainder: list[int] = []


class SuffixLink(UkkonenEdge):
    def __init__(self, dest: 'CharNode'):
        self.dest: 'CharNode' = dest

class Node:
    def __init__(self, is_leaf: bool, value: str):
        self.is_leaf = is_leaf
        self.value = value

class CharNode(Node):
    """ Tree implemented with CharTable as children for O(1) lookup
        of children
    """
    def __init__(self):
        self.array: CharTable = CharTable()
        self.suffix_link: SuffixLink|None = None
    
    def get_edge(self, direction: str) -> UkkonenEdge:
        return self.array[direction]

    def has_suffix_link(self) -> bool:
        return isinstance(self.suffix_link, SuffixLink)
    
    def get_UkkonenEdge(self, letter: str) -> UkkonenEdge:
        return self.array[letter]
    
    def insert_internal_node(self, index_to_insert: int, position: int, string: str) -> 'CharNode':
        direction = string[index_to_insert]
        relevant_edge = self.get_UkkonenEdge(direction)
        new_node = CharNode()
        old_dest = relevant_edge.insert_internal_node(position, new_node)
        
        #add new edge between new node and old destination
        next_direction = string[index_to_insert + 1]
        new_node.add_UkkonenEdge(next_direction, )


    def add_UkkonenEdge(self, letter: str, value: tuple[int, GlobalInt|int], leaf_value):
        self.array[letter] = UkkonenEdge(value, Node(is_leaf=True, value=leaf_value))

class BinaryNode(Node):
    def __init__(self, is_leaf: bool, value: str):
        super().__init__(is_leaf=is_leaf, value=value)
        self.left = None
        self.right = None
    
    def set_left_UkkonenEdge(self, dest):
        self.left = dest
    
    def set_right_UkkonenEdge(self, dest):
        self.right = dest
    
    def get_left_UkkonenEdge(self):
        return self.left
    
    def get_right_UkkonenEdge(self):
        return self.right
    
    def get_value(self):
        return self.value

    def is_leaf(self):
        return self.is_leaf
