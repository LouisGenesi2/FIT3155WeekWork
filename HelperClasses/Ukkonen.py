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
        
        
        self.strings = []
        


        self._construct_tree()


    def _construct_tree(self):
        self._curr_extension = 0
        self._curr_phase = 0
        while self._curr_extension < len(self.string):

    
    def _do_phase(self):
        pass

    def _do_extension(self) -> typing.Literal['r1', 'r2', 'r3']:
        pass

    def _rule_1(self):
        self.global_int += 1
        self._increment_extension()

    def _rule_2(self, ):
        curr_string_idx = (self._curr_extension, self._curr_phase)
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

    def _traverse_all(self) -> UkkonenEdge:
        """ traverses remainder and extension/phase to relevant edge
        """
        self._traverse_remainder()


    def _skip_count(self, curr_node: CharNode, susbtr_to_travel: tuple[int, int]) -> tuple[CharNode, UkkonenEdge|None, int|None, int]:
        """ Given a starting node and substring of the string to travel along (represented by indices), 
            return the latest Node you arrive to, the Edge you stop at, what index along that edge you stop at, and the amount
            of the subtring to travel you have not travelled.
        """
        traveled_node = curr_node
        amt_traveled = 0
        amt_to_travel = susbtr_to_travel[1] - susbtr_to_travel[0]
        
        while amt_traveled < amt_to_travel:
            idx_to_travel = susbtr_to_travel[0] + amt_traveled
            edge = self._find_edge_by_idx(traveled_node, idx_to_travel)     # Travel the relevant direction
            if edge is None:                                                # Scenario where direction to travel does not yet exist
                return traveled_node, None, None, amt_to_travel - amt_traveled
            
            is_mismatch, last_idx_traveled = self._find_idx_travel_mismatch(idx_road=edge.get_values(), idx_direction=susbtr_to_travel)
            amt_traveled += last_idx_traveled - edge.get_values()[0]

            if last_idx_traveled < edge.get_values[1]:                      # scenario where entire edge is not traversed
                return traveled_node, edge, last_idx_traveled, amt_to_travel - amt_traveled
            
            traveled_node = edge.traverse_edge()
        
        return traveled_node, None, None, 0                                 # scenario with perfect travel to a node
        # TODO: Ensure that traveled node in perfect traversal includes ending leaf node instantly

    
    def _get_appropriate_rule(self, rel_node: CharNode, rel_edge: UkkonenEdge|None, rel_edge_idx: int|None, amt_left: int) -> callable[[], None]:
        if amt_left == 0:
            if rel_edge is not None:
                return self._rule_3
            if not self._check_node_has_empty_edge(rel_node):
                return self._rule_2
        return self._rule_2

    def _check_node_has_empty_edge(self, node: CharNode) -> bool:
        if node['$'] is None:
            return False
        return True
            

    def _find_edge_by_idx(self, curr_node: CharNode, idx_to_travel: int) -> UkkonenEdge|None:
        return curr_node[self._get_letter(idx_to_travel)]

        
    def _find_idx_travel_mismatch(self, idx_road: tuple[int, int], idx_direction: tuple[int,int]) -> tuple[bool, int]:
        """ Compare whether indices of the string represent equal substrings, and returns until what index of idx_road the mismatch occurs 
            idx_road should be an existing edge, and idx_direction should be the desired path.

            Returns bool (True if mismatch), and idx of road traveled to
        """
        
        _, cut_off = self._get_cutoff(idx_road, idx_direction)     # If |road| < |direction|, test only for the portion of direction that is relevant
        
        length_of_subtring = cut_off - idx_direction[0]     # length of substrings to test
        for offset in range(0, length_of_subtring):
            if self._get_letter(idx_direction[0] + offset) != self._get_letter(idx_road[0] + offset):
                return (True, idx_road[idx_road[0] + offset])       # return idx in road where mismatch occurs
            
        return (False, idx_road[0] + length_of_subtring)            

    def _get_cutoff(self, idx_road: tuple[int,int], idx_direction: tuple[int, int]) -> tuple[int,int]:
        """ Get appropriate index for idx_direction such that |idx_road| >= |idx_direction|
        """
        if idx_direction[1] - idx_direction[0] > idx_road[1] - idx_road[0]:                 
            dist_over = (idx_direction[1] - idx_direction[0]) - (idx_road[1] - idx_road[0])
            cut_off = idx_direction[1] - dist_over
        else:
            cut_off = idx_direction[1]

        return (idx_direction[0], cut_off)

    def _update_active_node_w_remainder(self):
        """ Update active node by traversing remainder and adjusting remainder accordingly
        """
        self._active_node, _, _, amt_remainder_remaining = self._skip_count(self._active_node, self._remainder)
        remainder_adjustment = self._get_remainder_length() - amt_remainder_remaining
        self._decrement_remainder(remainder_adjustment)


    def _get_remainder_length(self) -> int:
        return self._remainder[1] - self._remainder[0]

    def _get_remainder_letter(self) -> str:
        if self._remainder is None:
            return 0
        return self._get_letter(self._remainder[0])

    def _get_remainder_length(self) -> int:
        return self._remainder[1] - self._remainder[0]

    def _get_letter(self, idx: int, string_id: int) -> str:
        return self._get_string(string_id)[idx]
    
    def _get_string(self, string_id: int) -> str:
        return self.strings[string_id]

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