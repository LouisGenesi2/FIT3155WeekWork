import os
from collections import Iterator

class BinaryNode:
    def __init__(self, is_leaf: bool, value: str):
        self.is_leaf = is_leaf
        self.value = value
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

class CharTable:
    ascii_min = 0
    ascii_max = 127
    
    def __init__(self):
        self.array = [0 for _ in range(128)]
        self.ascii_range = 0
    
    def _get_char_index(self, char):
        return ord(char)
    
    def __getitem__(self, char) -> str:
        return self.array[self._get_char_index(char)]

    def __setitem__(self, char):
        self.array[self._get_char_index(char)]


class CharFreqTable(CharTable):

    def add_char(self, char):
        self[char] = self[char] + 1
    
    def get_sorted(self):
        return SortedCharFreqTable(self.array)

class SortedCharFreqTable(Iterator):
    def __init__(self, array: list):
        map(lambda idx, val: (val, ord(idx)), enumerate(array))
        array.sort(key=lambda tuple: tuple[0])
        self.array: list[tuple[int, str]] = array
    
    def pop_max(self) -> tuple[int,str]:
        self.array.pop()
    
    def next(self):
        for _ in range(len(self.array)):
            self.pop_max()
        raise StopIteration

def file_to_char_table(file: os.PathLike) -> CharFreqTable:

    # read characters, incrementing at frequency
    with open(file, mode='r') as f:
        char_table = CharFreqTable()
        for line in f:
            for char in line:
                char_table.add_char(char)
    
    return char_table

def str_to_char_freq_table(string: str) -> CharFreqTable:
    char_table = CharFreqTable()
    for char in string:
        char_table.add_char(char)

    return char_table

def char_table_to_huffman_tree(char_table: CharFreqTable) -> BinaryNode:
    frequencies = char_table.get_sorted()

    # create tree from most frequent to least
    codes_tree_root = BinaryNode()
    active_node: BinaryNode = codes_tree_root
    for character in frequencies:
        new_node = BinaryNode(is_leaf=True, value=character) # left/char node
        next_node = BinaryNode(is_leaf=False, value='internal') # next internal node
        active_node.set_left_edge(new_node)
        active_node.set_right_edge(next_node)
        active_node=next_node

    return codes_tree_root

def get_codes(root_node: BinaryNode) -> CharTable:
    codes_table = CharTable()

    curr_node = root_node
    string_builder = ""
    while curr_node.is_leaf() is not True:
        returned_char = curr_node.get_left_edge().get_value()
        returned_char_code = string_builder + '1'

        codes_table[returned_char] = returned_char_code

        curr_node = curr_node.get_right_edge()
        string_builder += '0'

    # do final one
    codes_table[curr_node.get_value()] = string_builder + '1'

    return codes_table

def encode_elias(string: str) -> str:
    frequencies = str_to_char_freq_table(string)
    codes_table = get_codes(char_table_to_huffman_tree(frequencies))
    encoded_string = ""
    for char in string:
        encoded_string += codes_table[char]

def add_lengths_to_code(code: str) -> str:
    string_builder = code
    length = len(code) - 1
    while length >= 1:
        encoded_length = str_to_bin(length)
        string_builder =  encoded_length + string_builder
        length = len(encoded_length) - 1
    
    return string_builder



def str_to_bin(integer: int) -> str:
    "{0:b}".format(integer)

