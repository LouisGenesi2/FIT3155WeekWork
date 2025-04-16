from modular_exponentiation import squares_modulo, get_bitarray_backwards, get_modular_exponents
import random

def miller_robin(number: int, num_trials: int) -> bool:
    if number == 2 or number == 3:
        return True
    
    if number % 2 == 0:
        return False
    
    # get (2^s)*t
    s = 0
    t = number-1
    while t % 2 == 0:
        s = s+1
        t = t/2


    for _ in range(num_trials):
        witness = random.randint(2,number-2)
        
        exponents = [s]
        memo_arr = squares_modulo(
            exponents,
            witness,
            number,
            (2**s)*t,
            (witness**t)*witness**t%number
        )
        for j in range(1, s):
            if memo_arr[j] != 1 and memo_arr[j] != number-1:
                return False
    
    return True


print(miller_robin(11, 10))


    