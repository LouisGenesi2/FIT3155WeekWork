class BTreeArray:
    def __init__(self, t_val: int) -> None:
        self.arr: list[int] = []

    def get_arr(self) -> list[int]:
        return self.arr
    
    def __len__(self) -> int:
        return len(self.arr)
    
    def get_travel_idx(self, item: int) -> int:
        """ 
        """
        # TODO: binary search
        for idx, val in enumerate(self.arr):
            if val > item:
                return idx
            else:
                if idx == len(self) - 1:    # get to end of arr and item is biggest
                    return idx

        raise AssertionError('No travel index found')

class BTreeNode:
    def __init__(self, t_val: int, is_root: int) -> None:
        self.min: int = t_val - 1 if not is_root else 0
        self.max: int = t_val * 2 - 1
        self._root: bool = is_root
        self.leaf: bool = True
        self._keys_array: list[int] = []
        self._children_array: list[BTreeNode] = []

    def is_leaf(self) -> bool:
        return self.leaf
    
    def get_keys_array(self) -> list[int]:
        return self._keys_array

    def find_key_travel_idx(self, key: int) -> tuple[int, bool]:
        """ Finds idx which corresponds to child BTreeNode that should be traversed to
        """
        



class BTree:
    def __init__(self, t_val: int) -> None:
        self.root = BTreeNode(t_val=t_val, is_root=True)

    def insert(self, key: int) -> None:
        

    def del_val(self, key: int) -> None:
        pass

    def _get_to_leaf(self, key: int, pos: BTreeNode) -> BTreeNode:
        if pos.is_leaf():
            return pos
        