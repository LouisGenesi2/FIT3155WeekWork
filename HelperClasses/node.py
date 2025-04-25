from CharTable import CharTable



class Node:
    def __init__(self, is_leaf: bool, value: str = ''):
        self.is_leaf = is_leaf
        self.value = value

class UkkonenEdge:
    def __init__(self, value: tuple[int, int], dest, string_id: int):
        self.value = value
        self.dest = dest
        self.string_id = string_id

    def _update_end_value(self, value: int):
        old_end_value = self.value[1]
        self.value = (self.value[0], value)
        return old_end_value

    def _change_dest(self, new_dest: 'CharNode') -> 'CharNode':
        """ Returns old destination
        """
        old_dest = self.dest
        self.dest = new_dest
        return old_dest
    
    def get_values(self) -> tuple[int, int]:
        return self.value
        
    def change_end_value(self, new_value: int) -> int:
        old_value = self.value[1]
        self.value = (self.value[0], new_value)
        return old_value

    def insert_internal_node(self, insert_at: int, new_node: 'CharNode') -> 'CharNode':
        self._update_end_value(insert_at)
        return self._change_dest(new_node)
    
    def traverse_edge(self) -> 'CharNode':
        return self.dest

    def get_length(self) -> int:
        return self.value[1] - self.value[0]

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
    
class SuffixLink(UkkonenEdge):
    def __init__(self, dest: 'CharNode'):
        self.dest: 'CharNode' = dest
    
    def traverse(self) -> 'CharNode':
        return self.dest

class CharNode(Node):
    """ Tree implemented with CharTable as children for O(1) lookup
        of children
    """
    def __init__(self) -> None:
        self.array: CharTable[UkkonenEdge] = CharTable()
        self.suffix_link: SuffixLink|None = None
    
    def get_edge(self, direction: str) -> UkkonenEdge:
        return self.array[direction]

    def add_suffix_link(self, dest: 'CharNode') -> None:
        self.suffix_link = SuffixLink(dest)

    def has_suffix_link(self) -> bool:
        return isinstance(self.suffix_link, SuffixLink)
    
    def get_UkkonenEdge(self, letter: str) -> UkkonenEdge:
        return self.array[letter]


    def add_UkkonenEdge(self, letter: str, value: tuple[int, int], dest: Node, string_id: int) -> None:
        self.array[letter] = UkkonenEdge(value, dest, string_id)

    def __getitem__(self, item: str) -> UkkonenEdge:
        return self.array[item]