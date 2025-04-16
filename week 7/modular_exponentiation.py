import typing
import math

class ModuloArray:
    def __init__(self, initial_value, base, power, mod):
        self.array = [initial_value]
        self.endsone = False
        self.base = base
        self.power = power
        self.mod = mod

    def append(self, int: int):
        self.array.append(int)

    def __getitem__(self, idx) -> int:
        if idx > len(self.array) - 1:
            if self.get_ends_one():
                return 1
            else:
                raise IndexError("Modulo not calculated")
        return self.array[idx]
    
    def __setitem__(self, idx: int, val: int):
        if val == 1:
            self.set_ends_one()
        self.array[idx] = val

    def __len__(self):
        if self.get_ends_one():
            return math.inf
        else:
            return len(self.array)

    def set_ends_one(self):
        self.endsone = True

    def get_ends_one(self):
        return self.endsone
    
    def get_mod(self) -> int:
        return self.mod

def get_bitarray_backwards(power: int) -> list[typing.Literal[0,1]]:
    bitarray = []
    curr = power if power % 2 == 1 else power / 2
    while curr > 0:
        floor = curr // 2
        remainder = curr %2
        bitarray.append(remainder)
        curr = floor
    
    
    return bitarray

def get_bitarray_forwards(power: int) -> list[typing.Literal[0,1]]:
    return reversed(get_bitarray_backwards(power))


def get_modular_exponents(bitarray: list[typing.Literal[0,1]]) -> list[int]:
    exponents = [idx for idx, val in enumerate(bitarray) if val == 1]
    return exponents

def get_final_mod(exponents, memo: ModuloArray, i1: int, i2: int) -> int:
    exponent_one = exponents[i1]
    exponent_two = exponents[i2]
    if i2 == len(exponents) - 1:
        return memo[exponent_one] * memo[exponent_two] % memo.get_mod()
    else:
        return memo[exponent_one] * get_final_mod(exponents, memo, i1+1, i2+1) % memo.get_mod()
    

def squares_modulo(exponents: list[int], base: int, mod: int, power: int, basecase: int) -> ModuloArray:
    memo = ModuloArray(basecase, base, power, mod)
    curr_idx = 0
    for exponent in exponents:
        while len(memo) - 1 < exponent:
            prev = memo[curr_idx]
            new = prev*prev%mod
            if new == 1:    #early break
                memo[curr_idx] = 1
                return memo
            curr_idx += 1
            memo.append(new)
    return memo
            
            
def modular_exponentiation(base:int, power:int, mod:int) -> int:
    bitarray = get_bitarray_backwards(power)
    exponents = get_modular_exponents(bitarray)
    memo = squares_modulo(exponents, base, mod, power, base*base%mod)
    return get_final_mod(exponents, memo, 0,1)

            






    