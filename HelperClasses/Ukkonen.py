from node import CharNode, UkkonenEdge, Node
from GlobalInt import GlobalInt
import typing

class UkkonenTree:
    def __init__(self) -> None:
        # initialise root
        self.root: 'CharNode' = CharNode('<root>')
        self.root.add_suffix_link(self.root)

        self._global_int: GlobalInt = GlobalInt(0)
        self._active_node = self.root
        self._pending: 'CharNode'|None = None
        self._remainder: tuple[int, int]|None = None

        self._curr_string_id: int = 0
        self.strings: list[str] = []

        self._curr_extension: int = 0
        self._curr_phase: int = 0


    def _construct_tree(self) -> None:
        self._curr_extension = 0
        self._curr_phase = 0
        self._add_pending(self.root)
        
        curr_str_id = self._get_curr_string_id()
        while self._curr_extension < len(self._get_string(curr_str_id)) and self._curr_phase < len(self._get_string(curr_str_id)):
            self._do_extension()
        return None

    def _do_phase(self) -> None:
        pass

    def _do_extension(self) -> None:
        
        traveled_node, traveled_edge, edge_idx, amt_left = self._skip_count(
            self._active_node,
            (self._curr_extension, self._curr_phase)
        )
        rule_to_apply, args = self._get_appropriate_rule(
            traveled_node, 
            traveled_edge, 
            edge_idx, 
            amt_left
        )
        rule_to_apply(*args)

    def _rule_1(self, *args) -> None:
        raise Exception('Rule 1 should be automatic')

    @staticmethod
    def _rule_2(rule_2_version: typing.Callable[['UkkonenTree',UkkonenEdge,int,int], None]|typing.Callable[['UkkonenTree',CharNode,int], None]):
        def wrapper(self, *args) -> None:
            rule_2_version(*args)
            self._increment_extension()
        return wrapper
    
    @_rule_2
    def _rule_2_r(self, rel_edge: UkkonenEdge, mismatch_idx_road: int, mismatch_idx_dir: int) -> None:
        new_node = self._insert_internal_node(rel_edge, mismatch_idx_road)
        new_node.add_UkkonenEdge(self._get_letter(mismatch_idx_dir, self._get_curr_string_id()), (mismatch_idx_dir, self._global_int), Node(is_leaf=True), self._get_curr_string_id())
        

    @_rule_2
    def _rule_2_a(self, rel_node: CharNode, direction_str_idx: int) -> None:
        rel_node.add_UkkonenEdge(self._get_letter(direction_str_idx, self._get_curr_string_id()), (direction_str_idx, self._global_int), Node(is_leaf=True), self._get_curr_string_id())

    def _rule_3(self, *args) -> None:
        # self._increment_remainder()
        self._increment_phase()
    
    def _increment_global_int(self) -> None:
        self._global_int.increment_value()

    def _follow_suffix_link(self) -> None:
        if self._active_node.suffix_link is None:
            raise ValueError('No suffix link')
        else:
            self._active_node = self._active_node.suffix_link.traverse()

    def _decrement_remainder(self, amt: int) -> None:
        if self._remainder is None:
            raise Exception('Decrementing remainder when remainder is None')
        self._remainder = (self._remainder[0] + amt, self._remainder[1])
        if self._remainder[0] > self._remainder[1]:
            self._remainder = None


    def _traverse_remainder(self) -> UkkonenEdge:
        self._update_active_node_w_remainder()
    
        return self._active_node[self._get_remainder_letter()]

    def _skip_count(self, curr_node: CharNode, susbtr_to_travel: tuple[int, int]) -> tuple[CharNode, UkkonenEdge|None, int|None, int]:
        """ Given a starting node and substring of the string to travel along (represented by indices), 
            return the latest Node you arrive to, the Edge you stop at, what index along that edge you stop at, and the index
            of the substr_to_travel you need to test (this is always substr_to_travel[1])
        """
        traveled_node = curr_node
        amt_traveled = 0
        amt_to_travel = susbtr_to_travel[1] - susbtr_to_travel[0] + 1

        while amt_to_travel > 0:
            idx_to_travel = susbtr_to_travel[0] + amt_traveled              # Where you are up to on Direction substr
            edge = self._find_edge_by_idx(traveled_node, idx_to_travel)     # Travel the relevant direction
            if edge is None:                                                # Scenario where direction to travel does not yet exist
                dir_stopped = susbtr_to_travel[1]
                return traveled_node, None, None, dir_stopped
            edge_length = edge.get_length()
            
            if edge_length < amt_to_travel:
                traveled_node = edge.traverse_edge()
                amt_traveled += edge_length
                amt_to_travel -= edge_length
            else:
                idx_stopped = edge.get_values()[0] + amt_to_travel - 1     # Where in the road you stopped
                dir_stopped = susbtr_to_travel[1]                          # Where in the direction you stopped
                return traveled_node, edge, idx_stopped, dir_stopped
        
        return traveled_node, None, None, susbtr_to_travel[1]

    def _do_curr_travel(self)->tuple[CharNode, UkkonenEdge|None, int|None, int]:
        pass

    
    def _get_appropriate_rule(
            self: 'UkkonenTree',
            rel_node: CharNode,
            rel_edge: UkkonenEdge|None,
            rel_edge_idx: int|None,
            rel_substr_idx: int
    ) -> tuple[typing.Callable[['UkkonenTree'], None],tuple]                                                          \
        |tuple[typing.Callable[['UkkonenTree',UkkonenEdge,int,int], None], tuple['UkkonenTree',UkkonenEdge,int,int]]  \
        |tuple[typing.Callable[['UkkonenTree',CharNode,int], None], tuple['UkkonenTree',CharNode,int]]:
        
        if rel_edge_idx is not None and rel_edge is not None:
            if self._check_idxs_equal(rel_edge_idx, rel_substr_idx):    
                return self._rule_3, ()
            else:
                return self._rule_2_r, (self, rel_edge, rel_edge_idx, rel_substr_idx)
        else:
            return self._rule_2_a, (self, rel_node, rel_substr_idx) 
            

    def _find_edge_by_idx(self, curr_node: CharNode, idx_to_travel: int) -> UkkonenEdge|None:
        return curr_node[self._get_letter(idx_to_travel, self._get_curr_string_id())]     


    def _check_idxs_equal(self, idx1: int, idx2: int) -> bool:
        return self._get_letter(idx1, self._get_curr_string_id()) == self._get_letter(idx2, self._get_curr_string_id())

    def _get_letter(self, idx: int, string_id: int) -> str:
        return self._get_string(string_id)[idx]
    
    def _get_string(self, string_id: int) -> str:
        return self.strings[string_id]

    def _increment_extension(self) -> None:
        self._curr_extension += 1
        self._update_active_node()
        if self._curr_extension > self._curr_phase:
            self._increment_phase()
            

    def _update_active_node(self) -> None:
        """ Follow suffix link
        """
        self._active_node = self._active_node.get_suffix_link().traverse()

    def add_string(self, string: str) -> None:
        if self.strings != []:                                      # avoid first increment where string_id is initialised to 0
            self._set_curr_string_id(self._get_curr_string_id() + 1)
        self.strings.append(string)
        self._construct_tree()

    def _increment_phase(self) -> None:
        self._curr_phase += 1
        self._increment_global_int()

    def _insert_internal_node(self, edge: UkkonenEdge, pos: int) -> CharNode:
        """ Inserts internal node before pos. 
        """
        new_node = CharNode(f"<{chr(self._curr_extension+100)}{chr(self._curr_phase+100)}>")
        node2 = edge._change_dest(new_node)     # old destination
        old_val = edge.change_end_value(pos - 1)    # value before old dest
        new_node.add_UkkonenEdge(self._get_letter(pos, self._get_curr_string_id()), (pos , old_val), node2, self._get_curr_string_id())
        self._resolve_suffix_link(new_node)
        self._add_pending(new_node)
        return new_node

    def _add_pending(self, node: CharNode) -> None:
        self._pending = node
    
    def _get_pending(self) -> CharNode:
        assert self._pending is not None
        return self._pending

    def _resolve_suffix_link(self, new_node: CharNode) -> None:
        pending = self._get_pending()
        if isinstance(pending, CharNode):
            new_node.add_suffix_link(pending)

    def _get_curr_string_id(self) -> int:
        return self._curr_string_id
    
    def _set_curr_string_id(self, value: int) -> None:
        self._curr_string_id = value

    def get_suffixes_and_links(
        self
    ) -> tuple[list[str], list[tuple[str, str]]]:
        """
        Returns
        -------
        suffixes : list[str]
            Every suffix stored in the tree (one entry per leaf).
        links : list[tuple[str, str]]
            For each suffix-link, the pair (substring_at_source_node,
            substring_at_destination_node).
        """
        suffixes: list[str] = []
        node_label: dict[CharNode, str] = {self.root: ""}

        def dfs(node: CharNode, label: str) -> None:
            node_label[node] = label                              # label of this node

            # CharTable stores children in an array[128]; iterate over used slots
            for idx, edge in enumerate(node.array.array):
                if edge is None:
                    continue

                # substring carried by this edge
                start, end = edge.value
                if start == end:
                    edge_text = self.strings[edge.string_id][start]
                else:
                    edge_text = self.strings[edge.string_id][start:end+1]   # end is exclusive
                new_label = label + edge_text
                child = edge.traverse_edge()

                if isinstance(child, CharNode):       # internal node
                    dfs(child, new_label)
                else:                                 # leaf: we have a complete suffix
                    suffixes.append(new_label)

        dfs(self.root, "")

        links: list[tuple[str, str]] = []
        for src, src_label in node_label.items():
            if src.has_suffix_link():
                dst = src.suffix_link.dest
                dst_label = node_label.get(dst, "")   # root→"" if not visited yet
                links.append((src_label, dst_label))

        return suffixes, links

if __name__=='__main__':
    import string, random
    NUM_TRIALS   = 10_000              # how many times to run the test
    ALPHABET     = string.ascii_lowercase
    MIN_LEN      = 5                  # length of the *body* (before '$')
    MAX_LEN      = 64

    # --- test loop ---------------------------------------------------------------
    print('testing')
    for _ in range(NUM_TRIALS):
        body     = ''.join(random.choice(ALPHABET) for _ in range(random.randint(MIN_LEN, MAX_LEN)))
        test_str = f"{body}$"         # Ukkonen implementation expects a unique terminator

        tree = UkkonenTree()
        tree.add_string(test_str)

        suffixes, _ = tree.get_suffixes_and_links()
        assert len(test_str) == len(suffixes), f"Mismatch for {test_str!r}"
        for i in range(len(test_str)):
            assert test_str[i:] in suffixes

