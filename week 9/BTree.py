from typing import Generic, TypeVar, Callable, List, Optional, Sequence, Iterable, Iterator
from abc import abstractmethod
import random

def bisect_left(arr: list[int], key: int) -> int:
    """ Returns the first index where value is larger than or equal to the key.
    """
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < key:
            lo = mid + 1
        else:
            hi = mid
    return lo

def bisect_right(arr:list[int], key: int) -> int:
    """ Returns the first index where the value is strictly larger than the key
    """
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] <= key:
            lo = mid + 1
        else:
            hi = mid
    return lo


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
    
    def __setitem__(self, idx: KeyIndex, val: int) -> None:
        assert isinstance(idx, KeyIndex)
        assert isinstance(val, int)
        self.arr[idx] = val

    def get_arr(self) -> list[int]:
        return self.arr
    
    def set_arr(self, arr: list[int]) -> None:
        self.arr = arr
    
    def __len__(self) -> int:
        return len(self.get_arr())
    
    def get_travel_insertion_idx(self, item: int) -> ChildIndex:
        """ returns the idx that if done on an internal node, is where to travel,
            and if a leaf, is where to insert 
        """
        return ChildIndex(bisect_right(self.get_arr(), item))
    
    def get_travel_deletion_idx(self, item: int) -> ChildIndex|KeyIndex:
        """ used during deletion during travel.
            returns ChildIndex if found direction to go, KeyIndex if key found
        """
        arr = self.get_arr()
        key_pos_idx = bisect_left(arr, item)
        if key_pos_idx > len(arr) - 1:
            return ChildIndex(key_pos_idx) # signals to keep travelling; implicitly adjusted for right child
        if arr[key_pos_idx] > item:
            return ChildIndex(key_pos_idx) # signals to keep travelling
        if arr[key_pos_idx] == item:
            return KeyIndex(key_pos_idx) # signals it was found
        

        raise AssertionError('No travel index found')
    
    def get_insertion_location(self, item: int) -> KeyIndex:
        """ returns where key should go. This includes after the end of the current array
        """
        return KeyIndex(bisect_right(self.get_arr(), item))
        
    def get_deletion_key_loc(self, item: int) -> KeyIndex:
        """ returns where key is found, used for deletion
        """
        return KeyIndex(bisect_left(self.get_arr(), item))
    
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
        assert isinstance(idx, KeyIndex)
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
        arr = self.get_arr()
        item = arr.pop(idx)
        self.set_arr(arr)
        return item
    
    def __iter__(self) -> Iterator[int|None]:
        return iter(self.get_arr())
    
