from typing import Generic, TypeVar, Callable
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
    def to_l_child(self) -> 'ChildIndex':
        return ChildIndex(self.get_val())
    
    def to_r_child(self) -> 'ChildIndex':
        return ChildIndex(self.get_val() + 1)

class ChildIndex(BTreeIndex):
    """ Ensures separation between indexes related to keys and ones related to children
    """
    pass


class BTreeKeysArray:
    def __init__(self, t_val: int, init_arr: list[int] = []) -> None:
        self.min = t_val - 1
        self.arr: list[int] = init_arr

    def get_max(self) -> int:
        return (self.min + 1) * 2 - 1
    
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
    
    def get_potential_key_loc(self, item: int) -> KeyIndex:
        """ returns where key could be, and where to travel if not
        """
        # TODO: binary search
        for idx, val in enumerate(self.arr):
            if val > item:
                return KeyIndex(idx)
            else:
                if val == item:
                    return KeyIndex(idx)
                
                if idx == len(self) - 1:    # get to end of arr and item is biggest
                    return KeyIndex(idx)
    
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
        new_arr = self.get_arr()[0:idx] + [key] + self.get_arr()[idx:]
        self.set_arr(new_arr)

    def __add__(self, other_arr: 'BTreeKeysArray|list[int]') -> 'BTreeKeysArray':
        if isinstance(other_arr, BTreeKeysArray):
            new_arr = self.arr + other_arr.arr
        elif isinstance(other_arr, list):
            new_arr = self.arr + other_arr
        else:
            raise TypeError
        assert new_arr <= self.get_max()
        return BTreeKeysArray(self.get_t_val(), new_arr)
    
    def pop(self, idx: KeyIndex) -> int:
        return self.get_arr().pop(idx)
    
