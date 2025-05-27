from typing import Generic, TypeVar
from abc import abstractmethod

class BTreeIndex:
    def __init__(self, val: int) -> None:
        self.val = val

    def get_val(self) -> int:
        return self.val
    
    def __index__(self) -> int:
        return self.val
    
    def __add__(self, int: int) -> 'BTreeIndex':
        return BTreeIndex(self.get_val() + int)

class KeyIndex(BTreeIndex):
    """ Ensures separation between indexes related to keys and ones related to children
    """
    def to_l_child(self) -> 'ChildIndex':
        return ChildIndex(self.get_val)
    
    def to_r_child(self) -> 'ChildIndex':
        return ChildIndex(self.get_val + 1)

class ChildIndex(BTreeIndex):
    """ Ensures separation between indexes related to keys and ones related to children
    """
    pass


class BTreeKeysArray:
    def __init__(self, t_val: int, init_arr: list[int] = []) -> None:
        self.min = t_val - 1
        self.max = t_val * 2 - 1
        self.arr: list[int] = init_arr

    def get_t_val(self) -> int:
        return self.min + 1
    
    def get_arr(self) -> list[int]:
        return self.arr
    
    def set_arr(self, arr: list[int]) -> None:
        self.arr = arr
    
    def __len__(self) -> int:
        return len(self.get_arr())
    
    def get_travel_insertion_idx(self, item: int) -> KeyIndex:
        """ returns the idx that if done on an internal node, is where to travel,
            and if a leaf, is where to insert 
        """
        # TODO: binary search
        for idx, val in enumerate(self.arr):
            if val > item:
                return KeyIndex(idx)
            else:
                if idx == len(self) - 1:    # get to end of arr and item is biggest
                    return KeyIndex(idx)

        raise AssertionError('No travel index found')
    
    def get_key_idx(self, key: int) -> KeyIndex:
        """ Returns the index at which the key is stored.
        """
        # TODO: binary search
        for idx, val in enumerate(self.arr):
            if val == key:
                return KeyIndex(idx)
            
        raise AssertionError('Key not found in array')
    
    def __getitem__(self, idx: KeyIndex) -> int:
        assert isinstance(idx, KeyIndex)
        return self.get_arr()[idx]
    
    def slice(self, start_idx: KeyIndex, end_idx: KeyIndex) -> 'BTreeKeysArray':
        """ returns slice of self
        """
        assert isinstance(start_idx, KeyIndex) and isinstance(end_idx, KeyIndex)
        return BTreeKeysArray(self.get_t_val(), self.get_arr()[start_idx:end_idx])
    
    def insert_at_pos(self, key: int, idx: KeyIndex) -> None:
        """ Inserts key at index
        """
        new_arr = self.get_arr()[0:idx] + [key] + self.get_arr()[idx+1:]
        self.set_arr(new_arr)

    
class BTreeChildrenArray:
    def __init__(self, t_val: int, init_arr: 'list[BTreeNode|None]' = []) -> None:
        self.min = t_val
        self.max = t_val * 2
        self.arr: 'list[BTreeNode|None]' = init_arr
    
    def get_t_val(self) -> int:
        return self.min
    
    def set_arr(self, arr: 'list[BTreeNode|None]') -> None:
        self.arr = arr

    def get_arr(self) -> 'list[BTreeNode|None]':
        return self.arr

    def __getitem__(self, idx: ChildIndex) -> 'BTreeNode':
        assert isinstance(idx, ChildIndex)
        item = self.get_arr()[idx]
        assert item is not None
        return item
    
    def __len__(self) -> int:
        return len(self.get_arr())
    
    def slice(self, start_idx: ChildIndex, end_idx: ChildIndex) -> 'BTreeChildrenArray':
        """ returns slice of self
        """
        assert isinstance(start_idx, type(self)) and isinstance(end_idx, type(self))
        return BTreeChildrenArray(self.get_t_val(), self.get_arr()[start_idx:end_idx])
    
    def insert_at_pos(self, child: 'BTreeNode', idx: ChildIndex) -> None:
        """ Inserts key at index
        """
        new_arr = self.get_arr()[0:idx] + [child] + self.get_arr()[idx+1:]
        self.set_arr(new_arr)

