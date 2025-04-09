class GlobalInt:
    def __init__(self, value: int):
        self.value: int = value
    
    def increment_value(self):
        self.value += 1

    def get_value(self) -> int:
        return self.value

    def __eq__(self, other):
        return self.value == self._check_if_GlobalInt(other)

    def __ne__(self, other):
        return self.value != self._check_if_GlobalInt(other)

    def __lt__(self, other):
        return self.value < self._check_if_GlobalInt(other)

    def __le__(self, other):
        return self.value <= self._check_if_GlobalInt(other)

    def __gt__(self, other):
        return self.value > self._check_if_GlobalInt(other)

    def __ge__(self, other):
        return self.value >= self._check_if_GlobalInt(other)

    def _check_if_GlobalInt(self, other):
        return other.value if isinstance(other, GlobalInt) else other
