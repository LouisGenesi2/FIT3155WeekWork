from typing import Generic, TypeVar
from abc import abstractmethod

class BTreeIndex:
    def __init__(self, val: int) -> None:
        self.val = val

    def get_val(self) -> int:
        return self.val
    
    def __index__(self) -> int:
        return self.val

class KeyIndex(BTreeIndex):
    """ Ensures separation between indexes related to keys and ones related to children
    """
    pass

class ChildIndex(BTreeIndex):
    """ Ensures separation between indexes related to keys and ones related to children
    """
    pass

T = TypeVar('T')
I = TypeVar('I')
S = TypeVar("S")

class BTreeArray(Generic[T, I, S]):
    __slots__ = ("_min", "_max", "_arr")
    
    def __init__(self) -> None:
        self._min = None
        self._max = None
        self._arr: list[I] = None
        self.index_type: type = type(self)

    def get_arr(self) -> list[I]:
        return self._arr
    
    def set_arr(self, arr: list[I]) -> None:
        self._arr = arr

    def __len__(self) -> int:
        return len(self.get_arr())
    
    @abstractmethod
    def get_t_val(self) -> int:
        pass

    def slice(self, start_idx: T, end_idx: T) -> S:
        """ returns slice of self
        """
        assert isinstance(start_idx, type(self)) and isinstance(end_idx, type(self))
        return type(self)(self.get_t_val(), self.get_arr()[start_idx:end_idx])


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
        return len(self.arr)
    
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
    
    
    
    def insert_at_pos(self, key: int, idx: KeyIndex) -> None:
        """ Inserts key at index
        """
        new_arr = self.get_arr()[0:idx] + [key] + self.get_arr()[idx+1:]
        self.set_arr(new_arr)

    
class BTreeChildrenArray:
    def __init__(self, t_val: int, init_arr: 'list[BTreeNode]' = []) -> None:
        self.min = t_val
        self.max = t_val * 2
        self.arr: 'list[BTreeNode]' = init_arr
    
    def get_t_val(self) -> int:
        return self.min
    
    def get_arr(self) -> 'list[BTreeNode]':
        return self.arr

    def __getitem__(self, idx: ChildIndex) -> 'BTreeNode':
        assert isinstance(idx, ChildIndex)
        return self.get_arr()[idx]
    
    def slice(self, start_idx: ChildIndex, end_idx: ChildIndex) -> 'BTreeChildrenArray':
        """ returns BTreeChildrenArray of slice
        """
        assert isinstance(start_idx, ChildIndex) and isinstance(end_idx, ChildIndex)
        return BTreeChildrenArray(self.get_t_val(), self.get_arr()[start_idx:end_idx])
    
    def insert_at_pos(self, key: int, idx: KeyIndex) -> None:
        """ Inserts key at index
        """
        new_arr = self.get_arr()[0:idx] + [key] + self.get_arr()[idx+1:]
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
        self.get_children_array = children
        self.get_keys_array = keys

    def get_t_val(self) -> int:
        return self.t_val

    def is_full(self) -> bool:
        assert len(self.get_keys_array()) <= self.max   # should never exceed max
        return len(self.get_keys_array()) == self.max

    def is_leaf(self) -> bool:
        return self.leaf
    
    def get_keys_array(self) -> BTreeKeysArray:
        return self._keys_array

    def get_children_array(self) -> BTreeChildrenArray:
        return self._children_array
    
    def get_child(self, idx: ChildIndex) -> 'BTreeNode':
        return self.get_children_array()[idx]
    
    def get_travel_child(self, key: int) -> 'BTreeNode':
        """ Returns child tree which should be traversed to
        """
        idx = self.get_keys_array().get_travel_insertion_idx(key)
        l_child_idx = self.key_idx_to_l_child_idx(idx)
        return self.get_child(l_child_idx)
    
    def key_idx_to_l_child_idx(self, idx: KeyIndex) -> ChildIndex:
        return ChildIndex(idx.get_val())
    
    def key_idx_to_r_child_idx(self, idx: KeyIndex) -> ChildIndex:
        return ChildIndex(idx.get_val() + 1)

    def insert_key(self, key: int) -> int:
        """ Inserts a key into the keys array, and adjusts children array appropriately
        """
        assert self.is_leaf()
        self.get_keys_array()

    def known_insert(self, key: int, idx_to_insert: KeyIndex) -> None:
        """ Inserts a key knowing where to insert it. Occurs when promoting to parent
        """
        self.get_keys_array()
   
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
        # TODO: implement
        t_val = self.get_t_val()
        c_idx1, c_idx2, c_idx3, c_idx4 = ChildIndex(0), ChildIndex(t_val), ChildIndex(t_val + 1), ChildIndex(2*t_val+1)
        c_arr1, c_arr2, c_arr3 = self.get_children_array().slice(c_idx1, c_idx2), self.get_children_array()[c_idx2], self.get_children_array()[c_idx3:c_idx4]

        k_idx1, k_idx2, k_idx3, k_idx4 = KeyIndex(0), KeyIndex(t_val - 1), KeyIndex(t_val), KeyIndex(2*t_val)
        k_arr1, k_arr2, k_arr3 = self.get_keys_array().slice(k_idx1, k_idx2), self.get_keys_array()[k_idx2], self.get_keys_array()[k_idx3:k_idx4]

        return (
            (c_arr1, c_arr2, c_arr3),
            (k_arr1, k_arr2, k_arr3)
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
            next_pos = pos.get_travel_child(key)
            if next_pos.is_full():
                next_pos = self._break_full_node(key=key, node=next_pos, parent_node=pos)
            pos = next_pos

        assert pos.is_leaf()
        return pos
        
    
    def _break_full_node(self, key: int, node: BTreeNode, parent_node: BTreeNode) -> BTreeNode:
        """ Breaks up a full node and returns the node that is appropriate for the key
        """
        key_arrs, child_arrs = node.split_node_arrays() 


    def create_node(self, node: BTreeNode, child_idx: ChildIndex) -> BTreeNode:
        """ Creates a child node at the 
        """

        