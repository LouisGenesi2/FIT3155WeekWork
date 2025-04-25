from collections.abc import Iterator
import typing
T = typing.TypeVar('T')

class CharTable(typing.Generic[T]):
    ascii_min = 0
    ascii_max = 127
    
    def __init__(self) -> None:
        self.array: list[None|T] = [None for _ in range(128)]
        self.ascii_range = 0
    
    def _get_char_index(self, char: str) -> int:
        return ord(char)
    
    def __getitem__(self, char: str) -> T:
        return_val = self.array[self._get_char_index(char)]
        if return_val is None:
            raise IndexError(f'There is nothing assigned at index {char}')
        return return_val

    def __setitem__(self, char: str, value: T) -> None:
        self.array[self._get_char_index(char)] = value


class CharFreqTable(CharTable):

    def add_char(self, char):
        self[char] = self[char] + 1
    
    def get_sorted(self):
        return SortedCharFreqTable(self.array)

class SortedCharFreqTable(Iterator):
    def __init__(self, array: list):
        map_func: typing.Callable[[str, int], tuple[int, int]] = lambda idx, val: (val, ord(idx)) #TODO: fix
        map(map_func, enumerate(array))
        
        extract_tuple_func: typing.Callable[[tuple[int, int], int]] = lambda tuple: tuple[0]
        array.sort(key=extract_tuple_func)
        
        self.array: list[tuple[int, str]] = array
    
    def pop_max(self) -> tuple[int,str]:
        return self.array.pop()
    
    def next(self):
        for _ in range(len(self.array)):
            self.pop_max()
        raise StopIteration