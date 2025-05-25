class BTreeIndex:
    def __init__(self, val: int) -> None:
        self.val = val

    def get_val(self) -> int:
        return self.val
    
    def __index__(self) -> int:
        return self.val

class KeyIndex(BTreeIndex):
    pass

class ChildIndex(BTreeIndex):
    pass

class BTreeKeysArray:
    def __init__(self, t_val: int) -> None:
        self.min = t_val - 1
        self.max = t_val * 2 - 1
        self.arr: list[int] = []

    def get_arr(self) -> list[int]:
        return self.arr
    
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
    
    def key_idx_to_l_child_idx(self, idx: KeyIndex) -> ChildIndex:
        return ChildIndex(idx.get_val())
    
    def key_idx_to_r_child_idx(self, idx: KeyIndex) -> ChildIndex:
        return ChildIndex(idx.get_val() + 1)
    
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
    
class BTreeChildrenArray:
    def __init__(self, t_val: int) -> None:
        self.min = t_val
        self.max = t_val * 2
        self.arr: 'list[BTreeNode]' = []
    
    def get_arr(self) -> 'list[BTreeNode]':
        return self.arr

    def __getitem__(self, idx: ChildIndex) -> 'BTreeNode':
        assert isinstance(idx, ChildIndex)
        return self.get_arr()[idx]

class BTreeNode:
    def __init__(self, t_val: int, is_root: bool) -> None:
        self.min: int = t_val - 1 if not is_root else 0
        self.max: int = t_val * 2 - 1
        self._root: bool = is_root
        self.leaf: bool = True
        self._keys_array: BTreeKeysArray = BTreeKeysArray(t_val)
        self._children_array: BTreeChildrenArray = BTreeChildrenArray(t_val)

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
        return self.get_child(idx)
        

    def insert(self, key: int) -> int:
        """ Inserts a key into the keys array, and adjusts children array appropriately
        """
        assert self.is_leaf()
        self.get_keys_array()

    
    def transform_to_internal(self) -> None:
        pass

    def transform_to_leaf(self) -> None:
        pass



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
            pos = pos.get_travel_child(key)

        assert pos.is_leaf()
        return pos
        
        