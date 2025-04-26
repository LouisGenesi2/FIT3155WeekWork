"""test_skip_count.py

Unit tests for the private helper **UkkonenTree._skip_count** written with the
standard‑library **unittest** framework.  No third‑party test runner is
needed – you can simply run:

```bash
python -m unittest test_skip_count.py -v
```

These tests create very small, hand‑crafted suffix‑tree fragments so we can
exercise the helper in isolation without running the full construction
algorithm.
"""

import unittest
from typing import Tuple

# Local imports --------------------------------------------------------------
from Ukkonen import UkkonenTree
from node import CharNode, Node, UkkonenEdge


# ---------------------------------------------------------------------------
# Utility builders -----------------------------------------------------------
# ---------------------------------------------------------------------------


def _add_root_edge(
    tree: UkkonenTree,
    label_start: int,
    label_end: int,
    dest: CharNode | Node,
) -> UkkonenEdge:
    """Attach a single edge (label `s[label_start:label_end+1]`) to the root and
    return it."""
    first_letter = tree.strings[0][label_start]
    tree.root.add_UkkonenEdge(first_letter, (label_start, label_end), dest, 0)
    return tree.root.get_UkkonenEdge(first_letter)


def _make_minimal_tree(string: str, edge_span: Tuple[int, int]) -> Tuple[UkkonenTree, UkkonenEdge, CharNode]:
    """Return a minimal tree whose root has exactly *one* explicit edge whose
    label spans *edge_span* (inclusive) in *string*.

    The edge points to an internal `CharNode` which itself has a single leaf
    so that it really is an internal node.
    """
    tree = UkkonenTree()
    tree.strings = [string]
    tree._set_curr_string_id(0)

    internal = CharNode()
    # child leaf so the internal node is not a leaf itself
    next_index = edge_span[1] + 1
    if next_index < len(string):
        internal.add_UkkonenEdge(
            string[next_index],
            (next_index, next_index),
            Node(is_leaf=True),
            0,
        )

    edge = _add_root_edge(tree, edge_span[0], edge_span[1], internal)
    return tree, edge, internal


# ---------------------------------------------------------------------------
# Test‑cases -----------------------------------------------------------------
# ---------------------------------------------------------------------------

class TestSkipCount(unittest.TestCase):
    """Behavioural tests for UkkonenTree._skip_count."""

    # 1. Traversing an edge completely ---------------------------------------
    def test_full_edge_traversal(self):
        """Walking exactly the edge label should land on its child and leave no
        characters untraversed."""
        tree, edge, child = _make_minimal_tree("ab$", (0, 0))  # edge label = "a"

        node, rel_edge, rel_idx, amt_left = tree._skip_count(tree.root, (0, 0))

        self.assertIs(node, child)            # arrived at the child node
        self.assertIsNone(rel_edge)           # no partial edge left
        self.assertIsNone(rel_idx)
        self.assertEqual(amt_left, 0)         # nothing left to traverse

    # 2. Direction missing under the current node ----------------------------
    def test_missing_direction_returns_none_edge(self):
        """If the first letter is absent under the current node, _skip_count
        should return (curr_node, None, None, len(substr))."""
        tree, _edge, _child = _make_minimal_tree("ab$", (0, 0))

        # '$' lives at index 2 in the string but there is *no* edge '$' under root
        node, rel_edge, rel_idx, amt_left = tree._skip_count(tree.root, (2, 2))

        self.assertIs(node, tree.root)
        self.assertIsNone(rel_edge)
        self.assertIsNone(rel_idx)
        self.assertEqual(amt_left, 1)  # full length still to walk

    # 3. Stopping in the middle of an edge after a mismatch ------------------
    def test_stop_mid_edge_on_mismatch(self):
        """When the substring deviates part‑way through the current edge,
        _skip_count should return that edge together with the index of the last
        matched character and the remaining length still to travel."""
        # Build a root edge labelled "ab"  – indices (0, 1)
        tree, edge, _child = _make_minimal_tree("aba$", (0, 1))

        # Substring starts at the *second* 'a' – it matches 'a' but mismatches
        # on the next character ('b' vs '$').
        substring = (2, 3)  # "a$"
        node, rel_edge, rel_idx, amt_left = tree._skip_count(tree.root, substring)

        self.assertIs(node, tree.root)        # still at the root
        self.assertIs(rel_edge, edge)         # we are inside the same edge
        # rel_idx should point at the position of the mismatch (index 1 in string)
        self.assertLess(rel_idx, edge.get_values()[1])
        self.assertGreater(amt_left, 0)       # at least one char still to go


if __name__ == "__main__":
    unittest.main()