class BTreeChildrenArray:
    def __init__(self, t_val: int, init_arr: 'list[BTreeNode|None]' = []) -> None:
        self.min = t_val
        self.arr: 'list[BTreeNode|None]' = init_arr
    
    def get_max(self) -> int:
        return self.min * 2

    def get_t_val(self) -> int:
        return self.min
    
    def set_arr(self, arr: 'list[BTreeNode|None]') -> None:
        self.arr = arr

    def get_arr(self) -> 'list[BTreeNode|None]':
        return self.arr
    
    def pop(self, idx: ChildIndex) -> 'BTreeNode|None':
        return self.arr.pop(idx)

    def __getitem__(self, idx: ChildIndex) -> 'BTreeNode|None':
        assert isinstance(idx, ChildIndex)
        item = self.get_arr()[idx]
        return item
    
    def __len__(self) -> int:
        return len(self.get_arr())
    
    def slice(self, start_idx: ChildIndex, end_idx: ChildIndex) -> 'BTreeChildrenArray':
        """ returns slice of self
        """
        assert isinstance(start_idx, type(self)) and isinstance(end_idx, type(self))
        return BTreeChildrenArray(self.get_t_val(), self.get_arr()[start_idx:end_idx])
    
    def insert_at_pos(self, children: 'BTreeChildrenArray', idxs: 'list[ChildIndex]') -> None:
        """ Inserts children at idxs.
            Children are the children to insert. idx are the positions to insert them at.
        """
        # TODO: implement
        new_arr = []
        for arrs_idx, (child, idx) in enumerate(zip(children.get_arr(), idxs)):   #
            if arrs_idx == 0:
                if arrs_idx == len(children) - 1:
                    new_arr += self.get_arr()[0:idx] + [child] + self.get_arr()[idx:]
                else:
                    new_arr += self.get_arr()[0:idx] + [child] + self.get_arr()[idx:arrs_idx + 1]
            
            if arrs_idx == len(children) - 1:
                new_arr += [child] + self.get_arr()[idx:]
            else:
                new_arr += [child] + self.get_arr()[idx:arrs_idx + 1]
        
        self.set_arr(new_arr)

    def __add__(self, other_arr: 'BTreeChildrenArray|list[BTreeNode]') -> 'BTreeChildrenArray':
        if isinstance(other_arr, BTreeChildrenArray):
            new_arr = self.arr + other_arr.arr
        elif isinstance(other_arr, list):
            new_arr = self.arr + other_arr
        else:
            raise TypeError
        assert new_arr <= self.get_max()
        return BTreeChildrenArray(self.get_t_val(), new_arr)
    
    

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
    
    def get_child(self, idx: ChildIndex) -> 'BTreeNode|None':
        assert isinstance(idx, ChildIndex)
        return self.get_children_array()[idx]
    
    def get_key(self, idx: KeyIndex) -> int:
        assert isinstance(idx, KeyIndex)
        return self.get_keys_array()[idx]

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

    def known_single_key_insert(self, key: int, l_child: 'BTreeChildrenArray|None', r_child: 'BTreeChildrenArray|None', idx_to_insert: KeyIndex) -> None:
        """ Handles key insertion in insertion split case.
            Only one of l_child or r_child should be inserted, as a key insertion needs one child insertion.
            None means to leave left or right unchanged, use BTreeChildrenArray(init=[None]) BTreeChildrenArray(init=[<BTreeNode>]) for inserting an empty child or node
        """
        assert isinstance(idx_to_insert, KeyIndex)
        # An insertion must have exactly one child inserted. 
        assert (l_child is None and isinstance(r_child, BTreeChildrenArray)) or (r_child is None and isinstance(l_child, BTreeChildrenArray))
        
        keys = self.get_keys_array()
        keys.insert_at_pos(key, idx_to_insert)

        l_child_idx = idx_to_insert.to_l_child()
        r_child_idx = idx_to_insert.to_r_child()

        # add child
        children = self.get_children_array()
        if isinstance(l_child, BTreeChildrenArray):
            children.insert_at_pos(l_child, [l_child_idx])
        elif isinstance(r_child, BTreeChildrenArray):
            children.insert_at_pos(r_child, [r_child_idx])
        
   
    def transform_to_internal(self) -> None:
        pass

    def transform_to_leaf(self) -> None:
        pass

    def split_node_arrays(
        self
    ) -> tuple[tuple[BTreeKeysArray,BTreeKeysArray,BTreeKeysArray],
               tuple[BTreeChildrenArray,BTreeChildrenArray]]:
        """ Splits node arrays into 3. Used whenever stepping on full node
        """
        assert self.is_full()   # should always be done when full
        t_val = self.get_t_val()

        # split child array into 2
        c_idx1, c_idx2, c_idx3 = ChildIndex(0), ChildIndex(t_val + 1), ChildIndex(2*t_val+1)
        c_arr1, c_arr2 = self.get_children_array().slice(c_idx1, c_idx2),  self.get_children_array().slice(c_idx2,c_idx3)

        # split key array into 3
        k_idx1, k_idx2, k_idx3, k_idx4 = KeyIndex(0), KeyIndex(t_val), KeyIndex(t_val + 1), KeyIndex(2*t_val)
        k_arr1, k_arr2, k_arr3 = self.get_keys_array().slice(k_idx1, k_idx2), BTreeKeysArray(t_val, [self.get_keys_array()[k_idx2]]), self.get_keys_array().slice(k_idx3, k_idx4)

        return (
            (k_arr1, k_arr2, k_arr3),
            (c_arr1, c_arr2)  
        )

    def is_minimum(self) -> bool:
        assert len(self.get_keys_array()) > self.get_t_val() or self._root == True
        return len(self.get_keys_array()) == self.get_t_val()
        
    def pop(self, pos: KeyIndex, child_to_pop: ChildIndex) -> 'tuple[int, BTreeNode]':
        """ Removes the given position from the Node
        """
        # child popped should always be a neighbour
        assert abs(child_to_pop.get_val() - pos.get_val()) <= 1

        key = self.get_keys_array().pop(pos)
        child = self.get_children_array().pop(child_to_pop)
        return key, child

        