class BTreeChildrenArray:
    def __init__(self, t_val: int, init_arr: 'list[BTreeNode|None]' = [None]) -> None:
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
        arr = self.get_arr()
        item = arr.pop(idx)
        self.set_arr(arr)
        return item

    def __setitem__(self, idx: ChildIndex, val: 'BTreeNode|None') -> None:
        assert isinstance(idx, ChildIndex)
        assert isinstance(val, BTreeNode) or val is None
        self.arr[idx.get_val()] = val

    def __getitem__(self, idx: ChildIndex) -> 'BTreeNode|None':
        assert isinstance(idx, ChildIndex)
        item = self.get_arr()[idx]
        return item
    
    def __len__(self) -> int:
        return len(self.get_arr())
    
    def slice(self, start_idx: ChildIndex, end_idx: ChildIndex) -> 'BTreeChildrenArray':
        """ returns slice of self
        """
        assert isinstance(start_idx, ChildIndex) and isinstance(end_idx, ChildIndex)
        return BTreeChildrenArray(self.get_t_val(), self.get_arr()[start_idx:end_idx])
    
    def insert_at_pos(self, child: 'BTreeNode|None', idx: ChildIndex) -> None:
        """ Inserts children at idxs.
            Children are the children to insert. idx are the positions to insert them at.
        """
        new_arr = self.get_arr()[0:idx] + [child] + self.get_arr()[idx:]
        self.set_arr(new_arr)

    def __add__(self, other_arr: 'BTreeChildrenArray|list[BTreeNode]') -> 'BTreeChildrenArray':
        if isinstance(other_arr, BTreeChildrenArray):
            new_arr = self.arr + other_arr.arr
        elif isinstance(other_arr, list):
            new_arr = self.arr + other_arr
        else:
            raise TypeError
        assert len(new_arr) <= self.get_max()
        return BTreeChildrenArray(self.get_t_val(), new_arr)
    
    def __iter__(self) -> 'Iterator[BTreeNode|None]':
        return iter(self.get_arr())


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
        assert len(keys) == len(children) - 1
        self._children_array = children
        self._keys_array = keys

    def get_t_val(self) -> int:
        return self.t_val

    def is_full(self) -> bool:
        assert len(self.get_keys_array()) <= self.get_t_val() * 2 - 1   # should never exceed max
        assert len(self.get_children_array()) <= self.get_t_val() * 2
        assert len(self.get_children_array()) == len(self.get_keys_array()) + 1
        return len(self.get_keys_array()) == self.get_t_val() * 2 - 1

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
        return self.get_child(idx), idx
    
    def key_idx_to_l_child_idx(self, idx: KeyIndex) -> ChildIndex:
        return ChildIndex(idx.get_val())
    
    def key_idx_to_r_child_idx(self, idx: KeyIndex) -> ChildIndex:
        return ChildIndex(idx.get_val() + 1)

    def insert_key(self, key: int, child: 'BTreeNode|None') -> int:
        """ Inserts a key into the keys array, and adjusts children array appropriately
        """
        assert self.is_leaf()
        self.get_keys_array()

    def extend_keys(self, key: int, r_child: 'BTreeNode|None') -> None:
        """ Adds key and child to end of self
        """
        assert isinstance(r_child, BTreeNode) or r_child is None
        self.get_keys_array().get_arr().append(key)
        self.get_children_array().get_arr().append(r_child)

    def replace_child(self, new_child: 'BTreeNode|None', pos: ChildIndex) -> 'BTreeNode|None':
        """ replaces child stored at index. Returns old child stored
        """
        old_child = self.get_children_array()[pos]
        self.get_children_array()[pos] = new_child
        return old_child

    def known_single_key_insert(self, key: int, l_child: 'BTreeNode|None', idx_to_insert: KeyIndex) -> None:
        """ Handles key insertion. Insertion is always between existing keys. Use extend_keys for appending a new key to the end.
            l_child can be BTreeChildrenArray(init=[None]) or BTreeChildrenArray(init=[<BTreeNode>]) for inserting an empty child or node
        """
        assert isinstance(idx_to_insert, KeyIndex)

        # in case where insertion is an extension, must use extension
        if idx_to_insert.get_val() > len(self.get_keys_array()) - 1:
            raise ValueError('known_single_key_insert cannot be used for extensions')
        # An insertion must have exactly one child inserted. 
        assert isinstance(l_child, BTreeNode) or l_child is None
        keys = self.get_keys_array()
        keys.insert_at_pos(key, idx_to_insert)

        l_child_idx = idx_to_insert.to_l_child()
        r_child_idx = idx_to_insert.to_r_child()

        # add child
        children = self.get_children_array()
        
        children.insert_at_pos(l_child, l_child_idx)

        
   
    def transform_to_internal(self) -> None:
        self.leaf = False

    def transform_to_leaf(self) -> None:
        self.leaf = True

    def _split_node_arrays(
        self
    ) -> tuple[tuple[BTreeKeysArray,BTreeKeysArray,BTreeKeysArray],
               tuple[BTreeChildrenArray,BTreeChildrenArray]]:
        """ Splits node arrays into 3. Used whenever stepping on full node
        """
        assert self.is_full()   # should always be done when full
        t_val = self.get_t_val()

        # split child array into 2
        c_idx1, c_idx2, c_idx3 = ChildIndex(0), ChildIndex(t_val), ChildIndex(2*t_val+1)
        c_arr1, c_arr2 = self.get_children_array().slice(c_idx1, c_idx2),  self.get_children_array().slice(c_idx2,c_idx3)

        # split key array into 3
        k_idx1, k_idx2, k_idx3, k_idx4 = KeyIndex(0), KeyIndex(t_val - 1), KeyIndex(t_val), KeyIndex(2*t_val)
        k_arr1, k_arr2, k_arr3 = self.get_keys_array().slice(k_idx1, k_idx2), BTreeKeysArray(t_val, [self.get_keys_array()[k_idx2]]), self.get_keys_array().slice(k_idx3, k_idx4)

        assert len(c_arr1) == len(k_arr1) + 1 and len(c_arr2) == len(k_arr3) + 1
        return (
            (k_arr1, k_arr2, k_arr3),
            (c_arr1, c_arr2)  
        )

    def is_minimum(self) -> bool:
        assert len(self.get_keys_array()) >= self.get_t_val() - 1 or self._root == True
        return len(self.get_keys_array()) == self.get_t_val() - 1
        
    def pop(self, pos: KeyIndex, child_to_pop: ChildIndex) -> 'tuple[int, BTreeNode]':
        """ Removes the given position from the Node
        """
        # child popped should always be a neighbour
        assert abs(child_to_pop.get_val() - pos.get_val()) <= 1

        key = self.get_keys_array().pop(pos)
        child = self.get_children_array().pop(child_to_pop)
        return key, child

    def replace_key(self, pos: KeyIndex, key: int) -> int:
        """ Replaces key at position, returns old key
        """
        assert isinstance(pos, KeyIndex)
        keys = self.get_keys_array()
        old_key = keys[pos]
        keys[pos] = key
        return old_key
    
    
    

        


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
        try:
            leaf = self._get_to_leaf_insertion(key, self.get_root())
            idx_to_insert = leaf.get_keys_array().get_insertion_location(key)
            
            if idx_to_insert.get_val() <= len(leaf.get_keys_array()) - 1:
                leaf.known_single_key_insert(key=key, idx_to_insert=idx_to_insert, l_child=None)
            else:
                leaf.extend_keys(key, None)
        except Exception as e:
            raise Exception(f'Error inserting {key}, {e}')


    def del_val(self, key: int) -> None:
        pass

    def _get_to_leaf_insertion(self, key: int, pos: BTreeNode) -> BTreeNode:
        """ Given a key, get to the appropriate leaf
        """
        # edge case, root is leaf and is full
        if pos.is_full():
            pos = self._break_full_node(key=key, node=pos, parent_node=None, node_idx_in_parent=None)
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
        initial_child = parent.get_child(child_idx)

        child = initial_child
        while (not child.is_leaf()) and child.get_child(ChildIndex(0)) is not None:
            child = child.get_child(ChildIndex(0))
        successor = child.get_keys_array()[KeyIndex(0)]

        parent_key = parent.replace_key(key_idx, successor)
        # child.replace_key(KeyIndex(0), parent_key)

        
        self.delete_key(successor, initial_child)

        return initial_child

    def _swap_inorder_predecessor(self, parent: BTreeNode, key_idx: KeyIndex) -> BTreeNode:
        """ Swap key at key_idx with inorder predecessor. Returns the Node which previously contained the predecessor
        """
        child_idx = key_idx.to_l_child()
        initial_child = parent.get_child(child_idx)
        
        child = initial_child
        while (not child.is_leaf()) and child.get_child(ChildIndex(len(child.get_children_array()) - 1)) is not None:
            child_largest_child_idx = ChildIndex(len(child.get_children_array()) - 1)
            child = child.get_child(child_largest_child_idx)
        
        child_largest_idx = KeyIndex(len(child.get_keys_array()) - 1)
        predecessor = child.get_key(child_largest_idx)
        
        parent_key = parent.replace_key(key_idx, predecessor)
        # child.replace_key(child_largest_idx, parent_key)

        self.delete_key(predecessor, initial_child)
        return initial_child

    def _consolidate_parent(self, l_child: BTreeNode, r_child: BTreeNode, parent: BTreeNode, key_idx: KeyIndex) -> BTreeNode:
        """ Combines l_child and r_child, and key from parent identified with key_idx. Handles root deletion edge case
        """
        l_child_keys = l_child.get_keys_array()
        l_child_children = l_child.get_children_array()
        r_child_keys = r_child.get_keys_array()
        r_child_children = r_child.get_children_array()
        parent_key_wrapped = [parent.get_key(key_idx)]
        
        # remove parent key from parent
        parent_key, parent_child = parent.pop(key_idx, key_idx.to_r_child())

        consolidated_node = self.create_node_w_arrs(child_arrs = [l_child_children, r_child_children], key_arrs=[l_child_keys, parent_key_wrapped, r_child_keys])

        if parent._root is True and len(parent.get_keys_array()) == 0:
            self._set_root(consolidated_node)
        else:
            parent.replace_child(consolidated_node, key_idx.to_l_child())
        
        if  not l_child.is_leaf() or not r_child.is_leaf():
            consolidated_node.transform_to_internal()

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
        # rotate sibling into parent and get old key
        parent_key = parent.replace_key(key_idx, r_sibling_key)

        # rotate parent key into l_sibling, right child is the left child of former right sibling
        next_pos.extend_keys(key=parent_key, r_child=r_sibling_l_child)

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
        l_sibling_size = len(l_sibling.get_keys_array()) - 1
        l_sibling_key, l_sibling_r_child = l_sibling.pop(KeyIndex(l_sibling_size), KeyIndex(l_sibling_size).to_r_child())
        
        # rotate left sibling into parent and get old parent key
        parent_key = parent.replace_key(key_idx, l_sibling_key)

        # rotate parent key into r_sibling, left child is the right child of former left sibling
        next_pos.known_single_key_insert(key=parent_key, l_child=l_sibling_r_child, idx_to_insert=KeyIndex(0))

        return next_pos

    def _get_siblings(self, parent: BTreeNode, child_index: ChildIndex) -> list[BTreeNode|None]:
        """ Gets siblings of children.
        """
        siblings = []
        if child_index.get_val() > 0:
            l_child_idx = ChildIndex(child_index.get_val() - 1)
            siblings.append(parent.get_child(l_child_idx))
        else:
            siblings.append(None)
        
        if child_index.get_val() < len(parent.get_children_array()) - 1:
            r_child_idx = ChildIndex(child_index.get_val() + 1)
            siblings.append(parent.get_child(r_child_idx))
        else:
            siblings.append(None)

        return siblings

    
    def _resolve_deletion_rule(self, key: int, pos: BTreeNode) -> BTreeNode|bool:
        """ Given an internal node, check through all deletion cases and return where
            to continue traversal to leaf from, or False if deletion must stop (due to case 2 deletion)
        """
        
        travel_idx = pos.get_keys_array().get_travel_deletion_idx(key)
        
        # key found in internal node
        if isinstance(travel_idx, KeyIndex):
            # case 2

            r_child = pos.get_child(travel_idx.to_r_child())
            l_child = pos.get_child(travel_idx.to_l_child())
            
            if l_child is not None:
                if l_child.is_minimum() is False:
                    self._swap_inorder_predecessor(parent=pos, key_idx=travel_idx)
                    return False
            
            if r_child is not None:
                if r_child.is_minimum() is False:
                    self._swap_inorder_successor(parent=pos, key_idx=travel_idx)
                    return False
            
            if l_child is not None and r_child is not None:
                if l_child.is_minimum() and r_child.is_minimum():
                    next_pos = self._consolidate_parent(l_child=l_child, r_child=r_child, parent=pos, key_idx=travel_idx)
                    
                    return next_pos
        
        assert isinstance(travel_idx, ChildIndex)
        next_pos_child_idx_in_parent = travel_idx
        next_pos = pos.get_child(next_pos_child_idx_in_parent)
        if next_pos.is_minimum():
            # case 3 - find a sibling and apply a rule
            l_sibling, r_sibling = self._get_siblings(pos, next_pos_child_idx_in_parent)


            # adjust index for correct key 
            if next_pos_child_idx_in_parent.get_val() == len(pos.get_children_array()) - 1:
                idx_to_insert = KeyIndex(next_pos_child_idx_in_parent.get_val() - 1)
                index_between_l_sibling = KeyIndex(idx_to_insert.get_val())
            else:
                idx_to_insert = KeyIndex(next_pos_child_idx_in_parent.get_val())
                index_between_l_sibling = KeyIndex(idx_to_insert.get_val() - 1)

            if r_sibling is not None:
                if r_sibling.is_minimum():
                    next_pos = self._consolidate_parent(l_child=next_pos, r_child=r_sibling, parent=pos, key_idx=idx_to_insert)
                    
                    return next_pos
                
            if l_sibling is not None:
                if l_sibling.is_minimum():
                    
                    next_pos = self._consolidate_parent(l_child=l_sibling, r_child=next_pos, parent=pos, key_idx=index_between_l_sibling)
                    
                    return next_pos
                
            if r_sibling is not None:
                next_pos = self._r_sibling_rotate(parent=pos, key_idx=idx_to_insert)
                
                return next_pos
            if l_sibling is not None:
                next_pos = self._l_sibling_rotate(parent=pos, key_idx=idx_to_insert)
                
                return next_pos

        # case 1
        return next_pos



    def _get_to_leaf_deletion(self, key: int, pos: BTreeNode) -> BTreeNode|bool:
        """ Given a key, delete it from the Tree. Returns False if deletion should be stopped (already done under rule 2)
        """
        while not pos.is_leaf():
            pos = self._resolve_deletion_rule(pos=pos, key=key)
            if pos is False:
                return False
        return pos
        
    
    def _break_full_node(self, key: int, node: BTreeNode, parent_node: BTreeNode|None, node_idx_in_parent: ChildIndex|None) -> BTreeNode:
        """ Breaks up a full node and returns the node that is appropriate for the key
        """
        assert ( isinstance(parent_node, BTreeNode) and isinstance(node_idx_in_parent, ChildIndex) ) or ( parent_node is None and node_idx_in_parent is None and node._root)
        
        key_arrs, child_arrs = node._split_node_arrays()
        key_to_promote = key_arrs[1][KeyIndex(0)] # middle array is always a single item
        l_children, r_children = child_arrs

        # initialise new nodes
        l_child_node = BTreeNode(t_val=self.t_val, is_root=False)
        l_child_node.set_keys_children(keys=key_arrs[0], children=l_children)
        r_child_node = BTreeNode(t_val=self.t_val, is_root=False)
        r_child_node.set_keys_children(keys=key_arrs[2], children=r_children)

        if not node.is_leaf():
            l_child_node.transform_to_internal()
            r_child_node.transform_to_internal()
        
        if parent_node is not None:
            # edge case, promoting to right end of parent
            if node_idx_in_parent.get_val() == len(parent_node.get_children_array()) - 1:
                parent_node.extend_keys(key=key_to_promote, r_child=r_child_node)
                old_pointer = parent_node.replace_child(new_child=l_child_node, pos=node_idx_in_parent)
            else:
                parent_node.known_single_key_insert(key=key_to_promote, idx_to_insert=KeyIndex(node_idx_in_parent.get_val()), l_child=l_child_node)
                # fix right child pointer
                old_pointer = parent_node.replace_child(new_child=r_child_node, pos = ChildIndex(node_idx_in_parent.get_val() + 1))
            assert old_pointer is node # sanity check
        else:
            # case where breaking up root
            new_root = BTreeNode(t_val=self.t_val, is_root=True)
            new_root.set_keys_children(keys=BTreeKeysArray(t_val=self.t_val, init_arr=[key_arrs[1].get_arr()[0]]), children=BTreeChildrenArray(t_val=self.t_val, init_arr=[l_child_node, r_child_node]))
            new_root.transform_to_internal()
            self._set_root(new_root)
        
        if key < key_to_promote:
            return l_child_node
        elif key > key_to_promote:
            return r_child_node
        raise AssertionError()    # key should not already be in tree

            
        



    def _set_root(self, node: BTreeNode) -> None:
        self.root = node
        node._root = True


    def create_node_w_arrs(self, child_arrs: list[BTreeChildrenArray|BTreeNode], key_arrs: list[BTreeKeysArray|int]) -> BTreeNode:
        """ Creates a Node using children and keys in order. Used during deletion consolidate/ case 2c
        """
        new_child_arr = []
        for arr in child_arrs:
            new_child_arr += arr

        new_keys_arr = []
        for arr in key_arrs:
            new_keys_arr += arr
        
        assert len(new_keys_arr) == len(new_child_arr) - 1
        new_keys = BTreeKeysArray(t_val=self.t_val, init_arr=new_keys_arr)
        new_children = BTreeChildrenArray(t_val=self.t_val, init_arr=new_child_arr)
        new_node = BTreeNode(t_val=self.t_val, is_root=False)
        new_node.set_keys_children(keys=new_keys, children=new_children)

        return new_node


        
    def delete_key(self, key: int, pos: BTreeNode|str = 'root') -> None:
        """ Deletes a key from the BTree
        """
        try:
            if pos == 'root':
                pos = self.get_root()

            leaf = self._get_to_leaf_deletion(key, pos)
            if leaf is False:
                return None
            key_idx = leaf.get_keys_array().get_deletion_key_loc(key)
            assert leaf.get_key(key_idx) == key
            leaf.pop(key_idx, key_idx.to_r_child())
        except Exception as e:
            raise Exception(f'Error deleting {key}, {e}')

    def retrieve_keys_in_range(self, start_range_1_indexed: int, end_range_1_indexed: int) -> list[int]:
        """ Retrieves keys in range in order 
        """
        pos = self.get_root()
        all_keys = self.accumulate_keys(pos, [])
        return all_keys[start_range_1_indexed - 1: end_range_1_indexed]
    
    def accumulate_keys(self, pos: BTreeNode, acc: list[int]) -> list[int]:
        
        for idx, child_node in enumerate(pos.get_children_array().get_arr()):
            if isinstance(child_node, BTreeNode):
                self.accumulate_keys(child_node, acc)
            if idx != len(pos.get_children_array().get_arr()) - 1:
                acc.append(pos.get_keys_array().get_arr()[KeyIndex(idx)])
        return acc

