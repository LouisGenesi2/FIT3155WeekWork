def modular_exponentiation(base:int, power:int, mod:int) -> int:
    bitarray = []
    curr = power
    while curr > 0:
        floor = curr // 2
        remainder = curr %2
        bitarray.append(remainder)
        curr = floor
    
    exponents = [idx for idx, val in enumerate(bitarray) if val == 1]
    

    