class BTree:
    def __init__(self, t_val: int) -> None:
        self.root = BTreeNode(t_val=t_val, is_root=True)
        self.t_val = t_val

    def swap_children(self, node1: BTreeNode, node2: BTreeNode, child_idx1: ChildIndex, child_idx2: ChildIndex) -> None:
        """ Swap children of two nodes
        """
        node2.get_children_array()[child_idx2], node1.get_children_array()[child_idx1] = node1.get_child(child_idx1), node2.get_child(child_idx2)
        


    def get_root(self) -> BTreeNode:
        return self.root
    
    def insert(self, key: int) -> None:
        leaf = self._get_to_leaf_insertion(key, self.get_root())
        idx_to_insert = leaf.get_keys_array().get_potential_key_loc(key)
        leaf.known_single_key_insert(key=key, idx_to_insert=idx_to_insert, l_child=BTreeChildrenArray(init_arr=[None]), r_child=BTreeChildrenArray(init_arr=[None]))


    def del_val(self, key: int) -> None:
        pass

    def _get_to_leaf_insertion(self, key: int, pos: BTreeNode) -> BTreeNode:
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
    
    def _swap_inorder_successor(self, parent: BTreeNode, key_idx: KeyIndex) -> BTreeNode:
        """ Swap key at key_idx with inorder successor. Returns the Node which previously contained the successor
        """
        child_idx = key_idx.to_r_child()
        child = parent.get_child(child_idx)
        successor = child.get_keys_array()[0]
        curr = parent.get_keys_array()[key_idx]
        child.get_keys_array()[0] = curr
        parent.get_keys_array()[key_idx] = successor

        return child

    def _swap_inorder_predecessor(self, parent: BTreeNode, key_idx: KeyIndex) -> BTreeNode:
        """ Swap key at key_idx with inorder predecessor. Returns the Node which previously contained the predecessor
        """
        child_idx = key_idx.to_l_child()
        child = parent.get_child(child_idx)
        successor = child.get_keys_array()[-1]
        curr = parent.get_keys_array()[key_idx]
        child.get_keys_array()[-1] = curr
        parent.get_keys_array()[key_idx] = successor

        return child

    def _consolidate_parent(self, l_child: BTreeNode, r_child: BTreeNode, parent: BTreeNode, key_idx: KeyIndex) -> BTreeNode:
        """ Combines l_child and r_child, and key from parent identified with key_idx. Handles root deletion edge case
        """
        l_child_keys = l_child.get_keys_array()
        l_child_children = l_child.get_children_array()
        r_child_keys = r_child.get_keys_array()
        r_child_children = r_child.get_children_array()
        parent_key_wrapped = [parent.get_key(key_idx)]

        consolidated_node = self.create_node_w_arrs(child_arrs = [l_child_children, r_child_children], key_arrs=[l_child_keys, parent_key_wrapped, r_child_keys])

        if parent._root is True:
            self._set_root(consolidated_node)

        return consolidated_node
            

    def _r_sibling_rotate(self, parent: BTreeNode, key_idx: KeyIndex) -> BTreeNode:
        """ Counter clockwise rotation. Done during deletion where the next position is at minimum
            but right sibling has above minimum. 
            the smallest key in the right sibling of the key replaces the key,
            the key is moved to the next position.
            The left child of the former right sibling becomes the right child
            of the moved key from the parent into the next position.
        """
        next_pos = parent.get_child(key_idx.to_l_child())
        r_sibling = parent.get_child(key_idx.to_r_child())
        
        r_sibling_key, r_sibling_l_child = r_sibling.pop(KeyIndex(0), ChildIndex(0))
        parent_key, next_pos = parent.pop(key_idx, key_idx.to_l_child())

        # rotate r_sibling into parent, and point to l_sibling
        parent.known_single_key_insert(key=r_sibling_key, l_child=BTreeChildrenArray(t_val=self.t_val, init_arr=[next_pos]), r_child=None, idx_to_insert=key_idx)

        # rotate parent key into l_sibling, right child is the left child of former right sibling
        # TODO: check this insert
        next_pos.known_single_key_insert(key=parent_key, l_child=None, r_child=BTreeChildrenArray(t_val=self.t_val, init_arr=[r_sibling_l_child]), idx_to_insert=KeyIndex(len(next_pos.get_keys_array())))

        return next_pos


    def _l_sibling_rotate(self, parent: BTreeNode, key_idx: KeyIndex) -> BTreeNode:
        """ Clockwise rotation. Done during deletion where the next position is at minimum
            but left sibling has above minimum. 
            the largest key in the left sibling of the key replaces the key,
            the key is moved to the next position.
            The right child of the former left sibling becomes the left child
            of the moved key from the parent into the next position.
        """
        next_pos = parent.get_child(key_idx.to_r_child())
        l_sibling = parent.get_child(key_idx.to_l_child())
        
        # get largest key and right child of largest key in left sibling
        l_sibling_size = len(l_sibling.get_keys_array())
        l_sibling_key, l_sibling_r_child = l_sibling.pop(KeyIndex(l_sibling_size), KeyIndex(l_sibling_size).to_r_child())
        
        parent_key, next_pos = parent.pop(key_idx, key_idx.to_r_child())

        # rotate l_sibling into parent, and point to r_sibling
        parent.known_single_key_insert(key=l_sibling_key, r_child=BTreeChildrenArray(t_val=self.t_val, init_arr=[next_pos]), l_child=None, idx_to_insert=key_idx)

        # rotate parent key into r_sibling, left child is the right child of former left sibling
        # TODO: check this insert
        next_pos.known_single_key_insert(key=parent_key, r_child=None, l_child=BTreeChildrenArray(t_val=self.t_val, init_arr=[l_sibling_r_child]), idx_to_insert=KeyIndex(0))

        return next_pos

    def _get_siblings(self, parent: BTreeNode, child_index: ChildIndex) -> list[BTreeNode]:
        """ Gets siblings of children 
        """
        siblings = []
        if child_index.get_val() > 0:
            l_child_idx = ChildIndex(child_index.get_val - 1)
            siblings.append(parent.get_child(l_child_idx))
        else:
            siblings.append(None)
        
        if child_index < len(parent.get_children_array()):
            r_child_idx = ChildIndex(child_index.get_val() + 1)
            siblings.append(parent.get_child(r_child_idx))
        else:
            siblings.append(None)


    def _resolve_deletion_rule(self, key: int, pos: BTreeNode) -> BTreeNode:
        """ Given an internal node, check through all deletion cases and return where
            to continue traversal to leaf from
        """
        
        key_idx = pos.get_keys_array().get_potential_key_loc(key)
        
        if pos.get_key(key_idx) == key:
            # case 2
            r_child = pos.get_child(key_idx.to_r_child())
            l_child = pos.get_child(key_idx.to_l_child())
            
            if l_child is not None:
                if l_child.is_minimum() is False:
                    return self._swap_inorder_predecessor(parent=pos, key_idx=key_idx)
            
            if r_child is not None:
                if r_child.is_minimum() is False:
                    return self._swap_inorder_successor(parent=pos, key_idx=key_idx)
            
            if l_child is not None and r_child is not None:
                if l_child.is_minimum() and r_child.is_minimum():
                    return self._consolidate_parent(l_child=l_child, r_child=r_child, parent=pos, key_idx=key_idx)
            
        next_pos_child_idx_in_parent = key_idx.to_l_child()
        next_pos = pos.get_child(next_pos_child_idx_in_parent)
        if next_pos.is_minimum():
            # case 3
            l_sibling, r_sibling = self._get_siblings(pos, next_pos_child_idx_in_parent)
            if r_sibling is not None:
                if r_sibling.is_minimum():
                    return self._consolidate_parent(l_child=next_pos, r_child=r_sibling, parent=pos, key_idx=key_idx)
            if l_sibling is not None:
                if l_sibling.is_minimum():
                    return self._consolidate_parent(l_child=l_sibling, r_child=next_pos, parent=pos, key_idx=key_idx)
                
            if r_sibling is not None:
                return self._r_sibling_rotate
            if l_sibling is not None:
                return self._l_sibling_rotate

        return next_pos



    def _get_to_leaf_deleion(self, key: int, pos: BTreeNode) -> BTreeNode:
        """ Given a key, delete it from the Tree
        """
        while not pos.is_leaf():
            pos = self._resolve_deletion_rule(pos, key)
        return pos
        
    
    def _break_full_node(self, key: int, node: BTreeNode, parent_node: BTreeNode, node_idx_in_parent: ChildIndex) -> BTreeNode:
        """ Breaks up a full node and returns the node that is appropriate for the key
        """
        key_arrs, child_arrs = node.split_node_arrays()
        key_to_promote = key_arrs[1][0]
        l_child, r_child = child_arrs
        parent_node.known_single_key_insert(key=key_to_promote, child_idx=node_idx_in_parent, l_child=l_child, r_child=r_child)
        



    def _set_root(self, node: BTreeNode) -> None:
        assert len(self.root.get_keys_array()) == 0
        self.root = node
        node._root = True


    def create_node_w_arrs(self, child_arrs: list[BTreeChildrenArray|BTreeNode], key_arrs: list[BTreeKeysArray|int]) -> BTreeNode:
        """ Creates a child node at the 
        """
        new_child_arr = []
        for arr in child_arrs:
            new_child_arr += arr

        new_keys_arr = []
        for arr in key_arrs:
            new_keys_arr += arr
        
        assert len(new_keys_arr) == len(new_child_arr) - 1

        new_node = BTreeNode(t_val=self.t_val, is_root=False)
        new_node.set_keys_children(keys=new_keys_arr, children=new_child_arr)

        return new_node


        
    def delete_key(self, key: int) -> None:
        """ Deletes a key from the BTree
        """