def unique_random_ints(n: int,
                       pool: Optional[Iterable[int]] = None) -> List[int]:
    """
    Return `n` distinct random integers.

    Parameters
    ----------
    n : int
        How many integers to draw (must be ≥ 0).
    pool : Iterable[int] | None, default None
        Collection to sample from.  If None, the function uses
        `range(0, max(10, n) * 10)`, which is always large enough
        to supply `n` unique picks.

    Returns
    -------
    List[int]
        A list of `n` unique integers in random order.

    Raises
    ------
    ValueError
        If `n` exceeds the size of the (deduplicated) pool.
    TypeError
        If the pool contains non-integers.

    Examples
    --------
    >>> unique_random_ints(5)
    [18, 3, 71, 24, 55]

    >>> unique_random_ints(3, [10, 20, 30, 40])
    [40, 20, 10]
    """
    if n < 0:
        raise ValueError("`n` must be non-negative")

    # Build a candidate population.
    if pool is None:
        population: Sequence[int] = range(0, max(10, n) * 10)
    else:
        # Convert to list once; also deduplicate so “no repeats” is possible.
        population = list(dict.fromkeys(pool))          # keeps left-most order
        if not all(isinstance(x, int) for x in population):
            raise TypeError("All elements in `pool` must be integers")

    if n > len(population):
        raise ValueError(
            f"Cannot draw {n} unique values from a pool of size {len(population)}"
        )

    return random.sample(population, k=n)

