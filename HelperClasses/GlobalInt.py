class GlobalInt:
    def __init__(self, value: int):
        self.value: int = value
    
    def increment_value(self):
        self.value += 1

    def get_value(self) -> int:
        return self.value
    
    def __int__(self) -> int:
        return self.value

    def __eq__(self, other):
        return self.value == int(other)

    def __ne__(self, other):
        return self.value != int(other)

    def __lt__(self, other):
        return self.value < int(other)

    def __le__(self, other):
        return self.value <= int(other)

    def __gt__(self, other):
        return self.value > int(other)

    def __ge__(self, other):
        return self.value >= int(other)

    
    def __sub__(self, other) -> int:
        return self.value - int(other)
    
    def __add__(self, other) -> int:
        return self.value + int(other)
