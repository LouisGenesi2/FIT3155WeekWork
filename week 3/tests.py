import unittest
from boyer_moore import boyer_moore

class TestBoyerMoore(unittest.TestCase):
    def test_exact_match(self):
        """Test case where the pattern matches exactly at the start."""
        text = "abcdefghij"
        pattern = "abc"
        self.assertEqual(boyer_moore(pattern, text), [2])
    
    def test_no_match(self):
        """Test case where the pattern does not exist in the text."""
        text = "abcdefghij"
        pattern = "xyz"
        self.assertEqual(boyer_moore(pattern, text), [])
    
    def test_bad_character_rule(self):
        """Test case where bad character rule should trigger a jump."""
        text = "abcxabcd"
        pattern = "abcd"
        self.assertEqual(boyer_moore(pattern, text), [7])
    
    def test_good_suffix_rule(self):
        """Test case where good suffix heuristic should trigger a jump."""
        text = "mississipi"
        pattern = "issipi"
        self.assertEqual(boyer_moore(pattern, text), [9])
    
    def test_matched_prefix_rule(self):
        """Test case where matched prefix heuristic should be used."""
        text = "abababababa"
        pattern = "ababa"
        self.assertEqual(boyer_moore(pattern, text), [4, 6, 8, 10])
    
    def test_multiple_occurrences(self):
        """Test case where the pattern appears multiple times."""
        text = "abcdabcdabcd"
        pattern = "abcd"
        self.assertEqual(boyer_moore(pattern, text), [3, 7, 11])
    
    def test_partial_overlap(self):
        """Test case where the pattern partially overlaps with itself."""
        text = "aaaabaaab"
        pattern = "aaab"
        self.assertEqual(boyer_moore(pattern, text), [4, 8])
    
    def test_pattern_longer_than_text(self):
        """Test case where pattern is longer than text."""
        text = "abc"
        pattern = "abcd"
        self.assertEqual(boyer_moore(pattern, text), [])
    
    def test_single_character_text(self):
        """Test case where the text consists of a single character."""
        text = "a"
        pattern = "a"
        self.assertEqual(boyer_moore(pattern, text), [0])
    
    def test_single_character_pattern(self):
        """Test case where the pattern consists of a single character occurring multiple times."""
        text = "aaaaaa"
        pattern = "a"
        self.assertEqual(boyer_moore(pattern, text), [0, 1, 2, 3, 4, 5])
    
    def test_pattern_at_end(self):
        """Test case where the pattern appears at the very end of the text."""
        text = "xyzabc"
        pattern = "abc"
        self.assertEqual(boyer_moore(pattern, text), [5])
    
    def test_pattern_at_end_with_partial_overlap(self):
        """Test case where the pattern partially overlaps and ends at the last character."""
        text = "aaaaab"
        pattern = "aab"
        self.assertEqual(boyer_moore(pattern, text), [5])
    
    def test_empty_text(self):
        """Test case where text is empty."""
        text = ""
        pattern = "abc"
        self.assertEqual(boyer_moore(pattern, text), [])
    
    def test_empty_pattern(self):
        """Test case where pattern is empty."""
        text = "abcdefghij"
        pattern = ""
        self.assertEqual(boyer_moore(pattern, text), [])
    
    def test_pattern_same_as_text(self):
        """Test case where the pattern is exactly the same as the text."""
        text = "abc"
        pattern = "abc"
        self.assertEqual(boyer_moore(pattern, text), [2])
    
    def test_out_of_bounds_pattern(self):
        """Test case where the pattern is longer than the text, ensuring no out-of-bounds errors occur."""
        text = "abc"
        pattern = "abcdefg"
        self.assertEqual(boyer_moore(pattern, text), [])
    
    def test_large_text(self):
        """Test case with a large input text to check efficiency and correctness."""
        text = "a" * 1000 + "abc" + "a" * 1000
        pattern = "abc"
        self.assertEqual(boyer_moore(pattern, text), [1002])

if __name__ == "__main__":
    unittest.main()