def assert_tree_invariants(tree: BTree, vals, dels, **kwargs) -> bool:
    stored_keys = tree.retrieve_keys_in_range(1,100000)
    assert len(stored_keys) == len(set(stored_keys))
    assert len(stored_keys) == len(vals) - len(dels)
    for idx, val in enumerate(stored_keys[:-1]):
        assert val < stored_keys[idx + 1]
    
    pos = tree.get_root()
    check_leaf_status(pos)

    return True

def check_leaf_status(pos: BTreeNode) -> bool:
    for element in pos.get_children_array().get_arr():
        if element is not None:
            assert not pos.is_leaf()
            check_leaf_status(element)
    return True

if __name__=='__main__':
    random.seed(3)
    tree = BTree(t_val=50)
    vals_to_insert=unique_random_ints(1000)
    insertions = []
    n_delete = 100
    deletions = []
    for idx, val in enumerate(vals_to_insert):
        tree.insert(val)
        insertions.append(val)
        # if idx % 100 == 0:
        #     assert_tree_invariants(tree, insertions, [], insert=val)
        
    for i in range(n_delete):
        to_delete = random.choice(vals_to_insert)
        # edge case 1906
        deletions.append(to_delete)
        vals_to_insert = list(set(vals_to_insert) - set(deletions))
        tree.delete_key(to_delete)
        # assert assert_tree_invariants(tree, insertions, deletions, del_val = to_delete)
        
    
    
    stored_keys = tree.retrieve_keys_in_range(1,1000000)
    for val in vals_to_insert:
        assert val in stored_keys

    for deletion in deletions:
        assert deletion not in stored_keys
    
    assert assert_tree_invariants(tree, insertions, deletions, end=True)


