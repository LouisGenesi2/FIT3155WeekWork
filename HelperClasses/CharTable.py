from collections import Iterator

class CharTable:
    ascii_min = 0
    ascii_max = 127
    
    def __init__(self):
        self.array = [0 for _ in range(128)]
        self.ascii_range = 0
    
    def _get_char_index(self, char):
        return ord(char)
    
    def __getitem__(self, char) -> str:
        return self.array[self._get_char_index(char)]

    def __setitem__(self, char):
        self.array[self._get_char_index(char)]


class CharFreqTable(CharTable):

    def add_char(self, char):
        self[char] = self[char] + 1
    
    def get_sorted(self):
        return SortedCharFreqTable(self.array)

class SortedCharFreqTable(Iterator):
    def __init__(self, array: list):
        map(lambda idx, val: (val, ord(idx)), enumerate(array))
        array.sort(key=lambda tuple: tuple[0])
        self.array: list[tuple[int, str]] = array
    
    def pop_max(self) -> tuple[int,str]:
        self.array.pop()
    
    def next(self):
        for _ in range(len(self.array)):
            self.pop_max()
        raise StopIteration