class BTreeNode:
    def __init__(self, t_val: int, is_root: bool) -> None:
        self.t_val = t_val
        self._root: bool = is_root
        self.leaf: bool = True
        self._keys_array: BTreeKeysArray = BTreeKeysArray(t_val)
        self._children_array: BTreeChildrenArray = BTreeChildrenArray(t_val)

    def set_keys_children(self, keys: BTreeKeysArray, children: BTreeChildrenArray) -> None:
        """ In one swoop, set what's in the Node
        """
        assert isinstance(keys, BTreeKeysArray) and isinstance(children, BTreeChildrenArray)
        assert len(keys) == len(children) - 1 or (len(keys) == 0 and len(children) == 0)
        self._children_array = children
        self._keys_array = keys

    def get_t_val(self) -> int:
        return self.t_val

    def is_full(self) -> bool:
        assert len(self.get_keys_array()) <= self.get_keys_array().max   # should never exceed max
        return len(self.get_keys_array()) == self.get_keys_array().max

    def is_leaf(self) -> bool:
        return self.leaf
    
    def get_keys_array(self) -> BTreeKeysArray:
        return self._keys_array

    def get_children_array(self) -> BTreeChildrenArray:
        return self._children_array
    
    def get_child(self, idx: ChildIndex) -> 'BTreeNode':
        return self.get_children_array()[idx]
    
    def get_travel_child(self, key: int) -> 'tuple[BTreeNode, ChildIndex]':
        """ Returns child tree which should be traversed to and the index it was stored at
        """
        idx = self.get_keys_array().get_travel_insertion_idx(key)
        l_child_idx = self.key_idx_to_l_child_idx(idx)
        return self.get_child(l_child_idx), l_child_idx
    
    def key_idx_to_l_child_idx(self, idx: KeyIndex) -> ChildIndex:
        return ChildIndex(idx.get_val())
    
    def key_idx_to_r_child_idx(self, idx: KeyIndex) -> ChildIndex:
        return ChildIndex(idx.get_val() + 1)

    def insert_key(self, key: int, child: 'BTreeNode|None') -> int:
        """ Inserts a key into the keys array, and adjusts children array appropriately
        """
        assert self.is_leaf()
        self.get_keys_array()

    def known_single_key_insert(self, key: int, l_child: 'BTreeChildrenArray', r_child: 'BTreeChildrenArray', idx_to_insert: KeyIndex) -> None:
        """ Inserts a key knowing where to insert it. Occurs when promoting to parent
        """
        assert isinstance(idx_to_insert, KeyIndex)
        keys = self.get_keys_array()
   
    def transform_to_internal(self) -> None:
        pass

    def transform_to_leaf(self) -> None:
        pass

    def split_node_arrays(
        self
    ) -> tuple[tuple[BTreeKeysArray,BTreeKeysArray,BTreeKeysArray],
               tuple[BTreeChildrenArray,BTreeChildrenArray,BTreeChildrenArray]]:
        """ Splits node arrays into 3. Used whenever stepping on full node
        """
        assert self.is_full()   # should always be done when full
        t_val = self.get_t_val()

        # split child array into 3
        c_idx1, c_idx2, c_idx3, c_idx4 = ChildIndex(0), ChildIndex(t_val), ChildIndex(t_val + 1), ChildIndex(2*t_val+1)
        c_arr1, c_arr2, c_arr3 = self.get_children_array().slice(c_idx1, c_idx2), BTreeChildrenArray(t_val, [self.get_children_array()[c_idx2]]), self.get_children_array().slice(c_idx3,c_idx4)

        # split key array into 3
        k_idx1, k_idx2, k_idx3, k_idx4 = KeyIndex(0), KeyIndex(t_val - 1), KeyIndex(t_val), KeyIndex(2*t_val)
        k_arr1, k_arr2, k_arr3 = self.get_keys_array().slice(k_idx1, k_idx2), BTreeKeysArray(t_val, [self.get_keys_array()[k_idx2]]), self.get_keys_array().slice(k_idx3, k_idx4)

        return (
            (k_arr1, k_arr2, k_arr3),
            (c_arr1, c_arr2, c_arr3)  
        )


        

        

        


class BTree:
    def __init__(self, t_val: int) -> None:
        self.root = BTreeNode(t_val=t_val, is_root=True)

    def get_root(self) -> BTreeNode:
        return self.root
    
    def insert(self, key: int) -> None:
        leaf = self._get_to_leaf(key, self.get_root())


    def del_val(self, key: int) -> None:
        pass

    def _get_to_leaf(self, key: int, pos: BTreeNode) -> BTreeNode:
        """ Given a key, get to the appropriate leaf
        """
        # TODO: break up every full node
        while not pos.is_leaf():
            next_pos, next_pos_idx_in_parent = pos.get_travel_child(key)
            if next_pos.is_full():
                next_pos = self._break_full_node(key=key, node=next_pos, parent_node=pos, node_idx_in_parent=next_pos_idx_in_parent)
            pos = next_pos

        assert pos.is_leaf()
        return pos
        
    
    def _break_full_node(self, key: int, node: BTreeNode, parent_node: BTreeNode, node_idx_in_parent: ChildIndex) -> BTreeNode:
        """ Breaks up a full node and returns the node that is appropriate for the key
        """
        key_arrs, child_arrs = node.split_node_arrays()
        key_to_promote = key_arrs[1][0]
        child_to_promote
        parent_node.known_insert(key, node_idx_in_parent)


    def create_node(self, node: BTreeNode, child_idx: ChildIndex) -> BTreeNode:
        """ Creates a child node at the 
        """

        