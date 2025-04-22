from .GlobalInt import GlobalInt
from .node import CharNode, UkkonenEdge
import typing


class UkkonenTree:
    def __init__(self, string: str):
        # initialise root
        self.root: 'CharNode' = CharNode()
        self.root.add_suffix_link(self.root)
        
        self._global_int = 0
        self._active_node = self.root
        self._pending: 'CharNode'|None = None
        self._remainder: tuple[int, int]
        self._curr_extension = 0
        self._curr_phase = 0
        
        self.string = string
        


        self._construct_tree()


    def _construct_tree(self):
        pass
    
    def _do_phase(self):
        pass

    def _do_extension(self) -> typing.Literal['r1', 'r2', 'r3']:
        pass

    def _rule_1(self):
        self.global_int += 1
        self._increment_extension()

    def _rule_2(self):
        curr_edge = self._active_node[self._get_letter(self._curr_extension)]
        self._insert_internal_node()

    def _rule_3(self):
        pass

    def _follow_suffix_link(self):
        if self._active_node is self.root:
            self._decrement_remainder()
        self._active_node = self._active_node.suffix_link.traverse()

    def _decrement_remainder(self, amt: int):
        if self._remainder is None:
            raise Exception('Decrementing remainder when remainder is None')
        self._remainder[0] += amt
        if self._remainder[0] > self._reminader[1]:
            self._remainder = None


    def _traverse_remainder(self) -> UkkonenEdge:
        self._update_active_node_w_remainder()
    
        return self._active_node[self._get_remainder_letter()]

    def _traverse_all(self):
        """ traverses remainder and extension/phase to relevant edge
        """
        self._traverse_remainder()

    def _skip_count(self):
        pass

    def _update_active_node_w_remainder(self):
        while self._active_node[self._get_remainder_letter()].get_length() < self._get_remainder_length():
            edge = self._active_node[self._get_remainder_letter()]
            next_node = edge.traverse_edge()
            
            self._active_node = next_node
            amt_traversed = edge.get_length()
            self._decrement_remainder(amt_traversed)

    def _get_remainder_letter(self) -> str:
        if self._remainder is None:
            return 0
        return self._get_letter(self._remainder[0])

    def _get_remainder_length(self) -> int:
        return self._remainder[1] - self._remainder[0]

    def _get_letter(self, idx: int) -> str:
        return self.string[idx]

    def _get_ext_letter(self) -> str:
        return self._get_letter(self._curr_extension)

    def _increment_extension(self):
        self._curr_extension += 1

    def _increment_phase(self):
        self._curr_phase += 1

    def _insert_internal_node(self, edge: UkkonenEdge, pos: int) -> CharNode:
         
        new_node = CharNode()
        node2 = edge._change_dest(new_node)     # old destination
        old_val = edge.change_end_value(pos)    # value before old dest
        new_node.add_UkkonenEdge(self._get_letter(pos + 1), (pos + 1, old_val), node2)